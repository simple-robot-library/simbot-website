# 概述

Simple Robot 是一个基于 Kotlin 协程的 Bot 风格 [Kotlin 多平台](https://kotlinlang.org/docs/multiplatform.html)事件调度框架，
异步高效、Java友好~

## 多平台实现 {id="multiplatform-targets"}

Simple Robot 基于 [**KMP**](https://kotlinlang.org/docs/multiplatform.html) 实现多平台，
支持 JVM、JS、`wasm-js` 和多个 Kotlin/Native 目标。具体支持范围以各模块为准。

<tip>

自 `5.0` 起，QQ 组件的 `common`、`api`、`stdlib`、`core` 和内部签名模块均支持 `wasm-js`。
KOOK 与 OneBot v11 的核心模块也提供 `wasm-js` 目标。

</tip>


> 部分模块受 Ktor 或签名库等依赖限制，未提供下列全部 Native 目标。
> 例如 QQ 组件的核心模块不提供 Android Native、`watchosX64` 和 `watchosDeviceArm64` 目标。

<procedure collapsible="true" title="支持目标列表">
<list>
<li>macosX64</li>
<li>macosArm64</li>
<li>iosSimulatorArm64</li>
<li>iosX64</li>

<li>linuxX64</li>
<li>linuxArm64</li>
<li>watchosSimulatorArm64</li>
<li>watchosX64</li>
<li>watchosArm32</li>
<li>watchosArm64</li>
<li>tvosSimulatorArm64</li>
<li>tvosX64</li>
<li>tvosArm64</li>
<li>iosArm64</li>

<li>androidNativeArm32</li>
<li>androidNativeArm64</li>
<li>androidNativeX86</li>
<li>androidNativeX64</li>
<li>mingwX64</li>
<li>watchosDeviceArm64</li>
</list>
</procedure>

## Java友好

Java是重要的伙伴, Kotlin天生与Java具有极强的兼容性。

simbot 基于 **Java11**, 为运行时模块提供 JVM 平台实现以及相应的 **模块化(JPMS)** 信息、
提供 **Spring Boot** 的 starter 快速快发实现、
以及异步、阻塞、预处理桥接器（可用于转化为响应式类型）的多种风格的挂起函数桥接API。

有关其中的部分详细信息, 可前往参考 
<a href="java-friendly.md" /> 。

## Bot风格

simbot 主要用于对接 Bot 平台, 例如 QQ机器人、KOOK机器人和 OneBot 协议实现等，
因此 simbot 的 API 设计也是以 Bot 为起点进行设计的。

## 高性能异步事件调度框架

既然是 Bot, 那么就少不了事件。simbot 基于 [**Kotlin 协程库**](https://kotlinlang.org/docs/coroutines-overview.html)
实现高性能、无阻塞、轻量且灵活的异步调度机制。