---
title: 2_9 switch 语句
aliases: [多分支选择]
tags:
  - 课程/C++
chapter: 2
section: 2_9
course: C++ 程序设计
type: note
status: draft
created: 2026-03-17
updated: 2026-03-17
parent_moc: "[[C++ 程序设计 MOC]]"
chapter_note: "[[2_第 2 章 C++ 基础语法入门]]"
prerequisites: []
related: []
review_level: 0
---

# 2_9 switch 语句

## 核心概念

- **switch 语句**：多分支选择结构，适合判断固定值的情况
- **case**：每个分支的标签
- **default**：默认分支（可选）
- **break**：防止穿透到下一个 case

## 原理理解

switch 语句语法：

```cpp
switch (表达式) {
    case 值 1:
        // 代码
        break;
    case 值 2:
        // 代码
        break;
    default:
        // 默认代码
}
```

switch vs if-else：

| 特性 | switch | if-else |
|------|--------|---------|
| 判断类型 | 只能是整数/字符/枚举 | 任意类型 |
| 分支数量 | 适合多分支 | 适合少分支 |
| 判断条件 | 只能判断相等 | 可以判断范围 |

## 代码示例

```cpp
#include <iostream>
using namespace std;

int main() {
    int day = 3;

    switch (day) {
        case 1:
            cout << "星期一" << endl;
            break;
        case 2:
            cout << "星期二" << endl;
            break;
        case 3:
            cout << "星期三" << endl;
            break;
        case 4:
            cout << "星期四" << endl;
            break;
        case 5:
            cout << "星期五" << endl;
            break;
        default:
            cout << "周末" << endl;
    }

    // switch 穿透示例（不使用 break）
    int level = 2;
    switch (level) {
        case 1:
            cout << "一级" << endl;
        case 2:
            cout << "二级" << endl;
        case 3:
            cout << "三级" << endl;
            break;
    }
    // 输出：二级 三级（穿透了）

    return 0;
}
```

## 易错点

- **忘记 break**：会导致穿透到下一个 case
- **case 后必须是常量**：不能是变量
- **漏掉 default**：可能导致无匹配时不执行任何代码

## 总结

switch 是多分支选择的简洁写法，适合判断固定值，注意每个 case 后要加 break 防止穿透。
