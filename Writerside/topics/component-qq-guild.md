# QQ机器人

<a href="https://github.com/simple-robot/simpler-robot/releases">
<img alt="release" src="https://img.shields.io/github/v/release/simple-robot/simpler-robot?include_prereleases" />
</a>

<seealso>
<category ref="links">
<a href="https://github.com/simple-robot/simpler-robot/tree/dev/simbot-component-qq">QQ机器人组件源码</a>
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
<li><control>simbot-component-qq-api</control>

对 QQ 开放平台 API、模型、网关事件体的原始封装。
</li>
<li><control>simbot-component-qq-stdlib</control>

在 API 之上提供较低封装的 Bot、鉴权与事件接收实现。
</li>
<li><control>simbot-component-qq-core</control>

面向 simbot 的组件实现，也是大多数业务项目真正直接依赖的模块。
</li>
</list>

目前核心能力覆盖：

- 频道公域消息、频道/成员相关事件
- 论坛相关事件
- 频道私聊 `DMS`
- QQ群与 `C2C` 单聊能力
- 频道、QQ群与 C2C 消息撤回 API（自 `5.0` 起补充群聊与单聊支持）
- C2C 自定义菜单与多场景指令面板管理（自 `5.0` 起）
- 群基础信息、机器人群内状态、入群申请管理和成员禁言（自 `5.0` 起）

其中 QQ 群与 `C2C` 单聊能力自 `4.0.0-beta6` 起加入。
更细粒度的事件与对象范围，请以 <a href="component-qq-guild-event-list.md">事件列表</a> 和相邻对象章节为准。

> 序列化和网络请求相关分别基于 [Kotlin serialization](https://github.com/Kotlin/kotlinx.serialization)
> 和 [Ktor](https://ktor.io/).

- 前往**QQ机器人组件**的 [源码目录](https://github.com/simple-robot/simpler-robot/tree/dev/simbot-component-qq)

## 模块

<secondary-label ref="changed-5.0"/>

QQ 组件使用 `simbot-component-qq-*` 坐标，随标准库统一版本发布。

| 模块 | 内容 |
| --- | --- |
| `simbot-component-qq-common` | 共享常量与注解，自 `5.0` 起提供 |
| `simbot-component-qq-api` | API 请求、原始事件、消息模型与构建器 |
| `simbot-component-qq-stdlib` | Bot、鉴权和事件接收处理 |
| `simbot-component-qq-core` | simbot 组件实现，普通应用直接依赖此模块 |
| `simbot-component-qq-internal-ed25519` | 内部签名支持，通常不需要直接依赖 |

上述模块均支持 JVM、JS、`wasm-js` 和部分 Native 目标。
版本升级与旧坐标迁移参见 [](migration-5.0.md)。

## 命名说明

QQ机器人组件最初只支持 QQ 频道，因此使用 `simbot-component-qq-guild` 命名。
自 `5.0` 起，模块坐标调整为 `simbot-component-qq-*`。
包名与 `QQGuildComponent`、`QQGuildBotManager` 等类型名仍保留原有命名。

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

`simbot-component-qq-core`
即为QQ机器人组件的核心库，
也就是作为simbot组件所使用的
<tooltip term="组件">组件库</tooltip>
。

<tabs id="qg-build" group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
implementation("love.forte.simbot.component:simbot-component-qq-core:%qg-version%")
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Kotlin
implementation("love.forte.simbot.component:simbot-component-qq-core-jvm:%qg-version%")
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
implementation 'love.forte.simbot.component:simbot-component-qq-core:%qg-version%'
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Groovy
implementation 'love.forte.simbot.component:simbot-component-qq-core-jvm:%qg-version%'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<dependency>
    <groupId>love.forte.simbot.component</groupId>
    <artifactId>simbot-component-qq-core-jvm</artifactId>
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
