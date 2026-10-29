# 量子猫🐱 Quantcat (注解API)

<tldr>

`quantcat` 量子猫模块提供了一些 **注解** 风格的 simbot 事件处理 API 的定义。


</tldr>

`quantcat` 模块定义了一些注解, 以及服务这些注解的配套内容。这些注解的作用便是用于简化事件的监听、处理以及匹配的。
`quantcat` 模块仅提供定义和一部分基础的、默认的实现。

`quantcat` 是一种“标准”, **没有** 具体的注解解析实现。


<note>

Spring Boot starter 模块便是基于 `quantcat` 中定义的注解与其他配套功能进行实现的。

</note>

## 事件监听 @Listener

`@Listener` 注解标记在一个**函数**上, 用来声明此函数将会被解析为一个**事件处理器**。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Listener
suspend fun listen1(event: Event) {
    // ...
}

@Listener
suspend fun Event.listen2() {
    // ...
}
```

> 在 Kotlin 中, 被标记的函数最好是 `suspend` 可挂起函数。

</tab>
<tab title="Java" group-key="Java">

```Java
@Listener
public void listen1(Event event) {
    // ...
}

// 👇 支持 [[[CollectableReactivelyResult|basic-event-listener.md#CollectableReactivelyResult]]] 中所述的异步/响应式结果。
//    如果返回响应式结果, 记得添加对应的 [[[kotlinx-coroutines-xxx|https://github.com/Kotlin/kotlinx.coroutines/blob/master/reactive/README.md]]] 依赖。

@Listener
public CompletableFuture<?> listen2(Event event) {
    return ...
}

@Listener
public Mono<?> listen3(Event event) {
    return ...
}
```

</tab>
</tabs>

一个被标记了 `@Listener` 的函数, 它的参数、返回值等内容会被解析, 然后最终被处理为一个 `EventListener`, 进而被使用。
其中：

- 参数中,  `Event` 类型的参数会被视为本次事件监听的**目标类型**。
  如果没有, 则视为监听所有类型的事件。建议只有 **一个** `Event` 类型的参数。
- 参数中, 一些可知的类型的参数可以自动填充：
    - `EventListenerContext`
    - `EventContext`
    - `Event` 或某个子类型 (上一条所述)
    - `EventListener`

## 事件过滤 @Filter

`@Filter` 配合 `@Listener`, 用于简化对**文本**的匹配和一些已知的样板信息的匹配。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Listener
@Filter("你好")
suspend fun listen1(event: Event) {
    // ...
}

@Listener
@Filter(targets = [Filter.Targets(bots = ["bot-id-123"])])
suspend fun listen2(event: Event) {
    // ...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Listener
@Filter("你好")
public void listen1(Event event) {
    // ...
}

@Listener
@Filter(targets = {@Filter.Targets(bots = "bot-id-123")})
public void listen2(Event event) {
    // ...
}
```

</tab>
</tabs>

如上所示, 函数 `listen1` 将会用`"你好"`进行**正则匹配**, 只有一个消息事件 `MessageEvent` 中的文本消息符合这个正则,
才会进入此处理器。

函数 `listen2` 则会判断 `BotEvent` 中的 bot 是否能将 `"bot-id-123"` 视为自己, 如果可以才会进入此处理器。

下面会列举 `@Filter` 中详细的属性列表。

> 真正准确的描述更建议直接阅读源码注释或生成的API文档。

**@Filter**:

<deflist>
<def title="value">

`String`, 要进行文字匹配的值。匹配方式由 `matchType` 决定。

</def>
<def title="matchType">

`MatchType` 枚举, `value` 的匹配逻辑, 默认为 `REGEX_MATCHES`。

<deflist type="medium">
<def title="TEXT_EQUALS">文本全等匹配</def>
<def title="TEXT_EQUALS_IGNORE_CASE">文本忽略大小写的全等匹配</def>
<def title="TEXT_STARTS_WITH">文本开头匹配</def>
<def title="TEXT_ENDS_WITH">文本结尾匹配</def>
<def title="TEXT_CONTAINS">文本包含匹配</def>
<def title="REGEX_MATCHES">正则匹配</def>
<def title="REGEX_CONTAINS">正则 <code>find</code> 匹配</def>
</deflist>

</def>
<def title="mode">

`FilterMode`, 代表当前这个注解被解析后所产生的“过滤器”的实现模式。
默认为 `IN_LISTENER`。

<deflist type="medium">
<def title="INTERCEPTOR">

将 Filter 中的逻辑作为对应的事件处理器的专属拦截器 `EventInterceptor` 注册。
使用此模式则可以通过**优先级**的控制来使其与其他拦截器之间的关系（例如全局注册的拦截器）。

</def>
<def title="IN_LISTENER">

