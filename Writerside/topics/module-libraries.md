---
switcher-label: JavaAPI风格
---

# 模块一览

<tldr>

本页用于从模块层面快速理解 simbot4 的生态：
标准 API、核心实现、公共库、扩展库，以及官方组件库分别负责什么。

</tldr>

## 分层理解

从使用视角看，simbot4 的模块通常可以分为下面几层：

<list type="decimal">
<li>

`simbot-api`

标准 API。定义 `Application`、`Bot`、`Event`、`Message`、`Plugin`、`Component`、`Resource`
等核心抽象，本身不提供任何具体平台实现。

</li>
<li>

核心实现库

主要是 `simbot-core` 与 `simbot-core-spring-boot-starter`，
负责把 `simbot-api` 里的抽象真正运行起来。

</li>
<li>

公共基础库

位于 `simbot-commons/*`，提供 `ID`、时间戳、集合工具、原子类型、
`SuspendReserve`、状态循环等跨模块复用能力。

</li>
<li>

扩展库与周边库

例如 `simbot-extension-continuous-session`、`simbot-logger`、
`simbot-quantcat-common`、`simbot-test` 等。

</li>
<li>

组件库

平台能力由组件库提供。官方组件通常都在各自独立仓库维护与发布，
这里只按它们的模块结构介绍职责边界。

</li>
</list>

## 标准 API 与核心实现

### 标准 API

<deflist>
<def title="simbot-api">

标准库、抽象层。

- 定义能力接口：`SendSupport`、`ReplySupport`、`DeleteSupport` 等。
- 定义运行时核心：`Application`、`Bot`、`BotManager`、`EventDispatcher`。
- 定义通用模型：`Actor`、`Guild`、`ChatGroup`、`Contact`、`Message`、`Resource`。
- JVM 侧还提供 Java 友好桥接，例如 `launchApplicationAsync(...)`、
`launchApplicationBlocking(...)`、`EventListeners.block(...)` 等。

</def>
<def title="simbot-core">

核心实现库。

- 提供 `SimpleApplication`、`SimpleEventDispatcher` 等基础实现。
- 适合希望直接控制组件安装、Bot 注册和事件监听流程的场景。
- 大多数组件页中的“核心库使用方式”都是以它为基础。

</def>
<def title="simbot-core-spring-boot-starter">

Spring Boot 3 Starter。

- 为 Spring Boot 3 / Java 17+ 提供自动装配与注解驱动集成。
- 常用于 `@EnableSimbot`、`@Listener`、Bot 配置文件等开发方式。

</def>
<def title="simbot-core-spring-boot-starter-common">

Spring Boot Starter 公共支持模块。

- 承载 `love.forte.simbot.spring.common` 下的通用类型、异常与配置模型。
- 同时被 Starter 3 与 Starter 2 复用。
- 通常由两个 Starter 传递引入，不需要单独依赖。

</def>
<def title="simbot-core-spring-boot-starter-v2">

Spring Boot 2 Starter。

- 面向仍停留在 Spring Boot 2.x 的项目。
- 作用与 Starter 3 类似，但依赖的 Spring 生态版本不同。

</def>
</deflist>

## 公共基础库

这些模块大多不是“必须手动安装”的使用入口，
但它们构成了文档中很多基础概念的真实来源。

<deflist>
<def title="simbot-common-core">

公共核心工具库。

- `ID` / `UUID`
- `Async`
- 协程工具与 `Dispatchers`
- `Services`
- 文本、弱引用、属性容器等

</def>
<def title="simbot-common-time">

时间戳与时间单位相关支持。

- `Timestamp`
- 多平台时间实现

</def>
<def title="simbot-common-collection">

跨平台集合与并发容器工具。

- `ConcurrentMap`
- 队列工具
- `Flow` 相关集合辅助

</def>
<def title="simbot-common-atomic">

跨平台原子类型支持。

</def>
<def title="simbot-common-streamable">

`Streamable` 抽象支持。

</def>
<def title="simbot-common-stage-loop">

