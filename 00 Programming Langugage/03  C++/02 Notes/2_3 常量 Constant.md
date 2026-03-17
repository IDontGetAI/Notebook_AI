---
title: 2_3 常量 Constant
aliases: []
tags:
  - 课程/C++
chapter: 2
section:
course: C++ 程序设计
type: note
status: finished
created: 2026-03-17
updated: 2026-03-17
parent_moc: "[[C++ 程序设计 MOC]]"
chapter_note: "[[2_第 2 章 C++ 基础语法入门]]"
prerequisites: []
related: []
review_level: 0
---

# 2_3 常量 Constant

## 所属导航
- 总目录：[[C++ 程序设计 MOC]]
- 章节：[[2_第 2 章 C++ 基础语法入门]]


## 相关知识
- [[2_2 main 函数]] - 程序基本结构
- [[2_4 变量的 4 大特性]] - 变量概念
- [[2_5 基本运算符]] - 运算符
- [[3_5 字符串]] - 字符串详细知识

---

## 核心概念
- **常量（Constant）**：固定不变的值，程序运行期间不能修改
- 常量同样具有数据类型

```cpp
// 字面常量
int a = 1;           // 整型常量
float b = 3.14f;     // 单精度浮点型（需加f后缀）
double c = 3.14;     // 双精度浮点型（默认）
char d = 'x';        // 字符常量（单引号）

// 常量变量（const关键字）
const int MAX = 100;  // 声明后不可修改
```

```cpp
#include <iostream>
using namespace std;

int main() {
    // 字面常量
    int a = 1;
    float b = 3.14f;
    double c = 3.14;
    char ch = 'x';

    // const常量
    const int MAX_SIZE = 100;
    // MAX_SIZE = 200;  // 错误！无法修改const变量

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "MAX_SIZE = " << MAX_SIZE << endl;

    return 0;
}
```

## 运行结果 / 现象


```
a = 1
b = 3.14
MAX_SIZE = 100
```

## 原理理解

- **int 与 long**：在C++中占用相同内存（4字节），但历史原因导致命名不同
- **浮点数默认类型**：常量 `3.14` 默认为 `double`，需显式添加 `f` 后缀声明为 `float`
- **字符与字符串区别**：
  - `'x'` 是字符常量（单引号），占1字节
  - `"x"` 是字符串常量（双引号），占2字节（含 `\0`）
  - 不可直接赋值互换

## 易错点

- 混淆 `float` 和 `double` 的默认类型

- 字符与字符串赋值混用：`char a = "x"` 会导致编译错误

- 尝试修改 `const` 常量会触发编译错误

- 忘记浮点常量的 `f` 后缀可能导致精度损失警告


## 我的理解

常量是程序中的固定值，理解常量的类型对避免类型转换错误很重要。`const` 关键字用于保护不应该被修改的值。

## 一句话总结

常量具有类型（整型、浮点型、字符型、字符串），浮点常量默认为double需加f后缀声明float，字符用单引号字符串用双引号，const关键字用于声明不可修改的常量变量。

---

---


