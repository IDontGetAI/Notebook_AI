---
title: 2_8 break 和 continue 关键字
aliases: [循环控制]
tags:
  - 课程/C++
chapter: 2
section: 2_8
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

# 2_8 break 和 continue 关键字

## 核心概念

- **break**：立即终止整个循环
- **continue**：跳过本次循环剩余代码，进入下一次循环

## 原理理解

break vs continue 对比：

| 关键字 | 作用 | 使用场景 |
|--------|------|----------|
| **break** | 跳出整个循环 | 找到目标后提前结束 |
| **continue** | 跳过本次迭代 | 某些情况不需要处理 |

## 代码示例

```cpp
#include <iostream>
using namespace std;

int main() {
    // break 示例：找到第一个能被 3 整除的数
    cout << "break 示例：" << endl;
    for (int i = 1; i <= 10; i++) {
        if (i % 3 == 0) {
            cout << "找到 " << i << "，跳出循环" << endl;
            break;  // 跳出整个循环
        }
        cout << i << " ";
    }

    // continue 示例：跳过偶数
    cout << "\ncontinue 示例：" << endl;
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;  // 跳过偶数
        }
        cout << i << " ";
    }

    return 0;
}
```

## 运行结果

```
break 示例：
1
2
找到 3，跳出循环

continue 示例：
1 3 5 7 9
```

## 易错点

- **break 与 continue 混淆**：break 是结束循环，continue 是跳过本次
- **在 if 外使用**：break 和 continue 只能在循环或 switch 中使用

## 总结

break 用于提前终止循环，continue 用于跳过当前迭代，两者都是循环控制的重要工具。
