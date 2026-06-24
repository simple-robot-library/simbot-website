# Bot配置文件

<primary-label ref="doc-wip" />

<include from="refers.md" element-id="doc-TODO"></include>

> 注释实际上是不支持的，
> 如果要复制，记得清理掉注释

```json
{
    "component": "simbot.telegram",
    "ticket": {
        // 你的*完整的*Bot Token, 别忘了前面的'bot'
        "token": "bot123456789:aaaabbbbcccc"
    },
    // 一些可选地属性，config以及里面的属性都是可选的，且基本上默认为 `null`。
    "config": {
        "server": null,
        "proxy": null,
        "longPolling": null
    }
}
```

如果你希望通过长轮询的方式达成主动 **_订阅_** 事件的效果，
记得配置 `longPolling`.

```json
{
    "component": "simbot.telegram",
    "ticket": {
      // 你的*完整的*Bot Token, 别忘了前面的'bot'
      "token": "bot123456789:aaaabbbbcccc"
    },
    // 一些可选地属性，config以及里面的属性都是可选的，且基本上默认为 `null`。
    "config": {
        "server": null,
        "proxy": {
          "type": "http",
          "url": "http://localhost:7790"
        },
        //配置长轮询来'订阅'事件
        "longPolling": {
            // 长轮询内部的每次事件接收量上限
            "limit": 100
        }
    }
}
```

## 属性描述

<deflist>
<def title="component">

固定值 `simbot.telegram`，**必填**，代表此配置文件为Telegram组件的。

</def>
<def title="ticket">

bot的票据信息，是进行API请求的凭证，必填。

```json
{
  "ticket": { "token": "bot123456789:aaaabbbbcccc" }
}
```

<deflist>
<def title="token">

你的 **完整的** Bot Token, 别忘了前面的 `bot` 。

</def>
</deflist>

</def>
<def title="config">

其他可选配置。大部分属性和其本身都是可选的。

```json
{ "config": null }
```

```json
{ "config": {} }
```

<deflist>
<def title="server">

`String` 类型，API请求时使用的服务器地址。

默认为 `https://api.telegram.org`, 也就是 Telegram 的官方API地址。

```json
{
  "config": {
    "server": null
  }
}
```

</def>
<def title="proxy">

`ProxyConfiguration`，代理配置。

如果不为 `null`，会为内部使用的 `HttpClient` 配置代理。
根据 `type` 值的不同有不同的可配置项。

<deflist>
<def title="type='http'">

http代理，使用 `url` 配置代理地址。

```json
{
  "config": {
    "proxy": {
      "type": "http",
      "url": "http://127.0.0.1:7790"
    }
  }
}
```

</def>
<def title="type='socks'">

socks代理，使用 `host` 和 `port` 配置代理地址。

```json
{
  "config": {
    "proxy": {
      "type": "socks",
      "host": "127.0.0.1",
      "port": 7790
    }
  }
}
```

</def>
</deflist>
</def>
<def title="longPolling">

Telegram 的 [长轮询](https://core.telegram.org/bots/api#getupdates) 
配置。

配置 `longPolling` 可以主动拉取事件，以达到类似于 “事件订阅” 的效果。

```json
{
  "config": {
    "longPolling": null
  }
}
```

```json
{
  "config": {
    "longPolling": {
      "limit": 100,
      "timeout": 1800,
      "allowedUpdates": null,
      "retry": null
    }
  }
}
```

**默认为 `null`**，即不进行长轮询。

<deflist>
<def title="limit">

每次轮询拉取的最大事件数量。默认为 `null`, 使用 API 服务器的默认值 `100` 。

```json
{
  "config": {
    "longPolling": {
      "limit": 100,
    }
  }
}
```
</def>
<def title="timeout">

每次长轮询的超时时间，单位秒。默认 `1800`，即30分钟。

```json
{
  "config": {
    "longPolling": {
      "timeout": 1800,
    }
  }
}
```
</def>
<def title="allowedUpdates">

拉取的时间类型，字符串数组，默认为 `null`。
为 `null` 时拉取所有类型的事件。

```json
{
  "config": {
    "longPolling": {
      "allowedUpdates": ["message", "edited_channel_post"],
    }
  }
}
```

</def>
<def title="retry">

`LongPolling.Retry` 类型，为 `HttpClient` 配置重试。

与 `handleRetry` 不同，`retry` 是基于 Ktor 的 
[HttpRequestRetry](https://ktor.io/docs/client-request-retry.html#install_plugin)
插件实现的，发生在 HttpClient 内部。

所有属性不可为 `null`，但均可选，不配置则使用默认值。

<deflist>
<def title="maxRetries">

最大重试次数，默认`3` 。
</def>
<def title="delayMillis">

重试间隔，毫秒。默认`5000` 。
</def>
<def title="isDelayMillisMultiplyByRetryTimes">

重试间隔是否递增。默认 `false` 。
</def>
</deflist>

```json
{
  "config": {
    "longPolling": {
      "retry": {
        "maxRetries": 3
        "delayMillis":5000
        "isDelayMillisMultiplyByRetryTimes": false
      }
    }
  }
}
```

</def>
<def title="handleRetry">

`LongPolling.HandleRetry`, 类型，当拉取事件过程中产生异常时候的重试策略。

与 `retry` 不同，`handleRetry` 是对一次整个API请求（长轮询）
的过程进行异常捕获，并根据策略 `strategy` 来决定是否继续尝试轮询。

此配置及其属性不可为 `null`，但可选，不配置则使用默认值。
默认使用策略 `TIMEOUT_ONLY`，即只有出现了
`io.ktor.client.plugins.HttpRequestTimeoutException`
才会忽略异常重新拉取。

<deflist>
<def title="strategy">

`LongPolling.HandleRetryStrategy` 枚举类型，可选值：

<deflist style="medium">
<def title="NONE">遇到任何错误都会抛出异常、终止bot。</def>
<def title="TIMEOUT_ONLY">

如果遇到 
`io.ktor.client.plugins.HttpRequestTimeoutException`
则重新拉取，否则抛出异常、终止bot。

</def>
<def title="ALL">

遇到任何异常 (除了 `kotlinx.coroutines.CancellationException`)
都会继续重试。

</def>
</deflist>
</def>
<def title="delayMillis">

每次重试之间等待的时间，单位毫秒，默认为 `5000`。

> 等待时间在出现
> `io.ktor.client.plugins.HttpRequestTimeoutException`
> 时无效，因为超时异常算是一种长轮询中的预期内异常，通常不需要等待。

</def>
</deflist>

```json
{
  "config": {
    "longPolling": {
      "handleRetry": {
        "strategy": "TIMEOUT_ONLY",
        "delayMillis": 5000
      }
    }
  }
}
```

</def>

</deflist>

</def>
</deflist>

</def>
</deflist>
