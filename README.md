# FlClash 配置与排查知识库

这是从 2026-10-04 起本地配置与排查资料整理成的 GitHub / 云端 Codex 交接仓库，**更新于 2026-10-25**，基于 10-23 首次整理包补充。首次索引覆盖 90 个顶层交付文件、62 份源 YAML；本次更新入口脚本与浏览器实测记录，63 份脱敏 YAML 模板保持原样。真实凭据与原始日志仍留本地。

本次更新见 [10-25 补充说明](UPDATE_2026-10-25.md)，其中明确区分浏览器显式代理与系统级 TUN、规则模式混合出口与真实绕行。

## 先读这几份

1. [当前状态](docs/current-state.md)：哪个版本作为结构基线，哪个仍待实测。
2. [已确认结论与纠错](docs/findings.md)：避免重复走过的错误路线。
3. [本地单变量排查流程](docs/troubleshooting.md)：如何继续取得有效证据。
4. [版本目录](docs/config-catalog.md)：Windows、安卓与历史版本分开。
5. [云端接手提示词](BOOTSTRAP_PROMPT.md)：新任务直接复制使用。

## 文件布局

| 位置 | 内容 |
| --- | --- |
| AGENTS.md | Codex 的仓库级约定 |
| configs/current/ | 5 份重点维护的脱敏结构模板 |
| archive/configs/ | 其余历史配置模板，含过期/撤回标记 |
| docs/ | 状态、结论、时间线、排查流程、隐私与上传说明 |
| scripts/windows/ | 既有 Chrome 显式 7890 代理启动入口 |
| tools/check_repository.py | 不发网络请求的结构与脱敏检查 |
| metadata/ | 原文件索引、模板清单、交付校验摘要 |

**所有 YAML 都是脱敏模板。** 真实代理地址、账号、密码、UUID 和传输认证参数已替换。模板保留规则、分组和配置结构用于审查；不能直接导入使用。真实配置仍在原电脑，本仓库不提供自动恢复账号的映射。

附件原件、work/ 中的构建脚本和核心二进制、浏览器测试资料及原始网络日志继续留在本地；不将工作目录整体搬进 GitHub。其有效结论已整合进专题文档。

## 云端 Codex 使用

本次导入目标为 [Hourwx/my-first-repo](https://github.com/Hourwx/my-first-repo)，文件位于仓库根目录；导入范围、换行和校验记录见 [云端导入记录](docs/cloud-import.md)。

把本目录中的内容放到 GitHub 仓库根目录，保留 AGENTS.md；若合入已有仓库，先合并已有指导，避免覆盖。Codex 会在工作前读取 AGENTS.md，参见 [OpenAI 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。具体上传步骤见 [GitHub 与云端交接](docs/github-handoff.md)。

离线检查：

```bash
python -m pip install -r requirements.txt
python tools/check_repository.py
```

检查只验证模板和本仓库，不访问住宅代理、不下载软件、不进行登录。历史 Mihomo -t 结果见状态文档；这里没有捆绑内核或 Geo 数据。
