# Bot配置文件

<tldr>
<p>在使用 <b>Spring Boot</b> 时自动注册 bot 所需的配置文件。</p>
</tldr>

<tip>

如果你在使用 Spring Boot，
将配置文件放在在你的资源目录中:
<path>resources/simbot-bots/</path> ，
并以 `.bot.json` 作为扩展名，例如 `mybot.bot.json`。

这个扫描目录是可配置的。
这是属于 simbot4 Spring Boot starter 的配置，可参考
[集成 Spring Boot](Spring-Boot.md)。

</tip>

## 示例

```json
{
    "component": "simbot.qqguild",
    "ticket": {
        "appId": "你的botId",
        "secret": "你的bot secret, 用于获取API的access_token(4.0.0-beta6开始)",
        "token": "你的bot token, 用作API的access_token(4.0.0-beta6之前)"
    }
}
```
{collapsible="true" default-state="expanded" collapsed-title="简单示例"}

```json
{
  "component": "simbot.qqguild",
  "ticket": {
    "appId": "你的botId",
    "secret": "你的bot secret, 用于获取API的access_token(4.0.0-beta6开始)",
    "token": "你的bot token, 用作API的access_token(4.0.0-beta6之前)"
  },
  "config": {
    "serverUrl": null,
    "shard": {
      "type": "full"
    },
    "intents": {
      "type": "raw",
      "intents": 1073741827
    },
    "clientProperties": null,
    "timeout": null,
    "cache": {
      "enable": true,
      "transmit": null,
      "dynamic": null,
      "dispatcher": null
    },
    "disableWs": false,
    "contentAsMarkdownAll": false,
    "contentAsMarkdown": {
      "CHANNEL": true
    },
    "retry": {
      "maxRetries": 2,
      "exponentialDelay": true,
      "retryOnServerErrors": true
    }
  }
}
```
{collapsible="true" default-state="collapsed" collapsed-title="完整示例"}

## 属性描述

<deflist>
<def title="component">

固定值：`simbot.qqguild`

</def>
<def title="ticket">

bot用于登录的票据信息，必填。

<deflist type="wide">
<def title="appId">

`String`

bot开发配置中的 `appID`

</def>
<def title="secret">

`String`

bot开发配置中的 `AppSecret`, 
`4.0.0-beta6` 版本开始用于获取API访问所需的 `access_token`。

</def>
<def title="token">

`String`

bot开发配置中的 `Token`。
`4.0.0-beta6` 版本**之前**用作API访问所需的 token。

</def>
</deflist>

</def>

<def title="config">
可选项，提供一些额外的可配置属性。

<deflist>
<def title="serverUrl">

`String`

目标服务器地址。默认为 `null`。

QQ 开放平台自 `2026-08-10` 起将接口调用域名统一为
`https://api.bot.qq.com`，不再提供独立的沙箱接口域名。

| 配置值         | 实际值                                   |
|-------------|---------------------------------------|
| `null`      | `"https://api.bot.qq.com"`            |
| `"SANDBOX"` | `"https://sandbox.api.sgroup.qq.com"` |
| 其他          | 与配置值一致                                |

`"SANDBOX"` 仅为兼容已有配置而保留，现已弃用，使用时会输出警告；
新配置不应继续使用它。需要使用代理等自定义地址时，直接填写对应 URL。


</def>
<def title="shard">

`ShardConfig`

分片信息配置，默认为 `Full`。

根据 `type` 值的不同，可使用不同的属性。

<deflist>
<def title="type='full'">

无额外属性，代表一个全量单片。

```json
{
    "type": "full"
}
```

</def>
<def title="type='simple'">

```json
{
   "type": "simple",
   "value": 0,
   "total": 1
}
```

<deflist type="medium">
<def title="value">对应的分片信息属性。</def>
<def title="total">对应的分片信息属性。</def>
</deflist>

</def>
</deflist>


</def>
<def title="intents" id="config.intents">

`IntentsConfig?`

要订阅的事件的 intents 信息。默认 `1073741827`，
也就是订阅：
- 频道相关事件
- 频道成员相关事件
- 公域消息相关事件

```json
{
  "config": {
    "intents": {
      "type": "raw",
      "intents": 1073741827
    }
  }
}
```

根据 `type` 的不同可选的属性不同。

<tip>

