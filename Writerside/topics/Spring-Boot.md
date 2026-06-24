# Spring Boot

simbot Spring Boot starter 基于核心库实现，提供对 Spring Boot 应用的快速集成能力。

<note>

有关 Spring Boot 的更多信息，前往 [spring.io](https://spring.io) 了解更多。

</note>

## 什么是 Spring Boot starter?

参考 [官方文档](https://docs.spring.io/spring-boot/reference/using/build-systems.html#using.build-systems.starters)
的说明：

> Starters are a set of convenient dependency descriptors that you can include in your application. 

启动器是一组方便的依赖描述符，你可以将它包含在你的应用程序中。

而 simbot Spring Boot starter 便是这样一组描述符：允许你将 simbot 的核心功能更快捷、简单地集成进你的 Spring 应用程序中。
除了核心功能的实现，simbot starter 还实现了
<a href="advanced-quantcat.md"></a>，
你可以通过各类注解API更快速高效的编写你的事件处理逻辑 —— 与 Spring 应用一起。

## 模块关系

目前 Spring Boot 集成主要由下面三个模块组成：

<deflist>
<def title="simbot-core-spring-boot-starter-common">

Starter 2 / 3 共用的通用支持模块。
承载 <code>love.forte.simbot.spring.common</code> 下的公共类型、配置模型与异常定义。

</def>
<def title="simbot-core-spring-boot-starter">

面向 Spring Boot 3 / Java 17+ 的主 Starter。
主要包名前缀为 <code>love.forte.simbot.spring</code>。

</def>
<def title="simbot-core-spring-boot-starter-v2">

面向 Spring Boot 2 / Java 11+ 的兼容 Starter。
主要包名前缀为 <code>love.forte.simbot.spring2</code>。

</def>
</deflist>

## 安装

<procedure id="install-spring">
<step><control>准备Java</control>

我们推荐您使用 Spring Boot 3.x。因此 Java 的版本至少为 **Java17** 。

> 如果你打算使用 Spring Boot 2.x，
> 请参阅下文有关 2.x 版本的兼容模块的说明，
> 其 Java 的版本至少为 **Java11** 。

</step>
<step><control>准备 Spring Boot 项目</control>

前往 [start.spring.io][spring.start] 选择、创建一个 Spring Boot 项目下载。
当然，你也可以选择其他任意可行方式来创建项目，例如借助IDE。

更多参考:
- [如何构建你的第一个SpringBoot应用](https://docs.spring.io/spring-boot/tutorial/first-application/index.html)。
- [Spring Initializr][spring.start]
- [Spring Quickstart Guide](https://spring.io/quickstart/)

</step>
<step><control>添加 simbot starter 依赖</control>

<tabs>
<tab title="Spring Boot 3">

使用 Spring Boot 3，确保项目的JDK版本大于等于 JDK17。

<include from="refers.md" element-id="simbot-spring-3-build"></include>

</tab>
<tab title="Spring Boot 2">
<warning title="再考虑一下">

我们建议你优先考虑使用 Spring Boot 3。

<list>
<li>

首先，Spring Boot 2.x 目前最后的一个版本 v2.7.x 已经在 2023-11-24 结束了
_开放源码软件支持(OSS support)_ ，并会在 2026 年之前彻底结束支持。

(参考[Spring官方文档](https://spring.io/projects/spring-boot#support))

</li>
<li>

如果阻碍你使用 Spring Boot 3 的仅仅是Java的版本，
你仍有其他办法通过较低版本的Java使用 Spring Boot 3，
这其中的详细内容可参考 Jetbrains 的这篇
[技术博客](https://blog.jetbrains.com/zh-hans/idea/2024/06/java-runtimes-insights-from-the-spring-boot-point-of-view/)。

引用其中的相关说明：

> 此外，Spring Boot 3.x 要求使用 Java 17 作为基线，
> 因此如果您想利用您最喜欢的框架的新主要版本的强大功能，升级 Java 版本至关重要。
>
> 不过，如果现在不能升级，一些供应商（如 Oracle 和 BellSoft）
> 也提供了将 JVM 17 与 JDK 8 结合的解决方案（对于 JDK 11，BellSoft 也有类似的解决方案）。
> 这样会使您的应用程序认为它仍然运行在旧的 Java 版本上，但实际上它拥有一个较新的引擎。
> 对您来说，这意味着什么？ 无需升级 Java 或框架，也几乎无需进行代码更改，即可立即缩短延迟并提高吞吐量！

</li>
</list>

`simbot-core-spring-boot-starter-v2`
是用来兼容 Spring Boot v2 的，Java版本最低仅需Java11。
但是此模块**不保证**未来会持续维护、更新，也**不保证**其稳定性。

</warning>

<include from="refers.md" element-id="simbot-spring-2-build"></include>

</tab>
</tabs>

</step>
<step><control>添加组件及其要求的其他内容</control>

simbot的组件是功能的主要提供者，是**重要**的核心概念之一。
你可以前往 <a href="components-intro.md">组件库</a>
选择你所需要的组件并添加它们，而它们的手册通常都会有各自相应的**快速开始**或**安装**章节。

<note>
大部分官方组件都会需要你添加 Ktor 引擎，注意观察阅读、不要漏掉喔~
</note>

你也可以使用任何可用的第三方组件，并参照它们各自的文档说明进行安装。

</step>
</procedure>

## 使用
### 启用 simbot

在你的启动类或任意配置类上标记 `@EnableSimbot` 注解来在 Spring 中启用 simbot。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@EnableSimbot // 启用 simbot
@SpringBootApplication
class MyApplication

fun main(args: Array<String>) {
    runApplicarion<MyApplication>(*args)
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@EnableSimbot // 启用 simbot
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

</tab>
</tabs>

### 编写事件处理器

在 Spring Boot **可扫描到** 的范围内，创建任意类型，并将其标记为 Spring 的组件(`component`)：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component // 交给 Spring 管理
class MyEventHandlers {
    
    @Listener // 标记事件处理函数
    suspend fun handle1(event: Event) {
        // 处理事件...
    }
    
    @Listener // 标记事件处理函数
    @Filter("你好") // 快捷的注解过滤匹配条件
    suspend fun handle2(event: Event) {
        // 处理事件...
    }
    
    // 更多...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component // 交给 Spring 管理
public class MyEventHandlers {
    
    @Listener // 标记事件处理函数
    public void handle1(Event event) {
        // 处理事件...
    }
    
    @Listener // 标记事件处理函数
    @Filter("你好") // 快捷的注解过滤匹配条件
    public void handle2(Event event) {
        // 处理事件...
    }
    
    // 更多...
}
```

</tab>
</tabs>

<tip title="更多参考">
<list>
<li>
有关注解 API 的详情与描述，可参考 <a href="advanced-quantcat.md">量子猫</a>。
</li>
<li>
有关标准的事件类型都有哪些，可参考 <a href="basic-event.md">事件基础</a>。
</li>
</list>
</tip>

## 可配置项

starter 提供了一些可用的 spring 配置项。

> 对应的配置类型是 `love.forte.simbot.spring.common.application.SpringApplicationConfigurationProperties`。
>
> 配置属性的键均以 `simbot` 开头。

> 下面的实例中的配置项的值均为默认值。也就是它们都是可以省略的。

<tabs group="Spring Config">
<tab title="properties" group-key="properties">

以在 `application.properties` 文件中为例。

```
# simbot.application: 与 Application 相关的配置
simbot.application.application-launch-mode=NONE

# simbot.bots: 与 bot 配置相关的属性。
simbot.bots.auto-registration-failure-policy=ERROR
simbot.bots.auto-registration-mismatch-configurable-bot-manager-policy=ERROR_LOG
simbot.bots.auto-registration-resource-load-failure-policy=ERROR
simbot.bots.auto-start-bots=true
simbot.bots.auto-start-mode=ASYNC
simbot.bots.configuration-json-resources[0]=classpath:simbot-bots/*.bot.json

# simbot.components: 组件相关的配置信息。
simbot.components.auto-install-providers=true
simbot.components.auto-install-provider-configures=true

# simbot.plugins: 插件相关的配置信息。
simbot.plugins.auto-install-providers=true
simbot.plugins.auto-install-provider-configures=true
```

</tab>
<tab title="yaml" group-key="yaml">

以在 `application.yaml` 文件中为例。

```yaml
simbot:
  # simbot.application: 与 Application 相关的配置
  application:
    application-launch-mode: none
  # simbot.bots: 与 bot 配置相关的属性。
  bots:
    auto-registration-failure-policy: ERROR
    auto-registration-mismatch-configurable-bot-manager-policy: ERROR_LOG
    auto-registration-resource-load-failure-policy: ERROR
    auto-start-bots: true
    auto-start-mode: ASYNC
    configuration-json-resources:
      - 'classpath:simbot-bots/*.bot.json'
  # simbot.components: 组件相关的配置信息。
  components:
    auto-install-providers: true
    auto-install-provider-configures: true

  # simbot.plugins: 插件相关的配置信息。
  plugins:
    auto-install-providers: true
    auto-install-provider-configures: true
```

</tab>
</tabs>

<deflist>
<def title="simbot.application.application-launch-mode">

`ApplicationLaunchMode` 枚举, 保持 `Application` 活跃的策略。

默认为 `NONE`。

如果你的 Spring Boot 应用中没有可以保持程序活跃的内容
(最常见的例如 `spring-web`), 那么可以选择使用 `THREAD`。

<deflist type="medium">
<def title="NONE">
没有行为。
</def>
<def title="THREAD">
使用一个独立的非守护线程保持程序活跃。
</def>
</deflist>

</def>
<def title="simbot.bots.configuration-json-resources">

`Set<String>`, 需要加载的所有组件下它们对应的所有 `JSON` 格式 的 `Bot` 配置文件。

默认为 `classpath:simbot-bots/*.bot.json`, 即本项目中、资源目录下的 `resources/simbot-bots`
中的所有扩展名为 `.bot.json` 的配置文件。

</def>
<def title="simbot.bots.auto-registration-resource-load-failure-policy">

`BotConfigResourceLoadFailurePolicy` 枚举, 当加载用于注册bot的配置文件出现错误时的处理策略。

默认为 `ERROR`。

<deflist type="medium">
<def title="ERROR">当出现无法解析的资源文件时抛出异常来尝试中断整个处理流程。</def>
<def title="ERROR_LOG">当出现无法解析的资源文件时输出 <code>error</code> 级别的日志来尝试中断整个处理流程。</def>
<def title="WARN">当出现无法解析的资源文件时会输出 <code>warn</code> 日志。</def>
<def title="IGNORE">当出现无法解析的资源文件时仅会输出 <code>debug</code> 调试日志。</def>
</deflist>

</def>
<def title="simbot.bots.auto-registration-mismatch-configurable-bot-manager-policy">

`MismatchConfigurableBotManagerPolicy` 枚举, 当无法为某个 `SerializableBotConfiguration`
找到任何可供其注册的 `BotManager` 时的处理策略。

默认为 `ERROR`。

<deflist type="medium">
<def title="ERROR">
当无法为配置类找到任何可供注册的 <code>BotManager</code> 时抛出异常来尝试中断整个处理流程。
</def>
<def title="ERROR_LOG">
当无法为配置类找到任何可供注册的 <code>BotManager</code> 时输出 <code>error</code> 级别的日志来尝试中断整个处理流程。
</def>
<def title="WARN">
当无法为配置类找到任何可供注册的 <code>BotManager</code> 时会输出 <code>warn</code> 日志。
</def>
<def title="IGNORE">
当无法为配置类找到任何可供注册的 <code>BotManager</code> 时仅会输出 <code>debug</code> 调试日志。
</def>
</deflist>

</def>
<def title="simbot.bots.auto-start-bots">

`Boolean`, 是否在自动扫描的 `Bot` 注册后使用 `Bot.start` 启动它们。

默认为 `true`。

</def>
<def title="simbot.bots.auto-start-mode">

`BotAutoStartMode` 枚举, 当 `auto-start-bots` 为 `true` 时， 批量启动 `Bot` 的方式。

默认为 `ASYNC`。

<deflist type="medium">
<def title="SYNC">
依次同步启动。
</def>
<def title="ASYNC">

每个 `Bot` 独立地异步启动。
如果 `auto-registration-failure-policy` 为 `ERROR`,
则异步中任意 `Bot` 如果启动失败都会导致整体失败。

</def>
</deflist>

</def>
<def title="simbot.bots.auto-registration-failure-policy">

`BotRegistrationFailurePolicy`, 当自动扫描的bot注册或启动失败时的处理策略。
默认为 `ERROR`，直接异常以终止程序。

<deflist>
<def title="ERROR">

当bot注册或启动过程中出现异常或bot最终无法注册时都会抛出异常并终止程序。 是建议的默认选择。

</def>
<def title="ERROR_LOG">

当bot注册或启动过程中出现异常或bot最终无法注册时会输出带有异常信息的 `error` 日志。

</def>
<def title="WARN">

当bot注册或启动过程中出现异常或bot最终无法注册时会输出带有异常信息的 `warn` 日志。

</def>
<def title="IGNORE">

当bot注册或启动过程中出现异常或bot最终无法注册时仅会输出 `debug` 调试日志。

</def>
</deflist>

</def>
<def title="simbot.components.auto-install-providers">

是否通过 SPI 自动加载所有可寻得的组件。

默认为 `true`。

</def>
<def title="simbot.components.auto-install-provider-configures">

是否在加载 SPI providers 时候也同时加载它们的前置配置。 `auto-install-providers` 为 `true` 时有效。

默认为 `true`。

</def>
<def title="simbot.plugins.auto-install-providers">

是否通过 SPI 自动加载所有可寻得的插件。

</def>
<def title="simbot.plugins.auto-install-provider-configures">

是否在加载 SPI providers 时候也同时加载它们的前置配置。 `auto-install-providers` 为 `true` 时有效。

</def>
</deflist>

## 额外的定制化配置

starter 提供了大量的 `*Configurer` 类型来支持你对启动过程中的各个步骤添加**额外**的自定义配置。

<deflist>
<def title="SimbotApplicationConfigurationConfigurer">

针对 `Application` 配置属性的额外配置器。

</def>
<def title="SimbotDispatcherConfigurer">

针对 Spring 下的事件调度器 `EventDispatcher` 的额外配置器。

</def>
<def title="SimbotComponentInstaller">

`Component` 组件安装器。

</def>
<def title="SimbotPluginInstaller">

`Plugin` 插件安装器。

</def>
<def title="SimbotApplicationLauncherPreConfigurer">

构建 `Application` 过程中, 安插在配置、安装其他内容之前的额外配置器。

</def>
<def title="SimbotApplicationLauncherPostConfigurer">

构建 `Application` 过程中, 安插在配置、安装其他内容之后的额外配置器。

</def>
<def title="SimbotApplicationPreConfigurer">

`Application` 构建完成后, (在一定范围内) 安插在其他配置之前的额外配置器。

</def>
<def title="SimbotApplicationPostConfigurer">

`Application` 构建完成后, (在一定范围内) 安插在其他配置之后的额外配置器。

</def>
<def title="SimbotEventDispatcherPostConfigurer">

`Application` 构建完成后, 针对 `EventDispatcher` 的额外配置器。

</def>
<def title="SimbotEventListenerRegistrarPostConfigurer">

`Application` 构建完成后, 针对 `EventListenerRegistrar` 的额外配置器。

</def>
</deflist>


## 安装组件以及组件配置

你可以在上面的配置中看到，组件 `Component` 和 `Plugin` 默认情况下都是通过 SPI **自动加载** 的。

因此一般情况下, 你只需要前往 [**组件库**](components-intro.md) 选择你想要使用的组件, 或者选择某个/些你想要使用的第三方组件,
然后将它们添加到你的运行时环境中即可。

如果你想要添加更多定制化的配置或注册额外的组件、插件，
可参考实现上面提到的 `SimbotComponentInstaller`、`SimbotPluginInstaller`:

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component // 交给 Spring 管理
open class MyComponentInstaller: SimbotComponentInstaller {
    override fun install(installer: ComponentInstaller) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        installer.install(...)
        installer.install(...) { ... }
    }
}

@Component // 交给 Spring 管理
open class MyPluginInstaller: SimbotPluginInstaller {
    override fun install(installer: PluginInstaller) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        installer.install(...)
        installer.install(...) { ... }
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component // 交给 Spring 管理
public class MyComponentInstaller implements SimbotComponentInstaller {
    @Override
    public void install(@NotNull ComponentInstaller installer) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        installer.install(...);
        installer.install(..., config -> { ... });
    }
}

@Component // 交给 Spring 管理
public class MyPluginInstaller implements SimbotPluginInstaller {
    @Override
    public void install(@NotNull PluginInstaller installer) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        installer.install(...);
        installer.install(..., config -> { ... });
    }
}
```

</tab>
</tabs>

或者选择 `SimbotApplicationLauncherPreConfigurer` 和 `SimbotApplicationLauncherPostConfigurer`, 直接添加一个在 Application 构建阶段的配置。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component // 交给 Spring 管理
public class MyComponentInstaller implements SimbotApplicationLauncherPreConfigurer {
    @Override
    override fun configure(configurer: ApplicationFactoryConfigurer<SpringApplicationBuilder, SpringApplicationEventRegistrar, SpringEventDispatcherConfiguration>) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        configurer.install(...)
        installer.install(...) { ... }
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component // 交给 Spring 管理
public class MyComponentInstaller implements SimbotApplicationLauncherPreConfigurer {
    @Override
    public void configure(@NotNull ApplicationFactoryConfigurer<SpringApplicationBuilder, SpringApplicationEventRegistrar, SpringEventDispatcherConfiguration> configurer) {
        // 配置或安装，同一个工厂实例的多次配置会被合并
        configurer.install(...);
        installer.install(..., config -> { ... });
    }
}
```

</tab>
</tabs>

## 注册Bot

对于大多数组件而言，它们都支持通过 `*.bot.json` 配置文件在自动扫描、注册、启动。
bot的配置文件路径默认为 
<path>classpath:simbot-bots/*.bot.json</path> ，
也就是资源目录下的 <path>simbot-bots</path> 文件夹内所有以
`.bot.json` 作为扩展名的文件。

> 配置文件扫描的路径可以参考上面spring配置项的 `simbot.bots.configuration-json-resources`，
> 是否自动启动bot的配置可参考配置项 `simbot.bots.auto-start-bots`。

每一个不同的组件，它们的配置文件的内容是**不同**的。你需要参照你所使用的对应组件的文档说明来编写。
以 
<a href="component-onebot.md">OneBot组件</a>为例，它的配置文件的最简化是这样的：

```json
{
  "component": "simbot.onebot11",
  "authorization": {
    "botUniqueId": "123456",
    "apiServerHost": "http://localhost:3001",
    "eventServerHost":"ws://localhost:3001"
  }
}
```

各组件的手册内都会有有关 **Bot配置文件** 的说明章节，可前往对应的手册进行参考。


## 运行或打包

你可以参考 Spring Boot 针对不同构建工具的执行、打包或其他任何内容的详细说明手册：
- **Maven**: [Spring Boot Maven Plugin Documentation](https://docs.spring.io/spring-boot/docs/3.2.2/maven-plugin/reference/htmlsingle/)
- **Gradle**: [Spring Boot Gradle Plugin Reference Guide](https://docs.spring.io/spring-boot/docs/3.2.2/gradle-plugin/reference/htmlsingle/)

如果是借助 [start.spring.io][spring.start] 等工具生成的项目, 那么也可以参考项目目录中可能自带的 `HELP.md` 文档中的内容。

## 注意事项


## 常见问题

### 获取 Application、BotManager 或 Bot {id=get-bot}


在配合使用 Spring Boot 时，你可以直接通过bean注入的方式得到 `Application` 实例。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyComponent 
@Autowired // 其实注解可以省略，这里只是为了让'注入'行为比较显眼儿 
constructor(
    private val application: Application // 构造注入 Application
    
) {
    // ...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyComponent {
    private final Application application;
    
    @Autowired // 其实注解可以省略，这里只是为了让'注入'行为比较显眼儿 
    public MyComponent(Application application) { // 构造注入 Application
        this.application = application;
    }
    
    // ...
}
```

</tab>
</tabs>

你也可以基于此间接地获取 `BotManager`、`Bot` 等其他信息。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
@Component
class MyComponent(
    private val application: Application
) {
    // 假设这里是个定时任务
    // 或者其他什么跟事件没关系的地方
    fun runTask() {
        // 得到所有的BotManager并遍历
        for (botManager in application.botManagers) {
            // ...
            // 得到每一个BotManager中的所有已注册且未被关闭的Bot并遍历
            for (bot in botManager.all()) {
                // ...
            }
        }
    }
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
@Component
public class MyComponent {
    private final Application application;

    public MyComponent(Application application) {
        this.application = application;
    }

    // 假设这里是个定时任务
    // 或者其他什么跟事件没关系的地方
    public void runTask() {
        // 得到所有的BotManager并遍历
        for (var botManager : application.getBotManagers()) {
            // ...
            // 得到每一个BotManager中的所有已注册且未被关闭的Bot并遍历
            for (var it = botManager.all().iterator(); it.hasNext(); ) {
                var bot = it.next();
                // ...
            }
        }
    }
}
```

</tab>
</tabs>

这通常用于主动获取已注册的 Bot，然后用于主动发送消息等。

<warning title="注意！">

在 Spring 中，Bot的启动是**异步地**，因此在程序刚刚启动时并不能保证一定能够获取到对应的 Bot，例如获取时 Bot 仍处于启动中的状态。

你可以选择监听事件 `BotStartedEvent` (是否有这些事件取决于对应的组件是否实现了它，大部分官方组件库均有实现) 来监听并获得一个已经完成启动流程的bot，
或在获取时通过逻辑进行判断，如果bot没有找到（即尚未启动完成）则暂时跳过你的本次业务逻辑。

</warning>



[spring.start]: https://start.spring.io
