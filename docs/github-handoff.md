# 放入 GitHub 与云端 Codex

本次导入目标：[Hourwx/my-first-repo](https://github.com/Hourwx/my-first-repo)。仓库用途是版本审查、规则维护和排查知识交接，真实连接参数继续留在本地。导入过程见 [云端导入记录](cloud-import.md)。

1. 解压交付 ZIP，只把其中 flclash-knowledge/ 内的文件与目录放到仓库根目录；不要上传 ZIP 本身代替源码。
2. 若已有仓库，先比较 README.md、AGENTS.md、.gitignore；合并约定，不覆盖既有项目指导。本次目标仓库原来只有初始 README，没有既有 AGENTS.md 或项目代码。
3. 提交前运行 `python tools/check_repository.py`，并检查 Git diff 中没有真实账号、原始日志或本机资料。
4. 在你的云端 Codex 环境选择该 GitHub 仓库。若要自动安装检查依赖，可在环境 setup 中使用 `python -m pip install -r requirements.txt`；不需要住宅账号，不需要搭建代理或开放本地端口。
5. 新任务粘贴 BOOTSTRAP_PROMPT.md，填写本次具体问题。首次任务请它总结当前状态并做离线检查。

AGENTS.md 是持续的仓库约定；current-state.md 是带日期的事实；BOOTSTRAP_PROMPT.md 是每次任务的入口，三者分开维护。官方依据：[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[云端环境](https://learn.chatgpt.com/docs/environments/cloud-environment)。

云端源码不会自动变成本机已导入的 FlClash 配置。后续修改模板时，保持明确的版本差异；真实节点参数应在本地受控地合并后再验证，不能把仓库模板直接当订阅运行。


## 从 10-23 包升级到 10-25

已上传旧仓库时，使用补充 ZIP 的改动清单合并同名文件，优先更新两份启动器、docs/chrome-launcher.md、docs/current-state.md、10-25 专题及 AGENTS.md；不要删除或覆盖云端新增的工作。变更说明见 [本次更新](../UPDATE_2026-10-25.md)。尚未上传时，可直接采用完整 10-25 ZIP。

10-25 补充已合并到上述仓库 main 分支；上传范围和验证见 [云端导入记录](cloud-import.md)。本地桌面快捷方式不会通过 GitHub 自动同步，云端也不能操作用户电脑桌面。
