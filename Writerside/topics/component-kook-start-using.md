---
switcher-label: JavaAPI风格
---

# 开始使用

希望从完整示例开始？前往 [](component-kook-first-bot.md)。

本页介绍如何安装 KOOK 组件、注册 Bot 并监听事件。需要提前准备好平台所需的 Bot 账号认证信息等内容，再选择核心库或 Spring Boot 的示例。

页面中的代码片段用于说明各步骤。组合到同一个程序时，请先创建应用并注册监听器，再注册和启动 Bot，最后等待应用结束。示例中的 `join` 或 `block` 应放在启动流程末尾。


## 安装

<include from="component-kook.md" element-id="install-core" />

> 参考
<a href="component-kook.md#安装" />
。

## 使用
### 创建Application

<tabs group="simbot4impl">
<tab group-key="core" title="核心库">

在 `simbot-core` 中，提供了一个基础的 `Application` 实现类型：`SimpleApplication`。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val app = launchSimpleApplication {
    // 使用KOOK组件相关的内容。
    // 代表同时安装 `KookComponent` 和 `KookBotManager`
    useKook()
    // 其他配置...
}

// 继续注册监听器和 Bot，最后再等待应用结束
```

</tab>
<tab title="Java" group-key="Java">

```Java
final var applicationAsync = Applications.launchApplicationAsync(
    Simple.INSTANCE,
    configurer -> {
        // 安装 `KookComponent` 和 `KookBotManager`
        configurer.install(KookComponent.Factory);
        configurer.install(KookBotManager.Factory);
        // 其他...
    }
);

// 后续可在此 Future 完成后注册监听器和 Bot
var applicationFuture = applicationAsync.asFuture();
```
{switcher-key=%ja%}

```Java
final var application = Applications.launchApplicationBlocking(
    Simple.INSTANCE,
    configurer -> {
        // 安装 `KookComponent` 和 `KookBotManager`
        configurer.install(KookComponent.Factory);
        configurer.install(KookBotManager.Factory);
        // 其他...
    }
);

// 继续注册监听器和 Bot，最后再等待应用结束
```
{switcher-key=%jb%}

```Java
var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        configurer -> {
            // 安装 `KookComponent` 和 `KookBotManager`
            configurer.install(KookComponent.Factory);
            configurer.install(KookBotManager.Factory);
            // 其他...
        }
);

// 后续可在响应式链中注册监听器和 Bot
var applicationMono = Mono.fromFuture(applicationAsync.asFuture());
```
{switcher-key=%jr%}


<tip switcher-key="%jr%">

响应式示例使用 Reactor，依赖与桥接方式参考 [](java-friendly.md#reactive-bridging)。

</tip>

</tab>
</tabs>

</tab>
<tab group-key="spring" title="Spring">

在 Spring Boot 中，不需要你手动构建 `Application`。
你只需要在你的启动类上标记 `@EnableSimbot` 来启用 simbot 即可。

KOOK组件支持SPI自动加载，因此默认情况下不需要手动安装
`KookComponent` 和 `KookBotManager` 。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@EnableSimbot
@SpringBootApplication
open class BotApplication

fun main(vararg args: String) {
    runApplication<BotApplication>(*args)
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@EnableSimbot
@SpringBootApplication
public class BotApplication {
    public static void main(String[] args) {
        SpringApplication.run(BotApplication.class, args);
    }
}
```

</tab>
</tabs>

</tab>
</tabs>

### 注册Bot

<tabs group="simbot4impl">
<tab group-key="core" title="核心库">

在 Application 构建完成后，即可从 `Application.botManagers`
中寻找你所需的管理器（比如组件的Bot管理器：`KookBotManager`）
并注册你的Bot。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
suspend fun main() {
    val app = launchSimpleApplication {
        useKook()
        // ...
    }

    app.configure()
    app.join()
}

suspend fun Application.configure() {
    // 寻找、获得所需的BotManager
    val botManager = botManagers.firstKookBotManager()
    // 注册你所需的bot
    val bot = botManager.registerWs(
        clientId = "...",
        token = "...",
    ) {
        // 一些其他的可选配置属性
        // 大部分属性都在 botConfiguration 内配置
        botConfiguration.apply {
            // 一些配置，例如超时、Ktor engine等..
        }
        // 外层是独属于组件类型的某些配置
        // 比如定期同步数据的同步周期
        this.syncPeriods
        // 其他...
    }

    // 启动你的bot
    bot.start()
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
public static void main(String[] args) {
    final var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        configurer -> {
            // 安装KOOK组件相关内容
            configurer.install(KookComponent.Factory);
            configurer.install(KookBotManager.Factory);
            // 其他...
        }
    );

    applicationAsync
        .asFuture()
        // Application 转化为 Future
        .thenApply(app -> {
            // 配置
            configure(app);
            return app;
        })
        .thenCompose(Application::asFuture)
        // 阻塞这个Future直到Application被cancel
        .join();
}

