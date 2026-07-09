---
switcher-label: JavaAPI风格
---

# 消息元素

<tldr>

- 对那些 **核心库** 中、实现了 simbot4 标准库的 `Message.Element` 消息元素类型的说明，
- 对一些与 **核心库** 中“消息”相关的内容的补充说明。

</tldr>

<seealso>
<category ref="links">
<a href="basic-messages.md" />
</category>
</seealso>

<note>
有关消息元素、消息链的更多信息，可参考
<a href="basic-messages.md" /> 。
</note>

## 消息元素实现 {id='message-impl'}

所有的 `Message.Element` 特殊实现类型均定义在包 `love.forte.simbot.component.qguild.message` 中。

它们都继承了 `love.forte.simbot.component.qguild.message.QGMessageElement` 。

<deflist>
<def title="QGArk">对 API 模块中 Ark 消息的包装体，可用来发送 <code>Ark</code> 消息。</def>
<def title="QGContentText"></def>
<def title="QGMarkdown">

> 仅用于发送。添加自 `4.0.0-beta6` 。

</def>
<def title="QGAttachmentMessage"></def>
<def title="QGEmbed">对 API 模块中 Embed 消息的包装体，可用来发送 <code>Embed</code> 消息。</def>
<def title="QGReference">

发送消息时，QQ频道的消息引用。与官方发送消息API中的 `reference` 对应。

</def>
<def title="QGReplyTo">

<tip>仅用于发送。</tip>

发送消息时，指定一个需要回复的目标消息ID。

</def>
<def title="QGMedia">

> 仅用于发送。添加自 `4.0.0-beta6` 。

</def>
<def title="QGKeyboards">

> 仅用于群聊/单聊发送。添加自 `4.4.0` 。

对 API 模块中 `MessageKeyboards` 的包装体，可用来发送包含多行、多按钮的 Markdown 消息按钮。
旧的 `QGKeyboard` 只包装单个 `MessageKeyboard`，自 `4.4.0` 起应改用 `QGKeyboards`。

</def>
<def title="QGKeyboard">

> 仅用于群聊/单聊发送。自 `4.4.0` 起废弃。

旧的单按钮包装体，只能包装单个 `MessageKeyboard`，无法完整表达官方 `keyboard.content.rows[].buttons[]` 结构。
请使用 `QGKeyboards` 替代。

</def>
</deflist>

## 发送消息 {id='message-usage'}

在simbot中，使用组件的消息元素与使用其他消息元素别无二致，
通常使用 `SendSupport` 和 `ReplySupport` 的实现类中提供的 `send(...)` 和 `reply(..)` API 发送消息。

前者多由
<a href="component-qq-guild-actors.md">行为对象</a>
中的一些类型实现(例如`QGMember`、`QGTextChannel`)，
而后者则通常由与消息相关的事件实现(例如 `QGAtMessageCreateEvent`)。

此处以 `QGTextChannel` 为例，`send` 可以使用拼接后的消息链、字符串或单独的消息元素作为参数。

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val channel: QGTextChannel = ...
channel.send("消息内容")
channel.send("消息内容".toText() + At("user id".ID))
```

</tab>
<tab title="Java" group-key="Java">

<if switcher-key="%ja%">

```Java
QGTextChannel channel = ...

var sendTask1 = channel.sendAsync("消息内容");
var sendTask2 = channel.sendAsync(Messages.of(
        Text.of("文本消息"),
        At.of(Identifies.of("user id"))
));
```

</if>

<if switcher-key="%jb%">

```Java
QGTextChannel channel = ...;

channel.sendBlocking("消息内容");
channel.sendBlocking(Messages.of(
        Text.of("文本消息"),
        At.of(Identifies.of("user id"))
    ));
```

</if>

<if switcher-key="%jr%">

```Java
QGTextChannel channel = ...;

channel.sendReserve("消息内容")
        .transform(SuspendReserves.mono())
        .subscribe(receipt -> { ... });

channel.sendReserve(Messages.of(
        Text.of("文本消息"),
        At.of(Identifies.of("user id"))
    ))
    .transform(SuspendReserves.mono())
    .subscribe(receipt -> { ... });
```

</if>
</tab>
</tabs>

## Markdown 消息按钮 {id='message-keyboards'}

自 `4.4.0` 起，群聊和单聊 Markdown 消息按钮使用 `QGKeyboards` / `MessageKeyboards` 表示。
它支持按行组织多个按钮，并在发送体中仍序列化为官方 API 的 `keyboard` 字段。


<warning>

旧的 `QGKeyboard` 与直接使用 `MessageKeyboard` 的发送入口仅能表达单个按钮，且结构不完整无法直接被 API 使用，已经被废弃。

`QGKeyboard` 自 `4.4.0` 起废弃，编译期会以 `ERROR` 级别提示。
原本使用 `QGKeyboard.create(...)` 的位置，应替换为 `QGKeyboards.create(...)` 或 `QGKeyboards { ... }`。

</warning>

<tabs group="code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val keyboards = QGKeyboards {
    content {
        row {
            button {
                renderData("确认", visitedLabel = "已确认", style = 1)
                action {
                    type = 1
                    data = "confirm"
                    unsupportTips = "当前客户端暂不支持"
                    permissionAllAccessible()
                }
            }
        }
        row {
            addButton(MessageKeyboard.create("template-id"))
        }
    }
}

group.send(QGMarkdown.create("请选择") + keyboards)

// 只有一行按钮时，也可以直接包装 MessageKeyboards。
val singleRow = MessageKeyboards.create(
    listOf(
        MessageKeyboard.create("template-a"),
        MessageKeyboard.create("template-b")
    )
)

group.send(QGMarkdown.create("请选择") + QGKeyboards.create(singleRow))
```

</tab>
<tab title="Java" group-key="Java">

<if switcher-key="%ja%">

```Java
var keyboards = MessageKeyboards.create(List.of(
        MessageKeyboard.create("template-a"),
        MessageKeyboard.create("template-b")
));

var sendTask = group.sendAsync(Messages.of(
        QGMarkdown.create("请选择"),
        QGKeyboards.create(keyboards)
));
```

</if>

<if switcher-key="%jb%">

```Java
var keyboards = MessageKeyboards.create(List.of(
        MessageKeyboard.create("template-a"),
        MessageKeyboard.create("template-b")
));

group.sendBlocking(Messages.of(
        QGMarkdown.create("请选择"),
        QGKeyboards.create(keyboards)
));
```

</if>

<if switcher-key="%jr%">

```Java
var keyboards = MessageKeyboards.create(List.of(
        MessageKeyboard.create("template-a"),
        MessageKeyboard.create("template-b")
));

group.sendReserve(Messages.of(
        QGMarkdown.create("请选择"),
        QGKeyboards.create(keyboards)
)).transform(SuspendReserves.mono()).subscribe(receipt -> { ... });
```

</if>
</tab>
</tabs>
