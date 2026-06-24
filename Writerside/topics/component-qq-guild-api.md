---
switcher-label: Java API 风格
---

# API

## API模块

所有对 QQ 开放平台 API 的原始封装都在
API 模块 `simbot-component-qq-guild-api` 中。

这一层主要包含：

<list>
<li><control>love.forte.simbot.qguild.api</control>

各类 `QQGuildApi<T>` 实现，以及 Java 侧 `ApiRequests` 辅助函数。
</li>
<li><control>love.forte.simbot.qguild.model</control>

与开放平台响应结构对应的数据模型，例如 `Message`、`Guild` 等。
</li>
<li><control>love.forte.simbot.qguild.event</control>

网关事件体、`opcode`、`intent` 与分发结构。
</li>
<li><control>love.forte.simbot.qguild.message</control>

消息模型、内嵌格式编码器与若干构建辅助类型。
</li>
</list>

## API定义

可前往 <a href="component-qq-guild-api-list.md">API 类型总览</a>
或 <a href="%api-doc%">API 文档</a> 查看所有 API 实现。

消息发送相关的几个常用 API 需要特别区分：

<deflist>
<def title="MessageSendApi">

频道子频道发消息。

</def>
<def title="DmsSendApi">

频道私聊 `DMS` 发消息。

</def>
<def title="GroupMessageSendApi / UserMessageSendApi">

QQ群与 `C2C` 单聊发消息。

</def>
</deflist>

## 使用API

在 API 模块、stdlib 模块和核心组件模块中都可以使用 API。

所谓“使用 API”，就是提供所需参数，向 API 发起请求，并拿到预期的结果或错误。

### API模块中使用

在 API 模块中直接使用 API，通常需要这些参数：

- `HttpClient`: 用于发起请求的 Ktor `HttpClient` 对象。
- `token`: QQ频道API中用于鉴权的客户端 `access_token`。
   它通过API定期刷新，可在 `Bot` 中获取。
   如果API还支持旧格式，那么可以在[官方文档](https://bot.q.qq.com/wiki/develop/api/)中找到，比如 `Bot 100000.aaaabbbbccccdddd`。
- `server`: _可选_ 。QQ频道API有正式频道和沙箱频道之分，可通过此参数选择不同的服务器地址。在一些特殊需求下，也可以通过此方式自定义一个第三方服务器地址。
- `appId`: _可选_ 。如果提供，会将其添加到请求头 `X-Union-Appid` 中。这是新的 `access_token` 访问方式所要求的。

对 API 的请求在 Kotlin 中以挂起扩展函数提供；
在 Java 中可通过 `ApiRequests` 使用阻塞、异步与 `SuspendReserve` 三种桥接形式。

API 层常用入口有：

- `request`: 直接返回原始的 `HttpResponse` 结果，几乎不做校验
- `requestText`: 返回请求到的原始JSON字符串，会校验HTTP响应状态是否为 `2xx`。
- `requestData`: 会解析响应值为对应的实体对象后返回。会校验是否成功。

以 `GetGuildApi`（获取频道服务器详情）为例：

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
// 准备必要信息
val token = "..."
val client = HttpClient()
// 准备API对象
val api = GetGuildApi.create("频道ID")
// 发起请求
val response = api.request(client, token)
val text = api.requestText(client, token)
val data = api.requestData(client, token)
```

</tab>
<tab title="Java" group-key="Java">

```Java
// 准备必要信息
var token = "...";
var client = ApiRequests.newHttpClient();
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
ApiRequests.requestAsync(api, client, token)
                .thenAccept(response -> { ... });

ApiRequests.requestTextAsync(api, client, token)
                .thenAccept(text -> { ... });

ApiRequests.requestDataAsync(api, client, token)
        .thenAccept(data -> { ... });
```
{switcher-key="%ja%"}

```Java
var token = "...";
var client = ApiRequests.newHttpClient();
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
var response = ApiRequests.requestBlocking(api, client, token);
var rawText = ApiRequests.requestTextBlocking(api, client, token);
var data = ApiRequests.requestDataBlocking(api, client, token);
```
{switcher-key="%jb%"}


```Java
// 准备必要信息
var token = "...";
var client = ApiRequests.newHttpClient();
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
ApiRequests.requestReserve(api, client, token)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(response -> { ... });

ApiRequests.requestTextReserve(api, client, token)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(text -> { ... });

ApiRequests.requestDataReserve(api, client, token)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(data -> { ... });
```
{switcher-key="%jr%"}

</tab>
</tabs>

### Stdlib模块中使用

在 `simbot-component-qq-guild-stdlib` 中，一个 `love.forte.simbot.qguild.stdlib.Bot`
已经包含了客户端、鉴权与服务器地址等信息，
因此你可以使用 `Bot.requestXxx(api)` 或 `api.requestXxxBy(bot)` 来简化你的请求
(Java中可以使用 `BotRequests` 提供的静态方法)。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
// 准备必要信息
val bot: Bot = ...
// 准备API对象
val api = GetGuildApi.create("频道ID")
// 发起请求
// bot为主
val response = bot.request(api)
val text = bot.requestText(api)
val data = bot.requestData(api)
// api为主
val response1 = api.requestBy(bot)
val text1 = api.requestTextBy(bot)
val data1 = api.requestDataBy(bot)

```

</tab>
<tab title="Java" group-key="Java">

```Java
// 准备必要信息
Bot bot = ...
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
BotRequests.requestAsync(bot, api)
                .thenAccept(response -> { ... });

BotRequests.requestTextAsync(bot, api)
                .thenAccept(text -> { ... });

BotRequests.requestDataAsync(bot, api)
        .thenAccept(data -> { ... });
```
{switcher-key="%ja%"}

```Java
// 准备必要信息
Bot bot = ...
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
var response = BotRequests.requestBlocking(bot, api);
var text = BotRequests.requestTextBlocking(bot, api);
var data = BotRequests.requestDataBlocking(bot, api);
```
{switcher-key="%jb%"}


```Java
// 准备必要信息
Bot bot = ...
// 准备API对象
final var api = GetGuildApi.create("频道ID");
// 发起请求
BotRequests.requestReserve(bot, api)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(response -> { ... });

BotRequests.requestTextReserve(bot, api)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(text -> { ... });

BotRequests.requestDataReserve(bot, api)
        // 假设转化为 reactor 的 `Mono`
        .transform(SuspendReserves.mono())
        .subscribe(data -> { ... });
```
{switcher-key="%jr%"}

</tab>
</tabs>


### 核心模块中使用

核心模块中的 `QGBot` 提供了 `source`，
它对应 stdlib 层的 `Bot`。

- 如果你想继续走 stdlib 风格，使用 `bot.source`
- 如果你正在发送消息，通常更推荐优先参考 [](component-qq-guild-messages.md) 与各对象上的 `send(...)`

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val bot: QGBot = ...
val sourceBot = bot.source
// 使用 sourceBot
```

</tab>
<tab title="Java" group-key="Java">

```Java
QGBot bot = ...
var sourceBot = bot.getSource();
// 使用 sourceBot
```

</tab>
</tabs>

## 日志

开启名称前缀为 `love.forte.simbot.qguild.api` 的 DEBUG 级别日志，
可以看到 API 请求过程中的部分详细信息，例如出入参。

在 JVM 中，日志系统委托给 `SLF4J2 API`；在 native 平台中，可通过 `LoggerFactory.defaultLoggerLevel` 修改全局默认日志级别。

JVM 中默认会为日志中的部分片段染色。
如果需要关闭，添加 JVM 参数：

```
-Dsimbot.qguild.api.logger.color.enable=false
```
