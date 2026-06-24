---
switcher-label: Java API 风格
---
# 消息发送

在 KOOK 组件中，主要有两种发送消息的方式。

<include from="component-kook-KookBot.md" element-id="need-help"/>


<list type="decimal">
<li>直接构建并使用 API 发送消息。这是最原始的消息发送方式。</li>
<li>

在使用 simbot 核心库时，配合使用 **消息元素 `Message.Element`** 发送消息。

</li>
</list>

本章将主要介绍第 **1** 种方式: 使用 API 发送消息。而与 **消息元素** 相关的内容可前往参考
<a href="component-kook-message-element.md"/>。

## 使用 API

KOOK API 中用于发送消息的 API 主要就是 **向子频道发送消息** 和 **向用户发送私聊消息**。
它们的 API 封装分别为：

- `SendChannelMessageApi`: [发送频道聊天消息](https://developer.kookapp.cn/doc/http/message#发送频道聊天消息)
- `SendDirectMessageApi`:  [发送私信聊天消息](https://developer.kookapp.cn/doc/http/direct-message#发送私信聊天消息)

<note>

它们可以在 <a href="component-kook-api-list.md" /> 中找到。

</note>

这两个 API 的用法非常接近，但仍有两个区别需要先记住：

<deflist>
<def title="SendChannelMessageApi">

面向频道消息。
支持 `quote`、`nonce`、`tempTargetId`，并在 `4.2.0` 起支持 `templateId`。

</def>
<def title="SendDirectMessageApi">

面向私聊消息。
可通过 `targetId` 或 `chatCode` 两条路径构建请求。

</def>
</deflist>

下面以 `SendChannelMessageApi` 为主说明。

### 仅在API模块使用  {id="only_api"}

当你不依赖其他模块，仅依赖 **_API 模块 `simbot-component-kook-api`_** 时，
你可以使用比较贴合原始的方式直接使用 API。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val client = HttpClient()
val authorization = "Bot xxxxx"

val api = SendChannelMessageApi.create(
    targetId = "1234567890",
    content = "Hello KOOK"
)

val result = api.requestData(client, authorization)
```

</tab>
<tab title="Java" group-key="Java">

```Java
var client = ApiRequests.createHttpClient();
var authorization = "Bot xxxxx";

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

ApiRequests.requestDataAsync(api, client, authorization)
        .thenAccept(result -> {
            // 发送成功
        });
```
{switcher-key="%ja%"}

```Java
var client = ApiRequests.createHttpClient();
var authorization = "Bot xxxxx";

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

var result = ApiRequests.requestDataBlocking(
        api,
        client,
        authorization
);
```
{switcher-key="%jb%"}

```Java
var client = ApiRequests.createHttpClient();
var authorization = "Bot xxxxx";

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

ApiRequests.requestDataReserve(api, client, authorization)
        .transform(SuspendReserves.mono())
        .block();
```
{switcher-key="%jr%"}

</tab>
</tabs>

### 在标准库中使用 {id="use_in_stdlib"}

当你依赖使用 **_标准库模块 `simbot-component-kook-stdlib`_** 时，
标准库提供的 `Bot` 中基本已经包含了请求 API 所需要的基本信息，
因此其会提供一些扩展/辅助方法来简化你的请求逻辑。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val bot: Bot = ...

val api = SendChannelMessageApi.create(
    targetId = "1234567890",
    content = "Hello KOOK"
)

val result = api.requestDataBy(bot)
```

</tab>
<tab title="Java" group-key="Java">

```Java
Bot bot = ...;

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

BotRequests.requestDataByAsync(api, bot)
        .thenAccept(result -> {
            // 发送成功
        });
```
{switcher-key="%ja%"}

```Java
Bot bot = ...;

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

var result = BotRequests.requestDataByBlocking(api, bot);
```
{switcher-key="%jb%"}

```Java
Bot bot = ...;

var api = SendChannelMessageApi.create(
        null,
        "1234567890",
        "Hello KOOK"
);

BotRequests.requestDataByReserve(api, bot)
        .transform(SuspendReserves.mono())
        .block();
```
{switcher-key="%jr%"}

</tab>
</tabs>

### 在组件库配合simbot4核心库时使用

<warning>

虽然在使用组件库配合simbot4核心库时，我们更建议你使用 **消息元素** (
可参考
<a href="component-kook-message-element.md" />
)，而不是直接使用原始的API类型发送消息，但凡事都有例外。

**如果你明确确定此时必须要使用原始的API请求**，继续阅读即可。

</warning>

在 `simbot-component-kook-core` 中有两种常见做法：

<list>
<li>

继续使用原始 API：`KookBot.requestData(api)`、`api.requestDataBy(bot)`

</li>
<li>

直接使用对象上的发送能力：`KookChatCapableChannel.send(...)`、`KookUserChat.send(...)`

</li>
</list>

后者通常更贴近 simbot 的使用方式。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
suspend fun send(channel: KookChatCapableChannel) {
    channel.send("hello from kook core")
    channel.send("reply message", quote = null, tempTargetId = null)
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
KookChatCapableChannel channel = ...;

channel.sendAsync("hello from kook core")
        .thenAccept(receipt -> { });
```
{switcher-key="%ja%"}

```Java
KookChatCapableChannel channel = ...;

var receipt = channel.sendBlocking("hello from kook core");
```
{switcher-key="%jb%"}

```Java
KookChatCapableChannel channel = ...;

channel.sendReserve("hello from kook core")
        .transform(SuspendReserves.mono())
        .subscribe(receipt -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>

如果你只是需要把 `KookBot` 当作 stdlib 的 Bot 使用，也可以直接拿到 `sourceBot`：

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val kookBot: KookBot = ...
val bot = kookBot.sourceBot // 得到标准库的 Bot
```

</tab>
<tab title="Java" group-key="Java">

```Java
KookBot kookBot = ...;
Bot bot = kookBot.getSourceBot(); // 得到标准库的 Bot
```

</tab>
</tabs>

<tip>

如果你的目标只是“正常发一条消息”，
更推荐优先使用 simbot 的消息元素与 `send` / `reply` 能力；
直接操作原始 API 更适合：

- 需要用到平台专属字段
- 需要发送模板消息、卡片消息等原始结构
- 正在编写更底层封装

</tip>
