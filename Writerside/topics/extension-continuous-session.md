# 持续会话 Continuous Session

<primary-label ref="doc-wip" />
<secondary-label ref="experimental-sec" />

## 概述

在进行业务编写时，时常会遇到需要继续连续对话的场景，例如：

```
用户: 绑定账户
BOT: 好的，请输入您的账户
用户: 123456789
BOT: 绑定成功，您的账号为: 123456789
```

如上案例，用户首先发出第一个指令 `绑定账户`，使bot进入等待接受“账户”的状态，
随即接受后续绑定后完成状态。

想要实现这个功能的方式很多，例如最基础的可以通过状态机来完成。
但是当这个流程开始逐步变得复杂，在大量的状态面前手动实现一个状态机就会显得十分繁琐。

这时候，协程就会体现出它的作用。

而**持续会话模块 (`simbot-extension-continuous-session`)**便基于异步与协程对**持续会话**的封装与实现。

<warning title="实验性">

**持续会话**是一个独立的扩展模块，且处于**实验阶段**，
可能会在未来发生任何不兼容变更或被移除。

</warning>


## 安装

**持续会话**是一个独立的扩展模块，你需要额外添加它的依赖并配置它。

<procedure>
<step><control>添加依赖</control>

<tabs id="build" group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
implementation("love.forte.simbot.extension:simbot-extension-continuous-session:%version%")
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Kotlin
implementation("love.forte.simbot.extension:simbot-extension-continuous-session-jvm:%version%")
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
implementation 'love.forte.simbot.extension:simbot-extension-continuous-session:%version%'
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Groovy
implementation 'love.forte.simbot.extension:simbot-extension-continuous-session-jvm:%version%'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<dependency>
    <groupId>love.forte.simbot.extension</groupId>
    <artifactId>simbot-extension-continuous-session-jvm</artifactId>
    <version>%version%</version>
</dependency>
```

</tab>
</tabs>
</step>
<step><control>配置</control>

<tabs>
<tab title="核心库">

当前扩展提供的主要入口是 `EventContinuousSessionContext`。

它是一个 `Plugin`，
并且**不会**通过 SPI 自动安装，
因此需要你显式 `install(...)`：

```Kotlin
launchSimpleApplication {
    install(EventContinuousSessionContext) {
        // 可选：为持续会话配置额外协程上下文
        coroutineContext = Dispatchers.Default
    }
}
```

</tab>
<tab title="SpringBoot">

在 Spring Boot 中同样需要**显式安装**，
可以通过 `SimbotPluginInstaller` 完成：

```Kotlin
@Component
open class ContinuousSessionInstaller : SimbotPluginInstaller {
    override fun install(installer: PluginInstaller) {
        installer.install(EventContinuousSessionContext) {
            coroutineContext = Dispatchers.Default
        }
    }
}
```

</tab>
</tabs>

</step>
</procedure>

## 核心类型

<deflist>
<def title="ContinuousSessionContext&lt;T, R&gt;">

通用持续会话上下文。
`T` 是“推送进来的事件值”，`R` 是“本次推送返回的结果值”。

</def>
<def title="EventContinuousSessionContext">

面向 simbot 事件系统的现成实现，
固定把 `T` 设为 `Event`、`R` 设为 `EventResult`。

</def>
<def title="ContinuousSessionKey&lt;C&gt;">

一个会话的唯一标识。
当前实现中还提供了一个简单实现：`UnitContinuousSessionKey`。

</def>
<def title="InSession">

持续会话内部实际执行的逻辑体。
Java 侧可通过 `InSessions.block(...)`、`InSessions.async(...)`、`InSessions.mono(...)` 构造。

</def>
</deflist>

## 冲突策略

创建 session 时，源码中支持三种冲突策略：

- `FAILURE`: 已存在同 key 且仍活跃的 session 时抛出 `ConflictSessionKeyException`
- `REPLACE`: 取消旧 session，用新 session 替换
- `EXISTING`: 直接返回旧 session，忽略新的创建请求

## Kotlin 示例

```Kotlin
@OptIn(ExperimentalContinuousSessionAPI::class)
suspend fun handle(
    event: Event,
    sessions: EventContinuousSessionContext
): EventResult {
    val key = UnitContinuousSessionKey()

    val session = sessions.session(
        key = key,
        strategy = ContinuousSessionContext.ConflictStrategy.EXISTING
    ) {
        val next = awaitValue { EventResult.empty() }
        // 根据 next 继续处理
    }

    return session.push(event)
}
```

如果你希望在同一个会话里做多轮校验，
还可以使用：

- `awaitWith { ... }`
- `multipleAwaitWith { ... }`
- `awaitValue(...)`

## Java 风格

Java 下推荐优先使用异步风格的 `InSessions.async(...)`；
如果你的逻辑确实需要阻塞式写法，
源码文档也明确建议使用虚拟线程调度器或至少隔离调度器。

在构造 `InSession` 时可选：

- `InSessions.async(...)`
- `InSessions.block(...)`
- `InSessions.mono(...)`

其中 `mono(...)` 依赖 `kotlinx-coroutines-reactor` 运行时支持。

## 注意事项

<warning title="实验性">

当前模块仍标记为 `ExperimentalContinuousSessionAPI`，
并且构建脚本里也明确关闭了 ABI 稳定性校验。
这意味着它在后续版本中依然可能调整。

</warning>
