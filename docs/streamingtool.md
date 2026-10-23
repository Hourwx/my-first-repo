# 直播伴侣官网与安装包（10-21 证据）

官网为 `https://streamingtool.douyin.com/`。用户截图及本次内置浏览器均出现 ERR_CONNECTION_CLOSED。它不是已经固定 hosts 的 www.douyin.com。

原规则在规则模式下让此官网继承 `DOMAIN-SUFFIX,douyin.com,出口选择`。安装包 URL 为 `https://lf6-cdn-tos.douyinstatic.com/obj/venus/StreamingTool-13.1.1-x64.exe`，其域名原已有 `DOMAIN-SUFFIX,douyinstatic.com,DIRECT`。

此前下载任务记录：安装包 Content-Length 为 537508664，支持 Range；本地部分下载约 439 MB，仍不完整。HTTP 200/206 后存在停滞和 TLS abrupt close / EOF。Google DNS 与 Ali DNS 对同一 CDN 域名返回不同地址，提示 CDN 调度差异，未证明它是中断唯一原因。

候选模板只比 Windows 基线增加：

```yaml
rules:
  - DOMAIN,streamingtool.douyin.com,DIRECT
  - DOMAIN,streamingtool-hl.douyin.com,DIRECT
```

以上两条放在较宽泛抖音业务代理规则之前。另对这两个精确域名和 `lf6-cdn-tos.douyinstatic.com` 设置 `https://223.5.5.5/dns-query#DIRECT`。不是修改整个 douyin.com DNS，也不是把官网 IP 套用到下载站。

候选版已通过原交付时的离线 Mihomo -t，没有用户确认联网恢复。全局模式不会执行上述 DIRECT 例外。

本地复测应先看官网是否恢复，再确认安装包请求的目标 IP、出站和断开时间。不要自动执行或安装不完整 EXE，不要开启多线程下载或并行代理测试来替代用户链路验证。

语法依据：[Mihomo 指定域名 DNS](https://wiki.metacubex.one/config/dns/#nameserver-policy)、[路由规则](https://wiki.metacubex.one/config/rules/)。历史安装包版本和 URL 不代表现在最新版本。
