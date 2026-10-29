<show-structure for="chapter,procedure" depth="3"/>

# 消息元素与消息链

在 simbot 中, **消息**是一个重要的类型之一。

## 消息 Message

`Message` 即代表一个消息, 它可能是 `Message.Element` 或 `Messages`。

## 消息元素 Message.Element

是一个消息链的最小单元, 代表了一个有具体含义的消息。

### 标准消息元素 StandardMessage

核心库中定义了一些常见的、泛用型较高的消息类型, 它们都继承自 `StandardMessage` 接口。
这其中的类型有一些可能会在部分场景下被特殊处理, 例如 `PlainText`。

<deflist>
<def title="PlainText">

接口类型, 纯文本消息。代表一段只存在文本的消息。
一般不需要自己实现, 可以使用类型 `Text`。

<deflist type="medium">
<def title="text">

纯文本消息的文本内容。

</def>
</deflist>

</def>

<def title="Text">

`PlainText` 的标准实现类型。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val text = "text".toText()
val emptyText = Text()
val text1 = Text { "text" }
```

</tab>
<tab title="Java" group-key="Java">

```Java
val text = Text.of("text");
```

</tab>
</tabs>

</def>
<def title="MentionMessage">

代表一个描述“提及”的消息。常见表现形式即为 `At`。

<deflist>
<def title="At">

一个 “艾特(`@`)” 消息。

<deflist type="medium">
<def title="target">

被提及的目标的ID

</def>
<def title="type">

提及的形式, 如果有特殊形式, 则由解析它的实现者来解释含义, 
例如QQ频道中除了提及用户, 还能提及子频道, 那么它就会解析 `type="channel"` 的类型。
默认为 `user`。

</def>
</deflist>

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val at = At(1.ID)
```

</tab>
<tab title="Java" group-key="Java">

```Java
var at = At.of(Identifies.of(1));
```

</tab>
</tabs>


</def>
<def title="AtAll">

一个“提及所有”的消息。是 `object` 单例类型。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val atAll = AtAll
```

</tab>
<tab title="Java" group-key="Java">

```Java
var atAll = AtAll.INSTANCE;
```

</tab>
</tabs>

</def>
</deflist>

</def>
<def title="Image">

接口类型, 一个代表图片消息元素类型。
图片消息可能被分为 **离线图片 `OfflineImage`** 和 **远端图片 `RemoteImage`**。

<deflist>
<def title="OfflineImage">

接口类型, 实现 `Image`, 代表一个离线（本地）图片消息元素类型。通常是用来发送的消息类型。
`OfflineImage` 的实现类**不保证**可以序列化。

<deflist>
<def title="基于 ByteArray">

一个基于 `ByteArray` 的 `OfflineImage`, 是多平台实现。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
bytes: ByteArray = ...
val image = bytes.toOfflineImage();
```

</tab>
<tab title="Java" group-key="Java">

```Java
byte[] bytes = ...;
var image = OfflineImage.ofBytes(bytes);
```

</tab>
</tabs>


</def>
<def title="基于 Resource">

