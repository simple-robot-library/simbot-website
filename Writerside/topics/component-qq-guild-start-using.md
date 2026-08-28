---
switcher-label: JavaAPI风格
---

# 开始使用

## 安装

<include from="component-qq-guild.md" element-id="install-core" />

> 参考
<a href="component-qq-guild.md#安装" />
。

## 使用

### API 服务地址

QQ 开放平台自 `2026-08-10` 起将接口调用域名统一为
`https://api.bot.qq.com`，不再提供独立的沙箱接口域名。
组件默认使用此统一地址，无需额外配置。

旧的 `useSandboxServerUrl()` 和配置值 `"SANDBOX"` 仅为兼容已有项目而保留，
现已弃用，不应在新配置中继续使用。需要使用代理等自定义地址时，
可通过 `serverUrl` 显式配置。有关配置文件的完整说明，参考 [](component-qq-guild-bot-config.md) 。

### 事件监听配置

如果你不使用 [webhook](component-qq-guild-Webhook.md) 订阅事件，
那么你 _可能_ 需要配置事件订阅的 `intents`，因为 `intents` 的默认值只有三个类型的事件。

<tabs>
<tab title="代码配置">

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
botManager.register("..", "..", "..") {
    botConfig {
        // 配置Intents，例如追加群聊事件支持
        intents += EventIntents.GroupAndC2CEvent.intents
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```java
QQGuildBotManager manager = ...;
botManager.register("..", "..", "..", qgBotConfig -> {
    qgBotConfig.botConfig(botConfig -> {
        botConfig.addIntents(EventIntents.GroupAndC2CEvent.getIntents());
    });
});
```

</tab>
</tabs>

</tab>
<tab title="配置文件(在Spring中)">

示例中的 `intents` 的数值为在默认值的基础上添加了 `group_and_c2c_event` 类型事件的位值的最终数值。

```json
{
  "component": "simbot.qqguild",
  "ticket": {
    "appId": "...",
    "secret": "...",
    "token": "..."
  },
  "config": {
    "intents": {
      "type": "raw",
      "intents": 1107296259
    }
  }
}
```

> 有关配置文件更多内容和属性说明，参考 [](component-qq-guild-bot-config.md) 。

</tab>
</tabs>

### 创建Application

<tabs group="simbot4impl">
<tab group-key="core" title="核心库">

在 `simbot-core` 中，提供了一个基础的 `Application` 实现类型：`SimpleApplication`。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val app = launchSimpleApplication {
    // 使用QQ机器人组件相关的内容。
    // 代表同时安装 `QQGuildComponent` 和 `QQGuildBotManager`
    useQQGuild()
    // 其他配置...
}

app.join() // 挂起app直到cancel它
```

</tab>
<tab title="Java" group-key="Java">

```Java
final var applicationAsync = Applications.launchApplicationAsync(
    Simple.INSTANCE,
    configurer -> {
        // 安装 `QQGuildComponent` 和 `QQGuildBotManager`
        configurer.install(QQGuildComponent.Factory);
        configurer.install(QQGuildBotManager.Factory);
        // 其他...
    }
);

applicationAsync
        .asFuture()
        // Application 转化为 Future
        .thenCompose(Application::asFuture)
        // 阻塞这个Future直到Application被cancel
        .join();
```
{switcher-key=%ja%}

```Java
final var application = Applications.launchApplicationBlocking(
    Simple.INSTANCE,
    configurer -> {
        // 安装 `QQGuildComponent` 和 `QQGuildBotManager`
        configurer.install(QQGuildComponent.Factory);
        configurer.install(QQGuildBotManager.Factory);
        // 其他...
    }
);

// 阻塞直到被cancel
application.joinBlocking();
```
{switcher-key=%jb%}

```Java
var applicationAsync = Applications.launchApplicationAsync(
        Simple.INSTANCE,
        configurer -> {
            // 安装 `QQGuildComponent` 和 `QQGuildBotManager`
            configurer.install(QQGuildComponent.Factory);
            configurer.install(QQGuildBotManager.Factory);
            // 其他...
        }
);

// 例如：转化为 reactor.core.publisher.Mono;
var mono = Mono.fromFuture(applicationAsync.asFuture())
        .flatMap(app ->
                app.joinReserve().transform(
                        SuspendReserves.mono()
                )
        );

// 使用这个响应式类型，例如阻塞它。
/// 阻塞直到被cancel
mono.block();
```
{switcher-key=%jr%}

</tab>
</tabs>

</tab>
<tab group-key="spring" title="Spring">

在 Spring Boot 中，不需要你手动构建 `Application`。
你只需要在你的启动类上标记 `@EnableSimbot` 来启用 simbot 即可。

QQ机器人组件支持SPI自动加载，因此默认情况下不需要手动安装
`QQGuildComponent` 和 `QQGuildBotManager` 。

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
中寻找你所需的管理器（比如组件的Bot管理器：`QQGuildBotManager`）
并注册你的Bot。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
suspend fun main() {
    val app = launchSimpleApplication {
        useQQGuild()
        // ...
    }

    app.configure()
    app.join()
}

suspend fun Application.configure() {
    // 寻找、获得所需的BotManager
    val botManager = botManagers.firstQQGuildBotManager()
    // 注册你所需的bot
    val bot = botManager.register(
        appId = "...",
        secret = "...",
        token = "...",
    ) {
        // 一些其他的可选配置属性
        // 大部分属性都在 botConfigure 内配置
        botConfigure = ConfigurerFunction {
            // 比如添加订阅QQ群聊和C2C的事件。
            // 如果不配置，默认情况下仅订阅：
            // - 频道相关事件
            // - 频道成员相关事件
            // - 公域消息相关事件
            intents += EventIntents.GroupAndC2CEvent.intents
            // 如果要使用 [[[Webhook|component-qq-guild-Webhook.md]]] 的订阅方式，
            // 通过此属性取消 ws 的连接
            disableWs = true
            // 其他...
        }
        // 外层是独属于组件类型的某些配置
        cacheConfig = null
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
            // 安装QQGuild组件相关内容
            configurer.install(QQGuildComponent.Factory);
            configurer.install(QQGuildBotManager.Factory);
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
            .filter(it -> it instanceof QQGuildBotManager)
            .map(it -> (QQGuildBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var qqGuildBotManager = QQGuildBotManagerUsageKt
            .firstQQGuildBotManager(application.getBotManagers());

    // 注册Bot
    // 注册
    final var bot = qqGuildBotManager.register(
            "appid",
            "secret",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfigure 内配置
                config.botConfig(botConfig -> {
                    // 比如添加订阅QQ群聊和C2C的事件。
                    // 如果不配置，默认情况下仅订阅：
                    // - 频道相关事件
                    // - 频道成员相关事件
                    // - 公域消息相关事件
                    botConfig.setIntentsValue(
                            // 位运算合并 QQ群聊和C2C事件 的intents值
                            botConfig.getIntentsValue() | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue()
                    );
                    
                    // 如果要使用 [[[Webhook|component-qq-guild-Webhook.md]]] 的订阅方式，
                    // 通过此属性取消 ws 的连接
                    botConfig.setDisableWs(true);
                });

                // 外层是独属于组件类型的某些配置
                config.setCacheConfig(null);
                // 其他...
            });
    // 启动
    final var future = bot.startAsync().whenComplete((r, ex) -> {
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
                // 安装QQGuild组件相关内容
                configurer.install(QQGuildComponent.Factory);
                configurer.install(QQGuildBotManager.Factory);
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
            .filter(it -> it instanceof QQGuildBotManager)
            .map(it -> (QQGuildBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var qqGuildBotManager = QQGuildBotManagerUsageKt
            .firstQQGuildBotManager(application.getBotManagers());

    // 注册Bot
    // 注册
    final var bot = qqGuildBotManager.register(
            "appid",
            "secret",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfigure 内配置
                config.botConfig(botConfig -> {
                    // 比如添加订阅QQ群聊和C2C的事件。
                    // 如果不配置，默认情况下仅订阅：
                    // - 频道相关事件
                    // - 频道成员相关事件
                    // - 公域消息相关事件
                    botConfig.setIntentsValue(
                            // 位运算合并 QQ群聊和C2C事件 的intents值
                            botConfig.getIntentsValue() | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue()
                    );
                });

                // 外层是独属于组件类型的某些配置
                config.setCacheConfig(null);
                // 其他...
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
            configurer.install(QQGuildComponent.Factory);
            configurer.install(QQGuildBotManager.Factory);
            // 其他...
        }
    );

    // 例如：转化为 reactor.core.publisher.Mono;
    var mono = Mono.fromFuture(applicationAsync.asFuture())
        // 配置 Application
        .doOnNext(CoreMain::configure)
        .flatMap(app ->
            app.joinReserve().transform(
                SuspendReserves.mono()
            )
        );

    // 使用这个响应式类型，例如阻塞它。
    /// 阻塞直到被cancel
    mono.block();
}

public static void configure(Application application) {
    // 寻找所需的BotManager
    // 可以选择遍历寻找
    final var found = application.getBotManagers().stream()
            .filter(it -> it instanceof QQGuildBotManager)
            .map(it -> (QQGuildBotManager) it)
            .findFirst()
            .orElseThrow();

    // 也可以选择使用辅助API
    final var qqGuildBotManager = QQGuildBotManagerUsageKt
            .firstQQGuildBotManager(application.getBotManagers());

    // 注册Bot
    // 注册
    final var bot = qqGuildBotManager.register(
            "appid",
            "secret",
            "token",
            config -> {
                // 一些其他的可选配置属性
                // 大部分属性都在 botConfigure 内配置
                config.botConfig(botConfig -> {
                    // 比如添加订阅QQ群聊和C2C的事件。
                    // 如果不配置，默认情况下仅订阅：
                    // - 频道相关事件
                    // - 频道成员相关事件
                    // - 公域消息相关事件
                    botConfig.setIntentsValue(
                            // 位运算合并 QQ群聊和C2C事件 的intents值
                            botConfig.getIntentsValue() | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue()
                    );
                });

                // 外层是独属于组件类型的某些配置
                config.setCacheConfig(null);
                // 其他...
            });
    // 启动
    bot.startReserve()
            .transform(SuspendReserves.mono())
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
<a href="component-qq-guild-bot-config.md" />
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

### Webhook

使用 Webhook 接收事件参考 [](component-qq-guild-Webhook.md) 。

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
        // 此处是一个标准库中通用的类型：聊天群消息事件
        listen<ChatGroupMessageEvent> { event ->
            println("Event: $event")
            if (event.messageContent.plainText?.trim() == "你好") {
                event.reply("你也好")
            }

            // 使用listen时必须返回一个EventResult类型的结果
            EventResult.empty()
        }

        // 使用 process 监听一个事件
        // 此处监听的是QQ机器人组件中的专属类型：文字子频道中的At消息事件
        process<QGAtMessageCreateEvent> { event ->
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

    // 监听一个QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息事件
    eventDispatcher.register(
            EventListeners.async(
                    QGAtMessageCreateEvent.class,
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

    // 监听一个QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息事件
    eventDispatcher.register(
        EventListeners.block(
            QGAtMessageCreateEvent.class,
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

    // 监听一个QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息事件
    eventDispatcher.register(
            EventListeners.nonBlock(
                    QGAtMessageCreateEvent.class,
                    (context, event) -> {
                        System.out.println("Event: " + event);
                        if ("你好".equals(event.getMessageContent().getPlainText())) {
                            // 返回一个内容是响应式类型的EventResult类型的结果
                            final var mono = event.replyReserve("你也好")
                                    .transform(SuspendReserves.mono())
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
     * 此处是一个标准库中通用的类型：聊天群消息事件
     * 在QQ机器人组件中，它的真实实现类型会是QGGroupAtMessageCreateEvent
     */
    @Listener
    suspend fun onGroupMessage(event: ChatGroupMessageEvent) {
        println("ChatGroupMessageEvent: $event")
    }
    
    /**
     * 此处监听的是QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    suspend fun onMessage(event: QGAtMessageCreateEvent) {
        println("QGAtMessageCreateEvent: $event")
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
     * 此处是一个标准库中通用的类型：聊天群消息事件
     * 在QQ机器人组件中，它的真实实现类型会是QGGroupAtMessageCreateEvent
     */
    @Listener
    public void onGroupMessage(ChatGroupMessageEvent event) {
        System.out.println("ChatGroupMessageEvent: " + event);
    }

    /**
     * 此处监听的是QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public CompletableFuture<?> onMessage(QGAtMessageCreateEvent event) {
        System.out.println("QGAtMessageCreateEvent: " + event);
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
     * 此处是一个标准库中通用的类型：聊天群消息事件
     * 在QQ机器人组件中，它的真实实现类型会是QGGroupAtMessageCreateEvent
     */
    @Listener
    public void onGroupMessage(ChatGroupMessageEvent event) {
        System.out.println("ChatGroupMessageEvent: " + event);
    }

    /**
     * 此处监听的是QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public void onMessage(QGAtMessageCreateEvent event) {
        System.out.println("QGAtMessageCreateEvent: " + event);
        event.replyBlocking("你也好");
    }
}
```
{switcher-key=%jb%}

```Java
@Component
public class MyHandles {
    /**
     * 此处是一个标准库中通用的类型：聊天群消息事件
     * 在QQ机器人组件中，它的真实实现类型会是QGGroupAtMessageCreateEvent
     */
    @Listener
    public void onGroupMessage(ChatGroupMessageEvent event) {
        System.out.println("ChatGroupMessageEvent: " + event);
    }

    /**
     * 此处监听的是QQ机器人组件中的专属类型：QQ频道中文字子频道的At消息。
     * 并且过滤消息：消息中的文本消息去除前后空字符后，等于 '你好'
     */
    @Listener
    @ContentTrim
    @Filter("你好")
    public Mono<?> onMessage(QGAtMessageCreateEvent event) {
        System.out.println("QGAtMessageCreateEvent: " + event);
        return event.replyReserve("你也好")
            .transform(SuspendReserves.mono());
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
