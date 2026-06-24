# 实现事件 API

**事件**是一个 '事件调度框架' 的核心之一。有了事件，便有调度。

<note>

只建议使用 Kotlin 实现。需要实现的内容中绝大部分都包含 **挂起函数**，无法通过 Java 实现。

</note>

事件 API 的设计通常会同时考虑两层：

- Kotlin 侧的挂起主接口
- JVM 上面向 Java 的桥接调用形式

尤其是 `ContentEvent`、`MessageEvent` 这类“像属性一样”的挂起 API，
一般会通过 `@STP` 生成 getter 风格桥接。

## 一个最小例子

假设你要为组件定义一个“拥有内容主体”的事件类型：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@STP
interface FooMessageEvent : ContentEvent {
    override suspend fun content(): String
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
FooMessageEvent event = ...;

event.getContentAsync()
        .thenAccept(content -> { });
```
{switcher-key="%ja%"}

```Java
FooMessageEvent event = ...;

var content = event.getContentBlocking();
```
{switcher-key="%jb%"}

```Java
FooMessageEvent event = ...;

event.getContentReserve()
        .transform(SuspendReserves.mono())
        .subscribe(content -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>

当你的事件类型中存在 `guild()`、`member()`、`author()`、`messageContent()` 这类挂起查询时，
也应当优先沿用这一套设计方式，
使 Kotlin 与 Java 两侧看到的是同一份语义、不同风格的 API。

如果事件还要带少量固定字段，通常就直接放进实现类里：

```Kotlin
@STP
interface FooMessageEvent : ContentEvent {
    val messageId: ID
    override suspend fun content(): String
}

internal class FooMessageEventImpl(
    override val id: ID,
    override val messageId: ID,
    private val rawContent: String,
) : FooMessageEvent {
    override val time: Timestamp = Timestamp.now()
    override suspend fun content(): String = rawContent
}
```