有关 `intents` 的更多信息可参考 [官方文档](https://bot.q.qq.com/wiki/develop/api-v2/dev-prepare/interface-framework/event-emit.html#事件订阅Intents)

下面的参考内容也同样拷贝自官方文档，仅供参考，不确保时效性与准确性。

</tip>

```
GUILDS (1 << 0)
  - GUILD_CREATE           // 当机器人加入新guild时
  - GUILD_UPDATE           // 当guild资料发生变更时
  - GUILD_DELETE           // 当机器人退出guild时
  - CHANNEL_CREATE         // 当channel被创建时
  - CHANNEL_UPDATE         // 当channel被更新时
  - CHANNEL_DELETE         // 当channel被删除时

GUILD_MEMBERS (1 << 1)
  - GUILD_MEMBER_ADD       // 当成员加入时
  - GUILD_MEMBER_UPDATE    // 当成员资料变更时
  - GUILD_MEMBER_REMOVE    // 当成员被移除时

GUILD_MESSAGES (1 << 9)    // 消息事件，仅 *私域* 机器人能够设置此 intents。
  - MESSAGE_CREATE         // 发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。
                           // 内容与 AT_MESSAGE_CREATE 相同
  - MESSAGE_DELETE         // 删除（撤回）消息事件

GUILD_MESSAGE_REACTIONS (1 << 10)
  - MESSAGE_REACTION_ADD    // 为消息添加表情表态
  - MESSAGE_REACTION_REMOVE // 为消息删除表情表态

DIRECT_MESSAGE (1 << 12)
  - DIRECT_MESSAGE_CREATE   // 当收到用户发给机器人的私信消息时
  - DIRECT_MESSAGE_DELETE   // 删除（撤回）消息事件


GROUP_AND_C2C_EVENT (1 << 25)
  - C2C_MESSAGE_CREATE      // 用户单聊发消息给机器人时候
  - FRIEND_ADD              // 用户添加使用机器人
  - FRIEND_DEL              // 用户删除机器人
  - C2C_MSG_REJECT          // 用户在机器人资料卡手动关闭"主动消息"推送
  - C2C_MSG_RECEIVE         // 用户在机器人资料卡手动开启"主动消息"推送开关
  - GROUP_AT_MESSAGE_CREATE // 用户在群里@机器人时收到的消息
  - GROUP_MESSAGE_CREATE    // 群聊全量消息
  - GROUP_ADD_ROBOT         // 机器人被添加到群聊
  - GROUP_DEL_ROBOT         // 机器人被移出群聊
  - GROUP_MSG_REJECT        // 群管理员主动在机器人资料页操作关闭通知
  - GROUP_MSG_RECEIVE       // 群管理员主动在机器人资料页操作开启通知

GROUP_MEMBERS (1 << 24)
  - GROUP_MEMBER_ADD       // 群成员加入群聊
  - GROUP_MEMBER_REMOVE    // 群成员退出群聊

INTERACTION (1 << 26)
  - INTERACTION_CREATE     // 互动事件创建时

MESSAGE_AUDIT (1 << 27)
- MESSAGE_AUDIT_PASS     // 消息审核通过
- MESSAGE_AUDIT_REJECT   // 消息审核不通过

FORUMS_EVENT (1 << 28)  // 论坛事件，仅 *私域* 机器人能够设置此 intents。
  - FORUM_THREAD_CREATE     // 当用户创建主题时
  - FORUM_THREAD_UPDATE     // 当用户更新主题时
  - FORUM_THREAD_DELETE     // 当用户删除主题时
  - FORUM_POST_CREATE       // 当用户创建帖子时
  - FORUM_POST_DELETE       // 当用户删除帖子时
  - FORUM_REPLY_CREATE      // 当用户回复评论时
  - FORUM_REPLY_DELETE      // 当用户回复评论时
  - FORUM_PUBLISH_AUDIT_RESULT      // 当用户发表审核通过时

AUDIO_ACTION (1 << 29)
  - AUDIO_START             // 音频开始播放时
  - AUDIO_FINISH            // 音频播放结束时
  - AUDIO_ON_MIC            // 上麦时
  - AUDIO_OFF_MIC           // 下麦时

PUBLIC_GUILD_MESSAGES (1 << 30) // 消息事件，此为公域的消息事件
  - AT_MESSAGE_CREATE       // 当收到@机器人的消息时
  - PUBLIC_MESSAGE_DELETE   // 当频道的消息被删除时

```
{collapsible="true" default-state="collapsed" collapsed-title="内容参考"}

<deflist>
<def title="type='raw'">

直接使用 `intents` 原始的标记位最终数值。

所有的事件对应的位值信息可前往参考 [官方文档](https://bot.q.qq.com/wiki/develop/api-v2/dev-prepare/interface-framework/event-emit.html#事件订阅Intents) 。

```json
{
  "type": "raw",
  "intents": 1073741824
}
```

</def>
<def title="type='nameBased'">

通过名称寻找所有可用的 `EventIntents` 并合并为最终的 `intents`。
名称基于继承了 `EventIntents` 的 object 的简单名称，例如 `Guilds`。

名称支持开头大写或小写的驼峰，例如 `Guilds`, `guilds`,
或者全大写或全小写的snake(下划线)格式，例如 `PUBLIC_GUILD_MESSAGES`, `public_guild_messages`。

虽然支持的格式比较宽松，但名称匹配仍然是**区分大小写**的，
比如一个混用大小写的snake格式就是不允许的：`public_GUILD_messages` ❌。

> 开头小写的驼峰以及snake格式自 `v4.0.0-beta7` 开始支持，
> 在此之前仅支持开头大写的驼峰格式，例如 `Guild`。

```json
{
  "type": "nameBased",
  "names": ["Guilds", "PublicGuildMessages"]
}
```

<tip title="可选值参考">

`nameBased` 的具体可选值可参考 `EventIntentsAggregation.getByName` 的
[API文档](https://docs.simbot.forte.love/components/qq-guild/simbot-component-qq-guild-api/love.forte.simbot.qguild.event/-event-intents-aggregation/get-by-name.html)
或源码的文档注释。

此处会简单列举一下可选值的参考，但不保证绝对准确性，以实际代码中的效果与描述为准。

<deflist collapsible="true" default-state="collapsed" type="medium">
<def title="GUILDS">
<list>
<li>当机器人加入新guild时</li>
<li>当guild资料发生变更时</li>
<li>当机器人退出guild时</li>
<li>当channel被创建时</li>
<li>当channel被更新时</li>
<li>当channel被删除时</li>
</list>
</def>
<def title="GUILD_MEMBERS">
<list>
<li>当成员加入时</li>
<li>当成员资料变更时</li>
<li>当成员被移除时</li>
</list>
</def>
<def title="GUILD_MESSAGES">

消息事件，仅 **私域** 机器人能够设置此 intents。

<list>
<li>发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。内容与 AT_MESSAGE_CREATE 相同</li>
<li>删除（撤回）消息事件</li>
</list>
</def>
<def title="GUILD_MESSAGE_REACTIONS">
<list>
<li>为消息添加表情表态</li>
<li>为消息删除表情表态</li>
</list>
</def>
<def title="DIRECT_MESSAGE">
<list>
<li>当收到用户发给机器人的私信消息时</li>
<li>删除（撤回）消息事件</li>
</list>
</def>
<def title="GROUP_AND_C2C_EVENT">
<list>
<li>用户单聊发消息给机器人时候</li>
<li>用户添加使用机器人</li>
<li>用户删除机器人</li>
<li>用户在机器人资料卡手动关闭"主动消息"推送</li>
<li>用户在机器人资料卡手动开启"主动消息"推送开关</li>
<li>用户在群里@机器人时收到的消息</li>
<li>群聊全量消息</li>
<li>机器人被添加到群聊</li>
<li>机器人被移出群聊</li>
<li>群管理员主动在机器人资料页操作关闭通知</li>
<li>群管理员主动在机器人资料页操作开启通知</li>
</list>
</def>
<def title="GROUP_MEMBERS">
<list>
<li>群成员加入群聊，自 <code>4.4.0</code> 开始支持</li>
<li>群成员退出群聊，自 <code>4.4.0</code> 开始支持</li>
</list>
</def>
<def title="INTERACTION">
<list>
<li>互动事件创建时，自 <code>4.4.0</code> 开始支持按钮点击回调解析与回应</li>
</list>
</def>
<def title="MESSAGE_AUDIT">
<list>
<li>消息审核通过</li>
<li>消息审核不通过</li>
</list>
</def>
<def title="FORUMS_EVENT">

论坛事件，仅 **私域** 机器人能够设置此 intents。

<list>
<li>当用户创建主题时</li>
<li>当用户更新主题时</li>
<li>当用户删除主题时</li>
<li>当用户创建帖子时</li>
<li>当用户删除帖子时</li>
<li>当用户回复评论时</li>
<li>当用户回复评论时</li>
<li>当用户发表审核通过时</li>
</list>
</def>
<def title="AUDIO_ACTION">
<list>
<li>音频开始播放时</li>
<li>音频播放结束时</li>
<li>上麦时</li>
<li>下麦时</li>
</list>
</def>
<def title="PUBLIC_GUILD_MESSAGES">
消息事件，此为公域的消息事件
<list>
<li>当收到@机器人的消息时</li>
<li>当频道的消息被删除时</li>
</list>
</def>
</deflist>
</tip>


再举个例子，如果你想要订阅频道事件和**群聊消息事件**：

```json
{
  "type": "nameBased",
  "names": ["Guilds", "PublicGuildMessages", "GROUP_AND_C2C_EVENT"]
}
```

</def>
<def title="type='bitBased'">
<note>自 <code>4.0.0-beta7</code> 开始支持</note>

通过 `intents` 的位索引值来配置 `intents` 的结果。

```json
{
  "type": "bitBased",
  "bits": [0, 1, 30]
}
```

上面的 `0, 1, 30` 即代表订阅 `1<<0 | 1<<1 | 1<<30`。

`bits` 的元素值应当在 0 ~ 31 之内，但是代码内不做校验。

</def>
</deflist>

</def>
<def title="clientProperties">

`Map<String, String>?`

用作 `Signal.Identify.Data.properties` 中的参数。

```json
{
  "config": {
    "clientProperties": {
      "k1": "v1",
      "foo": "bar"
    }
  }
}
```

</def>
<def title="timeout" type="wide">

`TimeoutConfig?`

与部分超时相关的配置信息。
当任意属性不为 `null` 时会为 bot 中用于请求API的 `HttpClient`
配置 [HttpTimeout][HttpTimeout] 插件。

默认为 `null`。

<deflist>
<def title="apiHttpRequestTimeoutMillis">

`Long?`

API请求中的超时请求配置。参考 [HttpTimeout][HttpTimeout] 中的相关说明。

默认为 `null`。

</def>
<def title="apiHttpConnectTimeoutMillis">

`Long?`

API请求中的超时请求配置。参考 [HttpTimeout][HttpTimeout] 中的相关说明。

默认为 `null`。

</def>
<def title="apiHttpSocketTimeoutMillis">

`Long?`

API请求中的超时请求配置。参考 [HttpTimeout][HttpTimeout] 中的相关说明。

默认为 `null`。

</def>
</deflist>

</def>
<def title="cache">

`CacheConfig?`

缓存相关配置。

```json
{
  "config": {
    "cache": {
      "transmit": {
        "enable": true
      }
    }
  }
}
```

有关 `transmit` 的详细描述，
请参考 `TransmitCacheConfig` 的文档注释或 API Doc。

</def>
<def title="disableWs" id="disableWs">

> 添加自 `4.1.0`

`Boolean`

是否禁用ws的连接。如果为 `true`, 则启动bot时不会创建 websocket 连接。

默认为 `false`。

```json
{
  "config": {
    "disableWs": false
  }
}
```

</def>

<def title="contentAsMarkdownAll">

`Boolean?`，自 `4.5.0` 起可用。

为频道子频道、频道私信、QQ群和 C2C 单聊四种发送目的地统一指定：是否将普通文本放入 Markdown 的 `content` 字段发送。默认不启用。

</def>
<def title="contentAsMarkdown">

`Map<MessageDestination, Boolean>?`，自 `4.5.0` 起可用。

按目的地覆盖 `contentAsMarkdownAll` 的设置。可用键为 `CHANNEL`、`DMS`、`GROUP` 和 `USER`，分别对应频道子频道、频道私信、QQ群与 C2C 单聊。

```json
{
  "config": {
    "contentAsMarkdownAll": true,
    "contentAsMarkdown": {
      "DMS": false,
      "USER": false
    }
  }
}
```

上述配置会让频道子频道和 QQ 群的普通文本按 Markdown 发送，而两类私信仍按普通文本发送。

</def>
<def title="retry">

`RetryConfig?`，自 `4.5.0` 起可用。用于为 API HTTP 客户端启用 Ktor 的 <a href="https://ktor.io/docs/client-request-retry.html">HttpRequestRetry</a> 插件。

<deflist type="wide">
<def title="maxRetries">

`Int?`。最大重试次数；只有此项非 `null` 时才会启用重试。

</def>
<def title="exponentialDelay">

`Boolean`，默认 `false`。为 `true` 时使用 Ktor 默认的指数退避策略。

</def>
<def title="retryOnServerErrors">

`Boolean`，默认 `false`。为 `true` 时重试服务器错误响应。

</def>
</deflist>

如果需要自定义重试条件、超时、日志或拦截器，请在代码配置 `ConfigurableBotConfiguration` 时调用 `apiClientAdditionalConfiguration { ... }`，其中接收的是 Ktor `HttpClientConfig`。

```kotlin
val configuration = ConfigurableBotConfiguration().apply {
    contentAsMarkdownAll()
    contentAsMarkdown[MessageDestination.DMS] = false

    apiClientAdditionalConfiguration {
        install(HttpRequestRetry) {
            maxRetries = 2
            retryOnServerErrors()
        }
    }
}
```

</def>
</deflist>
</def>
</deflist>

[HttpTimeout]: https://ktor.io/docs/timeout.html
