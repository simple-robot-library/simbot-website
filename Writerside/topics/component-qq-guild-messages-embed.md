# Embed消息

`Embed` 是 QQ 开放平台中的结构化消息类型。
在当前组件中，它同样分成 API 层模型与组件层消息元素两层。


## API模块 {id='api-module'}

API 层使用的是 `love.forte.simbot.qguild.model.Message.Embed`。

最常见的入口是：

- `MessageSendApi.Body.embed`
- `DmsSendApi` 复用同样的发送体
- `EmbedBuilder` 用于构建 `Message.Embed`

## 组件库模块 {id='core-module'}

组件层提供 `love.forte.simbot.component.qguild.message.QGEmbed`，
它是一个 `QGMessageElement`，专门用于在 simbot 消息链中携带 `Embed`。

常用入口包括：

- `QGEmbed.byEmbed(embed)`
- `buildQGEmbed { ... }`

## 发送限制

使用时需要注意：

- `QGEmbed` 发送时会独立占用一个 `MessageSendApi.Body.embed`
- `Embed` 目前**不支持** QQ 群 / `C2C` 的 `GroupAndC2C` 发送链路

此外，还需要注意：

> `QGEmbed` 尽量不要和 `messageReference` 一起使用，
> 例如在 `MessageEvent.reply(...)` 中直接回复 `QGEmbed`，
> 否则消息可能不可见。

## 什么时候用哪一层

- 直接写开放平台请求：使用 `Message.Embed`
- 使用 simbot 消息链：使用 `QGEmbed`

