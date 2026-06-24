<show-structure for="chapter,procedure" depth="3"/>

# OneBot

<a href="https://github.com/simple-robot/simbot-component-onebot/releases/latest">
<img alt="release" src="https://img.shields.io/github/v/release/simple-robot/simbot-component-onebot" />
</a>

<seealso>
<category ref="links">
<a href="https://github.com/simple-robot/simbot-component-onebot">OneBot组件仓库</a>
<a href="https://ktor.io/">Ktor首页</a>
<a href="https://github.com/botuniverse/onebot-11">OneBot11</a>
</category>
</seealso>

## 概述

OneBot 组件是一个
[OneBot11协议](https://github.com/botuniverse/onebot-11)
的客户端SDK，
也是 Simple Robot 标准API下实现的组件库。

借助simbot核心库提供的能力，它支持众多高级功能和封装，比如组件协同、Spring支持等，
助你快速开发 OneBot 客户端应用！

> 序列化和网络请求相关分别基于 [Kotlin serialization](https://github.com/Kotlin/kotlinx.serialization)
> 和 [Ktor](https://ktor.io/)。

- 前往**OneBot组件**的 [GitHub 仓库](https://github.com/simple-robot/simbot-component-onebot)

## 模块

### 公共模块

OneBot组件为所有协议实现的模块提供了一些共享内容的模块，
命名为 `simbot-component-onebot-common`。

此模块中会定义一些通用的类型或注解等。
对于普通开发者来讲可以不用过多关注，此模块由其他组件模块引用并使用。

### OneBot11

在OneBot组件中，我们提供了针对 [OneBot11](https://github.com/botuniverse/onebot-11)
协议的组件实现模块，它们的坐标以 `simbot-component-onebot-v11` 作为开头：

<list>
<li><control>simbot-component-onebot-v11-common</control>

在OneBot11协议的实现模块中进行共享的模块。
对于普通开发者来讲可以不用过多关注，此模块由其他组件模块引用并使用。
</li>
<li><control>simbot-component-onebot-v11-core</control>

OneBot11协议作为一个simbot组件的实现模块。通常会是你**真正使用**的模块。
当前组件标识为 `simbot.onebot11`。
</li>
<li><control>simbot-component-onebot-v11-event</control>

对OneBot11协议中的[原始事件](https://github.com/botuniverse/onebot-11/tree/master/event)
类型提供定义的模块，
被 `simbot-component-onebot-v11-core` 引用并依赖。

<tip>

需要注意的是这里的事件并不是simbot中的**事件**，而仅仅是一种数据类实现，
是对原始事件的JSON结构的基本映射。
</tip>
</li>
<li><control>simbot-component-onebot-v11-message</control>

对OneBot11协议中的[原始消息段](https://github.com/botuniverse/onebot-11/blob/master/message/segment.md)
类型提供定义的模块。

这里定义的大部分类型都是针对消息段的数据类实现，
是对它们的JSON结构的基本映射，
被 `simbot-component-onebot-v11-core` 引用并依赖。

</li>
</list>

<tip>

对于普通应用开发者来说，通常直接依赖 `simbot-component-onebot-v11-core` 即可。
其余模块更多用于协议模型、底层封装或扩展实现。

</tip>


## 安装

### 安装OneBot11组件

<procedure title="前期准备" id="OneBot11-前期准备">
<step>
<control>准备OneBot11协议服务端</control>

OneBot组件是一个 OneBot 协议的**客户端**实现，
因此在使用之前，你需要准备一个支持 OneBot11 的**服务端**，
例如 `NapCat`, `Language.OneBot` 等。

<warning>

鉴于 OneBot 生态的特殊性，
此处不对具体服务端实现作更多展开说明。
你只需要确保它：

- 支持 OneBot11
- 提供 HTTP API
- 如需事件订阅，则提供正向 WebSocket

</warning>
</step>

</procedure>

<procedure title="安装依赖" id="OneBot11-安装依赖">
<step>
<control>安装simbot核心库实现</control>

<include from="refers.md" element-id="pre-component-install" />

</step>
<step>
<control>安装 <code>simbot-component-onebot-v11-core</code> 依赖</control>

<tabs id="build" group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
implementation("love.forte.simbot.component:simbot-component-onebot-v11-core:%ob-version%")
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Kotlin
implementation("love.forte.simbot.component:simbot-component-onebot-v11-core-jvm:%ob-version%")
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
implementation 'love.forte.simbot.component:simbot-component-onebot-v11-core:%ob-version%'
```

如果使用 Java 而不配合使用 Gradle 的 `kotlin` 插件, 那么你需要指定依赖的后缀为 `-jvm`。

```Groovy
implementation 'love.forte.simbot.component:simbot-component-onebot-v11-core-jvm:%ob-version%'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<dependency>
    <groupId>love.forte.simbot.component</groupId>
    <artifactId>simbot-component-onebot-v11-core-jvm</artifactId>
    <version>%ob-version%</version>
</dependency>
```

</tab>
</tabs>
</step>
<step>
<control>安装Ktor客户端引擎</control>

OneBot11组件使用 [Ktor](https://ktor.io) 作为 HTTP 客户端实现，
但是默认不会依赖任何具体的**引擎**。

因此，你需要选择并使用一个 Ktor Client 引擎实现。

<warning>

注意，你需要选择一个支持 **WebSocket** 的引擎。

</warning>

<include from="refers.md" element-id="engine-choose"/>
</step>
</procedure>
