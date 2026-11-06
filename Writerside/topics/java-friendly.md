---
switcher-label: JavaAPI风格
---

<show-structure for="chapter,procedure" depth="3"/>

# Java友好 ♥

<tldr>
对 simbot 中提供的诸项 Java 友好方案的介绍。
</tldr>

## Lambda

simbot 中相比于 simbot3, 对于部分 lambda 的场景进行了简单的优化,
在 Java 中需要手写返回 `return Unit.INSTANCE;` 的地方大大减少了。

## 阻塞、异步与响应式

simbot
借助编译器插件
[kotlin-suspend-transform-compiler-plugin][kstcp]
为 Java 和其他可能的平台提供阻塞、异步以及响应式风格的 API。项目中启用并配置编译器插件后，
标记 `@ST`（`@SuspendTrans`）或 `@STP`（`@SuspendTransProperty`）的挂起声明会生成相应桥接方法。
未标记的挂起函数及手写 Java 辅助方法，需要查看各自提供的入口。

[kstcp]: https://github.com/ForteScarlet/kotlin-suspend-transform-compiler-plugin

例如, 一个 Kotlin 中的挂起函数：

```Kotlin
import love.forte.simbot.suspendrunner.ST

@ST
suspend fun run(): Int {
    // ...
}
```

在 Java 中是难以调用的, 因为挂起函数在编译后会经过“编译魔法”而产生一些变化。

如果启用了项目中的插件配置，并给这个挂起函数添加 `@ST`，编译器插件会生成可供 Java 使用的桥接 API：

```Java
/**
 * 阻塞桥接，等待挂起函数完成后返回结果。
 */
public int runBlocking() { ... }

/**
 * 异步桥接，返回 future。
 */
public CompletableFuture<? extends Integer> runAsync() { ... }

/**
 * Reactive 桥接（自 5.0 起，实验性）。
 */
public Publisher<? extends Integer> runReactive() { ... }
```

## 真实命名规则

最常见的 JVM 侧桥接风格可以粗略理解为下面三类：

<deflist>
<def title="Blocking">

阻塞调用，通常是 `xxxBlocking()`。

例如：

- `bot.startBlocking()`
- `application.joinBlocking()`

</def>
<def title="Async">

异步调用，通常是 `xxxAsync()` 并返回 `CompletableFuture`。

例如：

- `bot.startAsync()`
- `event.replyAsync(...)`

也有少数 API 会显式改名，例如 `join()` 在 JVM 上的异步桥接是 `asFuture()`：

- `application.asFuture()`
- `bot.asFuture()`

</def>
<def title="Reactive">

自 `5.0` 起，桥接方法返回 `org.reactivestreams.Publisher`，通常命名为
`xxxReactive()`；属性风格的方法通常为 `getXxxReactive()`。具体名称可通过注解参数调整。
这类 API 使用 `ExperimentalReactiveBridgingApi` 标记，可能在后续版本变更或移除。

</def>
</deflist>

对于属性式、getter 风格的挂起 API，桥接命名会进一步偏向 getter。
例如 `content()`、`guildCount()` 这类 API 在 JVM 上更常看到 `getContent()`、`getGuildCount()` 这样的名称。


### 💡 文档表现

在文档中，可能会同时提供阻塞、异步、响应式三种风格的API。

此时你可以通过文档**右上角**的切换标签
<control>JavaAPI风格</control>
来修改展示的API风格。

<note>

动动手试试吧！现在显示的风格是：
<control switcher-key="%ja%">%ja%</control>
<control switcher-key="%jb%">%jb%</control>
<control switcher-key="%jr%">%jr%</control>

</note>

### ⚠️ 注意异步中的异常处理

当你在使用**异步**结果时（也包括下文会提到的各响应式类型结果），你需要多一些心眼儿。

以 `CompletableFuture` 为例，如果不做任何操作，
你很有可能会丢失且无法感知到**异常**。

例如：

```Java
var future = xxx.runAsync();
```

此时，如果 `runAsync` 内异步任务出现异常，代码中（或者控制台、日志等）实际上不会出现任何信息。
你需要使用明确的API进行异常处理：

```Java
// 假设返回结果是 Integer
CompletableFuture<? extends Integer> future = xxx.runAsync();

// 可以使用 exceptionally 在出现异常时计算一个新的结果
future.exceptionally(exception -> {
    logger.error("异常了！", exception);
    // 更建议返回一个真实的结果，但是确保下游不会出错的情况下，使用 `null` 也无可厚非。
    return null;
});

// 可以使用 handle 同时处理正常结果或异常结果
future.handle((value, exception) -> {
    if (exception != null) {
        // 如果出现了异常
        logger.error("异常了！", exception);
        return null;
    }
    
    // 正常结果
    return value;
});
        
// 可以使用 whenComplete 来注册回调，来感知到异常，而不影响下游的直接使用。
future.whenComplete((value, exception) -> {
    if (exception != null) {
        // 如果出现了异常
        logger.error("异常了！", exception);
        
        return;
    }

    // 使用 value 正常结果
    
});
```

下文所述的各种响应式结果通常也可能会有类似的问题，需要多加注意喔。


## 响应式桥接 {id="reactive-bridging"}

<primary-label ref="experimental"/>
<secondary-label ref="since-5.0"/>

借助编译器插件，其生成的 JVM 编译产物包含 `Reactive` 方法，返回 `org.reactivestreams.Publisher`，
以直接交给 Reactor 等响应式库处理并使用，挂起函数在订阅后执行。
返回非空值时发布该值，返回 `null` 时直接完成。依据响应式的特性，订阅所得元素永不为 null。

Kotlin 调用这些实验性桥接方法需要选择加入 `ExperimentalReactiveBridgingApi`。

```Java
Mono.from(bot.startReactive()).block();
```

<note>

虽然示例使用了 `block`，但是既然你选择使用响应式 API，那么我们并不建议你使用任何可能会导致阻塞行为的操作。
这里只是为了示例的便捷性才使用它，在真正的代码逻辑中请避免。

</note>

### 顺序组合响应式操作

以下示例需要 Reactor 的 `reactor-core` 依赖。通过 `Mono.from` 接入生成的 Publisher，
使用 `then` 等待前一个操作完成后执行下一个操作：

```Java
Mono.from(bot.startReactive())
        .then(Mono.from(bot.joinReactive()))
        .subscribe(ignored -> {}, Throwable::printStackTrace);
```

响应式链需要订阅后才会执行。返回 `null` 的桥接调用只发送完成信号，后续操作应通过 `then` 组合。

## 集成 Spring Boot

simbot 提供 Spring Boot starter 模块，具有对 Spring Boot 的集成能力。
Spring Boot starter 模块也实现了 [量子猫](advanced-quantcat.md) 模块, 提供基于**注解**的高效开发方案。

有关集成SpringBoot的更多信息可以前往 [**集成SpringBoot**](Spring-Boot.md) 。
