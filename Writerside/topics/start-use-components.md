# 选择组件库

组件库提供与具体平台交互的 Bot、事件和消息类型。先确定你想要连接的平台，再按对应的快速开始添加依赖、配置 Bot 并监听事件。

| 目标 | 准备内容 | 从这里开始 |
| --- | --- | --- |
| QQ 机器人开放平台 | 平台机器人账号、凭据，以及所需的事件订阅权限 | [](component-qq-guild-first-bot.md) |
| KOOK | KOOK 机器人账号和连接所需的凭据 | [](component-kook-first-bot.md) |
| OneBot 11 | 一个可访问的 OneBot 11 协议实现及其 HTTP、WebSocket 地址 | [](component-onebot-v11-first-bot.md) |

Telegram 和 Discord 组件的状态与版本说明见 [](components-intro.md)。也可以选择由社区维护的组件，参考 [](community-components.md)。

上表提供基于核心库的完整示例。需要了解其他配置或 Spring Boot 集成时，可继续阅读各组件的“开始使用”章节。

想了解组件标识、插件和 Bot 管理器之间的关系，可以阅读 [](components-and-plugins.md)。
各模块的职责与依赖选择见 [](module-libraries.md)。
