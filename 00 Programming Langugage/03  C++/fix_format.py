#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 C++ 笔记文件的格式问题"""

import os
import re

def fix_notes():
    """修复单节笔记的重复分隔符问题"""
    notes_dir = "./02 Notes"
    count = 0

    print("=== 修复单节笔记格式 ===\n")
    for filename in sorted(os.listdir(notes_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(notes_dir, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 修复重复的 ---
            # 查找末尾的重复 ---
            old_ending = "\n---\n\n---\n\n\n"
            old_ending2 = "\n---\n\n---\n\n"

            if old_ending in content:
                content = content.replace(old_ending, "\n---\n\n\n")
                count += 1
            elif old_ending2 in content:
                content = content.replace(old_ending2, "\n---\n\n")
                count += 1

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"已修复 {count} 个文件的分隔符问题")

def fix_chapters():
    """修复章节文件的本章内容链接"""
    chapters_dir = "./01 Chapters"
    count = 0

    print("\n=== 修复章节笔记内容 ===\n")
    for filename in sorted(os.listdir(chapters_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(chapters_dir, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 从 children 中提取链接
            children_match = re.search(r'children:\s*\n((?:\s*-\s*".*?"\n?)*)', content)
            lesson_links = []
            if children_match:
                for line in children_match.group(1).split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        link_text = line[1:].strip().strip('"')
                        # 提取 [[xxx]] 中的内容
                        link_match = re.search(r'\[\[(.+?)\]\]', link_text)
                        if link_match:
                            lesson_links.append(link_match.group(1))

            if lesson_links:
                # 构建本章内容列表
                lessons_content = "\n".join([f"- [[{link}]]" for link in lesson_links])

                # 替换本章内容部分
                old_pattern = "## 本章内容\n-\n"
                new_content = f"## 本章内容\n{lessons_content}\n"

                if old_pattern in content:
                    content = content.replace(old_pattern, new_content)
                    count += 1

                # 修复 frontmatter 中的空行问题 (aliases 后的空行)
                content = re.sub(r'(aliases:\n  - .+)\n\n\ntags:', r'\1\ntags:', content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"已修复 {count} 个章节文件的内容链接")

if __name__ == '__main__':
    fix_notes()
    fix_chapters()
    print("\n=== 所有修复完成 ===")
