<show-structure for="chapter,procedure" depth="3"/>

# 1. 实现 Bot

<note>

只建议使用 Kotlin 实现。Bot 包含 **挂起函数**，无法通过 Java 实现。

</note>

<procedure title="实现 Bot 的基本步骤">
   <step><a href="component-dev-impl-component.md">实现 <code>Component</code>。</a></step>
   <step>实现 <code>Bot</code>。</step>
   
</procedure>

<procedure title="Component">

因为 `Bot` 需要明确属于一个 `Component`，因此在这里，`Component` 是必须的了。

我们使用在
<a href="component-dev-impl-component.md" /> 
中介绍的 `FooComponent`，后续将不再赘述。

</procedure>

## 实现 Bot {id="impl-bot"}

`Bot` 从 `BotManager` 中创建，我们先来定义一个 `Bot` 的实现。

首先假设一下它的功能。
我们将其命名为 **`FooBot`**，并且假设它拥有与
**频道服务器(`Guild`)**、**子频道(`Channel`)**、**频道成员(`Member`)**
相关的能力。

我们假设它有一个字符串格式的唯一标识 `id`，并且需要再通过一个字符串格式的密码 `password` 进行登录。

### 定义 FooBot 接口 {id="def-bot-interface"}

<secondary-label ref="changed-5.0"/>

> 我们建议将接口的定义与实际的实现分开，并且仅对外暴露接口类型。
>
> 当然，这并非强制的，你也可以选择跳过接口定义这一环，直接编写实现类。

首先，定义接口 `FooBot` 并实现 `Bot`:

继承 `Bot` 需要选择加入 `InheritanceBotApi`。

```Kotlin
@OptIn(InheritanceBotApi::class)
interface FooBot : Bot {
    // 1️⃣
    override val coroutineContext: CoroutineContext
    override val isActive: Boolean
    override val isCompleted: Boolean
    override val isStarted: Boolean
    override fun onCompletion(handle: OnCompletion)
    @JvmSynthetic
    override suspend fun join()
    override fun cancel(reason: Throwable?)

    // 2️⃣
    @JvmSynthetic
    override suspend fun start()
    
    override val component: Component
    override val id: ID
    override val name: String

    override fun isMe(id: ID): Boolean

    override val contactRelation: ContactRelation?
    override val groupRelation: GroupRelation?
    override val guildRelation: GuildRelation?
}
```

上述代码中，**1️⃣** 以下的部分主要是跟协程、任务、任务状态与挂起相关，我们暂且忽略它，后续可以通过 `Job` 快捷的实现。
**2️⃣** 以下的部分则与 `Bot` 相关，是需要我们手动实现的。

### component

首先，我们来修改一下 `component` 属性的类型。因为我们上面说到过，这个实现属于 `FooComponent`，
因此修改为:

```Kotlin
interface FooBot : Bot {
    // 省略...
    
    val component: FooComponent
    
    // 省略...
}
```

### isMe(ID)

由于我们先前的假设，_"它有一个字符串格式的唯一标识 `id`"_ ，
那么 `FooBot` 中的 `isMe(ID)` 的实现就已经明确了：直接通过 `FooBot.id` 进行匹配即可，
不需要什么额外的逻辑。

```Kotlin
interface FooBot : Bot {
    // 省略...
    
    override fun isMe(id: ID): Boolean = id == this.id
    
    // 省略...
}
```

### 不支持的 relation {id="unsupported-relation"}

接下来，我们修改一下那三个 `*Relation` 的类型。上文我们提到，这个 Bot 仅支持频道那几个相关的功能，
而不支持**群聊(`Group`)**和**联系人(`Contact`)**，那么，我们先将这两个不支持的设置为始终为 `null`
来代表这些功能不被支持。

```Kotlin
interface FooBot : Bot {
    // 省略...
    
    /**
     * `FooBot` 不支持联系人相关的操作
     */
    override val contactRelation: ContactRelation?
        get() = null

    /**
     * `FooBot` 不支持群聊相关的操作
     */
    override val groupRelation: GroupRelation?
        get() = null
    
    // 省略...
}
```

<note title="补足说明">

对于不支持的功能，除了将返回值设置为 `null`, 别忘了添加一些友好且明确的说明，比如文档注释或标记 `@Deprecated`。

</note>

### 支持的 relation {id="supported-relation"}

接下来，准备实现我们支持的 `Relation`。首先先把那几个功能中需要支持的类型定义好：

- `FooGuild` 频道服务器
- `FooChannel` 子频道
- `FooMember` 频道成员

#### FooGuild

定义一个 `FooGuild`，让它实现 `Guild`。

