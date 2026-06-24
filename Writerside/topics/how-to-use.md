# 开始使用

<tldr>
本章节介绍开始使用 simbot4 的基本步骤。
</tldr>

<procedure>
<step>安装核心库或Spring starter, 或者其他任意的 Application 实现。</step>
<step>选择并安装你所需的组件库, 配置它们</step>
<step>启动你的程序, 或者打包、部署。</step>
</procedure>

## 安装 Application 实现

先添加一个基于 `simbot-api`、实现了完整 `Application` 能力的库，再按它的要求配置或使用。

### 官方实现

simbot4 提供了两个这样的库：`simbot-core`（也就是 **“核心库”**）和 Spring Boot 的 starter 实现。

<list>
<li>

前往 <a href="start-use-core.md">核心库</a>
了解如何添加并使用 <code>simbot-core</code> 以及它提供的 <code>Application</code> 实现：<code>Simple</code>。

</li>
<li>

前往 <a href="start-use-spring-boot-3.md">Spring Boot 3</a>
了解如何添加并使用 <code>simbot-core-spring-boot-starter</code> 以及它提供的 <code>Application</code> 实现。

</li>
<li>

如果你仍在使用 Spring Boot 2.x，
前往 <a href="start-use-spring-boot-2.md">Spring Boot 2</a>
了解如何添加并使用 <code>simbot-core-spring-boot-starter-v2</code>。

</li>
</list>

<note>

通常来说，虽然也需要添加组件库，但核心库（或其他 Application 实现库）的依赖依然是**必须的**。
因为组件库对核心库（或者标准库）的依赖通常**只在编译期**。

</note>

## 安装组件、插件

`Application` 提供了 `simbot-api`（也就是**“标准库”**）定义的诸多能力，比如组件、插件安装和事件调度，
但它不包含 **具体的平台实现**，比如 QQ 频道、KOOK、大别野等 **特定平台** 的事件和消息。

这些**特定平台**的实现，就是一个个不同的**组件或插件**。它们一般在各自独立的仓库中维护、发版，
依赖标准库，但彼此独立。
下文将它们称为 **“组件库”** 。

以我们 [**官方维护的组件库**](components-intro.md) 为例，它们都有各自的应用手册，
手册里也会提供类似“快速开始”的章节，说明如何配置、如何搭建项目。

接下来只要选择要用的组件库，把依赖加上，再完成配置就行。
如果只用一个组件库，也可以直接看对应的“快速开始”，里面会一起介绍核心库和组件库实现的安装。

下面是一个简单的添加依赖的**伪例子**：

<tabs group="build">
<tab title="Gradle (Kotlin DSL)" group-key="kts">

```Kotlin
// 使用核心库
implementation("love.forte.simbot:simbot-core:%version%")
// 添加组件库, 假设有两个叫做 foo1、bar2 的组件实现
implementation("com.example.component:foo1-core:x.xx")
implementation("io.github.Jojo.cp:bar2-impl:x.xx")
```

</tab>
<tab title="Gradle (Groovy)" group-key="groovy">

```groovy
// 使用核心库
implementation 'love.forte.simbot:simbot-core:%version%'
// 添加组件库, 假设有两个叫做 foo1、bar2 的组件实现
implementation 'com.example.component:foo1-core:x.xx'
implementation 'io.github.Jojo.cp:bar2-impl:x.xx'
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<!-- 使用核心库 -->
<dependency>
    <groupId>love.forte.simbot</groupId>
    <artifactId>simbot-core</artifactId>
    <version>%version%</version>
</dependency>
<!-- 添加组件库, 假设有两个叫做 foo1、bar2 的组件实现 -->
<dependency>
    <groupId>com.example.component</groupId>
    <artifactId>foo1-core</artifactId>
    <version>x.xx</version>
</dependency>
<dependency>
    <groupId>io.github.Jojo.cp</groupId>
    <artifactId>bar2-impl</artifactId>
    <version>x.xx</version>
</dependency>
```

</tab>
</tabs>

### 官方组件

- 前往 [**组件库**](components-intro.md) 找到需要的组件，再按引导或手册添加依赖并使用。

### 社区组件

- 前往 [**社区组件**](community-components.md) 找到需要的组件，或者自行开发组件、插件再使用。

### 组件开发

- 前往 [**组件开发**](component-dev.md) 了解开发组件库的方式与步骤。
