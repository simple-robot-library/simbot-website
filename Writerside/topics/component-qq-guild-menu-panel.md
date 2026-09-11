---
switcher-label: JavaAPI风格
---
<show-structure for="chapter,procedure" depth="3"/>
<primary-label ref="P_qg-5.0"/>

# 自定义菜单与指令面板

自 `5.0` 起，QQ机器人组件支持管理 QQ 开放平台的自定义菜单和指令面板。两类能力通过 `QGBot` 提供的管理器访问。

<seealso>
<category ref="links">
<a ignore-vars="true" href="https://bot.q.qq.com/wiki/develop/api-v2/server-inter/menu-panel/">QQ 开放平台菜单与指令面板官方文档</a>
</category>
</seealso>

## 自定义菜单

自定义菜单是机器人 C2C 单聊窗口底部的全局菜单，只在 C2C 单聊中展示。
菜单由 `CustomMenu` 表示，一个菜单包含若干 `CustomMenu.Item`：

| 类型常量 | 说明 |
| --- | --- |
| `CustomMenu.Item.TYPE_SEND_MESSAGE` | 点击后将预设消息填入聊天输入框 |
| `CustomMenu.Item.TYPE_LINK` | 跳转到指定链接 |
| `CustomMenu.Item.TYPE_SWITCH` | 展示并操作一个开关 |
| `CustomMenu.Item.TYPE_MENU` | 包含二级菜单；二级菜单项支持发送消息或跳转链接 |

开关项通过 `switchId` 和 `defaultValue` 描述。组件不在本地校验菜单类型与字段组合，具体有效性由 QQ 服务端决定。

### 读取与更新

通过 `QGBot.customMenus` 获取 `QGCustomMenuManager`：

```Kotlin
val bot: QGBot = ...
val manager = bot.customMenus

val current = manager.get()
println("version=${current.version}, menu=${current.menu}")

val receipt = manager.update {
    item {
        name = "帮助"
        type = CustomMenu.Item.TYPE_SEND_MESSAGE
        sendMessage = "/help"
    }
    item {
        name = "文档"
        type = CustomMenu.Item.TYPE_LINK
        link = "https://example.com/docs"
    }
}
println("updated version=${receipt.version}")
```

`update(...)` 会整体覆盖当前菜单；从未设置菜单时，读取结果中的 `menu` 为 `null`。
`QGCustomMenuSnapshot` 和 `QGCustomMenuUpdateReceipt` 都保留底层 API 返回的 `source`，并提供服务端版本号。

Java 中可以使用生成的异步、阻塞或 `SuspendReserve` 形式：

```Java
var manager = bot.getCustomMenus();
var current = manager.getBlocking();
var receipt = manager.updateBlocking(CustomMenu.parse(json));
System.out.println(receipt.getVersion());
```

### 自定义菜单互动

