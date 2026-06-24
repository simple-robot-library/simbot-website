# KOOK(开黑啦)

<a href="https://github.com/simple-robot/simbot-component-kook/releases/latest">
<img alt="release" src="https://img.shields.io/github/v/release/simple-robot/simbot-component-kook" />
</a>

<seealso>
<category ref="links">
<a href="https://github.com/simple-robot/simbot-component-kook">KOOK组件仓库</a>
<a href="https://developer.kookapp.cn/doc/reference">KOOK开发者平台</a>
<a href="https://ktor.io/">Ktor首页</a>
</category>
</seealso>

## 概述

**KOOK组件**
是一个 [Kotlin 多平台](https://kotlinlang.org/docs/multiplatform.html) 的 [**KOOK机器人官方API**](https://developer.kookapp.cn/doc/reference) 
SDK实现库，
也是 Simple Robot 标准API下实现的组件库，异步高效、Java友好！

> 序列化和网络请求相关分别基于 [Kotlin serialization](https://github.com/Kotlin/kotlinx.serialization)
> 和 [Ktor](https://ktor.io/).

- 前往**KOOK组件**的 [GitHub 仓库](https://github.com/simple-robot/simbot-component-kook)

## 模块

KOOK 组件主要分为下面三层：

<deflist>
<def title="simbot-component-kook-api">

KOOK API 的底层封装模块。

- 定义各类 API 请求
- 定义事件模型、对象模型与消息结构
- 适合仅需要原始 API 能力的场景

</def>
<def title="simbot-component-kook-stdlib">

基于 `api` 模块的 Bot 基础实现与事件处理模块。

适合想保留更接近原始 KOOK 事件流程、但又不想从零处理鉴权与订阅逻辑的场景。

</def>
<def title="simbot-component-kook-core">

完整的 simbot KOOK 组件模块。

普通开发者通常直接使用它，并通过 `useKook()`、`KookBotManager`、
`KookBot` 等 API 进行集成。

</def>
</deflist>

## 安装
### 安装组件库

<procedure id="install-core" title="安装依赖">
<step>
<control>安装simbot核心库实现</control>

<include from="refers.md" element-id="pre-component-install" />
</step>
<step>
<control>安装组件的核心库依赖</control>

`simbot-component-kook-core`
即为 KOOK 组件的核心库，
也就是作为simbot组件所使用的
<tooltip term="组件">组件库</tooltip> 。

<tabs id="kook-build" group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
implementation("love.forte.simbot.component:simbot-component-kook-core:%kook-version%")
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Kotlin
implementation("love.forte.simbot.component:simbot-component-kook-core-jvm:%kook-version%")
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
implementation 'love.forte.simbot.component:simbot-component-kook-core:%kook-version%'
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Groovy
implementation 'love.forte.simbot.component:simbot-component-kook-core-jvm:%kook-version%'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<dependency>
    <groupId>love.forte.simbot.component</groupId>
    <artifactId>simbot-component-kook-core-jvm</artifactId>
    <version>%kook-version%</version>
</dependency>
```

</tab>
</tabs>
</step>
<step>
<control>安装Ktor客户端引擎</control>

KOOK组件使用 [Ktor](https://ktor.io) 作为 HTTP 客户端实现，
但是默认不会依赖任何具体的**引擎**。

因此，你需要选择并使用一个 Ktor Client 引擎实现。

<warning>

如果你使用 `stdlib` / `core` 中的 Bot 接收事件，
那么你需要选择一个支持 **WebSocket** 的引擎。

</warning>

<include from="refers.md" element-id="engine-choose"/>
</step>
</procedure>
