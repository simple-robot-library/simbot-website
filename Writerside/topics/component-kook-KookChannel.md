# 子频道 KookChannel

`KookChannel` 表示服务器中的子频道，提供 `id`、`name`、`guildId` 等信息，
以及原始频道对象 `source`。可以通过服务器的频道集合或频道相关事件获取。

频道类型决定可用操作。发送消息可参考 [](component-kook-message-send.md)。

<include from="component-kook-KookBot.md" element-id="need-help"/>