一个基于 `Resource` 的 `OfflineImage`, 是多平台实现。
在 JVM 中, 可以通过 `Resources` 提供的工厂函数来基于不同的源构建 `Resource`, 
例如使用 `File` 或 `Path`。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
resource: Resource = ...
val image = resource.toOfflineImage();
```

</tab>
<tab title="Java" group-key="Java">

```Java
Resource resource = ...;
var image = OfflineImage.ofResource(resource);
```

</tab>
</tabs>

当通过 `Resource` 构建 `OfflineImage` 时, 根据 `Resource` 的类型可能会得到不同的结果。
例如在 JVM 平台下, 如果提供了一个 `PathResource`, 
则会实际得到一个直接基于 `Path` 的 `OfflineImage` 实现。

</def>
</deflist>

</def>
<def title="RemoteImage">

接口类型, 一个远程图片消息元素类型。`RemoteImage` 一般出现在接收到的消息事件里, 
由提供事件的实现者（例如某个组件下的插件）进行实现。
一般情况下不需要普通开发者实现或直接构建 `RemoteImage`。

</def>
<def title="RemoteUrlAwareImage">

接口类型, 继承 `RemoteImage`, 代表这个远程图片可以**获得其链接**。

</def>
</deflist>

</def>
<def title="EmoticonMessage">

接口类型, 表示某种表情符号的消息元素类型。

<deflist>
<def title="Emoji">

一个 `emoji` 表情。`Emoji` 主要服务于那些只能提供指定范围内 `emoji` 表情的场景, 
例如针对某个消息的 `reaction`。

</def>
<def title="Face">

一个表情。一般代表平台提供的自带系统表情。

</def>
</deflist>

</def>

<def title="MessageReference">

> 添加自 `v4.5.0` 。

一个用于表示“消息引用”的元素。
默认只有一个抽象属性 `id` 来表示引用目标的消息ID。

<tip>

当某个平台存在 _消息引用_ 的概念，
但是无法使用 `MessageReference` 进行描述（例如它通过多重ID确定唯一身份，而不是唯一ID）， 
则需要由平台实现者自行实现，无法使用 `MessageReference`，也无法使用 `MessageContent.reference`。

</tip>

<deflist>
<def title="MessageIdReference">

一个仅实现 `id` 的 `MessageReference` 简单实现。

</def>
</deflist>

</def>
</deflist>

### 扩展消息元素

除了标准的消息元素实现以外, 不同的组件、插件, 都有可能会提供更多的元素扩展, 
比如QQ频道组件中提供与 `Ark` 消息相关的元素实现。
这些额外的消息元素实现的序列化信息会被注册在 `Component.serializersModule` 中, 
并在安装时被一并加载到 `Application` 里。

## 消息链 Messages

一个 消息链。 消息链 `Messages` 本质上就是一组 `Message.Element` 集合。
消息链是**不可变的**。它通过 `plus` 与其他消息元素或消息链重新组合为新的消息链。

### 创建 `Messages` {id="create_messages"}

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
// 获取空实例
val empty = emptyMessages()
// 通过可变参数构建
val messages = messagesOf(At(1.ID), At(2.ID))
// 通过 Iterable 构建
val messagesFromList = listOf(At(1.ID), At(2.ID)).toMessages()

// 拼接新的元素
// 组装两个任意的 Message
val newMessages1 = At(1.ID) + At(2.ID)
// 通过 Messages.plus 组装
val newMessages2 = messages + At(1.ID)
```

</tab>
<tab title="Java" group-key="Java">

```Java
// 获取空实例
var empty = Messages.empty();
// 通过可变参数构建
var messages = Messages.of(At.of(Identifies.of(1)), At.of(Identifies.of(2)));
// 通过 Iterable 构建
var messagesFromList = Messages.of(List.of(At.of(Identifies.of(1)), At.of(Identifies.of(2))));

// 拼接新的元素
// 拼接 Message.Element, 得到新的消息链
var newMessages1 = messages.plus(At.of(Identifies.of(1)));
// 拼接 Messages, 得到新的消息链
var newMessages2 = messages.plus(messagesFromList);
```

</tab>
</tabs>


### 序列化

simbot 中所有的序列化相关实现均基于 `Kotlinx serialization`, `Messages` 也不例外。
`Messages` 会被作为一个 `List<Message.Element>` 基于多态进行序列化, 因此当需要进行序列化的时候, 
请确保消息链中的所有消息元素均支持序列化。

你可以：
- 通过 `Messages.standardSerializersModule` 得到所有标准消息元素的多态序列化信息。
- 通过 `Application.components.serializersModule` 得到已经注册的所有组件的序列化信息的聚合产物, 其中理应包含由组件定义的额外扩展的信息。
- 通过 `Messages.serializer` 得到针对 `Messages` 的序列化器。

