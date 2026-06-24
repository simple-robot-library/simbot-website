# 实现事件

相比较于上一篇的实现 Bot 相关的内容，
实现一个 **事件 `Event`** 则会简单的多。

## 事件 Event 定义 {id="event-def"}

什么是 **事件 `Event`** ? 在 simbot标准库中定义的 **`Event` 接口**就是事件。
我们先来看看 `Event` 的定义:

```Kotlin
/**
 * 一个 **事件**。
 */
public interface Event : IDContainer {
    public override val id: ID
    public val time: Timestamp
}
```

可以看到，`Event` 的接口中约束还是蛮少的：一个唯一标识，以及一个时间戳。

但这并非全部。simbot标准库提供了一些常见的、拥有更进一步含义的事件子类型定义，例如 `BotEvent`、`ChannelEvent` 等，
你可以在 [API 文档](https://docs.simbot.forte.love) 或 [](basic-event.md) 章节中找到更全面的列举与说明，此处不再赘述。

## 实现事件 {id="event-impl"}

实现一个事件，听上去没有什么难度。

> 按照习惯，我们**建议**你将实现类型的**定义**与**真正实现**分离开，
> 且仅对外暴露定义的抽象类型。

假设：我们有一个事件类型 `FooEvent`，它具有一个字符串格式的"事件主体"，用来代表一个"名称"。
而后经过思考与调研，我们决定使这个类型实现 `ContentEvent`, 也就是 **"具有一个主体(`content`)"** 的事件类型。

首先，我们来定义这个事件类型的接口:

```Kotlin
@STP
interface FooEvent : ContentEvent {
    /** 得到事件的 '主体' */
    override suspend fun content(): String // 修改返回类型为字符串
}
```

<note>

`@STP` 标记在类型上，
即为类型内所有的挂起函数进行标记。
因为 `ContentEvent` (或者说绝大多数 `Event` 类型) 中的挂起'属性'也都是标记的 `@STP` 的。

当然，你也可以选择手动在每个挂起函数上标记它。

如果只想看最小形态，可以把它理解成：

```Kotlin
interface FooEvent : ContentEvent {
    override suspend fun content(): String
}
```

</note>


然后，我们在内部的某个地方实现它:

```Kotlin
internal class FooEventImpl(
    override val id: ID, // 此事件的 ID
    val name: String,    // 上文提到的用来作为 '事件主体 `content`' 的 '名称'
): FooEvent {
    /** 假设事件戳就是这个类实例被构建的事件 */
    override val time: Timestamp = Timestamp.now()

    /** 让 '事件主体' 返回 '名称' */
    override suspend fun content(): String = name
}
```

至此为止，一个普通且常见的事件类型便实现完成了。

如果你只需要最小实现，通常就是“接口暴露挂起属性，内部类持有原始字段”这一层，不必再额外包一层转换对象。

如果 `FooEvent` 作为公开事件类型对外暴露，
那么 Java 使用者最终看到的通常会是 `@STP` 生成的 getter 风格桥接：

<tabs group="code">
<tab title="Java" group-key="Java">

```Java
FooEvent event = ...;

event.getContentAsync()
        .thenAccept(content -> { });
```
{switcher-key="%ja%"}

```Java
FooEvent event = ...;

var content = event.getContentBlocking();
```
{switcher-key="%jb%"}

```Java
FooEvent event = ...;

event.getContentReserve()
        .transform(SuspendReserves.mono())
        .subscribe(content -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>