```Kotlin
interface FooGuild : Guild {
    override val id: ID
    override val name: String
    
    /**
     * 获取所有 `FooChannel`
     */
    override val channels: Collectable<FooChannel>
    
    /**
     * `FooGuild` 中只有一种类型的 channel: `FooChannel`。
     * @see channels
     */
    override val chatChannels: Collectable<FooChannel>
        get() = channels

    /**
     * 查询 `FooChannel` 并得到结果，如果找不到则得到 `null`。
     */
    override suspend fun channel(id: ID): FooChannel?
    
    /**
     * `FooGuild` 中只有一种类型的 channel: `FooChannel`。
     * @see channel
     */
    override suspend fun chatChannel(id: ID): FooChannel? = channel(id)

    override val members: Collectable<FooMember>
    override val ownerId: ID?
    
    /**
     * `FooGuild` 不支持 Role 的获取，始终得到空的结果。 
     */
    override val roles: Collectable<Role>
        get() = emptyCollectable()

    @STP
    override suspend fun botAsMember(): FooMember
    
    @ST(blockingBaseName = "getMember", blockingSuffix = "", asyncBaseName = "getMember", reserveBaseName = "getMember")
    override suspend fun member(id: ID): FooMember?
}
```

并做如下假设:

- `FooGuild` 中只含有一种类型的 `Channel`: `FooChannel`，并且它本身实现 `ChatChannel`， 可代表为 **聊天频道**。
- `FooGuild` 的成员类型是 `FooMember`。
- `FooGuild` 没有针对 `Role` 的操作。

> 在真正的实现中，如果子频道有多种类型，那么就需要更细致的区分了。

<note>

可以注意到上述代码中我们在**挂起函数**上标记了一些注解，它们可能是 `@ST(...)` 或 `@STP`，
这便是编译器插件的应用。这些注解应当与它们重写的父函数上标记的一致，包括这其中的参数。

(参考 <a href="component-dev-compiler-plugin.md" />)

只有当挂起函数**没有返回值**，或返回值类型**没有变化**的时候，你可以选择直接用 `@JvmSynthetic` 来代替这几个编译器插件注解。
否则，你重写的返回值类型将无法在 Java 中被"看到"。

下文也会继续出现一些这些注解的应用，不要忘记了喔。

</note>

#### FooChannel

定义一个 `FooChannel`，让它实现 `ChatChannel`。

```Kotlin
interface FooChannel : ChatChannel {
    override val id: ID
    
    /**
     * `FooChannel` 没有分类。
     */
    override val category: Category?
        get() = null
        
    override val name: String

    @ST
    override suspend fun send(text: String): FooMessageReceipt
    @ST
    override suspend fun send(message: Message): FooMessageReceipt
    @ST
    override suspend fun send(messageContent: MessageContent): FooMessageReceipt
}
```

并做如下假设:

- `FooChannel` 没有分类(`Category`)。
- `FooChannel` 发送消息的返回值使用 `FooMessageReceipt` 类型。


#### FooMessageReceipt

定义一个 `FooMessageReceipt`，用来代表在 `FooXxx` 中发送消息的回执。

我们假设：回执中可以获取到消息发送后的 `id`, 以及可以根据ID删除它。

```Kotlin
class FooMessageReceipt(public val id: String) : MessageReceipt {
    @JvmSynthetic // 因为 delete 没有返回值，因此不需要使用 @ST 等编译器插件注解来覆盖实现
    override suspend fun delete(vararg options: DeleteOption) {
        val deleted = doDelete()
        // 如果成功，直接结束
        if (deleted) return

        // 没有成功，根据 options 来判断
        // 如果 options 要求忽略失败/错误的情况，则结束，否则抛出异常
        // 这里借助 standardAnalysis 来快捷的进行标准的判断
        val stdOpts = options.standardAnalysis()
        if (stdOpts.isIgnoreOnFailure) return

        // 没有要求忽略失败情况，则抛出异常
        throw DeleteFailureException("删除失败")
    }

    /**
     * 假设这里是用 id 删除消息的具体逻辑。
     * 比如通过 id 请求了一个 API。
     */
    private suspend fun doDelete(): Boolean {
        // TODO 实现根据ID删除消息的功能
        // 这里作为示例，直接返回 true
        return true
    }
}
```

> 如果是更为严谨的判断，那么在执行 `doDelete` 的时候还需要 `try-catch` 喔。

#### FooMember

定义一个 `FooMember`, 并实现 `Member`。

```Kotlin
interface FooMember : Member {
    override val id: ID
    override val name: String
    override val nick: String?
    override val avatar: String?

    @ST
    override suspend fun send(text: String): FooMessageReceipt
    @ST
    override suspend fun send(message: Message): FooMessageReceipt
    @ST
    override suspend fun send(messageContent: MessageContent): FooMessageReceipt
}
```

