# QQ机器人

<a href="https://github.com/simple-robot/simbot-component-qq-guild/releases/latest">
<img alt="release" src="https://img.shields.io/github/v/release/simple-robot/simbot-component-qq-guild" />
</a>

<seealso>
<category ref="links">
<a href="https://github.com/simple-robot/simbot-component-qq-guild">QQ机器人组件仓库</a>
<a href="https://ktor.io/">Ktor首页</a>
<a href="https://bot.q.qq.com/wiki/develop/api-v2/">QQ机器人开放平台</a>
</category>
</seealso>

## 概述

**QQ机器人组件**
是一个 [Kotlin 多平台](https://kotlinlang.org/docs/multiplatform.html) 的 [**QQ机器人官方API**][qg bot doc] SDK实现库，
也是 Simple Robot 标准API下实现的组件库，异步高效、Java友好！

QQ 组件主要分成三个层次：

<list>
<li><control>simbot-component-qq-guild-api</control>

对 QQ 开放平台 API、模型、网关事件体的原始封装。
</li>
<li><control>simbot-component-qq-guild-stdlib</control>

在 API 之上提供较低封装的 Bot、鉴权与事件接收实现。
</li>
<li><control>simbot-component-qq-guild-core</control>

面向 simbot 的组件实现，也是大多数业务项目真正直接依赖的模块。
</li>
</list>

从当前源码可见，核心能力覆盖：

- 频道公域消息、频道/成员相关事件
- 论坛相关事件
- 频道私聊 `DMS`
- QQ群与 `C2C` 单聊能力

其中 QQ 群与 `C2C` 单聊能力自 `4.0.0-beta6` 起加入。
更细粒度的事件与对象范围，请以 <a href="component-qq-guild-event-list.md">事件列表</a> 和相邻对象章节为准。

> 序列化和网络请求相关分别基于 [Kotlin serialization](https://github.com/Kotlin/kotlinx.serialization)
> 和 [Ktor](https://ktor.io/).

- 前往**QQ机器人组件**的 [ GitHub 仓库](https://github.com/simple-robot/simbot-component-qq-guild)

## 模块

QQ 组件主要分为下面几层：

<deflist>
<def title="simbot-component-qq-guild-api">

QQ 机器人官方 API 的底层封装模块。

- 定义 API 请求类型
- 定义原始事件模型
- 定义部分消息模型与构建器

</def>
<def title="simbot-component-qq-guild-stdlib">

基于 `api` 的低限度 Bot 实现与事件接收处理模块。

如果你希望保留更接近原始协议的事件流程，
或者正在做更底层的集成，可以关注它。

</def>
<def title="simbot-component-qq-guild-core">

真正作为 simbot 组件使用的核心模块。

普通应用开发时，通常直接依赖它即可。

</def>
<def title="simbot-component-qq-guild-internal-ed25519">

内部签名支持模块，一般不需要手动直接依赖。

</def>
</deflist>

## 命名说明

QQ机器人组件命名为 `simbot-component-qq-guild`，
因为最早开始QQ并未开放普通个人开发者使用QQ群聊、QQ单聊的功能，
因此此组件当时仅支持QQ频道。在开放后，其两端可以合并在一起使用，因此QQ群相关的能力才被支持。

> QQ群、QQ单聊功能自 `4.0.0-beta6` 版本起开始支持。

## 前提准备

### 机器人账号

你需要参考 [官方QQ机器人文档](https://bot.q.qq.com/wiki) ，并注册一个 
**机器人账号** 。审核通过，
便可登录 [QQ开放平台](https://q.qq.com/#/) 查看你的机器人账号信息了。

### 事件订阅方式

官方提供了 `webhook` 与 `websocket` 两种事件订阅方式。

目前，这两种接入路径都有对应实现或示例：

- 如果你要接入 `webhook` 回调，前往 [](component-qq-guild-Webhook.md)
- 如果你要使用 `websocket` 收事件，则继续参考本页与 [](component-qq-guild-start-using.md)

你可以在机器人后台中查看、配置自己的回调地址与订阅范围。

## 安装

### 安装组件库

<procedure id="install-core" title="安装依赖">
<step>
<control>安装simbot核心库实现</control>

<include from="refers.md" element-id="pre-component-install" />
</step>
<step>
<control>安装组件库</control>

`simbot-component-qq-guild-core` 
即为QQ机器人组件的核心库，
也就是作为simbot组件所使用的
<tooltip term="组件">组件库</tooltip>
。

<tabs id="qg-build" group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
implementation("love.forte.simbot.component:simbot-component-qq-guild-core:%qg-version%")
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Kotlin
implementation("love.forte.simbot.component:simbot-component-qq-guild-core-jvm:%qg-version%")
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
implementation 'love.forte.simbot.component:simbot-component-qq-guild-core:%qg-version%'
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Groovy
implementation 'love.forte.simbot.component:simbot-component-qq-guild-core-jvm:%qg-version%'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<dependency>
    <groupId>love.forte.simbot.component</groupId>
    <artifactId>simbot-component-qq-guild-core-jvm</artifactId>
    <version>%qg-version%</version>
</dependency>
```

</tab>
</tabs>
</step>
<step>
<control>安装Ktor客户端引擎</control>

QQ机器人组件使用 [Ktor](https://ktor.io) 作为 HTTP 客户端实现，
但是默认不会依赖任何具体的**引擎**。

因此，你需要选择并使用一个 Ktor Client 引擎实现。

<warning>

如果你使用 `websocket` 订阅事件，需要选择一个支持 **WebSocket** 的引擎。
如果你只做 `webhook` 回调并自行处理服务端接入，则只需要满足 HTTP 客户端侧的依赖要求。

</warning>

<include from="refers.md" element-id="engine-choose"/>
</step>
</procedure>


[qg bot doc]: https://bot.q.qq.com/wiki/develop/api-v2/
