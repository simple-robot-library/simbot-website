# 特性速览

<tldr>

simbot4 与 simbot3 相比 **完全不同**，是又一次的**彻底重构**产物。

</tldr>

## Kotlin 多平台 {id="kotlin_multiplatform"}

早在 simbot2 时代就已经开始畅想的，现在终于实现了。
simbot4 现已基于 [KMP](https://kotlinlang.org/docs/multiplatform.html) 全面支持 Kotlin 多平台。

## Java友好

贯彻一直以来的特点，simbot4也同样是Java友好的，
包括对所有挂起函数API的非挂起桥接、Spring Boot支持等。

更多内容参考 <a href="java-friendly.md">Java友好</a>。

## Kotlin 2.x 与 K2 编译器

simbot4 当前构建已全面建立在 **Kotlin 2.x** 与 **K2 编译器** 之上。

<note>

当前示例与构建说明以 Kotlin 2.x 时代的工具链为准。

</note>

## Java最低版本

JVM 平台中，Java最低要求为 **Java11**，
并且所有模块都提供相应的模块化信息支持。

JVM 平台中，Spring Boot starter 默认推荐使用 Spring Boot 3，
也因此在使用 `simbot-core-spring-boot-starter` 的时候 Java 需要确保版本为 **Java17+** 。

如果你仍停留在 Spring Boot 2.x，
则可以使用兼容模块 `simbot-core-spring-boot-starter-v2`，
其 Java 基线为 **Java11+** 。

## 过滤器的概念

移除 “过滤器(Filter)” 概念，加强 “拦截器(Interceptor)” 能力。
(在注解API中依旧保有 `@Filter` 注解。)

过滤器与拦截器的概念有些重复了，在 simbot3 中的**监听函数**类型的实现也因为了实现
“过滤器”概念而变得有些抽象且难以扩展。

## 大幅简化API


与 simbot3 相比，API**大幅简化**。
并得益于此，组件开发成本和核心库的维护成本都大大下降。

<procedure collapsible="true" title="部分细节">
<list>
<li>

移除了 `Event.Key` 与 `Message.Element.Key` 的机制。
这两个机制是增加开发繁琐度最主要的原因之一，而且可以说几乎没有什么实用性。

</li>
<li>

优化、并大幅简化 "行为对象" (例如 `Guild`、`Channel`) 的 API 与相互关系。
相互关系方案变更为单向由上到下传递。

举个例子，在 simbot3 中，`Guild.channel(...)` 可以获取到频道服务器内某个子频道，
而 `Channel.guild()` 则可以反向获取自己所属的 `Guild`。

```Kotlin
val guild = ...
val channel = guild.channel(1.ID) // 正向获取 Channel
val guildAgain = channel.guild()  // 反向获取 Guild
```

放在 `Guild <-> Channel <-> Member` 上同理，它们之间总是*双向*关联的。
但是这样实际上没有太大的易用性收益: 你既然能够获取到 `Channel`，那么 `Guild` 便是已知的。
而这种设计代来的最大的负面影响就是极大的增加了开发的工作量和复杂度。

因此，simbot4 将它们的关系重新设计为单向关联、由上至下，即 `Guild` 可以得到 `Channel`，
而 `Channel` 不能回头获取 `Guild`。对于某种类型实现，让它专注于自身。

</li>
<li>

事件定义优化、简化。除了上面提到的移除了 `Event.Key` 机制以外，
事件内的属性信息也得到了简化。

举个例子，在 simbot3 中，有两个事件：`OrganizationEvent`、`GuildEvent`，
它们分别对外提供 `organization` 和 `guild` 属性。
而又因为 `Guild` 继承 `Organization`，所以实际上这两个属性是 **同一回事儿**。

```Kotlin
interface GuildEvent : OrganizationEvent {
    suspend fun guild(): Guild
    
    // 样板式的“重定向”代码
    suspend fun organization(): Guild = guild()
}
```

重点就在这里，这里只列举了两个具有关系的事件，但是实际上这种 **同义不同名** 的属性非常之多。

```Kotlin
interface GuildEvent : OrganizationEvent, ChangedEvent, ContentEvent {
    suspend fun guild(): Guild
    
    // 样板式的“重定向”代码
    suspend fun organization(): Guild = guild()
    suspend fun after(): Guild = guild()
    suspend fun content(): Guild = guild()
}
```

这就导致当需要重写覆盖返回值类型为一个新的类型时，会产生非常多的样板代码。

在 simbot4 中，我们简化并尽力去避免出现 **同义不同名** 的事件属性，
以 `ContentEvent` 和 `SourceEvent` 为主要原点，使用 **同义同名** 的属性来层层融合。

```Kotlin
interface OrganizationEvent : ContentEvent {
    override suspend fun content(): Organization
}

interface GuildEvent : OrganizationEvent {
    override suspend fun content(): Guild // 同义同名, 直接重写覆盖
}
```

</li>
</list>
</procedure>

## 更多的单元测试

从 simbot4 开始，我们会尝试更注重**单元测试**。
事实上，之前的版本可以说完全没有把单元测试放在心上。
从这个版本开始，我们会逐步在完善单元测试上增加精力，
也可借此增加整个simbot库的稳定性与可靠性。

<note>
在编写与使用单元测试方面我们仍然是新手。
如果你有任何好的建议意见，欢迎反馈给我们或为我们提供
<a href="feedback-and-support.md">贡献与支持</a>
，非常感谢！
</note>
