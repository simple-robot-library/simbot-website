---
switcher-label: JavaAPI风格
---

# 事件监听与处理

## 事件调度器 EventDispatcher

所有的事件处理器都需要注册到 `EventDispatcher` 中, 
当 `EventDispatcher` 收到消息推送时, 它便会将这个事件交给其内部的处理器依次进行处理。

你可以在 `Application` 中获取到 `EventDispatcher`：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val app = ...
val eventDispatcher = app.eventDispatcher // 获取事件调度器
```

</tab>
<tab title="Java" group-key="Java">

```Java
var app = ...;
var eventDispatcher = app.getEventDispatcher(); // 获取事件调度器
```

</tab>
</tabs>

### 注册事件处理器

想要处理事件, 你便需要向 `EventDispatcher` 注册事件处理器 `EventListener`。

> 有关事件处理器的具体描述会在后续小节介绍。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val eventDispatcher = ...

dispatcher.register { // this: EventListenerContext
    // 处理事件...

    EventResult.empty() // 返回一个处理结果
}
```

Kotlin 中提供了一些扩展函数, 可用来更便捷地注册一个事件处理器。

处理所有类型的事件：

```Kotlin
val eventDispatcher = ...

dispatcher.process { // this: EventListenerContext
    // 处理事件, 但是不需要返回值

}
```

处理指定类型的事件：

```Kotlin
dispatcher.listen<Event> { // this: EventListenerContext
    // 处理事件

    EventResult.empty()
}

dispatcher.process<Event> { // this: EventListenerContext
    // 处理事件, 但是不需要返回值
    
}
```

Kotlin 中也提供了直接针对 `Application` 的便利扩展 `listener`：

```Kotlin
val app = ...

app.listeners { // this: EventListenerRegistrar
    listen<Event> { ... }
    process { ... }
    process<Event> { ... }
}
```

</tab>
<tab title="Java" group-key="Java">

处理所有类型的事件：

```Java
var eventDispatcher = ...;
dispatcher.register(EventListeners.async(context -> {
    // 处理事件...
    
    return CompletableFuture.completedFuture(EventResult.empty()); // 返回处理结果
}));
```

{switcher-key="%ja%"}

```Java
var eventDispatcher = ...;
dispatcher.register(EventListeners.block(context -> {
    // 处理事件...
    
    return EventResult.empty(); // 返回处理结果
}));
```

{switcher-key="%jb%"}

处理特定类型的事件：

```Java
var eventDispatcher = ...;
dispatcher.register(EventListeners.async(Event.class, (context, event) -> {
    // 处理事件...
    
    return CompletableFuture.completedFuture(EventResult.empty()); // 返回处理结果
}));
```

{switcher-key="%ja%"}

```Java
var eventDispatcher = ...;
dispatcher.register(EventListeners.block(Event.class, (context, event) -> {
    // 处理事件...
    
    return EventResult.empty(); // 返回处理结果
}));
```

{switcher-key="%jb%"}
</tab>
</tabs>

### 事件处理器注册回执

当通过 `register` 注册一个事件处理器后, 会返回一个 `EventListenerRegistrationHandle`。
可以将它称之为注册的回执, 或者句柄, 总之它的作用是通过调用 `dispose` 来“取消”这次注册的事件处理器。
取消注册后, 对应的事件处理器将不再有效。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val handle = register(...)
handle.dispose()
```

</tab>
<tab title="Java" group-key="Java">

```Java
var handle = register(...);
handle.dispose(); // 取消注册
```

</tab>
</tabs>

### 注册事件处理器的额外属性

注册事件处理器时, 可以提供一些额外的属性与配置信息, 例如优先级等。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val dispatcher = ...
dispatcher.register({ // this: EventListenerRegistrationProperties
    // 配置一些信息
    // 优先级
    priority = -1 // 通常默认值为 0, 越小越优先
    // 添加一个要注册的事件处理器的专属拦截器
    addInterceptor {
        // 拦截...
        invoke() // 执行拦截链的后续并返回真实结果
    }
}) {
    // 处理事件, 返回处理结果...
    ...
}
```

