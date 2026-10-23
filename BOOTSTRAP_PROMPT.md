请接手这个 FlClash 知识仓库，使用中文。

先阅读 AGENTS.md、README.md、docs/current-state.md 和 docs/findings.md，概括已经确认的事实、仍未确认的假设，以及当前版本之间的差别。不要立即重写配置。

用户环境主要是 Windows + FlClash + Chrome / 抖音客户端，另有安卓 FlClash。LinkCube 的住宅出口通过机场前置；Windows 最新结构基线使用手动机场跳板，吹雪云与安卓原有自动中转要分开保留。账号和地址已脱敏，仓库中的 YAML 不能直接联网运行。

请运行 python tools/check_repository.py 做离线检查。不要启动额外代理内核、批量 curl、测速、并行下载，不要清浏览器资料或降低证书校验。云端的网络结果不代表用户本机网络。

接下来的任务是：【在这里填写具体问题】。

如果涉及修复，先列出有证据支持的最小改动，区分 Windows 与安卓、首页与视频、网站与安装包、路由规则与 DNS 调度。完成变更后给出语义差异和本地复测步骤；未获本地实测反馈的部分继续标注待验证。
