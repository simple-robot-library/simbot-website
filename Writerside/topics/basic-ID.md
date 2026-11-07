# 唯一标识 ID

<tldr>

<p>一个针对“唯一标识”的简单值包装类型, 
用以屏蔽不同类型的ID之间的差异。</p>
<p><control>平台：</control> 多平台实现</p>

</tldr>

## 唯一标识类型

`ID` 是一个密封类型, 提供了如下几种类型的实现类型：

- `StringID`
- `UUID`
- `IntID`
- `LongID`
- `UIntID`
- `ULongID`

并可将它们简单的归类为：

- 字符串类型
- 数字类型
    - 有符号数字类型
    - 无符号数字类型

## 创建实例

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

在 Kotlin 中, 你可以使用扩展属性 `xxx.ID` 来构建对应类型的 `ID` 实例。

```Kotlin
val strID: StringID = "1".ID
val iID: IntID = 1.ID
val lID: LongID = 1L.ID
val uiID: UIntID = 1u.ID
val ul: ULong = 1u
val ulID: ULongID = ul.ID
```

对于 `UUID` 你可以：

- 使用 `UUID.random(...)` 获取一个随机值。
- 使用一个长度为 `16` 的 `ByteArray` 构建它。
- 使用两个分别代表高低位的 `Long` 构建它。
- 在 JVM 平台中使用 `java.util.UUID` 进行转化。

<br/>

```Kotlin
val uuid = UUID.random()
```

</tab>
<tab  title="Java" group-key="Java">

在 Java 中，你可以使用 `Identifies` 的工厂方法构建对应类型的 `ID` 实例。

```Java
var intID = Identifies.of(1);
var longID = Identifies.of(1L);
var uLongID = Identifies.ofULong(1);
var uIntID = Identifies.ofUInt(1);
var strID = Identifies.of("1");
var uuid = Identifies.uuid(); // random
```

</tab>
</tabs>

## 字面值

所有的ID实现类型的 `toString` 都会直接输出它们的“字面值”。
例如：

<tabs group="Code">
<tab title="Kotlin" group-key="Kotlin">

```Kotlin
val intId = 1.ID
val strId = "1".ID

println(intId) // 1
println(strId) // 1
```

</tab>
<tab  title="Java" group-key="Java">

```Java
var intID = Identifies.of(1);
var strID = Identifies.of("1");

System.out.println(intID); // 1
System.out.println(strID); // 1
```

</tab>
</tabs>

## 序列化

`ID` 基于 `kotlinx-serialization` 实现对其的序列化, 
且序列化的值是一个非结构化的**字面值**。

```Kotlin
@Serializable
data class Foo(val value: UIntID)
// 序列化结果: {"value": 123456}
```

## 其他注意事项

### equals 与 hashCode

`ID` 的所有类型均允许互相通过 `equals` 判断是否具有相同的**字面值**。
`equals` 实际上不会判断类型, 因此如果两个不同类型的 `ID` 的字面值相同, 
例如值为 `"1"` 的 `StringID` 和值为 `1` 的 `IntID`, 它们之间使用 `equals` 会得到 `true`。

如果你希望严格匹配两个 `ID` 类型, 那么使用 `equalsExact`。

在**不同类型**的两个 `ID` (例如 `StringID` 和 `IntID` ) `equals` 结果为 `true`
的情况下, 它们的 `hashCode` 则可能是**不同**的。
因此, 不适合将不同类型的 `ID` 混用于诸如 hash key 的地方。

### 数字的符号

在 Java 中使用数字ID时, 需要注意无符号ID类型与有符号ID类型之间的差异。
一个相同的数值, 使用无符号类型和有符号类型的ID构建的结果可能是不同的, 
获取到的 `value` 和字面值也可能是不同的。

Java在操作无符号ID的时候需要注意使用相关的无符号API。 以 `long` 为例：

```Java
long value = -1;

LongID longID = Identifies.of(value);
ULongID uLongID = Identifies.ofULong(value);

System.out.println(longID);  // 字面值：-1
System.out.println(uLongID); // 字面值：18446744073709551615

System.out.println(longID.getValue());  // value 数值：-1
System.out.println(uLongID.getValue()); // value 数值：-1
```

如果希望得到一些符合预期的结果, 你应该使用Java中的无符号相关API：

```Java
long value = Long.parseUnsignedLong("18446744073709551615");
ULongID uLongID = Identifies.ofULong(value);
System.out.println(uLongID); 
// 字面值：18446744073709551615
System.out.println(Long.toUnsignedString(uLongID.getValue()));
// 经转化的 value 数值： 18446744073709551615
```