那些扩展函数也同样支持：

```Kotlin
dispatcher.listen<Event>(propertiesConsumer = {
    // 配置一些信息...
}) {
    // 处理事件, 返回处理结果...
    ...
}

dispatcher.process<Event>(propertiesConsumer = {
    // 配置一些信息...
}) {
    // 处理事件...
    ...
}

dispatcher.process(propertiesConsumer = {
    // 配置一些信息...
}) {
    // 处理事件...
    ...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
var dispatcher = ...;
dispatcher.register(
        (properties) -> {
            // 配置一些信息...
            // 优先级
            properties.setPriority(-1);
            // 添加为当前注册的事件处理器的专属拦截器
            properties.addInterceptor(EventInterceptors.async(context -> {
                // 拦截...

                return context.invoke();
            }));
        },
        // 事件处理器...
        EventListeners.async(context -> {
            // 处理事件...
            return CompletableFuture.completedFuture(EventResult.empty()); // 返回处理结果
        }));
```

{switcher-key="%ja%"}

```Java
var dispatcher = ...;
dispatcher.register(
        (properties) -> {
            // 配置一些信息...
            // 优先级
            properties.setPriority(-1);
            // 添加为当前注册的事件处理器的专属拦截器
            properties.addInterceptor(EventInterceptors.block(context -> {
                // 拦截...
   
                return context.invoke();
            }));
        },
        EventListeners.block(Event.class, (context, event) -> {
            // 处理事件...
   
            return EventResult.empty(); // 返回处理结果
        }));
```

{switcher-key="%jb%"}

</tab>
</tabs>

## 事件处理器 EventListener

事件处理器 `EventListener` 是一个函数接口类型, 它定义了处理事件的方式：接收一个 `EventListenerContext`
, 然后经过处理, 返回 `EventResult`。

<tip>
在 Java 中, 你可以通过 `EventListeners` 的静态工厂API来通过 Java 友好的 lambda 方式构建阻塞或异步风格的实例。

```Java
var eventListener = EventListeners.async(context -> {
    // 处理事件...
    return CompletableFuture.completedFuture(EventResult.empty()); // 返回处理结果
});
```

{switcher-key="%ja%"}

```Java
var eventListener = EventListeners.async(Event.class, (context, event) -> {
    // 处理事件...
    return CompletableFuture.completedFuture(EventResult.empty()); // 返回处理结果
});
```

{switcher-key="%ja%"}

```Java
var eventListener = EventListeners.block(context -> {
    // 处理事件...

    return EventResult.empty(); // 返回处理结果
});
```

{switcher-key="%jb%"}

```Java
var eventListener = EventListeners.block(Event.class, (context, event) -> {
    // 处理事件...

    return EventResult.empty(); // 返回处理结果
});
```

{switcher-key="%jb%"}
</tip>


## 事件处理结果 EventResult {id="EventResult"}

`EventResult` 是 `EventListener` 中处理完事件后的返回值类型。

它主要提供了如下信息：

<deflist>
<def title="content">

`Any?` 类型, 代表事件的处理结果。处理结果可能是任何类型, 由事件处理器内的逻辑自由决定。
部分特殊类型下会在特殊的 `EventResult` 类型中被处理, 下文会介绍。

</def>
<def title="isTruncated">

是否截断的标记。如果为 `true`, 则会在此结果出现后直接终止本次事件处理流程, 
不再执行后续其他的事件处理器。一般默认为 `false`。

</def>
</deflist>

大多数情况下你不需要自己实现 `EventResult`。核心库中提供了 `StandardEventResult` 定义了部分常见、或具有特殊含义的类型, 
并且在 `EventResult` 中提供静态API来直接获取它们。

### Invalid

代表**无效**的结果。通常用于那些在类型匹配（比如 `dispatcher.listen<Event> {...}`）等地方使用, 
当某些有效性判断不匹配时返回, 代表本次处理**无效**, 没有进入真正的逻辑。

可以通过 `EventResult.invalid()` 获取。

### Error

