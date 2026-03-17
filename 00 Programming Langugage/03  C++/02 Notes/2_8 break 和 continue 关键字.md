---
title: 2_8 break 和 continue 关键字
aliases:
  - break 和 continue
tags:
  - 课程/C++
  - C++/基础语法
chapter: 2
section: 2_8
course: C++ 程序设计
type: note
status: unfinished
created: 2026-03-17
updated: 2026-03-17
parent_moc: "[[C++ 程序设计 MOC]]"
chapter_note: "[[2_第 2 章 C++ 基础语法入门]]"
prerequisites: []
related: []
review_level: 0
---

# 2_8 break 和 continue 关键字

## 所属导航
- 总目录：[[C++ 程序设计 MOC]]
- 章节：[[2_第 2 章 C++ 基础语法入门]]

## 前置知识
-

## 相关知识
-

---

## 核心概念
-

## 语法定义
```cpp
```

## 示例代码

```cpp
```

## 运行结果 / 现象

*

## 原理理解

*

## 易错点

*

## 面试 / 考试常见问法

*

## 练习题

*

## 我的理解

*

## 一句话总结

*

---

## 复习

* 掌握程度：
* 是否需要重看视频：
* 下次复习时间：

## 反向链接关注点

> 以后可从这些主题回链到本笔记

*



-- 以下为AI生成的文稿笔记内容 --

### 一、课前回顾

在循环结构中，break和continue是两个关键控制语句。break用于立即终止当前循环，而continue用于跳过当前循环的剩余部分并进入下一次循环迭代。

### 二、break关键字

﻿

00:24﻿

以下代码演示了break的执行逻辑：

a = 0

for i in range(3):

if i == 1:

break

a += i

执行过程分析：

- 初始状态：i = 0，a = 0
- 第一次循环：i = 0不满足i == 1，执行a += 0（a仍为0），i自增为1
- 第二次循环：i = 1触发break，直接跳出循环 - 最终结果：a = 0，i = 1

### 三、continue关键字

﻿

02:57﻿

以下代码演示了continue的执行逻辑：

a = 0

for i in range(3):

if i == 1:

continue

a += i

执行过程分析：

- 初始状态：i = 0，a = 0
- 第一次循环：i = 0不满足i == 1，执行a += 0（a仍为0），i自增为1
- 第二次循环：i = 1触发continue，跳过本次循环剩余代码，i自增为2
- 第三次循环：i = 2不满足i == 1，执行a += 2（a变为2），i自增为3
- 循环终止：i = 3不满足i < 3
- 最终结果：a = 2