以 Json 序列化为例：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val messages: Messages = ...
val application: Application = ...

val json = Json {
    // 合并整体的序列化信息
    serializersModule = SerializersModule {
        include(Messages.standardSerializersModule)
        include(application.components.serializersModule)
    }
    // 其他配置...
}

// 序列化
val jsonStr = json.encodeToString(Messages.serializer, messages)
// 反序列化
val messagesDecoded = json.decodeFromString(Messages.serializer, jsonStr)
```

</tab>
<tab title="Java" group-key="Java">

```Java
var json = JsonKt.Json(Json.Default, jsonBuilder -> {
    // 合并整体的序列化信息
    var modules = SerializersModuleBuildersKt.SerializersModule(moduleBuilder -> {
        moduleBuilder.include(Messages.standardSerializersModule());
        moduleBuilder.include(application.getComponents().getSerializersModule());
        return Unit.INSTANCE;
    });
    jsonBuilder.setSerializersModule(modules);
    // 其他配置...

    return Unit.INSTANCE;
});

// 序列化
var jsonStr = json.encodeToString(Messages.serializer(), messages);
// 反序列化
var messagesDecoded = json.decodeFromString(Messages.serializer(), jsonStr);
```

</tab>
</tabs>

<warning title="敏感信息">

消息元素中有可能会存在一些敏感信息，比如token等，这取决于组件实现。

因此请尽可能避免将序列化结果不做处理或加密就暴露在公开环境，
以免隐私或敏感信息泄露造成不可预知的严重后果。

</warning>

## 事件消息内容 MessageContent

`MessageContent` 是从 `MessageEvent` 事件中接收到的消息内容类型。

你可以在其中得到一些与消息相关的信息。


<deflist>
<def title="id">

这个消息的ID。如果没有什么可以作为ID的, 那么可能是一个随机ID。

</def>
<def title="messages">
    
`Messages` 类型, 此事件中解析出来的消息链。

</def>
<def title="plainText">

从接收到的消息中提取出的纯文本内容（一般来讲是 `PlainText` 类型的消息元素）拼接在一起的结果。

</def>
<def title="delete(...)">

删除这个消息。“删除”也可以理解为撤回, 如果平台某种类型的消息内容不支持被删除,
则可能会抛出 `UnsupportedOperationException`。

</def>
<def title="reference()">

<note>添加自 <code>v4.5.0</code> 。</note>

尝试获取一个消息引用 `MessageReference`。

`reference()` 在明确不支持或直接通过 `messages` 寻找获取时，
不会发生挂起。否则当需要通过网络查询结果时会产生挂起。

`reference` 所得结果**不一定**是 `messages` 中的元素。
如上所述，如果需要通过网络查询才能得到结果，则 `reference()` 
的结果不会包含在 `messages` 中。

- 如果实现者尚未针对性地实现此API，则默认逻辑为：
从 `messages` 中寻找第一个类型为 `MessageReference` 的元素。
- 如果实现者的所属平台不存在、不支持 _消息引用_ 的概念，则可能始终得到 `null`。
- 如果实现者的所属平台有明确的 _消息引用_ 概念，但是无法通过 `MessageReference` 这个类型进行表述，
则使用 `reference` 时应当抛出信息明确的 `UnsupportedOperationException` 异常。

</def>
<def title="referenceMessage()">

<note>添加自 <code>v4.6.0</code> 。</note>

根据 **消息引用** (或具体实现内部的某种真实引用) 查询此引用的源消息。

- 如果实现者尚未实现此功能，或 `reference` 返回 `null`,
则 `referenceMessage` 的结果为 `null`。
- 如果实现的对应平台明确存在**引用**的概念、但由于各种原因无法查询引用源消息时，
`referenceMessage` 将会抛出 `UnsupportedOperationException`。
- 否则，将根据具体地引用信息查询并得到其对应地 `MessageContent`。
与 `reference` 不同，`referenceMessage` 大概率会产生网络请求和挂起行为，
但具体行为还是以具体实现为准。

</def>


</deflist>



## 消息的发送

消息的发送功能主要定义在 `SendSupport` 和 `ReplySupport` 这两个接口中, 命名为 `send` 或 `reply`。
它们含义不同, 主要面向实现的目标也不同, 但是核心的功能是相同的：发送消息。

`ReplySupport` 已经在 [事件-消息事件](basic-event.md#d-message-event) 中出现过了, 
那么这里便使用 `SendSupport` 做介绍。

`send` 支持使用字符串文本、`Messages` 和 `MessageContent` 这三个类型作为发的消息内容。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
sendSupport.send("text")
sendSupport.send(messages)
sendSupport.send(messageContent)
```

