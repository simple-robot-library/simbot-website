# 群聊 QGGroup

<note>

自 `4.0.0-beta6` 开始支持。

</note>

`QGGroup` 是 QQ 群聊对象，实现 simbot 标准库中的 `ChatGroup`。
它通常来自 QQ 群聊消息事件，例如：

<deflist>
<def title="QGGroupAtMessageCreateEvent">

群聊中用户 `@` 机器人时触发的群消息事件，对应 API 模块事件 `GroupAtMessageCreate`。

</def>
<def title="QGGroupMessageCreateEvent">

群聊全量消息事件，对应 API 模块事件 `GroupMessageCreate`。
自 `4.3.0` 开始支持。

</def>
</deflist>

这两个事件都实现了标准库的 `ChatGroupMessageEvent`。
如果只关心“QQ群聊消息”这一抽象，可以监听 `ChatGroupMessageEvent`；
如果需要区分是否为全量消息，可以监听组件专属类型 `QGGroupAtMessageCreateEvent`
或 `QGGroupMessageCreateEvent`。

## 事件订阅 {id="events"}

群聊 @ 机器人消息与群聊全量消息同属 `EventIntents.GroupAndC2CEvent`。
配置 `intents` 时需要包含：

```Kotlin
intents += EventIntents.GroupAndC2CEvent.intents
```

或在 bot 配置文件中使用 `GROUP_AND_C2C_EVENT`。

<note>
`QGGroupMessageCreateEvent` 代表 QQ 平台的 `GROUP_MESSAGE_CREATE`。
只有当群主设定允许机器人接收群内全部消息时，平台才会推送这类事件。
</note>

## 基本信息 {id="properties"}

由于 QQ 群消息事件中只提供有限的群资料，`QGGroup` 的部分属性会固定为空值：

<deflist>
<def title="id">

群聊的 `group_openid`。

</def>
<def title="name">

始终为空字符串。

</def>
<def title="members">

始终为空结果。

</def>
<def title="member(id)">

始终返回 `null`。

</def>
<def title="ownerId">

始终返回 `null`。

</def>
</deflist>

通过群相关事件得到的 `QGGroupMember` 也只包含成员的 `member_openid`。
它不能用于主动发送私聊消息，调用 `send(...)` 会抛出 `UnsupportedOperationException`。

自 `4.4.0` 起，群消息事件的 `author()` 返回 `QGGroupAuthor`。
它在 `QGGroupMember` 的基础上额外提供 `memberRole` 与 `isBot`，可用于判断消息发送者的群内身份和是否为机器人。

## 发送与回复 {id="send-and-reply"}

`QGGroup` 支持使用 `send(...)` 向当前 QQ 群发送消息。
当 `QGGroup` 来自 `event.content()` 时，组件会自动携带当前消息的 `msgId`，
用于被动回复场景，不消耗主动消息次数。

```Kotlin
process<QGGroupMessageCreateEvent> { event ->
    val group = event.content()
    group.send("收到")
}
```

也可以直接使用消息事件的 `reply(...)`：

```Kotlin
process<QGGroupMessageCreateEvent> { event ->
    event.reply("收到")
}
```

`reply(...)` 会尝试附加引用回复效果。
对 `QGGroupMessageCreateEvent.reply(...)` 的发送前、发送后拦截事件分别是
`QGGroupMessageCreateEventPreReplyEvent` 与 `QGGroupMessageCreateEventPostReplyEvent`。

<note>
在群消息事件中使用 `content().send(...)` 或 `reply(...)` 时，QQ 平台可能会自动添加 `@目标` 效果。
</note>

## 上传群聊媒体 {id="upload-media"}

`QGGroup.uploadMedia(...)` 可上传用于向 QQ 群发送的 `QGMedia`。
目前上传仅支持链接，QQ 平台会对此链接进行转存。

```Kotlin
val group: QGGroup = event.content()
val media = group.uploadMedia(
    url = "https://example.com/image.png",
    type = 1
)
group.send(media)
```

`type` 使用 QQ 平台的媒体类型值：`1` 图片、`2` 视频、`3` 语音、`4` 文件（暂不开放）。
