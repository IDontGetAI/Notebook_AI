---
title: 2_9 switch 语句
aliases:
  - switch 语句
tags:
  - 课程/C++
  - C++/基础语法
chapter: 2
section: 2_9
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

# 2_9 switch 语句

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

### 一、switch语句

switch语句在实际编程中使用频率较低，但在特定场景下仍有一定应用价值。

#### 1.例题:switch语句演示

﻿

00:10

﻿

- switch语句执行机制为跳转逻辑：当变量grade值为'b'时，程序会直接跳转至case 'b'标签处开始执行
- break关键字的作用：若未添加break语句，程序会继续向下执行后续case语句，直至遇到break或switch语句结束
- default语句功能：当所有case条件均不匹配时，程序自动执行default部分的代码块

典型错误示例：注释掉break语句会导致程序连续执行多个case代码块，最终输出70-79和80-89两个区间结果。