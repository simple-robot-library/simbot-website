---
switcher-label: JavaAPI风格
---

<show-structure for="chapter,procedure" depth="3"/>

# 走马观花

<tldr>
<p>春风得意马蹄疾，一日看尽长安花。</p>
<p>—— 唐·孟郊《登科后》</p>
</tldr>

> 本章节提供一些常见的代码示例与风格展示，但是**不会**对它们做过多介绍，甚至不会介绍。
> 详细的内容可前往文档各处查阅。

## 构建Application

<tabs group="impl">
<tab title="核心库">

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val application = launchSimpleApplication {
    // 配置...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        appConfigurer -> {
            // 配置 ...
        });

// 异步结果可转化为 CompletableFuture
var future = applicationAsync.asFuture();
// ...
```
{switcher-key="%ja%"}

```Java
var application = Applications.launchApplicationBlocking(
        Simple.INSTANCE, 
        appConfigurer -> {
            // 配置 ...
        });
// ...
```
{switcher-key="%jb%"}
```Java
var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        appConfigurer -> {
            // 配置 ...
        });

// 异步结果可转化为 CompletableFuture,
// 进而转化为响应式类型
var future = applicationAsync.asFuture();
var mono = Mono.fromFuture(future);
// ...
```
{switcher-key="%jr%"}
</tab>
</tabs>

</tab>
<tab title="Spring">

在Spring中，你不需要关系 `Application` 的构建。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@SpringBootApplication
@EnableSimbot // Enable simbot
class Main

fun main(args: Array<String>) {
    runApplication<Main>(*args)
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@SpringBootApplication
@EnableSimbot // Enable simbot
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
```

</tab>
</tabs>
</tab>
</tabs>

## 事件监听

### 任意事件

<tabs group="impl">
<tab title="核心库">

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
application.listeners {
    register { // this: EventListenerContext
        println("收到事件: $event")
        EventResult.of(42)
    }

    // 不需要返回 EventResult 的扩展函数
    process { // this: EventListenerContext
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.async(context -> {
            System.out.println("收到事件: " + context.getEvent());
            return CompletableFuture.completedFuture(
                    EventResult.of(42)
            );
        })
);
```
{switcher-key="%ja%"}

```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.block(context -> {
            System.out.println("收到事件: " + context.getEvent());
            return EventResult.of(42);
        })
);
```
{switcher-key="%jb%"}
```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.nonBlock(context -> {
            System.out.println("收到事件: " + context.getEvent());
            // EventResult.of 包裹任意响应式或可收集类型，
            // 也支持 CompletableFuture
            return EventResult.of(Mono.just("Value"));
        })
);
```
{switcher-key="%jr%"}
</tab>
</tabs>

</tab>
<tab title="Spring">

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
open class MyHandles {
    @Listener
    suspend fun onEvent(event: Event) {
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    public CompletableFuture<?> onEvent(Event event) {
        System.out.println("收到事件: " + event)
        return CompletableFuture.completedFuture(42);
    }
}
```
{switcher-key="%ja%"}

```Java
@Component
public class MyHandles {
    @Listener
    public void onEvent(Event event) {
        System.out.println("收到事件: " + event)
    }
}
```
{switcher-key="%jb%"}

```Java
@Component
public class MyHandles {
    @Listener
    public Mono<?> onEvent(Event event) {
        System.out.println("收到事件: " + event)
        return Mono.just(42);
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>
</tab>
</tabs>

### 指定类型事件

这里以 `ChatGroupMessageEvent`(聊天群消息事件) 为例。

<tabs group="impl">
<tab title="核心库">

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
application.listeners {
    listen<ChatGroupMessageEvent> { event -> 
        // this: EventListenerContext
        println("收到事件: $event")
        EventResult.empty()
    }

    // 不需要返回 EventResult 的扩展函数
    process<ChatGroupMessageEvent> { event ->
        // this: EventListenerContext
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.async(
            ChatGroupMessageEvent.class,
            (context, event) -> {
                System.out.println("收到事件: " + event);
                return CompletableFuture.completedFuture(
                        EventResult.of(42)
                );
            }
        )
);
```
{switcher-key="%ja%"}

