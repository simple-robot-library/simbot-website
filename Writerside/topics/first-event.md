---
switcher-label: JavaAPI风格
---

# 第一次处理事件

本页通过一个本地测试事件，体验 simbot 的事件处理流程。完成后，程序会在控制台打印“收到测试事件”并退出。
这个例子无需平台账号。接入真实 Bot 时，再选择对应的组件并配置账号。

## 准备项目

准备一个使用 Gradle 的项目，JDK 版本为 11 或更高。本例使用 simbot `%version%`，Kotlin 示例使用 Kotlin `%kt-version%`。请选择需要使用的语言。

在 `build.gradle.kts` 中配置插件、仓库和依赖：

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
    // 本例借助测试模块构造事件
    implementation("love.forte.simbot:simbot-test:%version%")
}

application {
    mainClass = "MainKt"
}
```

`MainKt` 对应下面示例的文件名和无包名的顶层 `main` 函数。

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
    implementation("love.forte.simbot:simbot-test-jvm:%version%")
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
    implementation("love.forte.simbot:simbot-test-jvm:%version%")
    implementation("io.projectreactor:reactor-core:%reactor-version%")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor:%coroutines-version%")
}
```
{diff-lines="+4-5"}

</if>

</tab>
</tabs>

如果你已经有项目，可以将依赖和 `application` 配置合并到现有构建脚本中。

## 编写并运行

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

创建 `src/main/kotlin/Main.kt`：

```kotlin
import kotlinx.coroutines.flow.collect
import love.forte.simbot.application.listeners
import love.forte.simbot.core.application.launchSimpleApplication
import love.forte.simbot.event.process
import love.forte.simbot.test.event.TestEvent

suspend fun main() {
    val app = launchSimpleApplication()
    try {
        // 注册一个处理 TestEvent 的监听器
        app.listeners {
            process<TestEvent> {
                println("收到测试事件")
            }
        }

        // 推送测试事件并收集处理结果
        app.eventDispatcher.push(TestEvent()).collect()
    } finally {
        app.cancel()
    }
}
```

</tab>
<tab title="Java" group-key="Java">

创建 `src/main/java/Main.java`：

```java
import love.forte.simbot.application.Applications;
import love.forte.simbot.core.application.Simple;
import love.forte.simbot.event.EventListeners;
import love.forte.simbot.event.EventProcessors;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.test.event.TestEvent;

public class Main {
    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE);
        try {
            app.getEventDispatcher().register(EventListeners.block(TestEvent.class, (context, event) -> {
                System.out.println("收到测试事件");
                return EventResult.empty();
            }));
            EventProcessors.pushAndCollectToListBlocking(app.getEventDispatcher(), new TestEvent());
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
import love.forte.simbot.event.EventProcessors;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.test.event.TestEvent;
import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE);
        try {
            app.getEventDispatcher().register(EventListeners.async(TestEvent.class, (context, event) -> {
                System.out.println("收到测试事件");
                return CompletableFuture.completedFuture(EventResult.empty());
            }));
            EventProcessors.pushAndCollectToListAsync(app.getEventDispatcher(), new TestEvent(), app).join();
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
import love.forte.simbot.event.EventProcessors;
import love.forte.simbot.event.EventResult;
import love.forte.simbot.test.event.TestEvent;

public class Main {
    public static void main(String[] args) {
        var app = Applications.launchApplicationBlocking(Simple.INSTANCE);
        try {
            app.getEventDispatcher().register(EventListeners.nonBlock(TestEvent.class, (context, event) -> {
                System.out.println("收到测试事件");
                return EventResult.empty();
            }));
            EventProcessors.pushAndAsFlux(app.getEventDispatcher(), new TestEvent()).blockLast();
        } finally {
            app.cancel();
        }
    }
}
```
{switcher-key="%jr%"}

</tab>
</tabs>

在项目目录运行 `./gradlew run`，Windows 可使用 `gradlew.bat run`。如果项目没有 Gradle Wrapper，也可以使用已安装的 Gradle 执行 `gradle run`。

输出中应包含：

```text
收到测试事件
```

如果还看到 SLF4J 没有日志实现的提示，示例仍可运行。项目需要输出日志时，可以按所用环境配置日志实现。

`Application` 持有事件调度器，监听器负责处理匹配的事件。Kotlin 的 `push` 返回 `Flow`，在收集时执行。Java 示例分别展示阻塞、异步和响应式方式。两种示例结束时都调用 `cancel()` 关闭应用。
这里的 `TestEvent` 来自测试模块，实际接入平台时，事件由组件接收并推送。

## 下一步

- 前往 [](start-use-components.md) 选择并接入真实的平台 Bot，选择所需组件平台并跟随对应的快速开始完成依赖、账号和监听配置。
- 在 Spring Boot 中开发？前往 [](start-use-spring-boot-3.md)。
- 使用 Java？前往 [](java-friendly.md) 了解异步与响应式 API，再选择组件。
- 想了解事件处理结果与异常？前往 [](basic-event-listener.md)。
