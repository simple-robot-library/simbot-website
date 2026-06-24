# Bot配置文件

Bot配置文件通常情况下是配合Spring Boot starter的时候用的。

当使用Spring Boot starter时，
配置文件放在资源目录 <path>resources</path> 中的 <path>/simbot-bots/</path> 目录下，
以 `.bot.json` 格式结尾，例如 `myBot.bot.json`。

<warning title="记得清理注释">

实际上JSON配置文件是**不允许**使用注释的，这里只是方便展示。

</warning>

<tabs>
<tab title="较完整示例">

```json
{
    // 固定值
    "component": "simbot.onebot11",
    "authorization": {
        // 唯一ID，作为组件内 Bot 的 id，用于组件内去重。可以随便编，但建议是bot的qq号
        "botUniqueId": "123456",
        // api地址，是个http/https服务器的路径，默认localhost:3001
        "apiServerHost": "http://localhost:3001",
        // 订阅事件的服务器地址，是个ws/wss路径，默认 `null`
        // 如果为 `null` 则不会连接 ws 和订阅事件
        "eventServerHost": "ws://localhost:3001",
        // 配置的 token，可以是null, 代表同时配置 apiAccessToken 和 eventAccessToken
        "accessToken": null,
        // 用于API请求时用的 token，默认 null
        "apiAccessToken": null,
        // 用于连接事件订阅ws时用的 token，默认 null
        "eventAccessToken": null
    },
    // 额外的可选配置
    // config本身以及其内的各项属性绝大多数都可省略或null
    "config": {
        // API请求中的超时请求配置。整数数字，单位毫秒，默认为 `null`。
        "apiHttpRequestTimeoutMillis": null,
        // API请求中的超时请求配置。整数数字，单位毫秒，默认为 `null`。
        "apiHttpConnectTimeoutMillis": null,
        // API请求中的超时请求配置。整数数字，单位毫秒，默认为 `null`。
        "apiHttpSocketTimeoutMillis": null,
        // 每次尝试连接到 ws 服务时的最大重试次数，大于等于0的整数，默认为 2147483647
        "wsConnectMaxRetryTimes": null,
        // 每次尝试连接到 ws 服务时，如果需要重新尝试，则每次尝试之间的等待时长
        // 整数数字，单位毫秒，默认为 3500
        "wsConnectRetryDelayMillis": null,
        // 当使用非 [OneBotImage] 类型作为图片资源发送消息时，
        // 默认根据 [Resource] 得到一个可能存在的 [OneBotImage.AdditionalParams]。
        // 注意！这无法影响直接使用 [OneBotImage] 的情况。
        // defaultImageAdditionalParams 默认为 `null`。
        "defaultImageAdditionalParams": {
            // default: null
            "localFileToBase64": null,
            "type": null,
            "cache": null,
            "proxy": null,
            "timeout": null
        }
    }
}
```

</tab>
<tab title="简单示例">

```json
{
  "component": "simbot.onebot11",
  "authorization": {
    "botUniqueId": "123456",
    "apiServerHost": "http://localhost:3001",
    "eventServerHost":"ws://localhost:3001"
  }
}
```

</tab>
</tabs>

## 属性说明

配置文件对应的反序列化类型是
`OneBotBotSerializableConfiguration`。

## 顶层结构

<deflist>
<def title="component">

固定值，必须为 `simbot.onebot11`。

</def>
<def title="authorization">

鉴权与连接地址相关配置，必填。

</def>
<def title="config">

额外可选配置。绝大部分情况下都可以省略。

</def>
</deflist>

## authorization

<deflist>
<def title="botUniqueId">

组件内部用于区分不同 Bot 的唯一 ID。
建议直接使用你的机器人 QQ 号或一个稳定且不会重复的标识。

</def>
<def title="apiServerHost">

HTTP API 服务地址。
如果不配置，运行时默认值来自 `OneBotBotConfiguration.apiServerHost`，
即 `http://localhost:3001`。

</def>
<def title="eventServerHost">

正向 WebSocket 事件地址。
如果为 `null`，则不会建立 ws 连接，也不会接收推送事件。

</def>
<def title="accessToken">

共享鉴权 token。
如果配置了它，会同时写入 API 与事件连接两侧。

</def>
<def title="apiAccessToken">

只用于 HTTP API 请求的 token。
如果同时配置了 `accessToken` 与 `apiAccessToken`，
则以 `apiAccessToken` 为准。

</def>
<def title="eventAccessToken">

只用于正向 WebSocket 连接的 token。
如果同时配置了 `accessToken` 与 `eventAccessToken`，
则以 `eventAccessToken` 为准。

</def>
</deflist>

## config

<deflist>
<def title="apiHttpRequestTimeoutMillis / apiHttpConnectTimeoutMillis / apiHttpSocketTimeoutMillis">

分别对应 Ktor `HttpTimeout` 的请求、连接、读写超时配置。
如果三者都不提供，则不会额外配置超时插件。

</def>
<def title="wsConnectMaxRetryTimes">

每次 ws 断开后重新连接的最大尝试次数。
运行时默认值为 `2147483647`。

</def>
<def title="wsConnectRetryDelayMillis">

每次 ws 重连之间的等待时间，单位毫秒。
运行时默认值为 `3500`。

</def>
<def title="defaultImageAdditionalParams">

为“非 `OneBotImage` 类型但最终会被当作图片发送”的资源提供默认附加参数。
它**不会影响**你已经直接构建好的 `OneBotImage`。

可选子项：

- `localFileToBase64`
- `type`
- `cache`
- `proxy`
- `timeout`

</def>
</deflist>

## 使用建议

- 只做 API 调用时，可不配置 `eventServerHost`
- 需要监听事件时，再配置 `eventServerHost`
- 如果你的服务端 API 与 ws 分离部署，务必分别填写对应地址
