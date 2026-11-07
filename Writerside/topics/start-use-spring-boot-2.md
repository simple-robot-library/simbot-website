---
switcher-label: JavaAPI风格
---

# 使用 Spring Boot 2

<tldr>

在 JVM 平台下使用 Spring Boot 2 配合 simbot 进行
<control>兼容集成</control> 。

</tldr>

<warning title="兼容入口">

如果没有明确的历史包袱，仍建议优先使用 <a href="start-use-spring-boot-3.md">Spring Boot 3</a>。
本页对应的是 <code>simbot-core-spring-boot-starter-v2</code>，
主要用于兼容仍停留在 Spring Boot 2.x / Java 11 的项目。

</warning>

<note title="更多信息">
有关集成 Spring Boot 的详细内容可前往
<a href="Spring-Boot.md">Spring Boot</a>
进行参考。
</note>

## 安装

准备一个 Spring Boot 2 项目，JDK 版本为 11 或更高，然后添加兼容 starter：

<include from="refers.md" element-id="simbot-spring-2-build"></include>

接入平台时还需要添加组件及其所需的网络引擎，参见 [](start-use-components.md)。

## 与 Spring Boot 3 的主要差异

- 依赖坐标为 `love.forte.simbot:simbot-core-spring-boot-starter-v2`
- `@EnableSimbot` 位于 `love.forte.simbot.spring2`
- 相关配置、处理器与应用实现主要位于 `love.forte.simbot.spring2.*`
- Java 最低要求 11 不是 17（与 simbot 本体的要求一致）

## 使用

### 启用 simbot

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
import love.forte.simbot.spring2.EnableSimbot

@EnableSimbot
@SpringBootApplication
class MyApplication

fun main(args: Array<String>) {
    runApplication<MyApplication>(*args)
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
import love.forte.simbot.spring2.EnableSimbot;

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

前往
<a href="Spring-Boot.md#编写事件处理器">编写事件处理器</a>
了解更多。

### 安装组件以及组件配置

前往
<a href="Spring-Boot.md#安装组件以及组件配置">安装组件以及组件配置</a>
了解更多。

### 注册Bot

前往
<a href="Spring-Boot.md#注册bot">注册 Bot</a>
了解更多。

### 运行或打包

前往
<a href="Spring-Boot.md#运行或打包">运行或打包</a>
了解更多。

[spring.start]: https://start.spring.io