代表**出现错误**的结果。当出现了异常（例如由 `EventDispatcher` 捕获到的事件处理器中抛出的异常）时便会将异常包装到 `Error`
中, 
然后返回给事件推送者。

> 有关**事件推送**的内容会在下文介绍。

虽然也可以通过 `EventResult.error(...)` 人为构建, 但是通常交给调度器捕获即可, 人为构建的场景并不多。

### Empty

代表**没有结果**的结果。与 `Invalid` 有些类似, 但是含义不同。`Empty` 代表事件处理的逻辑**正常执行**了, 只是没什么可返回的内容。
还有一点不同是, `Empty` 可以指定 `isTruncated`, 而 `Invalid` 不行。

可以通过 `EventResult.empty(...)` 或在 `EventResult.of(...)` 的 content 参数为 `null` 时获取。

### Simple

除去上面这些类型以外, 处理逻辑**正常执行**, 且有需要返回的 `content` 时的类型。
可以通过 `EventResult.of(...)` 的 content 参数不为 `null` 时获取。

`Simple` 也具有特殊效果, 它实现了 `CollectableReactivelyResult`。

### CollectableReactivelyResult {id="CollectableReactivelyResult"}

一个特殊的标记类型, 如果返回值结果是 `CollectableReactivelyResult`, 
则事件调度器应当对 `content` 进行一次类型判断, 当返回值类型是符合条件的 **异步/响应式结果**, 则对其进行一次挂起收集。

例如返回的 `content` 为 `Mono` 类型(JVM) 或 `Deferred` 类型(Kotlin协程库自带), 那么就会使用 `await` 挂起并等待一次它们的结果。
这个过程不会阻塞线程, 也符合事件处理器处理事件时的依次处理的形式, 其主要服务JVM平台下的Java用户, 以允许使用更加丰富的响应式库来实现异步的事件处理。

<procedure title="支持的收集类型" collapsible="true">

- `java.util.concurrent.CompletionStage` (`java.util.concurrent.CompletableFuture`) (JVM)
- `kotlinx.coroutines.Deferred` (不支持 `kotlinx.coroutines.Job`)
- `kotlinx.coroutines.flow.Flow` (会被收集为 `List`)
- `kotlin.js.Promise` (JS)
- `org.reactivestreams.Publisher` (JVM) (不是 `reactor.core.publisher.Mono` 或 `reactor.core.publisher.Flux` 时:
  会被收集为 `List`)
- `reactor.core.publisher.Flux` (JVM) (会被收集为 `List`)
- `reactor.core.publisher.Mono` (JVM)
- `io.reactivex.CompletableSource` (JVM) (会挂起, 但是结果始终为 `null`)
- `io.reactivex.SingleSource` (JVM)
- `io.reactivex.MaybeSource` (JVM)
- `io.reactivex.ObservableSource` (JVM) (会被收集为 `List`)
- `io.reactivex.Flowable` (JVM) (会被收集为 `List`)
- `io.reactivex.rxjava3.core.CompletableSource` (JVM)
- `io.reactivex.rxjava3.core.SingleSource` (JVM)
- `io.reactivex.rxjava3.core.MaybeSource` (JVM)
- `io.reactivex.rxjava3.core.ObservableSource` (JVM) (会被收集为 `List`)
- `io.reactivex.rxjava3.core.Flowable` (JVM) (会被收集为 `List`)

<warning title="运行时库">

