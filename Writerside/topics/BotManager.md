---
switcher-label: JavaAPI风格
---

# Bot管理器 BotManager

Bot管理器 是 `simbot-api` 对外公开的接口类型 `BotManager`, 
它是
<tooltip term="插件"><control>插件</control></tooltip>
的一个特殊子类型。

## 安装、配置与获取

`BotManager` 被定义为用于处理与 `Bot` 相关行为的 `Plugin` 类型, 
但它也仍然是 `Plugin` 的子类型, 因此对于一个 `BotManager` 
的安装、配置与获取方式都与 `Plugin` 相同。
可参考章节
<a href="plugin.md" />
。

## 获取 (特别)

除了直接使用 `application.plugins` 获取以外, 作为一种特别的类型, 
`Application` 还提供了另外一个专门针对 `BotManager` 的获取方式：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val app = launchSimpleApplication {
    install(FooBotManager)
}

app.botManagers.forEach { botManager ->
    // 所有注册了的 BotManager...
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
Applications.launchApplicationAsync(Simple.INSTANCE, configurer -> {
    configurer.install(FooBotManager.Factory);
}).asFuture().thenAccept(app -> {
    for (var botManager : app.getBotManagers()) {
        // 所有注册了的 BotManager...
    }
});
```
{switcher-key="%ja%"}

```Java
var app = Applications.launchApplicationBlocking(Simple.INSTANCE, configurer -> {
    configurer.install(FooBotManager.Factory);
});

for (var botManager : app.getBotManagers()) {
    // 所有注册了的 BotManager...
}
```
{switcher-key="%jb%"}

</tab>
</tabs>

## 注册 Bot (通用) {id="register-bot-common"}

`BotManager` 实现了接口 `AutoConfigurableBotPlugin`, 也就是定义如何 **注册 Bot** 的接口。先看看这个接口的基本定义：

```Kotlin
public interface AutoConfigurableBotPlugin : BotPlugin {
    /**
     * 检测提供的 [configuration] 是否能够应用于 [register] 中。
     */
    public fun configurable(configuration: SerializableBotConfiguration): Boolean

    /**
     * 使用一个 [configuration] 注册并得到 [Bot]。
     */
    public fun register(configuration: SerializableBotConfiguration): Bot
}
```

可以看到, 想要注册一个 `Bot`, 我们首先需要了解这个 `BotManager` 是否实现了它所需要的 `SerializableBotConfiguration` 类型, 
然后再根据此类型提供并注册。

**假设** 一个 `FooBotManager` 提供了一个 `FooBotConfiguration`, 那么我们便可以通过 `register` 注册并得到一个尚未启动的 `Bot`。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val config = FooBotConfiguration()
// 配置...
val bot = botManager.register(config)
```

</tab>
<tab title="Java" group-key="Java">

```Java
var config = new FooBotConfiguration();
// 配置...
var bot = botManager.register(config);
```

</tab>
</tabs>

## 注册 Bot (特别) {id="register-bot-spec"}

不知道你有没有注意到上面我提到的这个接口 `AutoConfigurableBotPlugin` 的名字: **AutoConfigurable** 。
实际上这个接口中定义的这两个方法是设计用于**自动注册** Bot 的, 例如在 Spring Boot 中批量扫描配置文件并注册的。

那么有没有更适合在代码中注册的方式呢？

有, 但是**难以标准化**。

我们建议每一个 `BotManager` 的实现类型都应提供**专属于**各自的 Bot 注册方式。以 **QQ频道组件** 为例, 
QQ频道中的 bot 主要需要三个参数：`appid`、`secret`、`token`, 这都是注册一个 `Bot` 的必要信息。
QQ频道组件中的 `QQGuildBotManager` 便提供了针对 **QQ频道 Bot** 的专属注册API：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val bot = qqGuildBotManager.register("appid", "secret", "token")
```

</tab>
<tab title="Java" group-key="Java">

```Java
var bot = qqGuildBotManager.register("appid", "secret", "token");
```

</tab>
</tabs>

也可选的进行一些额外配置：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val bot = qqGuildBotManager.register("appid", "secret", "token") {
                // 一些非必须的配置...
        }
```

</tab>
<tab title="Java" group-key="Java">

```Java
var bot = qqGuildBotManager.register("appid", "secret", "token", conf -> {
                // 一些非必须的配置...
        });
```

</tab>
</tabs>

因此, 对于专属的 Bot 注册 API, 它们都在各自的类型中定义, 你只需要拿到你所需要的对应类型（例如 `QQGuildBotManager`）
后再对其进行操作即可。

<note>

针对 `Bot` 的其他描述可前往 
<a href="basic-bot.md" />
查看。

</note>