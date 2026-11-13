# Git 原理笔记

> 写给零基础的人：Git 到底是怎么把文件"存起来"的。

## 一、三个核心概念

### HEAD
HEAD 就是"你现在在哪儿"的标记，它是 `.git/HEAD` 这个文件。平时它不直接写提交编号，而是写 `ref: refs/heads/main`，意思是"我跟着 main 分支走"。你切换分支时，改的就是 HEAD 里的这一行。

### refs（引用）
refs 是给提交起的"名字"，存在 `.git/refs/` 目录下，比如分支 `refs/heads/main`、标签 `refs/tags/v1.0`。每个 ref 本质上就是一个小文件，里面只写着一个提交的编号。分支之所以能"前进"，是因为每次提交后 Git 会把这个文件里的编号换成最新提交的编号。

### objects（对象）
objects 是 Git 真正存内容的地方，在 `.git/objects/` 目录下。一共有四种对象：commit（提交）、tree（目录）、blob（文件内容）、tag（附注标签）。所有历史、所有文件版本，最终都存成这些对象。

## 二、SHA 是什么

SHA 是 Git 给每个对象算出来的"指纹"，是一串 40 位的十六进制字符，比如 `6e0ba18a42492640e3e95ff407bdfd00baa91a97`。它是根据对象的内容计算出来的：内容一样，编号就一样；内容只要改一个字，编号就完全不同。平时只写前 7 位（如 `6e0ba18`）也能用，只要不和别的对象重复就行。

## 三、commit 里的四个字段

用 `git cat-file -p <提交编号>` 可以看到一个提交的原始内容：

```
tree 402805cc90f7b7e1f17edb1df5f97a428179b4cd
parent f9e5ceb949edfa7e2af785c67cacb4d3327d8f28
author 小玄子 <...> 1794479907 +0800
committer 小玄子 <...> 1794479907 +0800

docs: 修正 README 列表格式
```

### tree
tree 指向这次提交时整个项目根目录的"快照"。提交本身不装文件，它只说"我的目录长这样，请看这个 tree"。tree 里再列出有哪些文件和子文件夹。

### parent
parent 指向上一个提交，就像链条上的前一节。正是靠一个个 parent 连起来，Git 才有了"历史"。普通提交有 1 个 parent，合并提交有 2 个，仓库的第一个提交没有 parent。

### author
author 是"谁写的这段改动"，包括名字、邮箱、时间。后面那串数字（如 `1794479907`）是从 1970 年开始算的秒数，`+0800` 表示东八区（北京时间）。

### committer
committer 是"谁最后把这个提交放进仓库"，格式和 author 一样。平时两者相同；当你 rebase、cherry-pick 或修改（amend）别人的提交时，author 不变，committer 会变成你。

## 四、从 HEAD 到文件内容的完整链条

以本仓库为例，一步一步往下找：

1. **HEAD** → 打开 `.git/HEAD`，内容是 `ref: refs/heads/main`，说明当前在 main 分支。
2. **ref** → 打开 `.git/refs/heads/main`，里面是提交编号 `6e0ba18…`。
3. **commit** → `git cat-file -p 6e0ba18` 看到 `tree 402805cc…`，这就是项目根目录。
4. **tree** → `git cat-file -p 402805cc` 看到 `100644 blob 83246026…  README.md`，也就是 README.md 的内容存在这个 blob 里。
5. **blob** → `git cat-file -p 83246026` 就能直接打印出 README.md 的文字内容。

一句话总结：**HEAD → 分支 → 提交 → 目录（tree）→ 文件内容（blob）**。如果有子文件夹，就在 tree 里继续往下找下一层 tree，直到找到 blob 为止。