用户操作自定义菜单时，平台会推送 `INTERACTION_CREATE` 事件。
此时互动类型为 `12`，组件事件中的 `QGInteractionCreateEvent.type` 也会返回 `12`；
解析后的菜单项标识位于 `event.resolved.featureId`。
互动事件仍需要通过 `event.respond(...)` 回应，详见 [](component-qq-guild-event-list.md#interaction-events) 。

对于开关菜单项，C2C 消息事件中的 `messageScene` 会携带场景信息，开关操作结果位于 `messageScene.ext`。
`ext` 是 `key=value` 形式的字符串列表；上游未提供场景信息时，`messageScene` 为 `null`。

## 指令面板

指令面板用于在会话中展示指令或链接。一个面板最多配置 20 个元素；元素类型由
`CommandPanel.Item.TYPE_COMMAND` 和 `CommandPanel.Item.TYPE_LINK` 表示。
`command` 类型在用户点击后将名称填入聊天输入框，`link` 类型用于跳转链接。
元素还可以设置描述和 `onlyAdmin`；名称最多 14 个字符，描述最多 30 个字符。
面板备注最多 255 个字符，仅供开发者标记用途，不会展示给用户。

面板的生效场景由 `QGCommandPanelScope` 表示：

| 场景 | 说明 |
| --- | --- |
| `C2C` | C2C 单聊 |
| `GROUP` | QQ 群聊 |
| `CHANNEL` | 文字子频道 |
| `DM` | 频道私信 |

目标范围由 `QGCommandPanelTargetType` 表示。`ALL` 对场景中的所有目标生效，`SPECIFIC` 只对指定用户或群生效。
只有 `C2C` 和 `GROUP` 支持 `SPECIFIC`；`CHANNEL` 和 `DM` 只能使用 `ALL`。

### 创建、读取与分页查询

通过 `QGBot.commandPanels` 获取 `QGCommandPanelManager`：

```Kotlin
val bot: QGBot = ...

val handle = bot.commandPanels.create {
    scope = QGCommandPanelScope.GROUP.value
    targetType = QGCommandPanelTargetType.ALL.value
    panel {
        remark("常用指令")
        item {
            name = "/help"
            desc = "查看帮助"
            type = CommandPanel.Item.TYPE_COMMAND
            onlyAdmin = false
        }
        item {
            name = "项目主页"
            desc = "打开项目网站"
            type = CommandPanel.Item.TYPE_LINK
            link = "https://example.com"
        }
    }
}

// 创建接口只返回面板 ID；需要完整内容时再主动查询详情。
val record = handle.get()
println("${record.id}: ${record.panel}")

// 按场景获取面板。Collectable 是冷的，开始收集时才会发起请求。
bot.commandPanels.list(QGCommandPanelScope.GROUP)
    .asFlow()
    .collect { panel -> println(panel.id) }
```

`create(...)` 返回只携带面板 ID 的 `QGCommandPanelHandle`，不会隐式查询详情。
也可以使用 `commandPanels.handle(panelId)` 创建同样的句柄；该操作本身不产生请求。

`list(...)` 默认自动根据 `next_cursor` 分页，直到服务端标记结束。
服务端每页默认返回 20 条，最多返回 50 条；如果只需要一页，将 `autoPagination` 设置为 `false`，
也可以传入 `startCursor` 和 `limit`。
由于结果基于冷流，只有开始收集 `Collectable` 时才会真正请求 QQ API。

### 修改关联目标与删除

`QGCommandPanelHandle` 表示一个面板及其操作行为：

- `update(...)` 整体覆盖面板元素和备注，不修改关联目标，并返回更新后的版本号。
- `addUserTargets(...)`、`removeUserTargets(...)` 管理 C2C 用户目标。
- `addGroupTargets(...)`、`removeGroupTargets(...)` 管理群聊目标。
- `delete(...)` 删除面板；成功时返回 `Unit`，不会自动查询或缓存删除后的状态。

关联目标操作对应 `QGCommandPanelTargetOperation.ADD` 和 `DEL`。
创建时每类目标列表一次最多可以传入 20 个用户或群 OpenID；关联目标的具体合法性由 QQ 服务端校验。

```Kotlin
val handle: QGCommandPanelHandle = ...

handle.update {
    remark("更新后的备注")
    item {
        name = "/status"
        type = CommandPanel.Item.TYPE_COMMAND
    }
}

handle.addUserTargets(listOf("user-openid".ID))
handle.addGroupTargets(listOf("group-openid".ID))
handle.removeUserTargets(listOf("user-openid".ID))
handle.delete()
```

Java 中可以使用对应的生成方法，例如：

```Java
var manager = bot.getCommandPanels();
var panel = CommandPanel.builder().build();
var handle = manager.createBlocking(
        QGCommandPanelScope.GROUP.getValue(),
        QGCommandPanelTargetType.ALL.getValue(),
        null,
        null,
        panel
);
var record = handle.getBlocking();
handle.updateBlocking(panel);
handle.deleteBlocking();
```

面板列表记录 `QGCommandPanelRecord` 是查询时的瞬时快照，提供原始的 `scopeValue`、`targetTypeValue`、
枚举形式的 `scope`、`targetType`、面板配置和版本号。列表查询通常不返回 `userOpenids` 与 `groupOpenids`，
详情查询才会在适用时返回它们。