</tab>
<tab title="Java" group-key="Java">

```Java
sendSupport.sendAsync("text");
sendSupport.sendAsync(messages);
sendSupport.sendAsync(messageContent);
```
{switcher-key="%ja%"}
```Java
sendSupport.sendBlocking("text");
sendSupport.sendBlocking(messages);
sendSupport.sendBlocking(messageContent);
```
{switcher-key="%jb%"}

</tab>
</tabs>


### 发送与回复选项 {id="send-options"}

<secondary-label ref="since-5.0"/>

`SendSupport.send(...)` 与 `ReplySupport.reply(...)` 新增带可变参数选项的重载，
分别接收 `SendOption` 和 `ReplyOption`。字符串、`Message` 与 `MessageContent` 均支持这些重载。

```Kotlin
val sendOptions: Array<out SendOption> = ...
sendSupport.send("text", *sendOptions)

val replyOptions: Array<out ReplyOption> = ...
replySupport.reply("text", *replyOptions)
```

具体选项由组件或其他实现方扩展。
实现方遇到已知但无法满足的选项时，应抛出明确的异常；未知选项通常忽略。
标准接口的默认实现会委托到不带选项的原有方法，因此选项是否生效仍取决于具体实现。

### 发送回执 MessageReceipt

当一个消息发送成功没有出错时, 便会返回一个回执 `MessageReceipt`。
`MessageReceipt` 继承了 `DeleteSupport`, 因此也可以使用 `delete(...)` 来进行“删除”行为, 
同样的, 如果平台的实现不支持, 也可能会抛出 `UnsupportedOperationException`。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val receipt = sendSupport.send(...)
receipt.delete() // 试着删除它
```

</tab>
<tab title="Java" group-key="Java">

```Java
sendSupport.sendAsync(...)
        // 试着删除它...
        .thenCompose(DeleteSupport::deleteAsync);

```
{switcher-key="%ja%"}
```Java
var receipt = sendSupport.sendBlocking(...);
receipt.deleteBlocking(); // 试着删除它
```
{switcher-key="%jb%"}

</tab>
</tabs>

### 标准回执类型 StandardMessageReceipt

`MessageReceipt` 有一个特殊类型实现：`StandardMessageReceipt`, 它定义了两个子类型：

- `SingleMessageReceipt`
- `AggregatedMessageReceipt`

顾名思义, 它们分别代表为一个独立回执和一个聚合回执。其中, 聚合回执是对多个独立回执的聚合。

为什么要分这两种类型？因为在平台实现中, 你使用一次 `send` 或 `reply` 发送消息, 
不一定真的只发送了一条消息。

举个例子, 你创建了一个包含3张图片消息的消息链并发送,  但是平台的底层API只支持一次发一个图片, 
那么这时候组件的实现中就会发送三条消息, 并得到三个实际上的发送结果。而将这三个结果“聚合”为一个结果返回给调用处, 
便是 `StandardMessageReceipt` 中这两个类型的主要作用。