```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.block(
            ChatGroupMessageEvent.class,
            (context, event) -> {
                System.out.println("收到事件: " + context.getEvent());
                return EventResult.of(42);
            }
        )
);
```
{switcher-key="%jb%"}
```Java
var eventListenerRegistrar = application.getEventDispatcher();

eventListenerRegistrar.register(
        EventListeners.nonBlock(
            ChatGroupMessageEvent.class,
            (context, event) -> {
                System.out.println("收到事件: " + context.getEvent());
                // EventResult.of 包裹任意响应式或可收集类型，
                // 也支持 CompletableFuture
                return EventResult.of(Mono.just(42));
            }
        )
);
```
{switcher-key="%jr%"}
</tab>
</tabs>

</tab>
<tab title="Spring">

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles1 {
    @Listener
    suspend fun onEvent(event: ChatGroupMessageEvent) {
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    public CompletableFuture<?> onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
        return CompletableFuture.completedFuture(42);
    }
}
```
{switcher-key="%ja%"}

```Java
@Component
public class MyHandles {
    @Listener
    public void onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
    }
}
```
{switcher-key="%jb%"}

```Java
@Component
public class MyHandles {
    @Listener
    public Mono<?> onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
        return Mono.just(42);
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>
</tab>
</tabs>


### 注解式条件过滤

<tabs group="impl">
<tab title="核心库">

> 核心库中没有预设的注解式条件过滤方案。
> 直接在代码中使用逻辑过滤，
> 比如 `if(xxx) {...}`。

</tab>
<tab title="Spring">

<tip title="匹配失效？">

一个常见的问题：当消息链中同时存在纯文本消息和其他类型的消息时，
`@Filter("文字")` 的匹配会“失效” ——

这实际上是因为当使用 `@Filter` 匹配时，被提取出的消息链中的纯文本消息存在一些**空字符**。
比如原消息是 `你好 @某用户`，此时提取出的纯文本消息是 `"你好 "`，这里结尾处有一个空字符。
而当使用 `@Filter("你好")` 进行匹配时，默认的匹配方式是正则全文匹配，
因此就会产生类似这种效果：

```
"你好".matches("你好 ")
```

进而导致匹配失败。

最简单的解决办法是加上注解 `@ContentTrim` 来表示提取出来用于匹配的纯文本内容先进行 `trim` 去除空字符后再匹配。

</tip>

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles1 {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    suspend fun onEvent(event: ChatGroupMessageEvent) {
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public CompletableFuture<?> onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
        return CompletableFuture.completedFuture(42);
    }
}
```
{switcher-key="%ja%"}

```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public void onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
    }
}
```
{switcher-key="%jb%"}


```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public Mono<?> onEvent(ChatGroupMessageEvent event) {
        System.out.println("收到事件: " + event)
        return Mono.just(42);
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>
</tab>
</tabs>

### 信息获取

> 此处(以及后续内容)忽略**核心库**或**Spring**环境的差异，环境差异不影响事件类型内的API。
> 下文以 Spring 环境为假设进行示例（因为代码会相对简洁，便于展示）。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles1 {
    @Listener
    @Filter("你好")
    suspend fun onEvent(event: ChatGroupMessageEvent) {
        println(event.id)
        println(event.time)
        
        // 消息内容，消息相关的事件中会有
        println(event.messageContent)
        // 消息内容中的纯文本内容
        println(event.messageContent.plainText)
        // 消息内容中的消息链
        println(event.messageContent.messages)
        
        // 事件主体，这里是‘聊天群消息事件’中的‘聊天群’
        val group = event.content()
        println(group.id)
        println(group.name)
        // ...
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public void onEvent(ChatGroupMessageEvent event) {
        System.out.println(event.getId());
        System.out.println(event.getTime());

        // 消息内容，消息相关的事件中会有
        var messageContent = event.getMessageContent();
        System.out.println(messageContent);
        // 消息内容中的纯文本内容
        System.out.println(messageContent.getPlainText());
        // 消息内容中的消息链
        System.out.println(messageContent.getMessages());
        
        // 事件主体，这里是‘聊天群消息事件’中的‘聊天群’
        event.getContentAsync().thenAccept(group -> {
            System.out.println(group.getId());
            System.out.println(group.getName());
        });
        
        // 异步处理倒也并非必须返回Future
        // 如果上述逻辑都并非阻塞，也不打算让后续处理函数等待它们完成
        // 那么就可以不用返回
    }
}
```
{switcher-key="%ja%"}


```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public void onEvent(ChatGroupMessageEvent event) {
        System.out.println(event.getId());
        System.out.println(event.getTime());

        // 消息内容，消息相关的事件中会有
        var messageContent = event.getMessageContent();
        System.out.println(messageContent);
        // 消息内容中的纯文本内容
        System.out.println(messageContent.getPlainText());
        // 消息内容中的消息链
        System.out.println(messageContent.getMessages());
        
        // 事件主体，这里是‘聊天群消息事件’中的‘聊天群’
        var group = event.getContent();
        System.out.println(group.getId());
        System.out.println(group.getName());
    }
}
```
{switcher-key="%jb%"}


```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public void onEvent(ChatGroupMessageEvent event) {
        System.out.println(event.getId());
        System.out.println(event.getTime());

        // 消息内容，消息相关的事件中会有
        var messageContent = event.getMessageContent();
        System.out.println(messageContent);
        // 消息内容中的纯文本内容
        System.out.println(messageContent.getPlainText());
        // 消息内容中的消息链
        System.out.println(messageContent.getMessages());
    
        // 事件主体，这里是‘聊天群消息事件’中的‘聊天群’
        event.getContentReserve()
                .transform(SuspendReserves.mono())
                // 异步中处理
                .subscribe(group -> {
                    System.out.println(group.getId());
                    System.out.println(group.getName());
                }); 
    
        // 响应式处理倒也并非必须返回响应式或可收集结果
        // 如果上述逻辑都并非阻塞，也不打算让后续处理函数等待它们完成
        // 那么就可以不用返回
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>

### 回复/发送消息

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles1 {
    @Listener
    @Filter("你好")
    suspend fun onEvent(event: ChatGroupMessageEvent) {
        // 回复"你也好"成功后，
        // 再向群内直接发送"你好呀"
        event.reply("你也好")
        event.content().send("你好呀")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public CompletableFuture<?> onEvent(ChatGroupMessageEvent event) {
        // 回复"你也好"成功后，
        // 再向群内直接发送"你好呀"
        return event.replyAsync("你也好")
                .thenCompose(r -> event.getContentAsync())
                .thenCompose(group -> group.sendAsync("你好呀"));
    }
}
```
{switcher-key="%ja%"}


```Java
@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public void onEvent(ChatGroupMessageEvent event) {
        // 回复"你也好"成功后，
        // 再向群内直接发送"你好呀"
        event.replyBlocking("你也好");
        event.getContent().sendBlocking("你好呀");
    }
}
```
{switcher-key="%jb%"}


```Java
import static love.forte.simbot.suspendrunner.reserve.SuspendReserves.mono;

@Component
public class MyHandles {
    @Listener
    @Filter("你好") // 匹配消息中的纯文本内容
    public Mono<Void> onEvent(ChatGroupMessageEvent event) {
        // 回复"你也好"成功后，
        // 再向群内直接发送"你好呀"
        return event.replyReserve("你也好")
                .transform(mono())
                .then(event.getContentReserve()
                        .transform(mono())
                        .flatMap(group ->
                                group.sendReserve("你好呀")
                                        .transform(mono())
                        )
                ).then();
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>


## 组件协同

安装多个组件，并监听它们的事件。

这里以 `QGGuildEvent` (QQ频道事件) 和 `OneBotEvent` (OneBot协议事件) 为例。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles1 {
    @Listener
    suspend fun onQGEvent(event: QGGuildEvent) {
        println("QQ频道: $event");
    }
    @Listener
    suspend fun onOBEvent(event: OneBotEvent) {
        println("OB协议: $event");
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    @Listener
    public void onQGEvent(QGGuildEvent event) {
        System.out.println("QQ频道: " + event);
    }
    @Listener
    public void onOBEvent(OneBotEvent event) {
        System.out.println("OB协议: " + event);
    }
}
```

</tab>
</tabs>
