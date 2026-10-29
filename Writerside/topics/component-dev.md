# 组件库开发

本章节下内容会为你介绍如何实现一套自定义的
<tooltip term="组件">组件库</tooltip>
, 包括
<tooltip term="组件标识">组件标识</tooltip>、
<tooltip term="插件">插件</tooltip>、
Bot、Bot管理器、事件等。

## 推荐组合

我们**强烈推荐**您使用 `Kotlin` + `Gradle` 的组合开发组件，
并在有条件的情况下支持 KMP 多平台。

尤其是当你使用 Kotlin 语言进行开发时, 只有 `Gradle` 支持多平台和子章节中会介绍到的 
<a href="component-dev-compiler-plugin.md" />。

而且很多高级功能 (例如 `BotManager`) 都**仅限**使用 Kotlin 实现。

## 注意事项
### Java 版本 {id="java-version"}

simbot 的 JVM 目标最低为 **Java11**。不论是使用 Kotlin 还是 Java 开发,
都应当满足此要求。

### Java 模块化 {id="JPMS"}

既然最低 Java 目标的要求是 **Java11**, 我们也强烈建议您在 JVM 平台上支持 Java 的模块化信息([JPMS](https://www.oracle.com/cn/corporate/features/understanding-java-9-modules.html))。

> 说的简单点儿, 就是提供一个合适的 `module-info.java`。

### 开发语言?

simbot4 是基于 Kotlin 多平台实现、提供 Java 友好 API 的事件调度框架。
对于普通开发者来讲, 我们提供了阻塞、异步等多种风格的 Java API 供开发者选择。

对于 **组件开发**, 我们**强烈建议**使用 [Kotlin](https://kotlinlang.org/) 语言。
能使用 Java 开发的组件部分比较有限, 尤其是涉及到 `Bot` 等需要网络请求等内容的实现。

如果你了解 Java 等语言, 那么 Kotlin 的上手也会很快。
如果不介意的话, 我建议尽可能地选择使用 Kotlin 进行 **组件开发**。

当然, 如果你的实现比较简单, 比如仅仅是注册一个事件监听器等, 那么 Java 也可以应付, 
但是不论如何其开发体验都远不及使用 Kotlin。

> 如果遇到了无法使用 Java 进行实现或使用 Java 实现起来十分困难的地方会进行标注说明。

### 严谨且友好
大部分情况下开发一个**组件库**都是为了将其共享给更多的人使用，也就是说组件库是服务**开发者用户**的。
simbot提供了大量便捷、友好的API或异常提示供**开发者用户**使用，而开发一个组件库也需要尽可能地使API严谨且友好一些。
