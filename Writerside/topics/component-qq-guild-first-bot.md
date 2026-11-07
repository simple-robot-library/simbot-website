---
switcher-label: JavaAPI风格
---

# 第一个 QQ 机器人

本页使用 QQ 机器人组件和 WebSocket 接收群聊 @ 消息。完成后，在机器人所在的 QQ 群中 @ 机器人，程序会在控制台打印消息，机器人会回复“你好，我已经收到消息了”。

## 准备

- 在 [QQ 开放平台](https://q.qq.com/) 创建机器人，取得 AppID 和 AppSecret，将测试账号加入沙箱并让机器人进入测试群。
- 在平台开通群聊消息相关能力，订阅 `GROUP_AT_MESSAGE_CREATE` 事件。平台入口与可用权限以机器人管理页面为准。
- 根据平台要求配置程序运行环境的出口 IP 白名单（如有需要），并确认网络可以访问 QQ 开放平台。

本例由程序主动建立 WebSocket 连接。Webhook 接入方式见 [](component-qq-guild-Webhook.md)。

## 创建项目

本示例使用 Kotlin 或 Java、Gradle、JDK 11 或更高版本和核心库 `simbot-core`。如果已经有项目，可以将依赖和配置合并到现有项目中。

在项目目录创建 `build.gradle.kts`：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

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
    runtimeOnly("io.ktor:ktor-client-cio:%ktor-version%")
    runtimeOnly("org.slf4j:slf4j-simple:%slf4j-version%")
}

application {
    mainClass = "MainKt"
}
```

`MainKt` 对应下方无包名的顶层 `main` 函数。

</tab>
<tab title="Java" group-key="Java">

```kotlin
plugins {
    java
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("love.forte.simbot:simbot-core-jvm:%version%")
    implementation("love.forte.simbot.component:simbot-component-qq-core-jvm:%qg-version%")
    runtimeOnly("io.ktor:ktor-client-cio:%ktor-version%")
    runtimeOnly("org.slf4j:slf4j-simple:%slf4j-version%")
}

