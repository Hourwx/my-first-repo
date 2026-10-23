# 当前交接状态（整理于 2026-10-23）

这里的“当前”指本地已交付资料的最新状态，不表示今天重新检查了运行实例。最近一次现场证据来自 2026-10-21。

| 平台/配置 | 模板 | 节点/规则 | 状态 |
| --- | --- | --- | --- |
| LinkCube Windows | linkcube-windows-baseline.example.yaml | 52 / 8570 | 10-21 恢复两条抖音 hosts、移除过期纽约；保留后续规则和手动跳板；原交付离线校验通过，不能等同本次联网已恢复 |
| LinkCube Windows 直播伴侣 | linkcube-windows-streamingtool-candidate.example.yaml | 52 / 8572 | 待本地实测的对照版；只增加两个官网精确 DIRECT 和三个精确 DNS 策略 |
| 吹雪云 Windows | blizzard-windows.example.yaml | 26 / 980 | 10-21 完整校验版，与 10-12 兼容版配置数据相同，保留自动中转及两条 hosts |
| LinkCube 安卓 | linkcube-android.example.yaml | 52 / 8503 | 本次从 10-13 安卓版本移除过期纽约节点及选择项；保持安卓 STUN 保护与自动中转；脱敏结构检查，未重新联网验证 |
| 吹雪云 安卓 | blizzard-android.example.yaml | 26 / 984 | 保留 10-12 DNS/首次连接/STUN 保护结构；没有套用 Windows hosts，不代表已经验证所有应用 |

## Windows 主要路径

用户指定的住宅出口通过机场中转。10-21 LinkCube 保留“出口选择”“机场跳板选择”“GLOBAL”三个组；现场前置选择为香港07。这是当时状态，不是要求永远固定这个节点。吹雪云 Windows 保留“机场中转自动择优”。

抖音业务域名按原规则走出口选择，视频与媒体域名按细分规则 DIRECT。两条历史有效 hosts 为：

```yaml
www.douyin.com: 155.102.54.136
imapi.douyin.com: 98.96.213.145
```

它们是目标网站地址，不是用户代理地址。用户在 10-12 确认首页能开、增加 imapi 对照后速度改善。10-21 恢复它们只通过了离线校验；不能保证这些地址永久有效，不能推广到其他子域名。

## Chrome / ChatGPT

保留原 Chrome 资料，完全退出旧实例、显式使用本地 HTTP 代理 7890 并禁用 QUIC，从首页重新发起登录后，用户确认成功。启动脚本在 scripts/windows/；日常快捷方式不自动继承该入口参数。此方案是保留可用路径，未隔离出 TUN、嗅探、扩展或系统代理的唯一根因。

## 尚未确认

- 直播伴侣官网导入新对照版后是否恢复；安装包是否能够下载完整。
- 10-21 再次出现的抖音错误与升级之间的精确因果关系。
- Windows TUN、内置 WebView、普通 Chrome、显式代理 Chrome 的具体路径差异。
- 当前住宅账号有效期、运营商属性、长期带宽与全部功能是否正常。没有在 10-23 重测。

纽约试用节点已由用户确认过期。current 模板中不含它；历史模板保留仅供追溯。
