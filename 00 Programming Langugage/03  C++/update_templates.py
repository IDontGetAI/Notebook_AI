#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 C++ 笔记文件以匹配新模板格式"""

import os
import re

def update_frontmatter(content, filename):
    """更新 frontmatter 部分"""
    # 提取 title
    title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename.replace('.md', '')

    # 提取 chapter
    chapter_match = re.search(r'^chapter:\s*(\d+)$', content, re.MULTILINE)
    chapter = chapter_match.group(1) if chapter_match else ""

    # 提取 chapter_note
    chapter_note_match = re.search(r'chapter_note:\s*"?\[\[(.+?)\]\]"?', content, re.MULTILINE)
    chapter_note = chapter_note_match.group(1) if chapter_note_match else ""

    # 提取 status
    status_match = re.search(r'^status:\s*(\w+)$', content, re.MULTILINE)
    status = status_match.group(1) if status_match else "unfinished"

    # 提取 created 和 updated
    created_match = re.search(r'^created:\s*(.+)$', content, re.MULTILINE)
    updated_match = re.search(r'^updated:\s*(.+)$', content, re.MULTILINE)
    created = created_match.group(1).strip() if created_match else ""
    updated = updated_match.group(1).strip() if updated_match else ""

    new_frontmatter = f"""---
title: {title}
aliases: []
tags:
  - 课程/C++
chapter: {chapter}
section:
course: C++ 程序设计
type: note
status: {status}
created: {created}
updated: {updated}
parent_moc: "[[C++ 程序设计 MOC]]"
chapter_note: "[[{chapter_note}]]"
prerequisites: []
related: []
review_level: 0
---

"""
    return new_frontmatter

