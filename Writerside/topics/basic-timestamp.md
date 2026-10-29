# 时间戳 Timestamp

<tldr>
<p>针对“时间戳”的简单值包装类型, 
以屏蔽时间戳<control>不同单位</control>带来的影响。</p>
<p><control>不是</control>一种日期API, 而是类似于时间单位的转化。</p>
<p><control>平台：</control> 多平台实现</p>
</tldr>

## 创建

你可以使用 `Timestamp.now()` 获取当前的 Unix 时间戳值, 
或使用 `Timestamp.ofMilliseconds(...)` 基于毫秒值获取一个结果。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val now = Timestamp.now()
val time = Timestamp.ofMilliseconds(123456L)
```

</tab>
<tab  title="Java" group-key="Java">

```Java
var now = Timestamp.now();
var time = Timestamp.ofMilliseconds(123456L);
```

</tab>
</tabs>


## 使用

`Timestamp` 通常用于获取各种单位下的时间戳数值结果。
它是对“时间戳值”的统一包装，不负责日期格式化、时区转换或字符串解析。

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val milliseconds = timestamp.milliseconds
val seconds = timestamp.timeAs(TimeUnit.SECONDS)
```

</tab>
<tab  title="Java" group-key="Java">

```Java
long milliseconds = timestamp.getMilliseconds();
long seconds = timestamp.timeAs(TimeUnit.SECONDS);
```

</tab>
</tabs>

## 与 Kotlin 标准库时间类型转换

<secondary-label ref="since-5.0"/>

`Timestamp.now()` 通过 `kotlin.time.Clock.System` 获取当前时间，
也可以向 `Timestamp.now(clock)` 提供指定的 `Clock`。
这两种方式都返回基于 `kotlin.time.Instant` 的 `StandardInstantTimestamp`。
`Timestamp.ofMilliseconds(...)` 仍返回 `MillisecondTimestamp`。

通过 `Instant.toTimestamp()` 将标准库的时间点包装为 `Timestamp`，
通过 `Timestamp.toInstant()` 转回标准库时间点：

```Kotlin
import love.forte.simbot.common.time.Timestamp
import love.forte.simbot.common.time.Timestamp.Companion.toTimestamp
import kotlin.time.Clock

val timestamp = Clock.System.now().toTimestamp()
val instant = timestamp.toInstant()
val now = Timestamp.now(Clock.System)
```

Java 中对应使用 `Timestamp.of(instant)` 和 `timestamp.toInstant()`。
`StandardInstantTimestamp.toInstant()` 直接返回其持有的 `Instant`；
其他实现默认根据 `milliseconds` 转换。

<note>

如果你需要的是日期时间格式化、时区换算等能力，
请在具体平台上配合对应日期 API 使用，
例如 JVM 上的 `java.time`。

</note>
