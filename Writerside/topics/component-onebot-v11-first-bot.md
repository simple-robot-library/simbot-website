---
switcher-label: JavaAPI风格
---

# 第一个 OneBot 11 机器人

本页连接一个已有的 OneBot 11 协议实现，在群聊中接收“你好”并回复“你也好”。

## 准备

先运行一个支持 OneBot 11 的协议服务端实现，让 Bot 登录并加入测试群。
确认该实现提供正向 HTTP API 和正向 WebSocket 事件地址，并了解它的鉴权配置。

simbot 的 OneBot 组件连接协议服务端实现，由协议实现负责连接目标平台。不同实现的地址、端口和配置方法可能不同，请以所用实现的文档为准。

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
    implementation("love.forte.simbot.component:simbot-component-onebot-v11-core:%ob-version%")
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
    implementation("love.forte.simbot.component:simbot-component-onebot-v11-core-jvm:%ob-version%")
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
    implementation("love.forte.simbot.component:simbot-component-onebot-v11-core-jvm:%ob-version%")
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
import io.ktor.http.Url
import love.forte.simbot.application.listeners
import love.forte.simbot.component.onebot.v11.core.useOneBot11
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotConfiguration
import love.forte.simbot.component.onebot.v11.core.bot.firstOneBotBotManager
import love.forte.simbot.core.application.launchSimpleApplication
import love.forte.simbot.event.ChatGroupMessageEvent
import love.forte.simbot.event.process

suspend fun main() {
    val app = launchSimpleApplication { useOneBot11() }
    try {
        app.listeners {
            process<ChatGroupMessageEvent> { event ->
                if (event.messageContent.plainText?.trim() == "你好") {
                    println("收到群消息：你好")
                    event.reply("你也好")
                }
            }
        }
        val config = OneBotBotConfiguration().apply {
            botUniqueId = System.getenv("ONEBOT_BOT_ID") ?: error("请设置 ONEBOT_BOT_ID")
            apiServerHost = Url(System.getenv("ONEBOT_HTTP_URL") ?: error("请设置 ONEBOT_HTTP_URL"))
            eventServerHost = Url(System.getenv("ONEBOT_WS_URL") ?: error("请设置 ONEBOT_WS_URL"))
            accessToken(System.getenv("ONEBOT_ACCESS_TOKEN"))
        }
        val bot = app.botManagers.firstOneBotBotManager().register(config)
        bot.start()
        println("Bot 已启动，等待群消息")
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
import love.forte.simbot.component.onebot.v11.core.component.OneBot11Component;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManagerUsageKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManager;
import love.forte.simbot.event.ChatGroupMessageEvent;
import io.ktor.http.URLUtilsKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotConfiguration;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(OneBot11Component.Factory);
            config.install(OneBotBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.block(ChatGroupMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return EventResult.empty();
                }
                System.out.println("收到群消息：你好");
                event.replyBlocking("你也好");
                return EventResult.empty();
            }));
            var config = new OneBotBotConfiguration();
            config.setBotUniqueId(required("ONEBOT_BOT_ID"));
            config.setApiServerHost(URLUtilsKt.Url(required("ONEBOT_HTTP_URL")));
            config.setEventServerHost(URLUtilsKt.Url(required("ONEBOT_WS_URL")));
            config.accessToken(System.getenv("ONEBOT_ACCESS_TOKEN"));
            var bot = OneBotBotManagerUsageKt.firstOneBotBotManager(app.getBotManagers()).register(config);
            bot.startBlocking();
            System.out.println("Bot 已启动，等待群消息");
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
import love.forte.simbot.component.onebot.v11.core.component.OneBot11Component;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManagerUsageKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManager;
import love.forte.simbot.event.ChatGroupMessageEvent;
import io.ktor.http.URLUtilsKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotConfiguration;
import java.util.concurrent.CompletableFuture;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(OneBot11Component.Factory);
            config.install(OneBotBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.async(ChatGroupMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return CompletableFuture.completedFuture(EventResult.empty());
                }
                System.out.println("收到群消息：你好");
                return event.replyAsync("你也好").thenApply(ignored -> EventResult.empty());
            }));
            var config = new OneBotBotConfiguration();
            config.setBotUniqueId(required("ONEBOT_BOT_ID"));
            config.setApiServerHost(URLUtilsKt.Url(required("ONEBOT_HTTP_URL")));
            config.setEventServerHost(URLUtilsKt.Url(required("ONEBOT_WS_URL")));
            config.accessToken(System.getenv("ONEBOT_ACCESS_TOKEN"));
            var bot = OneBotBotManagerUsageKt.firstOneBotBotManager(app.getBotManagers()).register(config);
            bot.startAsync()
                .thenRun(() -> System.out.println("Bot 已启动，等待群消息"))
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
import love.forte.simbot.component.onebot.v11.core.component.OneBot11Component;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManagerUsageKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotManager;
import love.forte.simbot.event.ChatGroupMessageEvent;
import io.ktor.http.URLUtilsKt;
import love.forte.simbot.component.onebot.v11.core.bot.OneBotBotConfiguration;
import reactor.core.publisher.Mono;