def update_body(content):
    """更新正文部分"""
    # 移除旧的 frontmatter
    body = re.sub(r'^---[\s\S]*?---\s*\n', '', content)

    # 提取 # title
    title_match = re.search(r'^#\s*(.+)$', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    # 提取所属导航
    nav_section = ""
    nav_match = re.search(r'## 所属导航([\s\S]*?)(?=##|$)', body)
    if nav_match:
        nav_content = nav_match.group(1).strip()
        lines = nav_content.split('\n')
        nav_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('- 总目录：'):
                nav_lines.append(line)
            elif line.startswith('- 章节：'):
                nav_lines.append(line)
        if nav_lines:
            nav_section = '\n'.join(nav_lines)
        else:
            nav_section = "- 总目录：[[C++ 程序设计 MOC]]\n- 章节：[[]]"
    else:
        nav_section = "- 总目录：[[C++ 程序设计 MOC]]\n- 章节：[[]]"

    # 提取相关知识（合并前置知识和相关知识）
    related_items = []

    prereq_match = re.search(r'## 前置知识([\s\S]*?)(?=##|$)', body)
    related_match = re.search(r'## 相关知识([\s\S]*?)(?=##|$)', body)

    if prereq_match:
        prereq_content = prereq_match.group(1).strip()
        for line in prereq_content.split('\n'):
            line = line.strip()
            if line.startswith('- [['):
                related_items.append(line)

    if related_match:
        related_content = related_match.group(1).strip()
        for line in related_content.split('\n'):
            line = line.strip()
            if line.startswith('- [['):
                if line not in related_items:
                    related_items.append(line)

    if related_items:
        related_knowledge = '\n'.join(related_items)
    else:
        related_knowledge = "-"

    # 提取核心概念内容并收集所有代码块
    all_code_blocks = []
    core_text = "-"

    core_match = re.search(r'## 核心概念([\s\S]*?)(?=##|$)', body)
    if core_match:
        core_content = core_match.group(1).strip()
        lines = []
        in_code_block = False
        current_code = []

        for line in core_content.split('\n'):
            if line.strip().startswith('```'):
                if in_code_block:
                    in_code_block = False
                    if current_code:
                        all_code_blocks.append('\n'.join(current_code))
                        current_code = []
                else:
                    in_code_block = True
                    current_code = []
            elif in_code_block:
                current_code.append(line)
            else:
                lines.append(line)

        core_text = '\n'.join(lines).strip()
        if not core_text:
            core_text = "-"

    # 从语法定义收集代码块
    syntax_match = re.search(r'## 语法定义([\s\S]*?)(?=##|$)', body)
    if syntax_match:
        syntax_content = syntax_match.group(1).strip()
        in_code = False
        current = []
        for line in syntax_content.split('\n'):
            if line.strip().startswith('```'):
                if in_code:
                    in_code = False
                    if current:
                        all_code_blocks.append('\n'.join(current))
                        current = []
                else:
                    in_code = True
                    current = []
            elif in_code:
                current.append(line)

    # 从示例代码收集代码块
    example_match = re.search(r'## 示例代码([\s\S]*?)(?=##|$)', body)
    if example_match:
        example_content = example_match.group(1).strip()
        in_code = False
        current = []
        for line in example_content.split('\n'):
            if line.strip().startswith('```'):
                if in_code:
                    in_code = False
                    if current:
                        all_code_blocks.append('\n'.join(current))
                        current = []
                else:
                    in_code = True
                    current = []
            elif in_code:
                current.append(line)

    # 构建核心概念部分（最多 2 个代码块）
    core_section = core_text
    for i, code in enumerate(all_code_blocks[:2]):
        lang = 'cpp'
        core_section += f'\n\n```{lang}\n{code}\n```'

    if not all_code_blocks:
        core_section += '\n\n```cpp\n```\n\n```cpp\n```'
    elif len(all_code_blocks) == 1:
        core_section += '\n\n```cpp\n```'

    # 提取运行结果
    result_section = "*"
    result_match = re.search(r'## 运行结果[\s/]*(?:现象)?([\s\S]*?)(?=##|$)', body)
    if result_match:
        result_content = result_match.group(1).strip()
        if result_content and result_content != '*':
            code_match = re.search(r'```[\s\S]*?```', result_content)
            if code_match:
                result_section = '\n' + code_match.group(0)
            else:
                result_section = result_content

    # 提取原理理解
    principle_section = "*"
    principle_match = re.search(r'## 原理理解([\s\S]*?)(?=##|$)', body)
    if principle_match:
        content = principle_match.group(1).strip()
        if content and content != '*':
            principle_section = content

    # 提取易错点
    mistakes_section = "*"
    mistakes_match = re.search(r'## 易错点([\s\S]*?)(?=##|$)', body)
    if mistakes_match:
        content = mistakes_match.group(1).strip()
        if content and content != '*':
            lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    lines.append(line)
                elif line:
                    lines.append(f'* {line}')
            if lines:
                mistakes_section = '\n\n'.join(lines)

    # 提取我的理解
    my_understanding = "*"
    understanding_match = re.search(r'## 我的理解([\s\S]*?)(?=##|$)', body)
    if understanding_match:
        content = understanding_match.group(1).strip()
        if content and content != '*':
            my_understanding = content

    # 提取一句话总结
    summary = "*"
    summary_match = re.search(r'## 一句话总结([\s\S]*?)(?=##|$)', body)
    if summary_match:
        content = summary_match.group(1).strip()
        if content and content != '*':
            summary = content

    # 构建新正文
    new_body = f"""# {title}

## 所属导航
{nav_section}


## 相关知识
{related_knowledge}

---

## 核心概念
{core_section}

## 运行结果 / 现象

{result_section}

## 原理理解

{principle_section}

## 易错点

{mistakes_section}


## 我的理解

{my_understanding}

## 一句话总结

{summary}

---


"""
    return new_body

def process_file(filepath):
    """处理单个文件"""
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经是新模板格式
    if 'aliases: []' in content and '## 前置知识' not in content:
        print(f"跳过 (已更新): {filename}")
        return False

    new_frontmatter = update_frontmatter(content, filename)
    new_body = update_body(content)
    new_content = new_frontmatter + new_body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"已更新：{filename}")
    return True

if __name__ == '__main__':
    # 处理 02 Notes 目录
    notes_dir = "./02 Notes"
    count = 0
    skipped = 0

    print("=== 开始更新单节笔记 (02 Notes) ===\n")
    for filename in sorted(os.listdir(notes_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(notes_dir, filename)
            if process_file(filepath):
                count += 1
            else:
                skipped += 1

    print(f"\n=== 单节笔记更新完成 ===")
    print(f"新更新：{count} 个文件")
    print(f"已跳过：{skipped} 个文件")
