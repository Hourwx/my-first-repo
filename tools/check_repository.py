"""Offline checks for this redacted knowledge repository; no network or core startup."""
from pathlib import Path
from copy import deepcopy
import ipaddress
import json
import re
import sys
import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError('Duplicate YAML key')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

SECRET_KEYS = {'password', 'username', 'uuid', 'obfs-password', 'private-key', 'public-key', 'short-id', 'secret', 'token', 'auth', 'authorization', 'api-key'}
PLACEHOLDERS = {
    '00000000-0000-4000-8000-000000000000',
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    '00000000',
}
DOC_NETWORKS = [ipaddress.ip_network(value) for value in ['192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '2001:db8::/32']]


def is_doc_address(value):
    try:
        address = ipaddress.ip_address(value)
    except (ValueError, TypeError):
        return False
    return any(address.version == network.version and address in network for network in DOC_NETWORKS)


def credential_errors(obj, path=''):
    errors = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_path = path + '.' + str(key)
            if str(key).lower() in SECRET_KEYS:
                allowed = isinstance(value, str) and (value.startswith('REDACTED_') or value in PLACEHOLDERS)
                if not allowed:
                    errors.append('unredacted sensitive field at ' + key_path)
            errors += credential_errors(value, key_path)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            errors += credential_errors(value, path + f'[{index}]')
    return errors


def analyze_config(doc, strict=False):
    errors = credential_errors(doc)
    proxies = doc.get('proxies', [])
    groups = doc.get('proxy-groups', [])
    for index, proxy in enumerate(proxies):
        if not is_doc_address(proxy.get('server')):
            errors.append(f'proxy {index} has a non-documentation endpoint')
    if not strict:
        return errors
    names = [item['name'] for item in proxies + groups]
    if len(names) != len(set(names)):
        errors.append('duplicate node/group names')
    available = set(names) | {'DIRECT', 'REJECT', 'REJECT-DROP', 'PASS', 'COMPATIBLE', 'GLOBAL'}
    for group in groups:
        for member in group.get('proxies', []):
            if member not in available:
                errors.append('missing selector member')
    for proxy in proxies:
        if proxy.get('dialer-proxy') and proxy['dialer-proxy'] not in available:
            errors.append('missing dialer-proxy group')
    for rule in doc.get('rules', []):
        parts = rule.split(',')
        destination = parts[-2] if parts[-1] == 'no-resolve' else parts[-1]
        if destination not in available:
            errors.append('unknown rule destination')
    if any('纽约' in item['name'] for item in proxies):
        errors.append('expired New York node in current template')
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    configs = {}
    current = list((root / 'configs/current').glob('*.example.yaml'))
    if len(current) != 5:
        errors.append('expected 5 current templates; update catalog deliberately if scope changes')
    for path in sorted(root.rglob('*.yaml')):
        if '.git' in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if not path.name.endswith('.example.yaml'):
            errors.append(relative + ': YAML is not labeled as a redacted example')
        try:
            doc = yaml.load(path.read_text(encoding='utf-8-sig'), Loader=UniqueKeyLoader)
            configs[relative] = doc
            errors += [relative + ': ' + message for message in analyze_config(doc, path.parent == root / 'configs/current')]
        except (yaml.YAMLError, ValueError, TypeError, KeyError):
            errors.append(relative + ': invalid YAML/config structure (values suppressed)')

    get = lambda name: configs['configs/current/' + name + '.example.yaml']
    try:
        baseline = get('linkcube-windows-baseline')
        candidate = get('linkcube-windows-streamingtool-candidate')
        expected = deepcopy(baseline)
        additions = ['DOMAIN,streamingtool.douyin.com,DIRECT', 'DOMAIN,streamingtool-hl.douyin.com,DIRECT']
        position = expected['rules'].index('DOMAIN,frontier-im.douyin.com,DIRECT')
        expected['rules'][position:position] = additions
        domains = ['streamingtool.douyin.com', 'streamingtool-hl.douyin.com', 'lf6-cdn-tos.douyinstatic.com']
        expected['dns']['nameserver-policy'].update({domain: 'https://223.5.5.5/dns-query#DIRECT' for domain in domains})
        if candidate != expected:
            errors.append('streamingtool candidate differs beyond its 2 rules and 3 DNS policies')
        for name in ['linkcube-windows-baseline', 'linkcube-windows-streamingtool-candidate', 'blizzard-windows']:
            hosts = get(name).get('hosts', {})
            if hosts.get('www.douyin.com') != '155.102.54.136' or hosts.get('imapi.douyin.com') != '98.96.213.145':
                errors.append(name + ': recorded Windows hosts changed without updating the handoff')
        for name in ['linkcube-android', 'blizzard-android']:
            hosts = get(name).get('hosts', {})
            if 'www.douyin.com' in hosts or 'imapi.douyin.com' in hosts:
                errors.append(name + ': Windows hosts accidentally introduced into Android lineage')
        front_groups = {g['name']: g for g in baseline['proxy-groups']}
        if front_groups.get('机场跳板选择', {}).get('type') != 'select':
            errors.append('LinkCube Windows manual front group changed')
        for name in ['linkcube-android', 'blizzard-windows', 'blizzard-android']:
            groups = {g['name']: g for g in get(name)['proxy-groups']}
            if groups.get('机场中转自动择优', {}).get('type') != 'url-test':
                errors.append(name + ': automatic front group changed')
    except (KeyError, ValueError, TypeError):
        errors.append('current templates missing required baseline structures')

    forbidden_suffixes = {'.exe', '.msi', '.part', '.har', '.pcap', '.pcapng', '.db', '.sqlite', '.mmdb', '.dat', '.reg', '.log', '.jsonl'}
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(part in {'.git', '.venv', '__pycache__'} for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in forbidden_suffixes or ('netlog' in path.name.lower() and path.suffix == '.json'):
            errors.append(relative + ': local artifact must stay outside repository')
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except UnicodeError:
            errors.append(relative + ': unexpected binary file')
            continue
        if re.search(r'[A-Za-z]:[\\/]+Users[\\/]', text, re.I):
            errors.append(relative + ': absolute local user path')
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text):
            errors.append(relative + ': email address found; review before publishing')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if re.match(r'[a-zA-Z]+:', target) or target.startswith('#'):
                    continue
                local_target = target.split('#')[0]
                if local_target and not (path.parent / local_target).exists():
                    errors.append(relative + ': broken local Markdown link')

    try:
        catalog = json.loads((root / 'metadata/templates.json').read_text(encoding='utf-8'))
        for row in catalog:
            doc = configs.get(row['repository_file'])
            if doc is None or len(doc.get('proxies', [])) != row['nodes'] or len(doc.get('rules', [])) != row['rules']:
                errors.append('template catalog counts do not match a YAML file')
        if len(catalog) != len(configs):
            errors.append('template catalog coverage differs from repository YAML count')
    except (ValueError, OSError, KeyError):
        errors.append('template catalog is missing or invalid')

    if errors:
        print(json.dumps({'result': 'FAILED', 'errors': sorted(set(errors))}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({'result': 'PASSED', 'templates': len(configs), 'current_templates': len(current), 'network_requests': 0, 'scope': 'offline structure and redaction checks; not live connectivity'}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
