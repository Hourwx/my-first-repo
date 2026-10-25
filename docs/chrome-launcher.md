# Chrome 7890 启动入口（2026-10-25 更新）

当前文件是 scripts/windows/Chrome_FlClash_7890.cmd 和 Chrome_FlClash_7890_Launcher.ps1。供用户在 Windows 本地按需运行；云端不要执行。

```text
--proxy-server=http://127.0.0.1:7890 --disable-quic chrome://newtab/
```

**10-25 只把默认目标从 ChatGPT 首页改为 Chrome 新标签页。** 原 Chrome 资料、显式代理与 QUIC 参数、监听检查和已有实例保护逻辑都保留。入口不再主动跳转 ChatGPT；浏览器本身的旧会话恢复属于另一项设置。

## 本地桌面入口

桌面名称：`Chrome（FlClash 7890）`。它指向本地保存的 CMD，工作目录为该 CMD 所在目录；本仓库不包含绑定旧电脑绝对路径的 LNK。用户迁移电脑时，应给本地保存的 CMD 创建新快捷方式。

用户明确要求只保留新版 Chrome 入口。10-25 已更新该快捷方式，移除普通 `green - Chrome` 和 `Google Chrome` 桌面入口，并将旧 LNK 备份在本地工作目录。原 Chrome 安装程序没有删除。随后旧图标未同步时，文件系统与 Shell 桌面目录均已核对只剩 7890 的普通 Chrome 入口，并发送目录变更通知。没有修改任务栏固定项或其他应用快捷方式。

## 使用与检查

FlClash 必须开启，并由 FlClashCore 在本地 IPv4 7890 监听。若当前 Chrome 不是按匹配参数启动，入口会提示先保存工作并正常退出再重开，不强制结束进程。显式代理只把 Chrome 请求交给 FlClash，后续仍按 FlClash 模式和规则选择 DIRECT 或代理。

继续使用原浏览器资料，没有 user-data-dir。入口不清站点数据、不改注册表、执行策略、DNS、WebRTC、TLS 校验或 FlClash 配置，不运行联网测试。

本次两份脚本与 10-23 快照逐字差异核对，仅 homeUrl 改变。PowerShell 静态解析无错误，CMD --check-only 正常返回。检查时监听就绪，但手动重启后的 Chrome 命令行未带 --disable-quic，故严格检查返回 conflict、WouldLaunch=false，符合原保护逻辑；Chrome 实验设置中的 QUIC 仍为禁用。没有用新默认目标实际自动启动浏览器做端到端测试。

此前显式 7890 代理、禁用 QUIC、原资料不变并重新发起认证的路径，已由用户确认 ChatGPT 登录成功。这一历史结果不等于所有网站和所有启动方式始终正常。

参考：[Chromium 启动参数](https://www.chromium.org/developers/how-tos/run-chromium-with-flags/)、[网络设置](https://www.chromium.org/developers/design-documents/network-settings/)。
