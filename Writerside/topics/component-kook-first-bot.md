# 第一个 KOOK 机器人

本页通过 WebSocket 连接 KOOK，在文字频道中接收“你好”并回复“你也好”。

## 准备

在 [KOOK 开发者中心](https://developer.kookapp.cn/) 创建机器人并取得其 Client ID 和 Bot Token，将机器人邀请到测试服务器，并确认它可以查看和发送文字频道消息。

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
    implementation("love.forte.simbot.component:simbot-component-kook-core:%kook-version%")
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
import love.forte.simbot.application.listeners
import love.forte.simbot.component.kook.firstKookBotManager
import love.forte.simbot.component.kook.useKook
import love.forte.simbot.component.kook.event.KookChannelMessageEvent
import love.forte.simbot.core.application.launchSimpleApplication
import love.forte.simbot.event.process

suspend fun main() {
    val clientId = System.getenv("KOOK_CLIENT_ID") ?: error("请设置 KOOK_CLIENT_ID")
    val token = System.getenv("KOOK_TOKEN") ?: error("请设置 KOOK_TOKEN")
    val app = launchSimpleApplication { useKook() }
    try {
        app.listeners {
            process<KookChannelMessageEvent> { event ->
                if (event.messageContent.plainText.trim() == "你好") {
                    println("收到频道消息：你好")
                    event.reply("你也好")
                }
            }
        }
        val bot = app.botManagers.firstKookBotManager().registerWs(clientId, token)
        bot.start()
        println("Bot 已启动，等待频道消息")
        app.join()
    } finally {
        app.cancel()
    }
}
```

监听器在 Bot 启动前注册，示例只处理普通成员的频道消息。

## 配置并运行

在运行程序的环境中设置 `KOOK_CLIENT_ID` 和 `KOOK_TOKEN`。例如在 macOS 或 Linux 终端中：

```shell
export KOOK_CLIENT_ID="你的 Client ID"
export KOOK_TOKEN="你的 Bot Token"
```

Windows PowerShell 可以使用 `$env:KOOK_CLIENT_ID = "你的 Client ID"` 和 `$env:KOOK_TOKEN = "你的 Bot Token"`。请勿将真实凭据提交到仓库。

在项目目录运行 `./gradlew run`，Windows 可使用 `gradlew.bat run`。没有 Gradle Wrapper 时，也可以使用已安装的 Gradle 执行 `gradle run`。

看到“Bot 已启动，等待频道消息”后，在机器人可访问的文字频道发送 `你好`。控制台应打印“收到频道消息：你好”，频道中应出现回复 `你也好`。

如果连接失败，检查 Client ID、Bot Token 与网络连接。如果没有收到回复，确认消息发送在文字频道中，机器人已加入服务器并具有查看、发送消息的权限。

更多配置方式与 Spring 集成见 [](component-kook-start-using.md)。
