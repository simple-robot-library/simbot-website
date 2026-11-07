# 使用 Spring Boot

<tldr>
在 Spring Boot 3 项目中启用 simbot，添加组件并监听事件。
</tldr>

本页适合已有 Spring Boot 项目的读者，示例使用 Java 17 或更高版本。
如果使用 Spring Boot 2，请参考 [](start-use-spring-boot-2.md)。

## 安装

准备一个 Spring Boot 3 项目，并添加 simbot starter：

<include from="refers.md" element-id="simbot-spring-3-build"></include>

完整的项目准备和依赖说明见 [](Spring-Boot.md#install-spring)。

## 使用

### 启用 simbot

在 Spring Boot 启动类上添加 `@EnableSimbot`：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```kotlin
import love.forte.simbot.spring.EnableSimbot
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@EnableSimbot
@SpringBootApplication(proxyBeanMethods = false)
class MyApplication

fun main(args: Array<String>) {
    runApplication<MyApplication>(*args)
}
```

</tab>
<tab title="Java" group-key="Java">

```java
import love.forte.simbot.spring.EnableSimbot;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@EnableSimbot
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

</tab>
</tabs>

### 编写事件处理器

在 Spring 扫描范围内创建组件，并使用 `@Listener` 标记处理函数：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```kotlin
import love.forte.simbot.event.Event
import love.forte.simbot.quantcat.common.annotations.Listener
import org.springframework.stereotype.Component

@Component
class MyEventHandlers {
    @Listener
    suspend fun onEvent(event: Event) {
        println("收到事件: $event")
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```java
import love.forte.simbot.event.Event;
import love.forte.simbot.quantcat.common.annotations.Listener;
import org.springframework.stereotype.Component;

@Component
public class MyEventHandlers {
    @Listener
    public void onEvent(Event event) {
        System.out.println("收到事件: " + event);
    }
}
```

</tab>
</tabs>

`Event` 可监听多种事件。需要处理消息时，可以换成具体的消息事件类型，参见 [](basic-event-listener.md)。

## 安装组件以及组件配置

选择 [](start-use-components.md) 中的平台组件，按照它的手册添加依赖和 Ktor 客户端引擎。
组件提供平台相关的 Bot 和事件，具体的凭据与权限由目标平台决定。

## 注册Bot

多数官方组件支持通过配置文件自动注册 Bot。将对应平台的配置放入资源目录下的 `simbot-bots/`，
文件名以 `.bot.json` 结尾。配置内容请参考所选组件的快速开始：

- [开始使用 QQ 组件](component-qq-guild-start-using.md)
- [开始使用 KOOK 组件](component-kook-start-using.md)
- [开始使用 OneBot 11 组件](component-onebot-v11-start-using.md)

默认情况下，starter 会扫描配置文件并启动注册的 Bot。扫描路径、自动启动等选项见 [](Spring-Boot.md#注册bot)。

## 运行或打包

启动 Spring Boot 应用，并在目标平台触发一个已订阅的事件。监听器输出“收到事件”表示事件已进入应用。
如果没有输出，请检查 Bot 是否启动、平台权限和事件订阅配置，再参考 [](FAQ.md)。

应用启动后的其他配置方式、主动获取 Bot 和打包说明见 [](Spring-Boot.md)。