public class Main {
    private static String required(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalArgumentException("请设置 " + name);
        return value;
    }

    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE, config -> {
            config.install(OneBot11Component.Factory);
            config.install(OneBotBotManager.Factory);
        });
        try {
            app.getEventDispatcher().register(EventListeners.nonBlock(ChatGroupMessageEvent.class, (context, event) -> {
                var text = event.getMessageContent().getPlainText();
                if (text == null || !text.trim().equals("你好")) {
                    return EventResult.empty();
                }
                System.out.println("收到群消息：你好");
                return EventResult.of(Mono.from(event.replyReactive("你也好")));
            }));
            var config = new OneBotBotConfiguration();
            config.setBotUniqueId(required("ONEBOT_BOT_ID"));
            config.setApiServerHost(URLUtilsKt.Url(required("ONEBOT_HTTP_URL")));
            config.setEventServerHost(URLUtilsKt.Url(required("ONEBOT_WS_URL")));
            config.accessToken(System.getenv("ONEBOT_ACCESS_TOKEN"));
            var bot = OneBotBotManagerUsageKt.firstOneBotBotManager(app.getBotManagers()).register(config);
            Mono.from(bot.startReactive())
                .doOnSuccess(ignored -> System.out.println("Bot 已启动，等待群消息"))
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

监听器在 Bot 启动前注册。`botUniqueId` 用于在组件中区分 Bot，可以使用协议实现对应的账号 ID。

## 配置并运行

设置 `ONEBOT_BOT_ID`、`ONEBOT_HTTP_URL` 和 `ONEBOT_WS_URL`。如果 HTTP 和 WebSocket 使用同一个 Access Token，再设置 `ONEBOT_ACCESS_TOKEN`。下面的地址仅为示例，使用请替换为协议实现提供的地址：

```shell
export ONEBOT_BOT_ID="你的 Bot ID"
export ONEBOT_HTTP_URL="http://127.0.0.1:3001"
export ONEBOT_WS_URL="ws://127.0.0.1:3001"
# 需要鉴权时设置
export ONEBOT_ACCESS_TOKEN="你的 Access Token"
```

Windows PowerShell 可用 `$env:ONEBOT_BOT_ID = "你的 Bot ID"` 等方式设置环境变量。请勿将真实凭据提交到仓库。如果 HTTP 和 WebSocket 使用不同的 Token，可以分别配置 `apiAccessToken` 和 `eventAccessToken`。

在项目目录运行 `./gradlew run`，Windows 可使用 `gradlew.bat run`。没有 Gradle Wrapper 时，也可以使用已安装的 Gradle 执行 `gradle run`。

看到“Bot 已启动，等待群消息”后，在测试群发送 `你好`。控制台应打印“收到群消息：你好”，群内应出现回复 `你也好`。

连接失败时，检查协议实现是否运行、地址和路径是否正确，以及鉴权配置是否一致。没有收到回复时，检查 Bot 是否在测试群中、协议实现是否推送群消息事件，以及 HTTP API 是否可用。

更多配置方式与 Spring 集成见 [](component-onebot-v11-start-using.md)。
