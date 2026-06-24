# 组件分发
<primary-label ref="doc-wip" />

组件要被应用发现并真正可用，主要有两条路径：

- 手动安装：在 `Application` 构建时显式 `install(Component.Factory)`、`install(Plugin.Factory)`。
- JVM 自动发现：通过 `ComponentFactoryProvider`、`PluginFactoryProvider` 配合 `META-INF/services` 或 `module-info.java` 暴露实现。

`QQ Guild`、`KOOK`、`OneBot11` 等官方组件也遵循这类分发方式。

## 最小交付单元

如果你要把一个组件真正“发布给别人使用”，至少要准备好下面几样东西：

<procedure title="组件分发最小清单">
<step>

一个可安装的 `Component` 及其 `ComponentFactory`。

</step>
<step>

如果组件带有 Bot 管理能力，再提供对应的 `Plugin` / `BotManager` 工厂。

</step>
<step>

把可序列化配置、消息元素等注册进 `serializersModule`。

</step>
<step>

在 JVM 环境中补齐 `ComponentFactoryProvider` / `PluginFactoryProvider` 的暴露方式。

</step>
</procedure>

## 标准组件参考

标准组件通常会同时准备几类入口：

- 组件工厂 Provider
- Bot 管理器或插件 Provider
- 可序列化 Bot 配置

一个很小的发布骨架通常会长这样：

```Kotlin
class FooComponentFactoryProvider : ComponentFactoryProvider<FooComponentConfiguration> {
    override fun loadConfigures(): Sequence<ComponentFactoryConfigurerProvider<FooComponentConfiguration>>? = null

    override fun provide(): ComponentFactory<*, FooComponentConfiguration> = FooComponent.Factory
}

class FooComponent : Component {
    override val id: String = "com.example.foo"
    override val serializersModule = SerializersModule { }

    companion object Factory : ComponentFactory<FooComponent, FooComponentConfiguration> {
        override val key: ComponentFactory.Key = object : ComponentFactory.Key {}
        override fun create(
            context: ComponentConfigureContext,
            configurer: ConfigurerFunction<FooComponentConfiguration>,
        ): FooComponent = FooComponent()
    }
}
```

```text
META-INF/services/love.forte.simbot.component.ComponentFactoryProvider
```

```text
com.example.foo.FooComponentFactoryProvider
```

## 为什么要暴露 serializersModule

组件分发不只是“让应用能 `install(...)` 到这个组件”。

对于组件体系来说，组件往往还负责把这些东西一起交给应用：

- Bot 配置文件的反序列化类型
- 组件特有消息元素
- 事件相关的序列化信息

如果这些类型没有进入组件的 `serializersModule`，
那么即使组件被安装成功，也可能在 Spring Boot 自动注册 Bot、
消息元素序列化、配置文件加载等环节失效。

最小写法一般只是把需要的序列化器放进去：

```Kotlin
override val serializersModule = SerializersModule {
    serializableBotConfigurationPolymorphic {
        subclass(FooBotConfiguration.serializer())
    }
    polymorphic(Message.Element::class) {
        subclass(FooMentionElement.serializer())
    }
}
```

## JVM 自动发现

如果你希望组件在 Spring Boot 一类环境中做到“加依赖即生效”，
那就不能只实现工厂，还需要暴露 Provider。

常见做法有两种：

- `META-INF/services/...`
- `module-info.java` 中的 `provides ... with ...`

两者的目标是一致的：
让运行时能够自动拿到你的 `ComponentFactoryProvider`
或 `PluginFactoryProvider`。

## 交叉参考

- [](component-dev-impl-component.md)
- [](component-dev-impl-plugin.md)
- [](component-dev-impl-bot-and-manager.md)

本页讨论的是一个组件库在“开发完成后，如何作为一个独立模块对外分发”的问题。

## 模块划分建议

对于一个较完整的组件库，通常至少会出现下面几类模块：

- `api/model`：原始协议请求、对象模型、事件模型
- `core`：真正作为 simbot 组件使用的主模块

普通开发者通常只会直接依赖 `core`，
因此 `core` 的对外 API 应当尽量稳定、清晰。

## 坐标与命名

组件库的命名最好在一开始就明确：

- 组件整体名称
- Maven 坐标中的 group / artifact
- `api` / `stdlib` / `core` 的命名层次

命名一旦对外发布，就尽量不要频繁调整。

## 发布前检查

在对外发布组件之前，建议至少确认下面几项：

<list type="decimal">
<li>核心模块可以单独作为依赖正常使用。</li>
<li>消息、事件、Bot 配置等公开模型具备稳定的序列化方案。</li>
<li>JVM 端的 Java 友好桥接示例已经补齐。</li>
<li>README、安装文档、快速开始、API 文档入口齐全。</li>
<li>版本号、兼容性说明、实验性标签已经明确标注。</li>
</list>

## 文档与样例

一个组件库如果准备对外分发，
除了产物本身，至少还应同时提供：

- 安装方式
- 最小启动示例
- Bot 配置说明
- 事件/消息核心能力示例
- 问题反馈与仓库入口
