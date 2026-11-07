---
switcher-label: JavaAPI风格
---

# 使用核心库

<tldr>

使用 `Application` 的基本实现模块 `simbot-core`。想先运行一个完整的纯本地例子，可以参考 [](first-event.md)。

</tldr>

## 准备

<include from="installation.md" element-id="prepare-simbot-core-snippet"></include>

> 也可前往
> <a href="installation.md#prepare-simbot-core">安装章节的准备部分</a>
> 参考更多。

## 安装

<include from="refers.md" element-id="simbot-core-build"></include>

> 也可前往
> <a href="installation.md#安装核心库">安装章节的安装部分</a>
> 参考更多。

## 使用

下面的片段分别展示创建和等待/保持应用的方法。接入组件时，请先注册监听器、注册并启动 Bot，再在程序末尾等待应用结束。

### 创建 Application

<tabs group="Code">

<tab title="Kotlin" group-key="Kotlin">

使用 `Simple` 工厂, 或使用扩展函数 `launchSimpleApplication`。

```Kotlin
val app = launchApplication(Simple) {
    // 配置...
}

// 或

val app = launchSimpleApplication {
    // 配置...
}

app.join() // 挂起直到被关闭
```

</tab>
<tab title="Java" group-key="Java">

```Java
var applicationAsync = Applications.launchApplicationAsync(Simple.INSTANCE, appConfigurer -> {
        // 配置 Application...
       
    });

// 异步结果可转化为 CompletableFuture
var future = applicationAsync.asFuture()
        .thenCompose(Application::asFuture);

// 阻塞当前线程直到应用被关闭
future.join();
```
{switcher-key="%ja%"}

```Java
var application = Applications.launchApplicationBlocking(Simple.INSTANCE, appConfigurer -> {
        // 配置 Application...

    });

// 注册事件处理器、注册bot等

// 阻塞当前线程直到被关闭
application.joinBlocking();
```
{switcher-key="%jb%"}

```Java
var applicationAsync = Applications.launchApplicationAsync(Simple.INSTANCE, appConfigurer -> {
        // 配置 Application...

    });

Mono.fromFuture(applicationAsync.asFuture())
        .flatMap(app -> Mono.from(app.joinReactive()))
        .block();
```
{switcher-key="%jr%"}


<tip switcher-key="%jr%">

响应式示例使用 Reactor，依赖与桥接方式参考 [](java-friendly.md#reactive-bridging)。

</tip>

</tab>
</tabs>

有关 `Application` 的配置与使用可直接前往参考 [基本内容-Application](basic-application.md) 章节,
它里面用于示例的内容就是 `simbot-core` 的实现 `Simple`。

## 安装组件

前往 [**组件库**](components-intro.md) 选择你想要使用的组件，或者选择某个/些你想要使用的第三方组件，
根据它们的手册安装、配置到你的 `Application` 中。

## 运行

完成组件配置和监听器注册后，执行 `main` 方法。`join()` 会挂起并等待应用关闭，适合放在函数末尾。
如果暂时没有平台账号，可以先运行 [](first-event.md) 中的本地事件示例。

> 在 native 平台下，你可能需要使用 `runBlocking { ... }` 包裹上述需要挂起的内容
> (因为 native 尚不支持可挂起的 main 入口，参考 [KT-52753](https://youtrack.jetbrains.com/issue/KT-52753/Native-Support-suspending-entrypoints))，
> 此时建议为其分配调度器，比如：`runBlocking(Dispatchers.Default) { ... }`。
