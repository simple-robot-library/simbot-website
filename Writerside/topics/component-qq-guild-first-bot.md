# 第一个 QQ 机器人

本页使用 QQ 机器人组件和 Webhook 接收群聊 @ 消息。完成后，在机器人所在的 QQ 群中 @ 机器人，程序会在控制台打印消息，机器人会回复“你好，我已经收到消息了”。

## 准备

- 在 [QQ 开放平台](https://q.qq.com/) 创建机器人，取得 AppID 和 AppSecret，将测试账号加入沙箱并让机器人进入测试群。
- 在平台开通群聊消息相关能力，订阅 `GROUP_AT_MESSAGE_CREATE` 事件。平台入口与可用权限以机器人管理页面为准。
- 准备可从公网访问的 HTTPS 回调地址，并将该地址的 `/callback` 路径转发到本例运行环境的 8080 端口。根据平台要求配置服务器出口 IP 白名单。

本例使用 Webhook。回调地址需要能被平台访问，单独填写 `localhost` 无法接收来自平台的请求。

## 创建项目

本示例使用 Kotlin/JVM、Gradle、JDK 11 或更高版本和核心库 `simbot-core`。如果已经有项目，可以将依赖和配置合并到现有项目中。

在项目目录创建 `build.gradle.kts`：

```kotlin
plugins {
    kotlin("jvm") version "%kt-version%"
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("love.forte.simbot:simbot-core:%version%")
    implementation("love.forte.simbot.component:simbot-component-qq-core:%qg-version%")
    implementation("io.ktor:ktor-server-netty:%ktor-version%")
    runtimeOnly("io.ktor:ktor-client-cio:%ktor-version%")
    runtimeOnly("org.slf4j:slf4j-simple:%slf4j-version%")
}

application {
    mainClass = "MainKt"
}
```

`ktor-client-cio` 提供 JVM HTTP 客户端引擎，`slf4j-simple` 用于输出日志。`MainKt` 对应下方无包名的 `Main.kt`。

创建 `src/main/kotlin/Main.kt`：

```kotlin
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.request.header
import io.ktor.server.request.receiveText
import io.ktor.server.response.respond
import io.ktor.server.response.respondText
import io.ktor.server.routing.post
import io.ktor.server.routing.routing
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import love.forte.simbot.application.listeners
import love.forte.simbot.common.function.ConfigurerFunction
import love.forte.simbot.component.qguild.bot.emitEvent
import love.forte.simbot.component.qguild.event.QGGroupAtMessageCreateEvent
import love.forte.simbot.component.qguild.firstQQGuildBotManager
import love.forte.simbot.component.qguild.useQQGuild
import love.forte.simbot.core.application.launchSimpleApplication
import love.forte.simbot.event.process
import love.forte.simbot.qguild.event.EventIntents
import love.forte.simbot.qguild.stdlib.Ed25519SignatureVerification
import love.forte.simbot.qguild.stdlib.EmitResult

suspend fun main() {
    val appId = System.getenv("QQ_APP_ID") ?: error("请设置 QQ_APP_ID")
    val secret = System.getenv("QQ_APP_SECRET") ?: error("请设置 QQ_APP_SECRET")
    val token = System.getenv("QQ_TOKEN") ?: ""
    val app = launchSimpleApplication { useQQGuild() }
    try {
        app.listeners {
            process<QGGroupAtMessageCreateEvent> { event ->
                println("收到群 @ 消息：${event.messageContent.plainText}")
                event.reply("你好，我已经收到消息了")
            }
        }
        val bot = app.botManagers.firstQQGuildBotManager().register(appId, secret, token) {
            botConfigure = ConfigurerFunction {
                disableWs = true
                intents += EventIntents.GroupAndC2CEvent.intents
            }
        }
        bot.start()
        println("HTTP 服务即将监听 8080 端口")
        embeddedServer(Netty, host = "0.0.0.0", port = 8080) {
            routing {
                post("/callback") {
                    val signature = call.request.header("X-Signature-Ed25519")
                    val timestamp = call.request.header("X-Signature-Timestamp")
                    if (signature == null || timestamp == null) {
                        call.respond(HttpStatusCode.BadRequest)
                        return@post
                    }
                    val result = bot.emitEvent(call.receiveText()) {
                        ed25519SignatureVerification = Ed25519SignatureVerification(signature, timestamp)
                    }
                    val response = when (result) {
                        is EmitResult.Verified -> Json.encodeToString(result.verified)
                        else -> "{}"
                    }
                    call.respondText(response, ContentType.Application.Json)
                }
            }
        }.start(wait = true)
    } finally {
        app.cancel()
    }
}
```

示例在注册监听器后启动 Bot，再启动 Ktor HTTP 服务。收到回调时，`emitEvent` 使用请求头校验签名，并处理平台的回调地址验证请求。

## 配置并运行

在运行程序的环境中设置 `QQ_APP_ID` 和 `QQ_APP_SECRET`。例如在 macOS 或 Linux 终端中：

```shell
export QQ_APP_ID="你的 AppID"
export QQ_APP_SECRET="你的 AppSecret"
```

Windows PowerShell 可以使用 `$env:QQ_APP_ID = "你的 AppID"` 和 `$env:QQ_APP_SECRET = "你的 AppSecret"`。请勿将真实凭据提交到仓库。

在项目目录运行 `./gradlew run`，Windows 可使用 `gradlew.bat run`。没有 Gradle Wrapper 时，也可以使用已安装的 Gradle 执行 `gradle run`。按 `Ctrl+C` 停止程序。

程序启动后，在平台配置完整的 HTTPS 回调地址，例如 `https://example.com/callback`，并完成地址验证。然后在测试群中 @ 机器人并发送一条消息。控制台应出现“收到群 @ 消息”，群内应收到机器人的回复。

若回调地址验证失败，检查公网 HTTPS 转发、路径、AppSecret 和请求头是否完整。若没有收到消息，检查事件订阅、沙箱成员及群聊权限。收到事件但回复失败时，检查平台回复权限和出口 IP 白名单。

组件当前的 `register` 接口保留 `token` 参数，示例在未设置 `QQ_TOKEN` 时传入空字符串。需要旧版 Token 的环境可通过 `QQ_TOKEN` 提供。Webhook 配置与事件处理的更多说明见 [](component-qq-guild-Webhook.md)，组件的其他配置方式见 [](component-qq-guild-start-using.md)。
