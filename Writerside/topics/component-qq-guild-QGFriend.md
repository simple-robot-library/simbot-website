# C2C单聊 QGFriend

<note>

自 `4.0.0-beta6` 开始支持。

</note>

`QGFriend` 表示 QQ 机器人中的一个 `C2C` 单聊目标。

和“传统好友列表”不同，`QGFriend` 更接近于
“来自事件上下文的可回复目标”：

- 它通常从 `C2C` 消息事件中得到
- 目前没有对应的“好友列表查询”能力
- 只能稳定拿到 `openid`

所以它通常表现为：

- `id` 可用于标识此单聊目标
- `name` 始终是空字符串，`avatar` 始终是 `null`

## 获取途径

处理 `C2C` 单聊相关事件时，
通常可以从事件的 `author`、`content` 或目标对象链路中拿到 `QGFriend`。

要看这个场景的事件本身，
可继续阅读：

- [](component-qq-guild-event-list.md)
- [](component-qq-guild.md)

## 可用能力

`QGFriend` 当前主要有两类能力：

<deflist>
<def title="发送消息">

继承 `Contact` 的发送能力，可直接发送 `String`、`Message`、`MessageContent`。

</def>
<def title="上传媒体">

通过 `uploadMedia(...)` 上传媒体，得到 `QGMedia`。
`QGMedia` 本身是一个消息元素，可用于后续的 `C2C` / QQ 群消息发送。

</def>
</deflist>

## 发送消息

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
suspend fun reply(friend: QGFriend) {
    friend.send("你好，这是一条 C2C 单聊消息")
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
QGFriend friend = ...;

friend.sendAsync("你好，这是一条 C2C 单聊消息")
        .thenAccept(receipt -> { });
```
{switcher-key="%ja%"}

```Java
QGFriend friend = ...;

var receipt = friend.sendBlocking("你好，这是一条 C2C 单聊消息");
```
{switcher-key="%jb%"}

```Java
QGFriend friend = ...;

friend.sendReserve("你好，这是一条 C2C 单聊消息")
        .transform(SuspendReserves.mono())
        .subscribe(receipt -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>

## 上传媒体

目前公开了两组上传函数：

- `uploadMedia(url: String, type: Int)`
- `uploadMedia(resource: Resource, type: Int)`  (`4.1.1` 起)

其中 `type` 与开放平台媒体类型一致：

- `1`: 图片
- `2`: 视频
- `3`: 语音
- `4`: 文件（当前平台侧仍有限制）

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
suspend fun upload(friend: QGFriend) {
    val media = friend.uploadMedia(
        url = "https://example.com/example.png",
        type = 1
    )

    // media: QGMedia
}
```

</tab>
<tab title="Java" group-key="Java">

```Java
QGFriend friend = ...;

friend.uploadMediaAsync("https://example.com/example.png", 1)
        .thenAccept(media -> { });
```
{switcher-key="%ja%"}

```Java
QGFriend friend = ...;

var media = friend.uploadMediaBlocking("https://example.com/example.png", 1);
```
{switcher-key="%jb%"}

```Java
QGFriend friend = ...;

friend.uploadMediaReserve("https://example.com/example.png", 1)
        .transform(SuspendReserves.mono())
        .subscribe(media -> { });
```
{switcher-key="%jr%"}

</tab>
</tabs>
