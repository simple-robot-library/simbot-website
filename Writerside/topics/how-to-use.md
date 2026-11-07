# 开始使用

<tldr>
选择开发方式和目标平台，跟随一个完整的简单示例，开始使用 simbot。
</tldr>

## 选择你的起点

| 你想做什么？ | 去这里看看！ |
| --- | --- |
| 体验平台无关的纯本地 Demo 级事件处理 | [](first-event.md)。在本地推送一个测试事件并观察处理结果。 |
| 在普通 Kotlin 或 Java 项目中接入 Bot | 了解 [](start-use-core.md)，再选择 [](start-use-components.md)。 |
| 在 Spring Boot 项目中接入 Bot | [](start-use-spring-boot-3.md)。已有 Spring Boot 2 项目可参考 [](start-use-spring-boot-2.md)。 |
| 从旧版本升级 | [](migration-5.0.md)。 |

如果已经确定使用的平台，也可以直接前往对应组件的快速开始。它们会一并介绍依赖、Bot 配置和事件监听等内容。

## 从项目到 Bot

接入某组件平台通常需要以下步骤：

1. 准备 Kotlin 或 Java 项目，并添加一个 `Application` 实现。
2. 选择平台组件，添加组件依赖和它需要的网络库 (Ktor) 引擎等。
3. 准备平台账号或协议服务，按组件说明配置并注册 Bot。
4. 注册事件监听器，启动 Bot，再运行应用并验证消息或事件。

各平台的凭据、权限和事件订阅方式不尽相同，具体内容以对应组件的手册为准。

## 安装 Application 实现

`Application` 是组件、插件和事件调度器的运行环境。官方提供两种常用实现：

- [](start-use-core.md)：使用核心库 `simbot-core`，在代码中配置应用、组件和 Bot。
- [](start-use-spring-boot-3.md)：在 Spring Boot 项目中使用 starter，结合 Spring 配置和注解编写监听器。

使用 Spring Boot 2 的项目可以选择 [](start-use-spring-boot-2.md)。
依赖坐标、JVM 版本和快照仓库的说明见 [](installation.md)。

## 安装组件、插件

组件库提供平台相关的事件、消息和 Bot 实现。选择组件后，按照它的文档添加依赖并完成配置。

### 官方组件

- [](component-qq-guild-first-bot.md)：接入 QQ 机器人官方开放平台 API。
- [](component-kook-first-bot.md)：接入 KOOK 官方开放平台 API。
- [](component-onebot-v11-first-bot.md)：连接 OneBot 11 协议实现。

更多组件和模块选择说明见 [](components-intro.md) 和 [](module-libraries.md)。

### 社区组件

前往 [](community-components.md) 了解社区组件。使用时请参考相应组件的版本、依赖和配置说明。

### 组件开发

如果你希望实现自己的组件或插件，前往 [](component-dev.md)。
