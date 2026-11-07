# OneBot11

## 交互方式

OneBot组件的OneBot11模块选择使用
[正向 HTTP](https://github.com/botuniverse/onebot-11/blob/master/communication/http.md)
作为API交互方式、
[正向 WebSocket](https://github.com/botuniverse/onebot-11/blob/master/communication/ws.md)
作为事件订阅的方式。

简单来说，就是不论是API交互还是事件订阅，都由OneBot组件作为**主动方**：主动发起HTTP请求、主动发起WebSocket连接。

### 反向？

#### 反向 HTTP

如果希望通过反向 HTTP 接收事件推送，需要自行搭建 HTTP 服务端，然后使用 `OneBotBot.push` 手动推送原始事件的 JSON 字符串。`push` 返回的 Flow 需要收集才能处理事件，也可以使用 `pushAndLaunch` 启动处理。
你可以前往参考
`OneBotBot` 的
<a href="component-onebot-v11-OneBotBot.md#外部事件" /> 。

#### 反向 WebSocket

目前OneBot11组件尚未支持通过 _反向 WebSocket_ 的而不是HTTP API形式来进行API请求，因为我们认为这个功能没有那么的**有必要**，
因为与上述的正向 HTTP 和正向 WebSocket 相比，反向的方式似乎没有什么非用不可的场景。

你可以参考并参与到 [#72](https://github.com/simple-robot/simbot-component-onebot/issues/72) 中的讨论，
如果你有合适的应用场景，欢迎提出，如果需求合理，也许会考虑添加对两个反向的支持。


