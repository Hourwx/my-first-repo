# 云端导入记录

2026-10-23，应用户要求，将上传资料包中的 flclash-knowledge/ 内容导入已连接的 Hourwx/my-first-repo 仓库根目录。原仓库只有初始 README；该文件替换为资料包说明，初始内容仍保留在 Git 历史中。

## 来源与完整性

- 原 ZIP：FlClash_云端Codex_GitHub资料包_2026-10-23.zip。
- ZIP SHA-256：`3b9358b46c65338249c0bd5566ed68c457376e3c26708c0ac6914956762cf389`。
- 原包共 86 个文件；原清单列出的 85 个文件均在导入前通过逐字节 SHA-256 校验，清单不包含自身。
- 单独上传的 README.md 与包内 README.md 字节相同。
- 导入 5 份当前模板、58 份历史模板，以及说明、离线检查工具、Windows 入口脚本和元数据；另增加本记录。ZIP 本身不提交。

## 导入调整

按照 .gitattributes 统一文本换行：通常为 LF，Windows .cmd/.ps1 工作区文件为 CRLF。默认文本规则补充 eol=lf，使不同平台的 Git 检出一致。63 份 YAML 模板仅调整换行，节点、分组、规则及顺序均未修改。

metadata/templates.json 中的 sha256 更新为导入后模板的校验值；source_sha256 和原文件索引继续保留原始值。metadata/package-files.sha256 更新为本次导入工作区文件的校验值，不包含自身。请在按 .gitattributes 正常检出的 Git 工作区中验证该清单；Git 原始对象或源码归档中的 Windows 脚本可能使用 LF。

README 和 GitHub 交接说明补充实际目标仓库。metadata/validation-report.json 仍是原资料包准备阶段的历史报告，其中的 github_upload_performed 和原始资料扫描结论不代表后续导入状态。

## 验证范围

云端使用 requirements.txt 指定的 PyYAML 6.0.3 运行 `python tools/check_repository.py`，检查模板结构、已知敏感字段的占位符、配置目录和文档链接。原始真实配置没有上传到云端，因此不能在这里重新执行针对原始账号的精确比对。

本次不运行 Windows 启动脚本或代理核心，不更改真实 FlClash 配置，不测试用户本机连通性。streamingtool 对照模板仍待用户本地验证，离线通过不表示故障已修复。

## 2026-10-25 补充导入

用户明确授权将本地 10-25 脱敏补充合并到本仓库 main 分支。基于导入前提交 `7d1f0ec9f6b14542df6c55bfa289d476656e95d5`，保留已有 README 目标仓库说明、本文历史记录、隐私说明、.gitattributes 换行规范及模板校验元数据。

本次合并 17 个补充文件，并更新本导入记录，共 18 个路径。没有删除远端文件，63 份 YAML 模板与导入前版本逐字相同；真实账号、代理端点、原始日志、截图和桌面 LNK 均不提交。启动器默认目标改为 chrome://newtab/，保留显式 7890 代理、禁用 QUIC、原资料和实例检查；没有在上传过程中执行启动器。

本地离线结构检查及已知源凭据/端点精确扫描通过。校验清单覆盖本次合并后的工作树，排除 .git、缓存和清单本身；Windows 脚本工作树仍为 CRLF，Git 对象按 .gitattributes 规范化为 LF。metadata/templates.json 保留先前云端换行归一化后的模板摘要。

metadata/validation-report.json 的原资料包检查结论保留；github_upload_performed 更新为本次提交的上传状态，github_update 记录本次合并基线与离线检查范围。metadata/update-2026-10-25.json 记录实际合并路径。本次没有改动用户本机 FlClash 配置或重新做网络探针；系统 TUN IPv6 与直播伴侣完整下载仍待分别验证。