阶段循环状态机支持。

</def>
<def title="simbot-common-suspend-runner">

Java 友好桥接相关支持。

- `SuspendReserve`
- `SuspendReserves`
- `@ST` / `@STP`

</def>
<def title="simbot-common-annotations">

通用标记性注解。

</def>
<def title="simbot-common-apidefinition">

通用 API 定义模型，主要用于 REST API 风格封装。

</def>
<def title="simbot-common-ktor-inputfile">

基于 Ktor 的 `InputFile` 上传抽象。

</def>
</deflist>

## 扩展与周边

<deflist>
<def title="simbot-extension-continuous-session">

持续会话扩展。

适合实现多轮会话、流程式对话、事件上下文延续等场景。

</def>
<def title="simbot-logger / simbot-logger-slf4j2-impl">

日志抽象与 JVM 上的 SLF4J 2.x 实现。

</def>
<def title="simbot-quantcat-common">

注解驱动监听能力支持。

`@Listener`、参数绑定、过滤、拦截等开发体验与它密切相关。

</def>
<def title="simbot-test">

测试工具模块，提供测试用 Bot、组件、事件和消息实现。

</def>
</deflist>

## 官方组件库

官方组件一般各自独立发版。
普通应用开发者最常直接依赖的是它们的 `*-core` 模块。

### QQ 组件

仓库：`simple-robot/simbot-component-qq-guild`

<deflist>
<def title="simbot-component-qq-guild-api">

QQ 机器人官方 API 的底层封装。

</def>
<def title="simbot-component-qq-guild-stdlib">

基于 API 的低限度 Bot 实现与事件处理支持。

</def>
<def title="simbot-component-qq-guild-core">

真正作为 simbot 组件使用的核心模块，通常也是普通开发者应直接使用的模块。

</def>
<def title="simbot-component-qq-guild-internal-ed25519">

内部签名支持模块，一般无需直接使用。

</def>
</deflist>

### KOOK 组件

仓库：`simple-robot/simbot-component-kook`

<deflist>
<def title="simbot-component-kook-api">

KOOK API 封装。

</def>
<def title="simbot-component-kook-stdlib">

Bot 基础实现与事件处理支持。

</def>
<def title="simbot-component-kook-core">

完整的 simbot KOOK 组件模块，普通开发通常直接使用它。

</def>
</deflist>

### OneBot 组件

仓库：`simple-robot/simbot-component-onebot`

<deflist>
<def title="simbot-component-onebot-common">

OneBot 通用定义。

</def>
<def title="simbot-component-onebot-v11-common">

OneBot v11 通用模型与共享定义。

</def>
<def title="simbot-component-onebot-v11-event">

OneBot v11 原始事件数据模型。

</def>
<def title="simbot-component-onebot-v11-message">

OneBot v11 原始消息段数据模型。

</def>
<def title="simbot-component-onebot-v11-core">

OneBot v11 的核心组件实现，也是普通开发者最常用的模块。

</def>
</deflist>

### Telegram 与 Discord

它们仍属于早期或预告性质的组件页。
如果没有明确的源码模块、`Module.md`、构建脚本与 API 定义作为依据，
则应当把它们视为占位入口，而不是已经完整可用的官方组件实现说明。

## 如何选模块

如果你只是想开发一个应用，通常按下面的顺序选择即可：

1. 先选一个 `Application` 实现：`simbot-core` 或 Spring Boot starter。
2. 再选一个或多个组件核心模块，例如 `simbot-component-kook-core`。
3. 如果需要注解监听体验，再关注 Spring Boot starter 与 `quantcat` 相关章节。
4. 只有在你明确知道自己在做更底层封装时，才需要直接依赖 `api` 或 `stdlib` 模块。

如果你是在开发组件、扩展或公共库，
还会接触 `simbot-gradle-suspendtransforms` 一类构建辅助模块；
这类模块更适合在 [](component-dev.md) 与 [](component-dev-compiler-plugin.md) 中阅读，
而不是作为普通应用运行时依赖来选择。