作为一段逻辑注入到事件处理器的前置中。
由于最终执行逻辑是与事件处理器的逻辑“融为一体”的,
所以使用此模式时, `Filter` 所产生的逻辑始终会在所有拦截器之后执行。

</def>
</deflist>

</def>
<def title="priority">

`Int`, 优先级。根据 `mode` 的不同, 分别代表作为拦截器时的优先级
或与其他 `IN_LISTENER` 逻辑之间的优先级。
默认为 `PriorityConstant.DEFAULT`。

</def>
<def title="targets">

`Filter.Targets` 数组, 后续介绍。默认为空。

> 虽然是数组, 但是只有**第一个**元素生效。

</def>
<def title="ifNullPass">

`Boolean`, 如果消息的 **纯文本内容 plainText** 为 `null`, 是否直接放行。
默认为 `false`。此参数只有当 `value` 不为空的时候有效。

</def>
</deflist>

**@Filter.Targets**:

<deflist>
<def title="components">

`String` 数组, 对 `Component` 进行匹配。 如果事件为 `ComponentEvent`, 则只有 `component.id` 在此列表中时才会放行。

</def>
<def title="bots">

`String` 数组, 对 `Bot` 进行匹配。 如果事件为 `BotEvent`, 则只有 `Bot.id` 在此列表中时才会放行。

</def>
<def title="actors">

`String` 数组, 对 `Actor` 进行匹配。 如果事件为 `ActorEvent`, 则只有 `Actor.id` 在此列表中时才会放行。

</def>
<def title="authors">

`String` 数组, 对消息发送者进行匹配。 如果事件为 `MessageEvent`, 则只有 `MessageEvent.authorId` 在此列表中才会放行。

</def>
<def title="chatRooms">

`String` 数组, 对事件的 `ChatRoom` 进行匹配。 如果事件为 `ChatRoomEvent`, 则只有 `ChatRoomEvent.content.id` 在此列表中才会放行。

</def>
<def title="organizations">

`String` 数组, 对事件的 `Organization` 进行匹配。 如果事件为 `OrganizationEvent`, 则只有 `OrganizationEvent.content.id`
在此列表中才会放行。

</def>
<def title="groups">

`String` 数组, 对事件的 `ChatGroup` 进行匹配。 如果事件为 `ChatGroupEvent`, 则只有 `ChatGroupEvent.content.id` 在此列表中才会放行。

</def>
<def title="guilds">

`String` 数组, 对事件的 `Guild` 进行匹配。 如果事件为 `GuildEvent`, 则只有 `GuildEvent.content.id` 在此列表中才会放行。

</def>
<def title="contacts">

`String` 数组, 对事件的 `Contact` 进行匹配。 如果事件为 `ContactEvent`, 则只有 `ContactEvent.content.id` 在此列表中才会放行。

</def>
<def title="ats">

`String` 数组, 对消息事件中 `At` 进行匹配。 如果事件为 `MessageEvent`,  
则只有 `MessageEvent.messageContent.messages` 中存在 `At` 消息且包含任意 at 目标时才会放行。

</def>
<def title="atBot">

`Boolean`，对消息事件中 `At` 进行匹配。
如果事件为 `MessageEvent`， 则只有 `MessageEvent.messageContent.messages` 中存在 `At` 消息且 id 属于事件 bot 时才会放行。

</def>
</deflist>

## @FilterValue 参数提取器

配合 `@Filter` 使用，当你使用**正则**类型的匹配方式进行文本匹配时，你可以使用参数提取来便捷的提取出匹配通过内容的某些值。
例如：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">


<compare type="top-bottom" first-title="正则标准方式" second-title="简写方式">

```Kotlin
@Filter("name: (?<name>.+), age: (?<age>\\d+)")
suspend fun Event.listen(
  @FilterValue("name") name: String, 
  @FilterValue("age") age: Int) {
    // ...
}
```

```Kotlin
@Filter("name: {{name}}, age: {{age,\\d+}}")
suspend fun Event.listen(
  @FilterValue("name") name: String, 
  @FilterValue("age") age: Int) {
    // ...
}
```

</compare>

</tab>
<tab title="Java" group-key="Java">

<compare type="top-bottom" first-title="正则标准方式" second-title="简写方式">

```Java
@Filter("name: (?<name>.+), age: (?<age>\\d+)")
public void listen(
  Event event,
  @FilterValue("name") String name, 
  @FilterValue("age") int age) {
    // ...
}
```

```Java
@Filter("name: {{name}}, age: {{age,\\d+}}")
public void listen(
  Event event,
  @FilterValue("name") String name, 
  @FilterValue("age") int age) {
    // ...
}
```

</compare>

</tab>
</tabs>


<note>

这是基于正则的 `Named Capturing Groups` 实现的，
可参考 [regular-expressions: named](https://www.regular-expressions.info/named.html) 等相关说明。

</note>

> _简写方式_ 最终会被转化成实际对应的 _标准方式_ 。
