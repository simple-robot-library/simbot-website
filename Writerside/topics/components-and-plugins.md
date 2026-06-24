# 组件与插件

本章节会介绍 simbot4 中的 **组件** 和 **插件** 的概念，
以及它们在 `Application` 中各自承担的职责。

## 组件

在文档中, 常说的
<tooltip term="组件"><control>组件</control></tooltip>
就是是对一组一个或多个 
<tooltip term="组件标识"><control>组件标识</control></tooltip> 和 
<tooltip term="插件"><control>插件</control></tooltip>
的统称。

它是simbot中特定平台功能的主要提供者，是重要的核心概念之一。

例如当我们说 “QQ频道组件”, 
就是在描述一个包含了 **QQ频道组件标识 (`QQGuildComponent`)**
和 **QQ频道Bot管理器 (`QQGuildBotManager`)**
的整体。

<note>
举个不恰当的例子。
如果将 simbot 不自量力地比喻为 Spring Boot，那么组件则可以类似地视为各种 starter。
</note>

组件通常会同时带来下面几类能力：

- 组件标识 `Component`
- 一个或多个插件，最常见的是 `BotManager`
- 序列化模块、消息元素、事件类型与行为对象实现

如果你只是想开发一个平台应用，通常只需要选择对应组件的 `*-core` 模块即可。

## 组件标识

参考章节 [组件标识](component-id.md) 。

## 插件

参考章节 [插件](plugin.md) 。

## 进一步阅读

- 如果你希望从模块层面理解 simbot 的结构，可前往 [](module-libraries.md)。
- 如果你正在选择官方组件，可前往 [](components-intro.md)。