application {
    mainClass = "Main"
}
```

<if switcher-key="%jr%">

响应式示例使用 Reactor，在上面的 `dependencies` 中添加标记的依赖：

```kotlin
dependencies {
    implementation("love.forte.simbot:simbot-core-jvm:%version%")
    implementation("love.forte.simbot.component:simbot-component-qq-core-jvm:%qg-version%")
    implementation("io.projectreactor:reactor-core:%reactor-version%")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor:%coroutines-version%")
    runtimeOnly("io.ktor:ktor-client-cio:%ktor-version%")
    runtimeOnly("org.slf4j:slf4j-simple:%slf4j-version%")
}
```
{diff-lines="+4-5"}

</if>

</tab>
</tabs>

`ktor-client-cio` 提供 JVM HTTP 和 WebSocket 客户端引擎，`slf4j-simple` 用于输出日志。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

创建 `src/main/kotlin/Main.kt`：

```kotlin
import love.forte.simbot.application.listeners
import love.forte.simbot.common.function.ConfigurerFunction
import love.forte.simbot.component.qguild.event.QGGroupAtMessageCreateEvent
import love.forte.simbot.component.qguild.firstQQGuildBotManager
import love.forte.simbot.component.qguild.useQQGuild
import love.forte.simbot.core.application.launchSimpleApplication
import love.forte.simbot.event.process
import love.forte.simbot.qguild.event.EventIntents

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
                intents += EventIntents.GroupAndC2CEvent.intents
            }
        }
        bot.start()
        println("Bot 已启动，等待群 @ 消息")
        app.join()
    } finally {
        app.cancel()
    }
}
```

</tab>
<tab title="Java" group-key="Java">

创建 `src/main/java/Main.java`。在页面顶部选择 Java API 风格。示例统一以阻塞方式创建应用，使用所选风格启动 Bot、处理事件并等待应用结束：

```java
import love.forte.simbot.application.Applications;
import love.forte.simbot.core.application.Simple;
import love.forte.simbot.event.EventListeners;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.component.qguild.QQGuildComponent;
import love.forte.simbot.component.qguild.QQGuildBotManagerUsageKt;
import love.forte.simbot.component.qguild.bot.QQGuildBotManager;
import love.forte.simbot.component.qguild.event.QGGroupAtMessageCreateEvent;
import love.forte.simbot.qguild.event.EventIntents;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(QQGuildComponent.Factory);
            config.install(QQGuildBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.block(QGGroupAtMessageCreateEvent.class, (context, event) -> {
                System.out.println("收到群 @ 消息：" + event.getMessageContent().getPlainText());
                event.replyBlocking("你好，我已经收到消息了");
                return EventResult.empty();
            }));
            var bot = QQGuildBotManagerUsageKt.firstQQGuildBotManager(app.getBotManagers())
                .register(required("QQ_APP_ID"), required("QQ_APP_SECRET"),
                    System.getenv().getOrDefault("QQ_TOKEN", ""), config -> config.botConfig(botConfig ->
                        botConfig.setIntentsValue(botConfig.getIntentsValue()
                            | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue())));
            bot.startBlocking();
            System.out.println("Bot 已启动，等待群 @ 消息");
            app.joinBlocking();
        } finally {
            app.cancel();
        }
    }
}
```
{switcher-key="%jb%"}

```java
import love.forte.simbot.application.Applications;
import love.forte.simbot.core.application.Simple;
import love.forte.simbot.event.EventListeners;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.component.qguild.QQGuildComponent;
import love.forte.simbot.component.qguild.QQGuildBotManagerUsageKt;
import love.forte.simbot.component.qguild.bot.QQGuildBotManager;
import love.forte.simbot.component.qguild.event.QGGroupAtMessageCreateEvent;
import love.forte.simbot.qguild.event.EventIntents;
import java.util.concurrent.CompletableFuture;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(QQGuildComponent.Factory);
            config.install(QQGuildBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.async(QGGroupAtMessageCreateEvent.class, (context, event) -> {
                System.out.println("收到群 @ 消息：" + event.getMessageContent().getPlainText());
                return event.replyAsync("你好，我已经收到消息了").thenApply(ignored -> EventResult.empty());
            }));
            var bot = QQGuildBotManagerUsageKt.firstQQGuildBotManager(app.getBotManagers())
                .register(required("QQ_APP_ID"), required("QQ_APP_SECRET"),
                    System.getenv().getOrDefault("QQ_TOKEN", ""), config -> config.botConfig(botConfig ->
                        botConfig.setIntentsValue(botConfig.getIntentsValue()
                            | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue())));
            bot.startAsync()
                .thenRun(() -> System.out.println("Bot 已启动，等待群 @ 消息"))
                .thenCompose(ignored -> app.asFuture())
                .join();
        } finally {
            app.cancel();
        }
    }
}
```
{switcher-key="%ja%"}

```java
import love.forte.simbot.application.Applications;
import love.forte.simbot.core.application.Simple;
import love.forte.simbot.event.EventListeners;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.component.qguild.QQGuildComponent;
import love.forte.simbot.component.qguild.QQGuildBotManagerUsageKt;
import love.forte.simbot.component.qguild.bot.QQGuildBotManager;
import love.forte.simbot.component.qguild.event.QGGroupAtMessageCreateEvent;
import love.forte.simbot.qguild.event.EventIntents;
import reactor.core.publisher.Mono;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(QQGuildComponent.Factory);
            config.install(QQGuildBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.nonBlock(QGGroupAtMessageCreateEvent.class, (context, event) -> {
                System.out.println("收到群 @ 消息：" + event.getMessageContent().getPlainText());
                return EventResult.of(Mono.from(event.replyReactive("你好，我已经收到消息了")));
            }));
            var bot = QQGuildBotManagerUsageKt.firstQQGuildBotManager(app.getBotManagers())
                .register(required("QQ_APP_ID"), required("QQ_APP_SECRET"),
                    System.getenv().getOrDefault("QQ_TOKEN", ""), config -> config.botConfig(botConfig ->
                        botConfig.setIntentsValue(botConfig.getIntentsValue()
                            | EventIntents.GroupAndC2CEvent.INSTANCE.getIntentsValue())));
            Mono.from(bot.startReactive())
                .doOnSuccess(ignored -> System.out.println("Bot 已启动，等待群 @ 消息"))
                .then(Mono.from(app.joinReactive()))
                .block();
        } finally {
            app.cancel();
        }
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>

示例在 Bot 启动前注册监听器，并为 WebSocket 增加群聊和单聊事件的订阅。

## 配置并运行

在运行程序的环境中设置 `QQ_APP_ID` 和 `QQ_APP_SECRET`。例如在 macOS 或 Linux 终端中：

```shell
export QQ_APP_ID="你的 AppID"
export QQ_APP_SECRET="你的 AppSecret"
```

Windows PowerShell 可以使用 `$env:QQ_APP_ID = "你的 AppID"` 和 `$env:QQ_APP_SECRET = "你的 AppSecret"`。请勿将真实凭据提交到仓库。

在项目目录运行 `./gradlew run`，Windows 可使用 `gradlew.bat run`。没有 Gradle Wrapper 时，也可以使用已安装的 Gradle 执行 `gradle run`。按 `Ctrl+C` 停止程序。

看到“Bot 已启动，等待群 @ 消息”后，在测试群中 @ 机器人并发送一条消息。控制台应出现“收到群 @ 消息”，群内应收到机器人的回复。

若连接失败，检查 AppID、AppSecret、网络和出口 IP 白名单。若没有收到消息，检查事件订阅、沙箱成员及群聊权限。收到事件但回复失败时，检查平台回复权限。

组件当前的 `register` 接口保留 `token` 参数，示例在未设置 `QQ_TOKEN` 时传入空字符串。需要旧版 Token 的环境可通过 `QQ_TOKEN` 提供。Webhook 配置与事件处理的更多说明见 [](component-qq-guild-Webhook.md)，组件的其他配置方式见 [](component-qq-guild-start-using.md)。
