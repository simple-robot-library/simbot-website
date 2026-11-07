<primary-label ref="experimental" xmlns=""></primary-label>

# 自定义事件解析器

<note>

自 `v1.8.0` 起支持。

</note>

参考 [component-onebot#206](https://github.com/simple-robot/simbot-component-onebot/pull/206)

通过 `OneBotBotConfiguration.addCustomEventResolver(...)` 注册 `CustomEventResolver`，
可以根据原始事件的初步解析结果返回自定义的 simbot `Event`。解析器会按注册顺序执行，
第一个非 `null` 结果将作为事件使用。

解析器收到的 `Context` 提供当前 `bot`、JSON 解析器和 `rawEventResolveResult`。
返回 `null` 表示跳过当前解析器。所有解析器均未处理时，组件会继续尝试标准事件解析，
或使用未知事件兜底。

该 API 标记为 `ExperimentalCustomEventResolverApi`，Kotlin 中使用时需要选择加入。
也可以使用 `CustomKotlinSerializationEventResolver` 提供反序列化器。
解析器发生异常时，组件会记录异常并继续尝试其他解析器，具体处理可参考对应 API 注释。

有关未知事件和未支持事件的区别，参见 [](component-onebot-v11-event.md)。
