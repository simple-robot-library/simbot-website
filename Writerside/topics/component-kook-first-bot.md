---
switcher-label: JavaAPI风格
---

# 第一个 KOOK 机器人

本页通过 WebSocket 连接 KOOK，在文字频道中接收“你好”并回复“你也好”。

## 准备

在 [KOOK 开发者中心](https://developer.kookapp.cn/) 创建机器人并取得其 Client ID 和 Bot Token，将机器人邀请到测试服务器，并确认它可以查看和发送文字频道消息。

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
    implementation("love.forte.simbot.component:simbot-component-kook-core:%kook-version%")
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
    implementation("love.forte.simbot.component:simbot-component-kook-core-jvm:%kook-version%")
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
    implementation("love.forte.simbot.component:simbot-component-kook-core-jvm:%kook-version%")
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

</tab>
<tab title="Java" group-key="Java">

创建 `src/main/java/Main.java`。在页面顶部选择 Java API 风格。示例统一以阻塞方式创建应用，使用所选风格启动 Bot、处理事件并等待应用结束：

```java
import love.forte.simbot.application.Applications;
import love.forte.simbot.core.application.Simple;
import love.forte.simbot.event.EventListeners;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.component.kook.KookComponent;
import love.forte.simbot.component.kook.KookBotManagersKt;
import love.forte.simbot.component.kook.bot.KookBotManager;
import love.forte.simbot.component.kook.event.KookChannelMessageEvent;
import kotlin.Unit;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(KookComponent.Factory);
            config.install(KookBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.block(KookChannelMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return EventResult.empty();
                }
                System.out.println("收到频道消息：你好");
                event.replyBlocking("你也好");
                return EventResult.empty();
            }));
            var bot = KookBotManagersKt.firstKookBotManager(app.getBotManagers())
                .registerWs(required("KOOK_CLIENT_ID"), required("KOOK_TOKEN"), config -> Unit.INSTANCE);
            bot.startBlocking();
            System.out.println("Bot 已启动，等待频道消息");
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
import love.forte.simbot.component.kook.KookComponent;
import love.forte.simbot.component.kook.KookBotManagersKt;
import love.forte.simbot.component.kook.bot.KookBotManager;
import love.forte.simbot.component.kook.event.KookChannelMessageEvent;
import kotlin.Unit;
import java.util.concurrent.CompletableFuture;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(KookComponent.Factory);
            config.install(KookBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.async(KookChannelMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return CompletableFuture.completedFuture(EventResult.empty());
                }
                System.out.println("收到频道消息：你好");
                return event.replyAsync("你也好").thenApply(ignored -> EventResult.empty());
            }));
            var bot = KookBotManagersKt.firstKookBotManager(app.getBotManagers())
                .registerWs(required("KOOK_CLIENT_ID"), required("KOOK_TOKEN"), config -> Unit.INSTANCE);
            bot.startAsync()
                .thenRun(() -> System.out.println("Bot 已启动，等待频道消息"))
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
import love.forte.simbot.component.kook.KookComponent;
import love.forte.simbot.component.kook.KookBotManagersKt;
import love.forte.simbot.component.kook.bot.KookBotManager;
import love.forte.simbot.component.kook.event.KookChannelMessageEvent;
import kotlin.Unit;
import reactor.core.publisher.Mono;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(KookComponent.Factory);
            config.install(KookBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.nonBlock(KookChannelMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return EventResult.empty();
                }
                System.out.println("收到频道消息：你好");
                return EventResult.of(Mono.from(event.replyReactive("你也好")));
            }));
            var bot = KookBotManagersKt.firstKookBotManager(app.getBotManagers())
                .registerWs(required("KOOK_CLIENT_ID"), required("KOOK_TOKEN"), config -> Unit.INSTANCE);
            Mono.from(bot.startReactive())
                .doOnSuccess(ignored -> System.out.println("Bot 已启动，等待频道消息"))
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
