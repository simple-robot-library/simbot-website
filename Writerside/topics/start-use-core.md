---
switcher-label: JavaAPI风格
---

# 使用核心库

<tldr>

使用 `Application` 的基本实现模块 `simbot-core`。

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
        .flatMap(app -> app.joinReserve().transform(SuspendReserves.mono()))
        .block();
```
{switcher-key="%jr%"}

</tab>
</tabs>

有关 `Application` 的配置与使用可直接前往参考 [基本内容-Application](basic-application.md) 章节,
它里面用于示例的内容就是 `simbot-core` 的实现 `Simple`。

## 安装组件

前往 [**组件库**](components-intro.md) 选择你想要使用的组件，或者选择某个/些你想要使用的第三方组件，
根据它们的手册安装、配置到你的 `Application` 中。

## 运行

执行你的程序入口 `main` 方法，体验一下吧~

> 在 native 平台下，你可能需要使用 `runBlocking { ... }` 包裹上述需要挂起的内容
> (因为 native 尚不支持可挂起的 main 入口，参考 [KT-52753](https://youtrack.jetbrains.com/issue/KT-52753/Native-Support-suspending-entrypoints))，
> 此时建议为其分配调度器，比如：`runBlocking(Dispatchers.Default) { ... }`。