### FooGuildRelation

准备工作已经做好，接下来定义 `GuildRelation` 的实现类型 `FooGuildRelation`。

```Kotlin
interface FooGuildRelation : GuildRelation {
    override val guilds: Collectable<FooGuild>

    @ST(blockingBaseName = "getGuild", blockingSuffix = "", asyncBaseName = "getGuild", reserveBaseName = "getGuild")
    override suspend fun guild(id: ID): FooGuild?

    @STP
    override suspend fun guildCount(): Int
}
```

然后修改我们的 `FooBot` 接口，用 `FooGuildRelation` 类型替代 `GuildRelation`。

```Kotlin
interface FooBot : Bot {
    // 省略...
    
    override val guildRelation: FooGuildRelation
    
    // 省略...
}
```

> 因为明确支持 `Guild` 相关操作，所以返回值则不需要是 nullable 的了。

我们再来看看此时的 `FooBot` 的完整定义:

```Kotlin
interface FooBot : Bot {
    // 1️⃣
    override val coroutineContext: CoroutineContext
    override val isActive: Boolean
    override val isCompleted: Boolean
    override val isStarted: Boolean
    override fun onCompletion(handle: OnCompletion)

    @JvmSynthetic
    override suspend fun join()
    override fun cancel(reason: Throwable?)

    // 2️⃣
    @JvmSynthetic
    override suspend fun start()

    override val component: FooComponent
    override val id: ID
    override val name: String

    override fun isMe(id: ID): Boolean = id == this.id

    /**
     * `FooBot` 不支持联系人相关的操作
     */
    override val contactRelation: ContactRelation?
        get() = null

    /**
     * `FooBot` 不支持群聊相关的操作
     */
    override val groupRelation: GroupRelation?
        get() = null

    override val guildRelation: FooGuildRelation
}
```

### 实现 FooBot 接口 {id="impl-foo-bot"}

接下来，我们创建一个 `FooBotImpl`，来实现 `FooBot`。

先看结果：

```Kotlin
internal class FooBotImpl(
    override val id: ID,
    private val password: String,
    override val component: Component,
    /**
     * 要求其中必须有一个为当前 bot 准备的 Job。
     */
    override val coroutineContext: CoroutineContext
) : FooBot, JobBasedBot() {
    override val job: Job = coroutineContext[Job]!!

    // 用来登录时加锁
    private val startLock = Mutex()

    // 记录登录后的用户信息
    @Volatile
    private lateinit var userInfo: UserInfo

    override suspend fun start() {
        startLock.withLock {
            // 确保 Job 还存活
            job.ensureActive()

            // 执行登录逻辑, 并记录结果（用户信息）
            userInfo = doStart()
        }
    }

    private data class UserInfo(val username: String)

    private suspend fun doStart(): UserInfo {
        // TODO 这里假设使用 id 和 password 进行登录, 并得到一个包含用户名的用户信息
        //  比如通过请求一个 API 来实现登录

        // 这里仅做示例，因此返回一个假的结果
        return UserInfo("forte")
    }

    /**
     * 用户名。登录后才会得到，否则会抛出异常。
     */
    override val name: String
        get() = userInfo.username

    /**
     * 针对 FooGuild 的实现。
     * 一般来讲保存为始终如一的实例即可，
     * 没必要即用即造：GuildRelation 通常应当是不可变的。
     */
    override val guildRelation: FooGuildRelation = FooGuildRelationImpl()

    /**
     * 真正的 FooGuildRelation 内部实现，一般会将其隐藏
     *
     * 不一定必须使用 inner class 这种形式，能实现就好。
     */
    private inner class FooGuildRelationImpl : FooGuildRelation {
        override val guilds: Collectable<FooGuild>
            get() = TODO("查询频道服务器的集合，包装为 FooGuild 并返回")

        override suspend fun guild(id: ID): FooGuild? {
            TODO("根据ID查询指定的频道服务器，找不到的时候返回 null")
        }

        override suspend fun guildCount(): Int {
            TODO("查询所有频道服务器的数量，或者在没有 API 支持的情况下返回 -1")
        }
    }
}
```

首先可以观察到，`FooBotImpl` 实现了 `JobBasedBot`。这是一个辅助的抽象类，
它会根据一个 `Job` 类型来实现前文我们提到的那些 **1️⃣** 以下的那部分内容，比如 `join` 之类的。

因此接下来，我们只需要实现剩下的那些 **2️⃣** 部分的内容即可。
比如 **启动/登录(`start`)**、`guildRelation` 。
