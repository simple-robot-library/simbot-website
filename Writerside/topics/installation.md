# 安装

simbot的核心功能由实现了 simbot-api 模块的内容提供。

## 使用核心库

核心库是最基础的对 simbot-api 的实现模块。

### 准备 {id='prepare-simbot-core'}

<snippet id="prepare-simbot-core-snippet">

准备一个 Kotlin 或 Java 项目。

- 如果是 Java 或 Kotlin/JVM 项目, 请确保 JDK 版本是 **JDK11** 或以上。
- 如果是 Kotlin 多平台项目, 可参考 [概述](outline.md#multiplatform-targets) 了解支持的平台。

</snippet>

### 安装核心库

<include from="refers.md" element-id="simbot-core-build"></include>

<tip>

如果你还不清楚 <code>simbot-api</code>、<code>simbot-core</code>、组件核心模块和公共库之间的区别，
可以先阅读 <a href="module-libraries.md">模块一览</a>。

</tip>

## 使用 Spring Boot

参考
<b><a href="Spring-Boot.md"></a></b>
了解更多。


## 安装组件库

<tooltip term="组件">组件库</tooltip>
是平台功能的主要提供者，是重要的核心概念之一。

前往
<a href="components-intro.md">组件库</a>
选择、添加你所需的组件库，并可以前往它们各自的手册了解更多信息。

## 使用快照

如果你打算使用某个库的快照版本，你需要配置快照仓库。

<tabs group="build">
<tab title="Gradle(Kotlin DSL)" group-key="kts">

```Kotlin
// 其他配置省略...

// 配置仓库
repositories {
    mavenCentral()
    // 额外添加快照仓库
    maven {
        url = uri("https://oss.sonatype.org/content/repositories/snapshots/")
        mavenContent {
            snapshotsOnly()
        }
    }
}

// 引用依赖
dependencies {
    // 使用快照版本
    implementation("要添加的依赖:name:xxx-SNAPSHOT")
}
```

</tab>
<tab title="Gradle(Groovy)" group-key="groovy">

```Groovy
// 其他配置省略...

// 配置仓库
repositories {
    mavenCentral()
    // 额外添加快照仓库
    maven {
        url = 'https://oss.sonatype.org/content/repositories/snapshots/'
        mavenContent {
            snapshotsOnly()
        }
    }
}

// 引用依赖
dependencies {
    // 使用快照版本
    implementation '要添加的依赖:name:xxx-SNAPSHOT'
}
```

</tab>
<tab title="Maven" group-key="maven">

```xml
<!-- 其他配置省略... -->

<!-- 配置快照仓库 -->
<repositories>
    <repository>
        <id>sonatype-snapshot</id>
        <name>Sonatype Snapshots Repository</name>
        <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </repository>
</repositories>

<!-- 引用依赖 -->
<dependency>
    <groupId>要添加的依赖</groupId>
    <artifactId>name</artifactId>
    <version>xxx-SNAPSHOT</version>
</dependency>
```

</tab>
</tabs>

快照的版本可以前往 [快照仓库](https://oss.sonatype.org/content/repositories/snapshots/love/forte/simbot/) 
根据坐标路径寻找。

比如：[`simbot-core` 的快照版本列表](https://oss.sonatype.org/content/repositories/snapshots/love/forte/simbot/simbot-core/)
以及它的 [maven-metadata.xml](https://oss.sonatype.org/content/repositories/snapshots/love/forte/simbot/simbot-core/maven-metadata.xml)。
