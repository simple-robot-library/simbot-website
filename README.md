# Simple Robot Documentation Website

这是 [Simple Robot](https://github.com/simple-robot/simpler-robot/tree/dev)
的手册网站。

## 文档版本

| 分支 | 文档版本 | 发布地址 | 维护范围 |
| --- | --- | --- | --- |
| `master` | 5.x | <https://simbot.forte.love/> | 当前版本 |
| `docs/v4` | 4.x | <https://simbot.forte.love/v4/> | 旧版，仅进行少量修正 |

4.x 从 `3a796218` 建立，保留核心 4.15.0、QQ 4.5.0、KOOK 4.4.0、OneBot 1.9.0 的文档。
两个分支沿用 `Writerside/s4` instance；`writerside.cfg` 的 `version` 固定为所属大版本，用于隔离搜索。
`versionName` 引用 `v.list` 中的完整依赖版本，当前分别为 `5.0.0-Alpha2` 和 `4.15.0`。

页头版本切换器共用根目录的 `help-versions.json`，发布时从两版构建产物的 `productVersionName` 自动生成。
升级 `v.list` 中的依赖版本后，下拉列表随下一次发布更新；`public/` 中的站点公共文件以 `master` 为准。
版本清单按旧版、当前版排列；当前前端会将紧随 `isCurrent` 条目的版本标为 EAP，因此当前版放在末尾。
4.x 显示旧版提示，并禁止搜索引擎收录；站内 Algolia 搜索仍可用，按 `product`、`version` 区分记录。
Algolia 的 `doc` 索引需将这两个字段配置为可搜索的 faceting 属性。

## 构建与发布

两个分支共用 `.github/workflows/build-documentation.yml` 中的构建、报告检查和产物准备流程。
PR 检查使用目标版本的 PR 合并结果及另一版本的维护分支；正式发布使用两个维护分支。
任一版本检查失败时停止本次发布，线上保留上一次成功发布的站点。

正式发布合并两份构建结果，一次上传 GitHub Pages：5.x 在根目录，4.x 在 `v4/`。
站点部署成功后，依次发布两版 Algolia 索引。Pages 发布共用一个并发组，避免两次发布相互覆盖。
两个分支的 Writerside 配置、公共文件或工作流发生变化时会触发发布。

当前 builder 会在生成的绝对 URL 中追加 instance 版本。
`.github/scripts/prepare-documentation.py` 将页面元数据、sitemap、LLM 文件和搜索记录中的该前缀
统一为实际发布地址，并检查版本、旧版 noindex 和渲染结果；Algolia 的版本字段保持为 `5.x`、`4.x`。

首次发布前，需先提交并推送 `docs/v4` 分支，再推送 `master` 中的迁移配置。
后续修改工作流时，应同步到两个分支。CI 只读取已推送的提交，本地 worktree 中未提交的修改不会参与线上构建。

本地构建可在任一文档 worktree 根目录执行，产物写到仓库外：

```shell
docker run --rm \
  -v "$PWD:/opt/sources" \
  -v /tmp/simbot-writerside-output:/opt/output \
  -e SOURCE_DIR=/opt/sources \
  -e MODULE_INSTANCE=Writerside/s4 \
  -e OUTPUT_DIR=/opt/output \
  -e RUNNER=other \
  jetbrains/writerside-builder:2026.10.0423
```

构建报告 `report.json` 也需通过检查；容器退出成功不能代替文档检查。

## License

```
    Copyright (C)  2024  ForteScarlet.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".
```
