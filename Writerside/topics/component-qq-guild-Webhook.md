# Webhook

<tip>

从组件 `v4.1.0` 开始支持 Webhook ，
参考:
- [#223](https://github.com/simple-robot/simbot-component-qq-guild/pull/223)

</tip>

根据官方文档的说法：

![QQ机器人-websocket不再维护.png](QQ机器人-websocket不再维护.png)

因此后续应该就只剩下 webhook 一种事件订阅方式了，也就是客户端作为被动接受事件的一方。

本章节简单介绍下在QQ机器人组件中如何使用 webhook 的方式接收事件。

## 禁用Websocket

首先，在配置中禁用 ws 的连接。

<tabs>
<tab title="配置文件">

如果你在使用配置文件（常见于在配合spring时），添加配置项 `config.disableWs=true`

```json
{
  "ticket": {
    "appId": "...",
    "secret": "...",
    "secret": "...",
  },
 "config": {
   "disableWs"：true
 } 
}
```

</tab>
<tab title="代码配置">

```kotlin
// 设置 disableWs 为 true
configuration.disableWs = true
```

</tab>
</tabs>

## 处理HTTP请求

Webhook 通过接收来自QQ的事件推送请求来实现事件监听。
在组件中，暂不支持内嵌的 HTTP 服务器 (参考 [#224](https://github.com/simple-robot/simbot-component-qq-guild/issues/224))，
因此你需要自行搭建 HTTP 服务器。

此处给出在 Spring Boot 和 Ktor server 场景下的示例。

<tabs>
<tab title="Spring web">

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
private const val SIGNATURE_HEAD = "X-Signature-Ed25519"
private const val TIMESTAMP_HEAD = "X-Signature-Timestamp"

/**
 * 处理所有qq机器人的回调请求的处理器。
 */
@RestController
@RequestMapping("/callback")
class CallbackHandler(
    private val application: Application
) {
    /**
     * 处理 `/callback/qq/{appId}` 的事件回调请求，
     * 找到对应的 bot 并向其推送事件。
     */
    @PostMapping("/qq/{appId}")
    fun handleEvent(
        @PathVariable("appId") appId: String,
        @RequestHeader(SIGNATURE_HEAD) signature: String,
        @RequestHeader(TIMESTAMP_HEAD) timestamp: String,
        @RequestBody payload: String,
    ): CompletableFuture<out ResponseEntity<Any?>> {
        // 寻找指定 `appId` 的 QGBot
        val targetBot = application.botManagers
            .filterIsQQGuildBotManagers()
            .firstNotNullOfOrNull {
                it.all().firstOrNull { bot ->
                    bot.source.ticket.appId == appId
                }
            }

        // 如果找不到，响应 404 异常
        if (targetBot == null) {
            throw ResponseStatusException(
                HttpStatus.NOT_FOUND,
                "app $appId not found"
            )
        }

        // 在 servlet web 中，在异步中处理.
        // 作用域、是否要用异步等根据你的项目情况调整。
        val entityAsync = application.async {
            val result = targetBot.emitEvent(
                payload,
            ) {
                // 配置 ed25519SignatureVerification, 即代表进行签名校验
                ed25519SignatureVerification = Ed25519SignatureVerification(
                    signature,
                    timestamp
                )
            }

            val body: Any? = when (result) {
                is EmitResult.Verified -> result.verified
                else -> null
            }

            // 响应结果。
            ResponseEntity.ok(body)
        }

        return entityAsync.asCompletableFuture()
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
/**
 * 处理所有qq机器人的回调请求的处理器。
 */
@RestController
@RequestMapping("/callback")
public class CallbackHandler {
    private static final String SIGNATURE_HEAD = "X-Signature-Ed25519";
    private static final String TIMESTAMP_HEAD = "X-Signature-Timestamp";

    private final Application application;

    public CallbackHandler(Application application) {
        this.application = application;
    }

    /**
     * 处理 `/callback/qq/{appId}` 的事件回调请求，
     * 找到对应的 bot 并向其推送事件。
     */
    @PostMapping("/qq/{appId}")
    public CompletableFuture<ResponseEntity<?>> handleEvent(
            @PathVariable("appId") String appId,
            @RequestHeader(SIGNATURE_HEAD) String signature,
            @RequestHeader(TIMESTAMP_HEAD) String timestamp,
            @RequestBody String payload
    ) {
        // 寻找指定 `appId` 的 QGBot
        final var targetBot = application.getBotManagers().stream()
                // 1. 寻找类型是 QQGuildBotManager 的 BotManager
                .filter(manager -> manager instanceof QQGuildBotManager)
                .map(QQGuildBotManager.class::cast)
                // 2. 寻找 appId 匹配的 bot
                .flatMap(manager ->
                        // 使用 manager.all() 可以直接访问 QGBot 类型，
                        // 而使用 manager.allStreamable() 得到的是 Bot 类型，需要再转化一次
                        // 二者都可以，这里选择第一个方案
                        Streamable.of(manager.all()).asStream())
                .filter(bot -> {
                    // 寻找 bot.appId 为函数入参 appId 的 bot
                    // bot.id 本质上也是使用的 appId, 因此直接使用 bot.getId().toString() 也是可以的。
                    var botAppId = bot.getSource().getTicket().getAppId();
                    return appId.equals(botAppId);
                })
                // 得到第一个符合条件的bot
                .findFirst()
                // 如果没找到，自行处理。这里选择抛出异常并响应404。
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "app " + appId + " not found"));

        // 在 servlet web 中，在异步中处理.
        // 作用域、是否要用异步等根据你的项目情况调整。

        // 如果要进行接口校验，配置 ed25519 校验所需要的内容
        final var options = new EmitEventOptions();
        options.setEd25519SignatureVerification(
                new Ed25519SignatureVerification(
                        signature,
                        timestamp
                )
        );

        // 推送事件。如有需要，你也可以选择使用阻塞API (emitEventAsyncBlocking)
        var future = targetBot.emitEventAsync(payload, options);

        // 得到处理结果（的future），并返回body
        // 如果没有需要返回的body，也可以是null
        return future.thenApply(result -> {
            var body = switch (result) {
                case EmitResult.Verified verified -> verified.getVerified();
                default -> null;
            };

            // 将 Body 放到响应体中，返回。
            return ResponseEntity.ok(body);
        });
    }
}
```

</tab>
</tabs>
</tab>
<tab title="Spring webflux">

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
private const val SIGNATURE_HEAD = "X-Signature-Ed25519"
private const val TIMESTAMP_HEAD = "X-Signature-Timestamp"

/**
 * 处理所有qq机器人的回调请求的处理器。
 */
@RestController
@RequestMapping("/callback")
class CallbackHandler(
    private val application: Application
) {
    /**
     * 处理 `/callback/qq/{appId}` 的事件回调请求，
     * 找到对应的 bot 并向其推送事件。
     */
    @PostMapping("/qq/{appId}")
    suspend fun handleEvent(
        @PathVariable("appId") appId: String,
        @RequestHeader(SIGNATURE_HEAD) signature: String,
        @RequestHeader(TIMESTAMP_HEAD) timestamp: String,
        @RequestBody payload: String,
    ): ResponseEntity<Any?> {
        // 寻找指定 `appId` 的 QGBot
        val targetBot = application.botManagers
            .filterIsQQGuildBotManagers()
            .firstNotNullOfOrNull {
                it.all().firstOrNull { bot ->
                    bot.source.ticket.appId == appId
                }
            }

        // 如果找不到，响应 404 异常
        if (targetBot == null) {
            throw ResponseStatusException(
                HttpStatus.NOT_FOUND,
                "app $appId not found"
            )
        }

        val result = targetBot.emitEvent(
            payload,
        ) {
            // 配置 ed25519SignatureVerification, 即代表进行签名校验
            ed25519SignatureVerification = Ed25519SignatureVerification(
                signature,
                timestamp
            )
        }

        val body: Any? = when (result) {
            is EmitResult.Verified -> result.verified
            else -> null
        }

        // 响应结果
        return ResponseEntity.ok(body)
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
/**
 * 处理所有qq机器人的回调请求的处理器。
 */
@RestController
@RequestMapping("/callback")
public class CallbackHandler {
    private static final String SIGNATURE_HEAD = "X-Signature-Ed25519";
    private static final String TIMESTAMP_HEAD = "X-Signature-Timestamp";

    private final Application application;

    public CallbackHandler(Application application) {
        this.application = application;
    }

    /**
     * 处理 `/callback/qq/{appId}` 的事件回调请求，
     * 找到对应的 bot 并向其推送事件。
     */
    @PostMapping("/qq/{appId}")
    public Mono<ResponseEntity<?>> handleEvent(
            @PathVariable("appId") String appId,
            @RequestHeader(SIGNATURE_HEAD) String signature,
            @RequestHeader(TIMESTAMP_HEAD) String timestamp,
            @RequestBody String payload
    ) {
        // 寻找指定 `appId` 的 QGBot
        final var targetBot = application.getBotManagers().stream()
                // 1. 寻找类型是 QQGuildBotManager 的 BotManager
                .filter(manager -> manager instanceof QQGuildBotManager)
                .map(QQGuildBotManager.class::cast)
                // 2. 寻找 appId 匹配的 bot
                .flatMap(manager ->
                        // 使用 manager.all() 可以直接访问 QGBot 类型，
                        // 而使用 manager.allStreamable() 得到的是 Bot 类型，需要再转化一次
                        // 二者都可以，这里选择第一个方案
                        Streamable.of(manager.all()).asStream())
                .filter(bot -> {
                    // 寻找 bot.appId 为函数入参 appId 的 bot
                    // bot.id 本质上也是使用的 appId, 因此直接使用 bot.getId().toString() 也是可以的。
                    var botAppId = bot.getSource().getTicket().getAppId();
                    return appId.equals(botAppId);
                })
                // 得到第一个符合条件的bot
                .findFirst()
                // 如果没找到，自行处理。这里选择抛出异常并响应404。
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "app " + appId + " not found"));

        // 在 servlet web 中，在异步中处理.
        // 作用域、是否要用异步等根据你的项目情况调整。

        // 如果要进行接口校验，配置 ed25519 校验所需要的内容
        final var options = new EmitEventOptions();
        options.setEd25519SignatureVerification(
                new Ed25519SignatureVerification(
                        signature,
                        timestamp
                )
        );

        targetBot.joinReserve().transform(SuspendReserves.mono())

        // 以响应式的方式推送事件
        final var mono = targetBot
                .emitEventReserve(payload, options)
                .transform(SuspendReserves.mono());

        // 得到处理结果，并返回body
        // 如果没有需要返回的body，也可以是null
        return mono.map(result -> {
            var body = switch (result) {
                case EmitResult.Verified verified -> verified.getVerified();
                default -> null;
            };

            // 将 Body 放到响应体中，返回。
            return ResponseEntity.ok(body);
        });
    }
}
```

</tab>
</tabs>

</tab>
<tab title="Ktor server">

```kotlin
private const val SIGNATURE_HEAD = "X-Signature-Ed25519"
private const val TIMESTAMP_HEAD = "X-Signature-Timestamp"

// 你也可以考虑直接把注册好的 bot 保存起来，而不只是保存 application
// 或者使用一些DI方案，都可以。
lateinit var simbotApplication: love.forte.simbot.application.Application

suspend fun main() {
    // 启动simbot application,
    // 然后启动内嵌的 HTTP 服务
    // 当然，具体的启动顺序或逻辑根据你的项目需求而定。
    simbotApplication = launchSimbot()

    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module)
        .start(wait = true)
}

/**
 * 启动 simbot application
 */
suspend fun launchSimbot(): love.forte.simbot.application.Application {
    val application = launchSimpleApplication {
        useQQGuild()
    }

    // 这里配置你的 bot、事件监听等...
    // 你也可以考虑直接把注册好的 bot 保存起来，而不只是保存 application

    return application
}

fun Application.module() {
    configureRouting()
}

fun Application.configureRouting() {
    routing {
        post("/callback/qq/{appId}") {
            val appId = call.parameters["appId"]

            // 寻找指定 `appId` 的 QGBot
            val targetBot = simbotApplication.botManagers
                .filterIsQQGuildBotManagers()
                .firstNotNullOfOrNull {
                    it.all().firstOrNull { bot ->
                        bot.source.ticket.appId == appId
                    }
                }

            // 如果找不到，响应 404 异常
            if (targetBot == null) {
                call.respond(HttpStatusCode.NotFound)
                return@post
            }

            // 准备参数
            val signature = call.request.header(SIGNATURE_HEAD)
                ?: run {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        "Required header $SIGNATURE_HEAD is missing"
                    )
                    return@post
                }

            val timestamp = call.request.header(TIMESTAMP_HEAD)
                ?: run {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        "Required header $TIMESTAMP_HEAD is missing"
                    )
                    return@post
                }

            val payload = call.receiveText()

            val result = targetBot.emitEvent(
                payload,
            ) {
                // 配置 ed25519SignatureVerification, 即代表进行签名校验
                ed25519SignatureVerification = Ed25519SignatureVerification(
                    signature,
                    timestamp
                )
            }

            val respond: String? = when (result) {
                is EmitResult.Verified ->
                    // 如果你安装了插件 ContentNegotiation,
                    // 那么也可以直接响应对象。
                    // 这里懒得装了，所以提前序列化成JSON字符串
                    Json.encodeToString(result.verified)

                else -> null
            }

            // 响应成功结果
            call.respondText(
                respond ?: "{}",
                ContentType.Application.Json
            )
        }
    }
}
```

</tab>
</tabs>

### Opcode=13 路径验证

在首次配置回调地址时，服务端会对此地址发送 `opcode=13` 的校验请求。

> 参考 [官方文档](https://bot.q.qq.com/wiki/develop/api-v2/dev-prepare/interface-framework/event-emit.html#webhook方式)

组件默认支持处理此事件，如果 `opcode=13`, `emitEvent` 则会返回 `EmitResult.Verified`，
其中的 `verified` 就是 `opcode=13` 时服务端所需要的结果。


```kotlin
val respond: Any? = when (result) {
    is EmitResult.Verified -> result.verified
    else -> null
}
```

直接将 `verified` 响应即可。

> 此类型默认基于 `kotlinx-serialization` 支持序列化，
> 如果你打算使用其他序列化方案，请注意字段的下划线转化。

<warning>

由于目前 Kotlin 多平台下对 Ed25519 可靠的库少之又少，
因此暂无法保证签名校验和路径验证中的加密可以在 **JVM以外** 的平台上运行良好。

如果你有好的方案或推荐，欢迎通过 [Issue](https://github.com/simple-robot/simbot-component-qq-guild/issues/new/choose)
向我们反馈！

</warning>

### 签名校验

在接收到事件推送时，可以通过请求头中的签名信息结合bot的 `secret` 校验本次请求。

> 参考 [官方文档](https://bot.q.qq.com/wiki/develop/api-v2/dev-prepare/interface-framework/sign.html)

组件默认支持进行请求头校验，在使用 `emitEvent` 时提供所需的校验信息即可。

<tabs>
<tab title="Java" group-key="Java">

```java
var options = new EmitEventOptions();
options.setEd25519SignatureVerification(
    new Ed25519SignatureVerification(
        // X-Signature-Ed25519
        signature, 
        // X-Signature-Timestamp
        timestamp
    );
);

bot.emitEventXxx(payload, options);
// emitEventBlocking(...);
// emitEventAsync(...);
// emitEventReserve(...);
```

</tab>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
bot.emitEvent(payload) {
    // 配置 ed25519SignatureVerification, 即代表进行签名校验
    ed25519SignatureVerification = Ed25519SignatureVerification(
        // X-Signature-Ed25519
        signature, 
        // X-Signature-Timestamp
        timestamp 
    )
}
```

</tab>
</tabs>

<warning>

由于目前 Kotlin 多平台下对 Ed25519 可靠的库少之又少，
因此暂无法保证签名校验和路径验证中的加密可以在 **JVM以外** 的平台上运行良好。

如果你有好的方案或推荐，欢迎通过 [Issue](https://github.com/simple-robot/simbot-component-qq-guild/issues/new/choose)
向我们反馈！

</warning>

## 示例

可以在仓库的 [samples](https://github.com/simple-robot/simbot-component-qq-guild/tree/dev/main/samples) 模块下找到示例模块。
