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

群消息事件只提供有限的群资料，普通 `QGGroup` 的基础属性如下：

| 属性或方法 | 结果 |
| --- | --- |
| `id` | 群聊的 `group_openid` |
| `name` | 空字符串；`QGGroupWithInfo` 使用查询所得的群名称 |
| `members` | 空结果 |
| `member(id)` | `null` |
| `ownerId` | `null` |
| `roles` | `OWNER`、`ADMIN`、`MEMBER` 三种 `QGGroupRole` |

群成员由 `QGGroupMember` 表示，`id` 为成员的 `member_openid`。
自 `5.0` 起还提供所属群的 `groupId`。
群成员不能用于主动发送私聊消息，调用 `send(...)` 会抛出 `UnsupportedOperationException`。

自 `4.4.0` 起，群消息事件的 `author()` 返回 `QGGroupAuthor`。
它在 `QGGroupMember` 的基础上额外提供 `memberRole` 与 `isBot`，可用于判断消息发送者的群内身份和是否为机器人。

## 查询群资料与机器人状态 {id="group-info"}

<secondary-label ref="since-5.0"/>

| 方法 | 结果 |
| --- | --- |
| `groupInfo()` | 查询群基本信息，返回 `GroupInfo` 快照 |
| `includeInfo()` | 查询资料并返回 `QGGroupWithInfo` |
| `groupInfoOrQuery()` | 已有 `QGGroupWithInfo` 时使用其快照，否则查询 |
| `includeInfoOrSelf()` | 已有 `QGGroupWithInfo` 时返回自身，否则查询 |
| `botState()` | 查询机器人在当前群内的 `GroupBotState` 快照 |
| `botAsMemberWithState()` | 查询机器人状态，返回 `QGGroupBotMember` |

`QGGroupWithInfo` 提供 `groupInfo`、`name`、`groupFingerMemo`、`groupClassText`、`groupTags` 和 `groupMemberNum`。
快照保留本次查询的结果，需要刷新时再次调用查询方法。
`includeInfo()` 会检查响应中的群 OpenID；与当前群 ID 不一致时抛出 `IllegalStateException`。

```Kotlin
val group: QGGroup = event.content()
val withInfo = group.includeInfo()
println("${withInfo.name}: ${withInfo.groupMemberNum}")

val botMember = group.botAsMemberWithState()
println("${botMember.id}: ${botMember.memberRole}")
```

`QGGroupBotMember` 还提供 `botState`、`joinTime`、`allowProactiveMsg` 和 `recvMsgSetting`。
自 `5.0` 起，`botAsMember()` 也会请求平台，并返回群成员 OpenID；
需要机器人的 AppID 时使用 `bot.id`。这些查询可能因网络或平台权限问题失败。

通过 `bot.groupRelation` 也可以使用 `groupInfo(groupId)` 和 `groupBotState(groupId)`。
`groupRelation.group(id)` 仍只包装群 ID，不校验群是否存在；`groups` 仍为空，`groupCount()` 仍返回 `-1`。

## 入群申请 {id="join-requests"}

<secondary-label ref="since-5.0"/>

`group.joinRequests` 和 `bot.groupRelation.joinRequests(groupId)` 返回 `Collectable<QGGroupJoinRequest>`。
开始收集时才发起请求，并按平台游标自动翻页。

申请提供 `joinRequestId`、`memberOpenid`、`username`、`applyAt`、`applySource`、`bot`、
`riskTips`、`unionOpenid`、`invitedBy` 和 `verifyInfo`，以及底层的 `source` 快照。
通过 `accept()` 接受申请，通过 `reject(...)` 拒绝：

```Kotlin
group.joinRequests.asFlow().collect { request ->
    println("${request.username}: ${request.verifyInfo}")
    // 根据业务条件选择接受或拒绝。
    request.accept()
}
```

拒绝选项包括 `QGGroupJoinRequestRejectOption.reason("理由")` 和
`QGGroupJoinRequestRejectOption.AddToBlacklist`。
多个理由按传入顺序直接拼接，不额外插入分隔符。
已知群、成员和申请 ID 时，也可以调用 `groupRelation.approveJoinRequest(...)` 或 `rejectJoinRequest(...)`。
群和管理员权限由平台校验，请求失败时抛出相应异常。

## 成员禁言 {id="member-mutes"}

<secondary-label ref="since-5.0"/>

`group.muteSetting()` 查询完整的 `GroupMuteSetting`，包含全员禁言规则和成员的单独禁言记录。
`member.muteState()` 查询该成员的记录；返回 `null` 仅表示没有单独记录，仍可能受全员禁言影响。
两者使用相同的群禁言查询 API，可能共享服务端速率限制。

| 操作 | `QGGroup` 方法 | `QGGroupMember` 方法 |
| --- | --- | --- |
| 增加禁言 | `addMemberMute(memberId, expireAt)` | `addMute(expireAt)` |
| 更新禁言到期时间 | `updateMemberMute(memberId, expireAt)` | `updateMute(expireAt)` |
| 解除单独禁言 | `unmuteMember(memberId)` | `unmute()` |

`expireAt` 使用 `kotlin.time.Instant` 表示绝对到期时间。
也可以使用 `addMemberMuteAtMilliseconds(...)`、`updateMemberMuteAtMilliseconds(...)`，
或成员的 `addMuteAtMilliseconds(...)`、`updateMuteAtMilliseconds(...)`，传入自 Unix epoch 起的毫秒数。
扩展函数 `addMuteFor(duration)`、`updateMuteFor(duration)` 及群和关系对象上的
`addMemberMuteFor(...)`、`updateMemberMuteFor(...)` 支持 `kotlin.time.Duration`，可选提供作为起点的 `now: Instant`，时长必须为有限的正值。

```Kotlin
import love.forte.simbot.component.qguild.group.addMuteFor
import kotlin.time.Duration.Companion.minutes

val member = event.author()
member.addMuteFor(10.minutes)
member.unmute()
```

批量操作使用 `group.setMemberMutes(changes)`，每次提交 1～20 项。
变更项通过 `QGGroupMemberMuteChange.add(...)`、`update(...)` 和 `remove(...)` 创建。
`bot.groupRelation` 也提供带 `groupId` 的对应方法。
机器人需要群管理员身份，平台只允许操作普通成员，最长禁言 30 天。
解除成员单独禁言不会修改全员禁言规则；操作失败时抛出平台或参数校验异常。

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

群消息事件的 `messageContent` 自 `5.0` 起支持撤回当前收到的消息，
而 `content().send(...)` 与 `reply(...)` 返回的消息回执也可以撤回对应的机器人消息。
消息时效、群成员权限以及不支持场景的处理方式，参见
[消息撤回](component-qq-guild-messages.md#message-delete)。

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
