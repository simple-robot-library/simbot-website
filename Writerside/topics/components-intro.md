# 概述

<tooltip term="组件"><control>组件</control></tooltip>
是 simbot 中特定平台功能的主要提供者，也是核心概念之一。
它通常由一组
<tooltip term="组件标识"><control>组件标识</control></tooltip> 和
<tooltip term="插件"><control>插件</control></tooltip>
组成。

比如说“QQ频道组件”，
指的就是一个包含 **QQ频道组件标识 (`QQGuildComponent`)**
和 **QQ频道Bot管理器 (`QQGuildBotManager`)**
的整体。

<note>
举个不恰当的例子。
如果将 simbot 比喻为 Spring Boot，那么组件则可以类似地视为各种 starter。
</note>

## 标准组件

手册里主要介绍的标准组件有：

- [QQ机器人组件](component-qq-guild.md)
- [OneBot组件](component-onebot.md)
- [KOOK组件](component-kook.md)

另外还有仍处于早期或预告阶段的页面：

- [Telegram组件（预告）](component-telegram.md)
- [Discord组件（预告）](component-discord.md)

<note>

官方组件通常按独立仓库发版，
所以这里也按 <code>api</code> / <code>stdlib</code> / <code>core</code> 这类边界来组织。

</note>

## 模块选择建议

大多数情况下，直接选择对应组件的 `*-core` 模块就够了。
只有在需要更底层的 API 封装、事件接入或自定义二次封装时，
才需要进一步关注 `api`、`stdlib` 或协议模型模块。

更多整体结构可前往 [](module-libraries.md) 继续阅读。
