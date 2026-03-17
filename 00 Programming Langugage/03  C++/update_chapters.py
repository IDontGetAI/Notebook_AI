#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 C++ 章节文件以匹配新模板格式"""

import os
import re

def update_chapter_frontmatter(content, filename):
    """更新章节文件 frontmatter 部分"""
    # 提取 title
    title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename.replace('.md', '')

    # 提取 aliases
    aliases = []
    aliases_match = re.search(r'aliases:\s*\n((?:\s*-\s*.+\n?)*)', content)
    if aliases_match:
        for line in aliases_match.group(1).split('\n'):
            line = line.strip()
            if line.startswith('-'):
                aliases.append(line[1:].strip())

    # 提取 chapter
    chapter_match = re.search(r'^chapter:\s*(\d+)$', content, re.MULTILINE)
    chapter = chapter_match.group(1) if chapter_match else ""

    # 提取 status
    status_match = re.search(r'^status:\s*(\w+)$', content, re.MULTILINE)
    status = status_match.group(1) if status_match else "ongoing"

    # 提取 created 和 updated
    created_match = re.search(r'^created:\s*(.+)$', content, re.MULTILINE)
    updated_match = re.search(r'^updated:\s*(.+)$', content, re.MULTILINE)
    created = created_match.group(1).strip() if created_match else ""
    updated = updated_match.group(1).strip() if updated_match else ""

    # 提取 children
    children = []
    children_match = re.search(r'children:\s*\n((?:\s*-\s*".*?"\n?)*)', content)
    if children_match:
        for line in children_match.group(1).split('\n'):
            line = line.strip()
            if line.startswith('-'):
                children.append(line[1:].strip())

    # 构建 lesson_1, lesson_2 等
    lessons = {}
    for i, child in enumerate(children[:10], 1):
        # 提取链接文本 [[xxx]]
        link_match = re.search(r'\[\[(.+?)\]\]', child)
        if link_match:
            lessons[f'lesson_{i}'] = link_match.group(1)

    # 构建 aliases 字符串
    aliases_str = ""
    if aliases:
        aliases_str = "aliases:\n" + "".join([f"  - {a}\n" for a in aliases])
    else:
        aliases_str = "aliases: []"

    # 构建 children 字符串
    children_str = ""
    for i in range(1, min(len(children) + 1, 10)):
        lesson_key = f'lesson_{i}'
        if lesson_key in lessons:
            children_str += f'  - "[[{lessons[lesson_key]}]]"\n'

    new_frontmatter = f"""---
title: {title}
{aliases_str}
tags:
  - 课程/C++
  - 章节导航
chapter: {chapter}
course: C++ 程序设计
type: chapter
status: {status}
created: {created}
updated: {updated}
parent_moc: "[[C++ 程序设计 MOC]]"
children:
{children_str}---

"""
    return new_frontmatter

def update_chapter_body(content):
    """更新章节文件正文部分"""
    # 移除旧的 frontmatter
    body = re.sub(r'^---[\s\S]*?---\s*\n', '', content)

    # 提取 # title
    title_match = re.search(r'^#\s*(.+)$', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    # 提取本章内容中的链接（用于本章内容部分）
    lesson_links = []
    content_section_match = re.search(r'## 本章内容([\s\S]*?)(?=##|$)', body)
    if content_section_match:
        content_section = content_section_match.group(1)
        # 查找所有 [[xxx]] 格式的链接
        for match in re.finditer(r'\[\[(.+?)\]\]', content_section):
            link = match.group(1)
            if link not in lesson_links:
                lesson_links.append(link)

    # 构建本章内容列表
    lessons_content = ""
    if lesson_links:
        for link in lesson_links:
            lessons_content += f"- [[{link}]]\n"
    else:
        lessons_content = "-\n"

    # 提取本章重点
    key_points = ""
    key_points_match = re.search(r'## 本章重点([\s\S]*?)(?=##|$)', body)
    if key_points_match:
        content = key_points_match.group(1).strip()
        if content:
            # 保留现有的重点内容
            lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    lines.append(line)
                elif line.startswith('**'):
                    lines.append(f'- {line}')
                elif line:
                    lines.append(f'- {line}')
            if lines:
                key_points = '\n'.join(lines)
            else:
                key_points = "-"
        else:
            key_points = "-"
    else:
        key_points = "-"

    # 提取本章关联知识
    related_knowledge = ""
    related_match = re.search(r'## 本章关联知识[\s\S]*?([\s\S]*?)(?=##|$)', body)
    if related_match:
        content = related_match.group(1).strip()
        if content:
            lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    lines.append(line)
                elif line:
                    lines.append(f'- {line}')
            if lines:
                related_knowledge = '\n'.join(lines)
            else:
                related_knowledge = "-"
        else:
            related_knowledge = "-"
    else:
        related_knowledge = "-"

    new_body = f"""# {title}

## 上级导航
- [[C++ 程序设计 MOC]]

## 本章内容
{lessons_content}
## 本章重点
{key_points}

## 本章关联知识
{related_knowledge}

"""
    return new_body

def process_chapter_file(filepath):
    """处理单个章节文件"""
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经是新模板格式
    # 新模板特征：children 使用 lesson_x 格式，没有"本章前置知识"
    if '本章前置知识' not in content and 'lesson_1' in content:
        print(f"跳过 (已更新): {filename}")
        return False

    new_frontmatter = update_chapter_frontmatter(content, filename)
    new_body = update_chapter_body(content)
    new_content = new_frontmatter + new_body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"已更新：{filename}")
    return True

if __name__ == '__main__':
    # 处理 01 Chapters 目录
    chapters_dir = "./01 Chapters"
    count = 0
    skipped = 0

    print("=== 开始更新章节笔记 (01 Chapters) ===\n")
    for filename in sorted(os.listdir(chapters_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(chapters_dir, filename)
            if process_chapter_file(filepath):
                count += 1
            else:
                skipped += 1

    print(f"\n=== 章节笔记更新完成 ===")
    print(f"新更新：{count} 个文件")
    print(f"已跳过：{skipped} 个文件")
