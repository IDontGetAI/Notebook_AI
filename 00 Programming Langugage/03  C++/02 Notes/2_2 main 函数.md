---
title: 2_2 main 函数
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

# 2_2 main 函数

## 所属导航
- 总目录：[[C++ 程序设计 MOC]]
- 章节：[[2_第 2 章 C++ 基础语法入门]]


## 相关知识
- [[1_8 操作系统是计算机管理员]] - 程序运行机制
- [[2_1 头文件 iostream]] - 基本程序结构
- [[2_3 常量 Constant]] - 数据类型
- [[3_6 函数]] - 函数详细知识

---

## 核心概念
- **main函数**：程序执行的入口点，操作系统通过调用main函数启动程序
- **唯一性**：程序只能有一个main函数，否则操作系统无法确定调用哪个
- **程序生命周期**：main函数开始执行 -> 程序运行 -> main函数结束 -> 程序终止

```cpp
// 标准形式
int main() {
    // 程序代码
    return 0;  // 返回0表示正常结束
}

// 带参数形式
int main(int argc, char* argv[]) {
    // argc: 参数个数
    // argv: 参数数组
    return 0;
}
```

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "程序开始执行" << endl;
    // 程序逻辑
    cout << "程序即将结束" << endl;
    return 0;  // 向操作系统返回状态码
}
```

## 运行结果 / 现象


```
程序开始执行
程序即将结束
```

## 原理理解

- **操作系统视角**：操作系统不识别"程序"概念，仅视为对main函数的调用
- **入口唯一性**：main函数是程序执行的唯一入口和出口
- **跨语言共性**：
  - C/C++：`int main()`
  - Java：`public static void main(String[] args)`
  - Python：隐含main机制（`if __name__ == "__main__"`）

## 易错点

- **重复定义**：程序中只能有一个main函数，重复定义会导致编译错误

- **忘记返回值**：虽然现代编译器允许省略，但建议显式写 `return 0;`

- **返回值含义**：返回0通常表示成功，非0表示错误（具体值可自定义）


## 我的理解

main函数是程序与操作系统的桥梁，操作系统只认main函数。理解这一点对理解程序生命周期和操作系统原理非常重要。

## 一句话总结

main函数是程序的唯一入口，操作系统通过调用它启动程序，程序运行期间main函数内的代码依次执行，返回后程序终止。

---


