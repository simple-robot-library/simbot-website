# 实现消息 API
<primary-label ref="doc-wip" />

标准API中定义了诸多与消息相关的API与类型。
它们由组件进行实现或扩展，来达成实现功能的目的。

组件实现消息 API 时，通常会同时考虑这些内容：

- 为组件定义自己的消息元素根类型
- 为接收消息定义组件自己的 `MessageContent`
- 在可发消息的对象上实现 `send(...)`
- 为发送结果定义组件自己的 `MessageReceipt`

## 消息元素

组件通常会在标准 `Message.Element` 之上再细分一层自己的根接口。

常见做法是按组件划分自己的消息元素根类型，例如：

- `QGMessageElement`：QQ Guild 组件消息元素根类型
- `KookMessageElement`：KOOK 组件消息元素根类型
- `OneBotMessageElement`：OneBot11 组件消息元素根类型

这么做的好处是：

- 可以表达“只在此组件有意义”的消息元素
- 可以在组件内部做定向解析
- 可以把接收侧与发送侧的特殊消息独立建模

## 消息事件内容

接收侧通常不会直接把原始平台消息裸露给业务层，
而是包装成组件自己的消息内容类型。

常见内容类型：

<deflist>
<def title="QQ Guild">

`QGMessageContent`

</def>
<def title="KOOK">

`KookReceiveMessageContent`、`KookChannelMessageDetailsContent`

</def>
<def title="OneBot11">

`OneBotMessageContent`

</def>
</deflist>

这一层通常要解决两件事：

- 如何把平台原始消息映射为 simbot 标准消息链
- 如何保留组件特有的附加信息，例如引用、附件、平台原始体等

这类“像属性一样的挂起 API”在 JVM 上通常会以 `@STP` 生成 getter 风格桥接，
因此 Java 侧更常看到：

- `getContent()`
- `getContentAsync()`
- `getContentReserve()`

## 消息发送

发送能力通常实现在“可交流对象”本身上，例如频道、群、好友、成员、私聊会话等。

常见发送入口包括：

- `QGTextChannel.send(...)`、`QGFriend.send(...)`、`QGBot.sendTo(...)`
- `KookChatCapableChannel.send(...)`、`KookUserChat.send(...)`
- `OneBotFriend.send(...)`、`OneBotGroup.send(...)`、`OneBotMember.send(...)`

如果这些 API 是挂起函数，通常还会通过 `@ST` / `@STP`
自动生成 Java 友好的三桥接形式：

- `xxxAsync(...)`
- `xxxBlocking(...)`
- `xxxReserve(...)`

因此，实现组件消息发送 API 时，建议优先从“挂起主接口 + 自动桥接”这个模式出发。

最小实现一般就是“接口 + 一个发送入口”。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
interface MyChat {
    @ST
    suspend fun send(message: Message): MyMessageReceipt
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
MyChat chat = ...;

chat.sendAsync(message)
        .thenAccept(receipt -> { });
```
{switcher-key="%ja%"}

```Java
MyChat chat = ...;

var receipt = chat.sendBlocking(message);
```
{switcher-key="%jb%"}

```Java
MyChat chat = ...;

chat.sendReserve(message)
        .transform(SuspendReserves.mono())
        .subscribe(receipt -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>

## 消息回执

大多数组件都会给发送结果定义自己的回执类型，
以承载平台特有字段。

常见回执类型包括：

- `QGMessageReceipt`
- `KookMessageReceipt`
- `KookMessageCreatedReceipt`
- `OneBotMessageReceipt`

设计回执时可以优先考虑：

- 是否需要保留平台返回的消息 ID
- 是否有审核、异步确认或聚合发送等额外状态
- 是否要兼容标准 `MessageReceipt`

如果只需要最基础的回执，通常保留一个 ID 就够了：

```Kotlin
class MyMessageReceipt(
    val messageId: ID,
) : MessageReceipt {
    override suspend fun delete(vararg options: DeleteOption) {
        throw UnsupportedOperationException("delete is not supported")
    }
}
```
