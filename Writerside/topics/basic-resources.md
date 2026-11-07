# 资源 Resource

`Resource` 用于表示一个可以读取**二进制**数据的资源，通常用于表示一个文件资源。

`Resource` 通常用于配合其他类型，
例如 [](basic-messages.md#标准消息元素-standardmessage) 中的图片类型。

## 获取

### Common

在全平台下，`Resource` 提供了部分通用类型。

<deflist>
<def title="ByteArray" id="ByteArray">

通过 `ByteArray` 直接构建一个 `Resource`。这是最基础最普通的 `Resource`,
没有什么资源读取，而是直接提供现成的字节数组。

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
val bytes: ByteArray = ...
val bytesResource = bytes.toResource()
```

</tab>
<tab title="Java" group-key="Java">

```java
var bytes = new byte[0];
var bytesResource = Resources.valueOf(bytes);
```

</tab>
</tabs>
</def>
<def title="File" id="File">

通过一个文件路径构建一个 `Resource`，也就是通过文件构建。

<note>

从 **v4.7.0** 开始基于 [kotlinx-io](https://github.com/Kotlin/kotlinx-io/)
增加在全平台下对文件系统的支持。

</note>

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
val fileResource1 = fileResource("/file/image.jpg")
val fileResource2 = fileResource("file", "image.jpg")
```

</tab>
<tab title="Java" group-key="Java">

```java
var fileResource1 = Resources.valueOfPath("/file/image.jpg");
var fileResource2 = Resources.valueOfPath("file", "image.jpg");
```

</tab>
</tabs>


</def>
</deflist>

### JVM

基于 JVM 的文件系统，在 JVM 平台下提供了更多可用的 `Resource` 类型实现。

<deflist>
<def title="File" id="Java-File">

基于 `java.io.File` 的 `Resource` 实现。

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
val file = File("sample.txt")
val resource = file.toResource()
```

</tab>
<tab title="Java" group-key="Java">

```java
var file = new File("sample.txt");
var resource = Resources.valueOf(file);
```

</tab>
</tabs>
</def>
<def title="Path" id="Java-Path">

基于 `java.nio.file.Path` 的 `Resource` 实现。

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
val path = Path("file.txt")
val resource = path.toResource()
```

</tab>
<tab title="Java" group-key="Java">

```java
var path = Paths.get("file.txt");
var resource = Resources.valueOf(path);
```

</tab>
</tabs>
</def>
<def title="URI" id="Java-URI">

基于 `java.net.URI` 和 `java.net.URL` 的 `Resource` 实现。

<tabs>
<tab title="Kotlin" group-key="Kotlin">

```kotlin
val uri = URI.create("file:///file.txt")
val url = uri.toURL()

val uriResource = uri.toResource()
val urlResource = url.toResource()
```

</tab>
<tab title="Java" group-key="Java">

```java
var uri = URI.create("file:///file.txt");
var url = uri.toURL();

var uriResource = Resources.valueOf(uri);
var urlResource = Resources.valueOf(url);
```

</tab>
</tabs>
</def>
</deflist>