public static void configure(Application application) {
    // 寻找所需的BotManager
    // 可以选择遍历寻找
    final var found = application.getBotManagers().stream()
            .filter(it -> it instanceof KookBotManager)
            .map(it -> (KookBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var KookBotManager = KookBotManagersKt
            .firstKookBotManager(application.getBotManagers());

    // 注册Bot
    final var bot = KookBotManager.registerWs(
            "clientId",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfiguration 内配置
                final var botConfiguration = config.getBotConfiguration();
                // 一些配置，例如超时、Ktor engine等..

                // 外层是独属于组件类型的某些配置
                // 比如定期同步数据的同步周期
                final var syncPeriods = config.getSyncPeriods();
                // ...
                config.setSyncPeriods(syncPeriods);
                // 其他...

                return Unit.INSTANCE;
            });
    // 启动
    final var future = bot.startAsync()
            .whenComplete((r, ex) -> {
                // 在使用 Future 的时候，记得处理异常
                if (ex != null) {
                    Logger.getGlobal().log(
                            Level.SEVERE,
                            "bot启动出现异常！",
                            ex
                    );
                }
            });
    // 你可以选择处理等待这个future，也可以选择不管他，直接在异步中处理。
}
```
{switcher-key=%ja%}

```Java
public static void main(String[] args) {
    final var application = Applications.launchApplicationBlocking(
            Simple.INSTANCE,
            configurer -> {
                // 安装KOOK组件相关内容
                configurer.install(KookComponent.Factory);
                configurer.install(KookBotManager.Factory);
                // 其他...
            }
    );

    configure(application);
    application.joinBlocking();
}

public static void configure(Application application) {
    // 寻找所需的BotManager
    // 可以选择遍历寻找
    final var found = application.getBotManagers().stream()
            .filter(it -> it instanceof KookBotManager)
            .map(it -> (KookBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var KookBotManager = KookBotManagerUsageKt
            .firstKookBotManager(application.getBotManagers());

    // 注册Bot
    final var bot = KookBotManager.registerWs(
            "clientId",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfiguration 内配置
                final var botConfiguration = config.getBotConfiguration();
                // 一些配置，例如超时、Ktor engine等..

                // 外层是独属于组件类型的某些配置
                // 比如定期同步数据的同步周期
                final var syncPeriods = config.getSyncPeriods();
                // ...
                config.setSyncPeriods(syncPeriods);
                // 其他...

                return Unit.INSTANCE;
            });
    // 启动
    bot.startBlocking();
}
```
{switcher-key=%jb%}

```Java
public static void main(String[] args) {
    var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        configurer -> {
            // 安装QQ机器人组件相关内容
            configurer.install(KookComponent.Factory);
            configurer.install(KookBotManager.Factory);
            // 其他...
        }
    );

    // 例如：转化为 reactor.core.publisher.Mono;
    var mono = Mono.fromFuture(applicationAsync.asFuture())
        // 配置 Application
        .doOnNext(CoreMain::configure)
        .flatMap(app ->
            Mono.from(app.joinReactive())
        );

    // 使用这个响应式类型，例如阻塞它。
    /// 阻塞直到被cancel
    mono.block();
}

public static void configure(Application application) {
    // 寻找所需的BotManager
    // 可以选择遍历寻找
    final var found = application.getBotManagers().stream()
            .filter(it -> it instanceof KookBotManager)
            .map(it -> (KookBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var KookBotManager = KookBotManagerUsageKt
            .firstKookBotManager(application.getBotManagers());

    // 注册Bot
    final var bot = KookBotManager.registerWs(
            "clientId",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfiguration 内配置
                final var botConfiguration = config.getBotConfiguration();
                // 一些配置，例如超时、Ktor engine等..

                // 外层是独属于组件类型的某些配置
                // 比如定期同步数据的同步周期
                final var syncPeriods = config.getSyncPeriods();
                // ...
                config.setSyncPeriods(syncPeriods);
                // 其他...

                return Unit.INSTANCE;
            });
    // 启动
    Mono.from(bot.startReactive())
            // 在使用响应式编程的时候，记得处理异常
            .doOnError(ex -> {
                Logger.getGlobal().log(
                        Level.SEVERE,
                        "bot启动出现异常！",
                        ex
                );
            })
            // 你也可以选择返回Mono然后做进一步处理
            // 此处直接使其在异步中运行。
            .subscribe();
}
```
{switcher-key=%jr%}
</tab>
</tabs>

</tab>
<tab group-key="spring" title="Spring">

在 Spring 中，通常可以选择使用 `.bot.json` 格式的配置文件来快速、自动地批量注册bot。

默认情况下，在你的项目的资源目录
<path>resource</path> 
中创建目录 
<path>/simbot-bots/</path> ，
然后前往参考
<b>
<a href="component-kook-bot-config.md" />
</b> 
并配置你的 JSON 格式的配置文件，例如 `abc.bot.json`。

默认情况下starter会自动扫描上述资源目录并加载、自动启动它们，这一切是在**异步**中进行的。

<tip>

上述的 _资源目录 `/simbot-bots/`_ 、_自动启动_、以及 _在异步中启动_ 这些都是可配置的。

有关Spring Boot环境下可用的**配置信息**，可前往
[集成Spring Boot](Spring-Boot.md)
参考更多。
</tip>

</tab>
</tabs>

### 事件监听

<tabs group="simbot4impl">
<tab group-key="core" title="核心库">

从 `Application` 中获取 `EventDispatcher` 即可注册事件监听函数。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

Kotlin 中，可以使用 `Application.listeners {}` 扩展函数。

```Kotlin
// 省略构建Application相关内容...

suspend fun Application.configure() {
    // bot相关内容省略....

    // Kotlin 中，可以使用 Application.listeners 扩展函数。
    listeners {
        // 使用 listen 监听一个事件
        // 此处是一个标准库中通用的类型：聊天子频道消息事件
        listen<ChatChannelMessageEvent> { event ->
            println("Event: $event")
            if (event.messageContent.plainText?.trim() == "你好") {
                event.reply("你也好")
            }

            // 使用listen时必须返回一个EventResult类型的结果
            EventResult.empty()
        }

        // 使用 process 监听一个事件
        // 此处监听的是KOOK组件中的专属类型：普通频道内的消息事件
        process<KookChannelMessageEvent> { event ->
            println("Event: $event")
            if (event.messageContent.plainText.trim() == "你好") {
                event.reply("你也好")
            }

            // 使用 process 不需要返回 EventResult，默认视为返回 EventResult.empty()
        }
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
// 省略构建Application相关内容...

public static void configure(Application application) {
    // bot相关内容省略....

    final var eventDispatcher = application.getEventDispatcher();

    // 监听一个KOOK组件中的专属类型：普通频道内的消息事件
    eventDispatcher.register(
            EventListeners.async(
                    KookChannelMessageEvent.class,
                    (context, event) -> {
                        System.out.println("Event: " + event);
                        if ("你好".equals(event.getMessageContent().getPlainText())) {
                            // 返回一个异步的EventResult类型的结果
                            return event.replyAsync("你也好")
                                    .thenApply(result -> EventResult.empty());
                        }

                        // 返回一个异步的EventResult类型的结果
                        return CompletableFuture.completedFuture(EventResult.empty());
                    }
            )
    );
}
```
{switcher-key=%ja%}

<tip switcher-key="%ja%">

也可以使用 `EventListeners.nonBlock` 后返回一个内容为 `Future` 的 `CompletableFuture`:

```Java
var future = ...
return EventResult.of(future);
```

此方式与响应式风格的API方式类似。

</tip>

```Java
// 省略构建Application相关内容...

public static void configure(Application application) {
    // bot相关内容省略....
    
    final var eventDispatcher = application.getEventDispatcher();

    // 监听一个KOOK组件中的专属类型：普通频道内的消息事件
    eventDispatcher.register(
        EventListeners.block(
            KookChannelMessageEvent.class,
            (context, event) -> {
                System.out.println("Event: " + event);
                if ("你好".equals(event.getMessageContent().getPlainText())) {
                    event.replyBlocking("你也好");
                }

                // 返回一个EventResult类型的结果
                return EventResult.empty();
            }
        )
    );
}
```
{switcher-key=%jb%}

```Java
// 省略构建Application相关内容...

public static void configure(Application application) {
    // bot相关内容省略....

    final var eventDispatcher = application.getEventDispatcher();

    // 监听一个KOOK组件中的专属类型：普通频道内的消息事件
    eventDispatcher.register(
            EventListeners.nonBlock(
                    KookChannelMessageEvent.class,
                    (context, event) -> {
                        System.out.println("Event: " + event);
                        if ("你好".equals(event.getMessageContent().getPlainText())) {
                            // 返回一个内容是响应式类型的EventResult类型的结果
                            final var mono = Mono.from(event.replyReactive("你也好"))
                                    .then();

                            return EventResult.of(mono);
                        }

                        // 返回一个空的EventResult类型的结果
                        return EventResult.empty();
                    }
            )
    );
}
```
{switcher-key=%jr%}

<tip switcher-key="%jr%">

`EventResult.of(...)` 的内容可以是异步的或响应式的，
事件处理器会对这种结果进行一次收集或挂起。

</tip>

</tab>
</tabs>

<note>

更多有关 `EventResult` 的信息可参考
<a href="basic-event-listener.md#EventResult">EventResult</a>

</note>

</tab>
<tab group-key="spring" title="Spring">

在 Spring 中，使用注解 `@Listener` 注册一个监听函数。
可监听到的事件即为参数中的事件类型。
也因此，参数中的事件类型的参数应当**最多**只有1个。

<tip>

`@Listener` 需要在被Spring管理的bean中使用，例如需要在类上标记 `@Component`。

</tip>

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyHandles {
    /**
     * 此处是一个标准库中通用的类型：子频道消息事件
     * 在KOOK组件中，它的真实实现类型会是 KookChannelMessageEvent
     */
    @Listener
    suspend fun onChannelMessage(event: ChatChannelMessageEvent) {
        println("ChatChannelMessageEvent: $event")
    }
    
    /**
     * 此处监听的是KOOK组件中的专属类型：普通频道内的消息事件。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    suspend fun onMessage(event: KookChannelMessageEvent) {
        println("KookChannelMessageEvent: $event")
        // 回复消息
        event.reply("你也好")
    }
}


```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyHandles {
    /**
     * 此处是一个标准库中通用的类型：子频道消息事件
     * 在KOOK组件中，它的真实实现类型会是 KookChannelMessageEvent
     */
    @Listener
    public void onChannelMessage(ChatChannelMessageEvent event) {
        System.out.println("ChatChannelMessageEvent: " + event);
    }

    /**
     * 此处监听的是KOOK组件中的专属类型：普通频道内的消息事件。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public CompletableFuture<?> onMessage(KookChannelMessageEvent event) {
        System.out.println("KookChannelMessageEvent: " + event);
        return event.replyAsync("你也好");
        // 可以直接返回任意 Future 类型，
        // 或者返回 EventResult，其中包裹着 Future 类型。
    }
}
```
{switcher-key=%ja%}

```Java
@Component
public class MyHandles {
    /**
     * 此处是一个标准库中通用的类型：子频道消息事件
     * 在KOOK组件中，它的真实实现类型会是 KookChannelMessageEvent
     */
    @Listener
    public void onChannelMessage(ChatChannelMessageEvent event) {
        System.out.println("ChatChannelMessageEvent: " + event);
    }

    /**
     * 此处监听的是KOOK组件中的专属类型：普通频道内的消息事件。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public void onMessage(KookChannelMessageEvent event) {
        System.out.println("KookChannelMessageEvent: " + event);
        event.replyBlocking("你也好");
    }
}
```
{switcher-key=%jb%}

```Java
@Component
public class MyHandles {
    /**
     * 此处是一个标准库中通用的类型：子频道消息事件
     * 在KOOK组件中，它的真实实现类型会是 KookChannelMessageEvent
     */
    @Listener
    public void onChannelMessage(ChatChannelMessageEvent event) {
        System.out.println("ChatChannelMessageEvent: " + event);
    }

    /**
     * 此处监听的是KOOK组件中的专属类型：普通频道内的消息事件。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public Mono<?> onMessage(KookChannelMessageEvent event) {
        System.out.println("KookChannelMessageEvent: " + event);
        return Mono.from(event.replyReactive("你也好"));
        // 可以直接返回任意(kotlinx.coroutines支持的)响应式类型，
        // 不过需要注意，确保运行时环境中有对应的依赖，
        // 以Mono为例，需要添加 [[[kotlinx-coroutines-reactor|https://github.com/Kotlin/kotlinx.coroutines/tree/master/reactive]]]
        // 也可以返回 EventResult，其中包裹着响应式类型。
    }
}
```
{switcher-key=%jr%}


</tab>
</tabs>

</tab>
</tabs>
