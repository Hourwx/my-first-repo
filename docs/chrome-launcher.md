# 已验证的 Chrome 入口

仓库保留原交付的两个文件：scripts/windows/Chrome_FlClash_7890.cmd 和 Chrome_FlClash_7890_Launcher.ps1。它们是供 Windows 用户本地按需运行的入口，云端不要执行。

启动参数：

```text
--proxy-server=http://127.0.0.1:7890 --disable-quic https://chatgpt.com/
```

继续使用原浏览器资料，没有 user-data-dir。显式代理仅把 Chrome 送到本地 FlClash；后续分流仍由 FlClash 模式及规则决定。

启动前只读检查本地 7890 是否由 FlClashCore 监听，并判断已有 Chrome 是否使用匹配参数；若不匹配，提示用户保存工作、正常退出后重开，不强制结束进程。入口不清站点数据、不修改注册表、执行策略、DNS、WebRTC 或 TLS 校验，不运行联网测试。

用户已经确认相同启动方式能够打开 ChatGPT 并登录；脚本交付时验证了本地监听/实例判断与快捷方式，不代表脚本每次都已完成实际登录验证。

使用期间 FlClash 必须开启且端口仍为 7890。普通快捷方式不会永久继承这些参数。端口将来变化时要同步核对实际监听，而非只看 YAML 的 mixed-port。

参考：[Chromium 启动参数](https://www.chromium.org/developers/how-tos/run-chromium-with-flags/)、[网络设置](https://www.chromium.org/developers/design-documents/network-settings/)。
