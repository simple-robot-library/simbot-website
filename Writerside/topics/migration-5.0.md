# 5.0 更新与迁移

<primary-label ref="P_since-5.0"/>

当前 `5.x` 仍处于 alpha 阶段。本手册将 `5.0` 的 preview、alpha 等预发布版本中的更新统一标记为 `5.0`。
依赖示例使用实际发布版本 `%version%`。

## 模块与依赖

自 `5.0` 起，QQ、KOOK、OneBot 组件迁入
[Simple Robot 主仓库](https://github.com/simple-robot/simpler-robot)，随标准库统一版本发布。
原有组件版本号与标准库版本号不再分别维护。各模块说明参见 [](module-libraries.md)。

QQ 组件的 Maven 坐标由 `simbot-component-qq-guild-*` 调整为 `simbot-component-qq-*`，
groupId 仍为 `love.forte.simbot.component`。例如：

```Kotlin
implementation("love.forte.simbot.component:simbot-component-qq-core:%qg-version%")
```

Maven 或未使用 Kotlin Gradle 插件的 Java 项目应使用 `simbot-component-qq-core-jvm`。
旧坐标保留重定位发布；新项目和更新后的依赖声明应使用新坐标。
QQ 组件的包名仍使用 `qguild`，无需将其批量替换为 `qq`。

新增的 `simbot-component-qq-common` 存放共享常量与注解。
`Timestamp`、`TimeUnit` 等时间类型迁至 `simbot-common-time`，包名保持不变。
直接使用这些类型的公共库应声明相应模块依赖。

当前版本使用 Kotlin `%kt-version%`、Ktor `3.3.3`、kotlinx-coroutines `1.11.0`、
kotlinx-serialization `1.11.0`。项目中显式声明的依赖版本也应与之协调。

## 标准 API

| 内容 | 更新与迁移 |
| --- | --- |
| 消息发送与回复 | 新增带 `SendOption` / `ReplyOption` 的重载。具体选项由实现方扩展，参见 [](basic-messages.md#send-options)。 |
| 插件生命周期 | 新增 `CancellablePlugin` 与 `PluginAlreadyCancelledException`。`CloseablePlugin` 已移除，插件取消行为使用 `cancel(cause)`，参见 [](plugin.md#cancellable-plugin)。 |
| Application 取消 | `RequestCancel` 在取消任务前触发，`Cancelled` 在发起任务取消后触发；等待全部任务结束使用 `join()` 或 `onCompletion`，参见 [](basic-application.md#cancel)。 |
| Bot 继承 | 实现 `Bot` 需要选择加入 `InheritanceBotApi`。调用现有 Bot 的 API 无需因此添加此标记。 |
| 时间戳 | 新增 `Timestamp.now(clock)`、`Instant.toTimestamp()` 和 `Timestamp.toInstant()`，使用 Kotlin 标准库的 `kotlin.time.Clock` / `Instant`，参见 [](basic-timestamp.md)。 |
| 公共协程工具 | 新增 `Dispatchers.IOOrUnconfined` 与继续传播 `CancellationException` 的 `runCatchingCancellable(...)`。 |
| Java 响应式桥接 | 新增返回 `org.reactivestreams.Publisher` 的桥接方法，标记为 `ExperimentalReactiveBridgingApi`，参见 [](java-friendly.md#reactive-bridging)。 |
| 提及判断 | `EventMentionAware.isMention(event)` 返回 `false` 后继续常规判定，可继续检查消息中的 `At` 元素。 |

实验性、内部 API 和 Java 专用 API 等选择加入标记改为编译错误级别。
Kotlin 代码使用这些 API 时需要明确添加对应的 `@OptIn(...)`；例如 `ExperimentalSimbotAPI`、`Api4J`、
`ExperimentalQGApi` 和 `ExperimentalQGMediaApi`。

组件开发者实现带发送或回复选项的重载时，应自行解析选项。
标准接口的默认实现会委托到原有的不带选项的方法，具体实现未重写时会忽略选项。

## QQ 组件

### 新增能力

- 群基础信息查询、机器人群内状态查询和带群资料的 `QGGroupWithInfo`。
- 入群申请分页查询、接受与拒绝，以及拒绝理由和加入黑名单选项。
- 群与成员禁言状态查询、成员禁言的增加、更新和解除。
- C2C 自定义菜单、指令面板、群聊与 C2C 消息撤回。
- 附件的类型化属性和 `wasm-js` 平台支持。

对应说明见 [](component-qq-guild-QGGroup.md)、[](component-qq-guild-menu-panel.md)
和 [](component-qq-guild-messages.md)。

### 行为与类型变更

| 原有用法或类型 | 当前行为与迁移 |
| --- | --- |
| `QGGroup.botAsMember()` | 每次请求 QQ 平台，可能因权限或网络问题失败。返回成员的 ID 为群成员 OpenID；获取 AppID 使用 `bot.id`。需要原始状态时使用 `botAsMemberWithState()`。 |
| `QGGroupMember` | 新增所属群的 `groupId` 和禁言操作。自定义实现需要补齐新增成员。 |
| 自定义 `QGGroup`、`QGGroupMember`、`QGGroupAuthor` | 需要选择加入 `QGInternalInheritanceApi`，这些接口不保证外部实现的兼容性。 |
| `QQGuild` | 已废弃，常量迁至 `love.forte.simbot.qguild.common.QQ`。`QQ.URL` 是字符串；Ktor API 需要 `Url` 时使用 `Url(QQ.URL)`。 |
| QQ 专用注解 | `ApiModel`、`ApiModelConstructor`、`ExperimentalQGApi` 等迁至 `love.forte.simbot.qguild.common`；`QGApi4J` 改用 `love.forte.simbot.annotations.Api4J`。旧包下的兼容定义已废弃。 |
| 沙箱配置 | 默认 API 域名为 `https://api.bot.qq.com`。沙箱常量、配置入口已移除或废弃；Bot 文件中的 `"SANDBOX"` 仍按旧地址解析并输出警告，参见 [](component-qq-guild-bot-config.md)。 |
| `DeleteMessageApi` | 已废弃，使用 `DeleteChannelMessageApi`。群聊与 C2C 撤回分别使用 `GroupMessageDeleteApi` 和 `UserMessageDeleteApi`。 |
| QQ API 模型的 `data class` | 改为普通类，旧的 `copy()`、`componentN()` 兼容成员已废弃。创建请求模型优先使用已有的 builder、DSL 或工厂方法。 |
| `GroupAtMessageCreate.Author` / `GroupMessageCreate.Author` | 旧的公开构造函数以 `ERROR` 级别废弃，完整构造函数为 `internal`。测试或适配代码可通过序列化器解析事件数据；其他公开的事件构造入口使用 `EventModelConstructor` 标记。 |
| `QGAttachmentMessage` | 使用 `url`、`filename`、`size` 等类型化字段，旧构造函数、`properties`、`copy()`、解构方法及 `id` 已废弃。详见 [](component-qq-guild-messages.md#attachments)。 |

消息按钮、菜单、面板及部分论坛、日程 API 中的有限值参数改用 value class。
例如按钮的 `actionType` 使用 `MessageKeyboardActionType`，菜单项使用 `CustomMenuItemType`，
面板场景使用 `CommandPanelScope`。原始值可通过相应类型的 `of(...)` 包装。
从早期 `5.0` 预览版本迁移时，也需要更新菜单与面板的旧常量和类型名，参见
[](component-qq-guild-menu-panel.md)。

这些类型及构造签名的变化会影响 JVM 二进制兼容性。依赖旧版编译产物的应用和扩展库需要重新编译。
