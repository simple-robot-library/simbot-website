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

<warning>
非 JVM 平台（尤其是 native 平台）的
<code>Timestamp.now</code>
尚在实验中, 可能不稳定、或产生预期外的行为和结果。
</warning>

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

<note>

如果你需要的是日期时间格式化、时区换算等能力，
请在具体平台上配合对应日期 API 使用，
例如 JVM 上的 `java.time`。

</note>