需要注意的是, 除了 Kotlin 自带的那些类型, 其他大部分响应式结果都需要额外的运行时库。
参考：[kotlinx-coroutines-reactive](https://github.com/Kotlin/kotlinx.coroutines/blob/master/reactive/README.md)。

</warning>

</procedure>

## 事件处理器上下文 EventListenerContext

每一个事件处理器在处理事件时, 都会被提供一个 `EventListenerContext`。

<deflist>
<def title="context">

`EventContext` 类型, 
本次事件处理流程的整体上下文。
其中包括本次流程中的一些有用信息, 例如被推送的**事件**。

</def>
<def title="event">

`Event` 类型, 
本次事件处理流程中被推送的那个事件。来自 `context.event`。

</def>
<def title="listener">

当前这个 `EventListener` 自身。

</def>
<def title="plainText">

本次事件处理器进行处理时, 用于匹配的事件中消息文本内容。

这是一个**可变**的属性, 它的初始值一般与 `messageContent.plainText` 相同, 如果不是 `MessageEvent` 则为 `null`。
这个属性主要的作用是服务拦截器、条件匹配逻辑等地方, 让他们可以将对文本内容的处理结果延续下去, 

比如第一个拦截器对文本进行“去除空白字符”(`String.trim`), 那么第二个拦截器便会在此基础上再做判断。

</def>
</deflist>

## 事件上下文 EventContext

一个在事件处理流程中流转的上下文。 用于承载本次事件处理前后的诸项信息。

<note>

`EventContext` 实现了 `CoroutineScope`, 
因此它可以作为一个协程作用域使用。它的协程上下文通常与 `EventDispatcher` 有关, 
但是不含有 `Job`。

</note>

<deflist>
<def title="event">

`Event` 类型, 
本次事件处理流程中被推送的那个事件。来自 `context.event`。

</def>
<def title="attributes">

可以由使用者自由使用的、本次流程中在事件处理器之间传递共享的附加属性集。

</def>
</deflist>

## 注解 API

simbot 定义了一套**注解API**，用来支持使用注解快速实现事件处理逻辑。
这套注解API主要由 `Spring Boot starter` 进行实现。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
class MyListeners {
    @Listener // 注解API，标记一个函数为事件处理函数
    suspend fun handle(event: Event) {
        // ...   
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
public class MyListeners {
    @Listener // 注解API，标记一个函数为事件处理函数
    public void handle(Event event) {
        // ...   
    }
}
```

</tab>
</tabs>

它被命名为 `quantcat(量子猫)`，
你可以前往文章
[量子猫](advanced-quantcat.md)
来了解更多。

## 事件推送

想要使事件处理器工作, 那么就要推送事件。可以通过 `EventDispatcher.push`
推送一个事件, 并得到一个处理结果流 `Flow<EventResult>`。

<note>

事件推送的任务通常是你安装的插件或者注册的 Bot 来完成的。如果只是普通的 Bot 应用开发者, 则大部分情况下不需要自行推送事件。

</note>

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val resultFlow = dispatcher.push(event)
// 事件推送的结果流是冷流, 
// 你必须收集这个流, 事件才会真正开始被处理
resultFlow.collect()
```

</tab>
<tab title="Java" group-key="Java">

在 Java 中直接操作 `Flow` 可能会有一些困难, 
你可以使用 `EventProcessors` 中提供的各种静态API来进行事件推送。

<if switcher-key="%ja%">

```Java
// 推送事件、并在异步中收集结果。
// 其中第三个参数 `application` 是用于执行异步任务的 `CoroutineScope` 类型, 
// 你可以使用 `Application` （继承了 `CoroutineScope`）, 
// 或者使用 Kotlin 的 `GlobalScope` （有关它的注意事项参见其文档注释）
var asyncListFuture = EventProcessors.pushAndCollectToAsync(dispatcher, event, application, new ArrayList<>());

// 如果希望收集为 List, 也有简写形式
var otherAsyncListFuture = EventProcessors.pushAndCollectToListAsync(dispatcher, event, application);

// 也可以使用 Java 中的 Collector, 就像在 Stream 中使用它一样
var asyncCollectListFuture = EventProcessors.pushAndCollectToAsync(dispatcher, event, application, Collectors.toList());

// 借助 Collector, 也可以实现一些复杂的结果收集, 比如：
// -> 只过滤出类型为 StandardEventResult.Simple 的结果
var asyncCollectSimpleListFuture = EventProcessors.pushAndCollectToAsync(
                dispatcher, event, application,
                Collectors.filtering(
                    result -> result instanceof StandardEventResult.Simple,
                    Collectors.toList()    
                ));

// -> 根据是否为 StandardEventResult.Error 为依据分组, 并计算每组的结果数量
var asyncTypeCountingFuture = EventProcessors.pushAndCollectToAsync(
                dispatcher, event, application,
                Collectors.partitioningBy(
                    result -> result instanceof StandardEventResult.Error,
                    Collectors.counting()
                ));
```

你也可以将结果转化为响应式的 `reactor.core.publisher.Flux`。

```Java
var resultFlux = EventProcessors.pushAndAsFlux(dispatcher, event);
resultFlux.subscribe(result -> {
    // 事件推送的结果流是冷流, 因此转化后的 `Flux` 也是冷的, 
    // 你必须消费其中的元素才能使得事件真正的被处理。
});
```

<warning>

使用 `pushAndAsFlux`
需要项目运行时环境中存在 [kotlinx-coroutines-reactor](https://github.com/Kotlin/kotlinx.coroutines/tree/master/reactive)。

</warning>

</if>


<if switcher-key="%jb%">

```Java
// 转化为阻塞的 Stream
var stream = EventProcessors.pushAndAsStream(dispatcher, event, application);
stream.forEach(result -> {
    // 因为 push 事件的结果 Flow 是冷流, 
    // 因此转化为 Stream 后也是冷的, 你必须使用 stream 的终结函数, 例如 forEach、collect 等, 
    // 事件才会被真正的处理。
});

// 推送事件、并阻塞地收集结果。
// 其中第三个参数 `application` 是用于执行异步任务的 `CoroutineScope` 类型, 
// 你可以使用 `Application` （继承了 `CoroutineScope`）, 
// 或者使用 Kotlin 的 `GlobalScope` （有关它的注意事项参见其文档注释）
var list = EventProcessors.pushAndCollectToBlocking(dispatcher, event, new ArrayList<>());

// 如果希望收集为 List, 也有简写形式
var otherList = EventProcessors.pushAndCollectToListBlocking(dispatcher, event);

// 也可以使用 Java 中的 Collector, 就像在 Stream 中使用它一样
var collectList = EventProcessors.pushAndCollectToBlocking(dispatcher, event, Collectors.toList());

// 借助 Collector, 也可以实现一些复杂的结果收集, 比如：
// -> 只过滤出类型为 StandardEventResult.Simple 的结果
var collectSimpleList = EventProcessors.pushAndCollectToBlocking(
        dispatcher, event,
        Collectors.filtering(
                result -> result instanceof StandardEventResult.Simple,
                Collectors.toList()
        ));

// -> 根据是否为 StandardEventResult.Error 为依据分组, 并计算每组的结果数量
var typeCounting = EventProcessors.pushAndCollectToBlocking(
        dispatcher, event,
        Collectors.partitioningBy(
                result -> result instanceof StandardEventResult.Error,
                Collectors.counting()
        ));
```

</if>
</tab>
</tabs>

如上面的示例中所说, 通过 `push` 得到的 `Flow` 结果是一个**冷流**, 因此你必须收集、消费其中的元素, 
它才会使得事件被处理, 并且这也受到你对这个流的中间操作。

举个例子：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val flow = dispatcher.push(event)
flow.take(2) // 取前两个元素
    .collect {
        // 消费结果
    }
```

</tab>
<tab title="Java" group-key="Java">

<if switcher-key="%ja%">

```Java
var flux = EventProcessors.pushAndAsFlux(dispatcher, event);
flux.take(2) // 取前两个结果
        .subscribe(result -> {
            // 消费结果
        });
```

</if>


<if switcher-key="%jb%">

```Java
var stream = EventProcessors.pushAndAsStream(dispatcher, event, application);
stream.limit(2) // 取前两个结果
        .forEach(result -> {
            // 消费结果
        });
```

</if>
</tab>
</tabs>

在示例中, 我们在获取到结果流时只取了**前两个**结果。此时, 在消费结果时真正处理了事件的事件处理器也**只有前两个**, 
因为我们得到的流是冷流, 每一次结果都是一次“实时”的事件处理。

你可以依据这些类型的特性来自由决定结果流的处理形式, 例如在收集前指定调度器, 
这时则可能在收集前便已经有事件处理器开始处理事件了。
