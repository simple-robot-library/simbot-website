# 未知事件与未支持事件

组件会通过 `UnsupportedKookEvent` 推送尚未提供专门组件事件实现的事件。
它提供解析后的 `sourceEvent` 和原始 JSON `sourceEventRaw`。
随着组件支持更多事件，同一事件可能改由专门的事件类型推送。

API 层的 `UnknownExtra` 用于承载无法匹配现有 extra 类型的数据。
可先在 [](component-kook-event-list.md) 中查找已有事件类型。

<include from="component-kook-KookBot.md" element-id="need-help"/>
