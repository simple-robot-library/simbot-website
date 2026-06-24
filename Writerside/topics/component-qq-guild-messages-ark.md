# Ark消息

`Ark` 是 QQ 开放平台中的模板消息结构。
在当前组件中，`Ark` 既有 API 层的数据模型，也有组件层的消息元素封装。


## API模块 {id='api-module'}

API 层使用的是 `love.forte.simbot.qguild.model.Message.Ark`。

你通常会在这些地方接触到它：

- `MessageSendApi.Body.ark` 与 `DmsSendApi` 的发送体
- `GroupMessageSendApi` / `UserMessageSendApi` 的 `GroupAndC2CSendBody.ark`
- `ArkMessageTemplates` 提供的若干模板消息辅助类型
- `buildArk(...)` 等构建函数

如果你当前只是在直接拼开放平台请求体，
那么使用 `Message.Ark` 即可，不必依赖组件层的 `QGArk`。

## 组件库模块 {id='core-module'}

组件层提供 `love.forte.simbot.component.qguild.message.QGArk`，
它是一个 `QGMessageElement`，可直接放进 simbot 的消息链里。

常用入口：

<deflist>
<def title="QGArk.create(...)">

根据 `templateId` 与 `kvs` 构建一个 `QGArk`。

</def>
<def title="QGArk.byArk(...)">

把 API 层的 `Message.Ark` 包装成组件消息元素。

</def>
<def title="toArk() / toMessage() / toRealArk()">

在 API 层模型与组件层消息元素之间来回转换。

</def>
</deflist>

## 发送行为

发送时，`QGArk` 会被解析为真正的 `Ark` 请求体：

- 频道消息支持 `MessageSendApi`
- `DMS` 支持 `DmsSendApi`
- QQ 群与 `C2C` 发送场景也支持 `Ark`

如果你只是想在 simbot 消息链里使用它，
优先选择 `QGArk`；
如果你正在写底层 API 代码，优先选择 `Message.Ark`。

