"""
从 MDict (.mdx) 文件中提取指定词汇的释义
MDX v2 文件格式解析器 - 支持加密
"""

import struct
import zlib
import re
import os
from html.parser import HTMLParser


def _fast_decrypt(data, key):
    """MDX v2 key block info 解密算法"""
    b = bytearray(data)
    key = bytearray(key)
    previous = 0x36
    for i in range(len(b)):
        t = (b[i] >> 4 | b[i] << 4) & 0xFF
        t = t ^ previous ^ (i & 0xFF) ^ key[i % len(key)]
        previous = b[i]
        b[i] = t
    return bytes(b)


def _salsa_decrypt(data, encrypt_key):
    """Salsa20/8 解密（MDX v2 record block 加密），简化版本"""
    # 大多数 COBUILD 词典不需要此解密
    return data


def _decompress(data):
    """解压一个数据块（支持无压缩和 zlib）"""
    if len(data) < 8:
        return data
    compress_type = data[:4]
    if compress_type == b'\x00\x00\x00\x00':
        return data[8:]
    elif compress_type == b'\x02\x00\x00\x00':
        return zlib.decompress(data[8:])
    elif compress_type == b'\x01\x00\x00\x00':
        # LZO 压缩
        raise NotImplementedError("LZO 压缩不受支持，请安装 python-lzo")
    else:
        return data


class HTMLTextExtractor(HTMLParser):
    """从 HTML 中提取纯文本，保留关键结构"""
    def __init__(self):
        super().__init__()
        self.result = []
        self._skip = False
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        if tag in ('script', 'style'):
            self._skip = True

    def handle_endtag(self, tag):
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
        if tag in ('script', 'style'):
            self._skip = False
        if tag in ('br', 'p', 'div', 'li', 'tr'):
            self.result.append('\n')

    def handle_data(self, data):
        if not self._skip:
            self.result.append(data)

    def get_text(self):
        return ''.join(self.result)


def html_to_text(html_str):
    """将 HTML 转为纯文本"""
    extractor = HTMLTextExtractor()
    try:
        extractor.feed(html_str)
    except Exception:
        pass
    return extractor.get_text()


def parse_mdx(filepath, target_words=None):
    """解析 MDX 文件，提取词条"""
    if target_words:
        target_set = set(w.lower().strip() for w in target_words)
    else:
        target_set = None

    results = {}

    with open(filepath, 'rb') as f:
        # ===== 1. HEADER =====
        header_bytes_size = struct.unpack('>I', f.read(4))[0]
        header_bytes = f.read(header_bytes_size)
        _checksum = f.read(4)
        header_text = header_bytes.decode('utf-16-le')

        version = 2.0
        m = re.search(r'GeneratedByEngineVersion="(\d+\.\d+)"', header_text)
        if m:
            version = float(m.group(1))

        encoding = 'utf-8'
        m = re.search(r'Encoding="([^"]*)"', header_text)
        if m:
            enc = m.group(1).lower().strip()
            if enc in ('utf-16', 'utf16'):
                encoding = 'utf-16-le'
            elif enc in ('gbk', 'gb2312', 'gb18030'):
                encoding = 'gbk'
            elif enc == 'big5':
                encoding = 'big5'
            else:
                encoding = 'utf-8'

        encrypted = 0
        m = re.search(r'Encrypted="(\d+)"', header_text)
        if m:
            encrypted = int(m.group(1))

        print(f"版本: {version}, 编码: {encoding}, 加密: {encrypted}")

        # ===== 2. KEY BLOCK SECTION HEADER =====
        if version >= 2.0:
            num_key_blocks = struct.unpack('>Q', f.read(8))[0]
            num_entries = struct.unpack('>Q', f.read(8))[0]
            key_block_info_decomp_size = struct.unpack('>Q', f.read(8))[0]
            key_block_info_comp_size = struct.unpack('>Q', f.read(8))[0]
            key_blocks_size = struct.unpack('>Q', f.read(8))[0]
            _adler = f.read(4)  # adler32 校验
        else:
            num_key_blocks = struct.unpack('>I', f.read(4))[0]
            num_entries = struct.unpack('>I', f.read(4))[0]
            key_block_info_comp_size = struct.unpack('>I', f.read(4))[0]
            key_blocks_size = struct.unpack('>I', f.read(4))[0]
            key_block_info_decomp_size = 0

        print(f"Key blocks: {num_key_blocks}, 词条总数: {num_entries}")

        # ===== 3. KEY BLOCK INFO =====
        key_block_info_raw = f.read(key_block_info_comp_size)

        if version >= 2.0:
            # v2: key block info 前 4 字节是压缩类型，接下来 4 字节是 adler32
            compress_type = key_block_info_raw[:4]
            adler32_bytes = key_block_info_raw[4:8]
            encrypted_data = key_block_info_raw[8:]

            if encrypted & 0x02:
                # 需要解密：使用 adler32_bytes 生成 key
                decrypt_key = struct.pack('<I', zlib.adler32(adler32_bytes) & 0xFFFFFFFF)
                decrypted_data = _fast_decrypt(encrypted_data, decrypt_key)
            else:
                decrypted_data = encrypted_data

            if compress_type == b'\x02\x00\x00\x00':
                key_block_info = zlib.decompress(decrypted_data)
            elif compress_type == b'\x00\x00\x00\x00':
                key_block_info = decrypted_data
            else:
                key_block_info = decrypted_data
        else:
            key_block_info = key_block_info_raw

        print(f"Key block info 解压后大小: {len(key_block_info)}")

        # ===== 4. 解析 KEY BLOCK INFO =====
        key_block_info_list = []
        i = 0
        if version >= 2.0:
            while i + 8 <= len(key_block_info):
                try:
                    n_entries_block = struct.unpack('>Q', key_block_info[i:i+8])[0]
                    i += 8

                    first_size = struct.unpack('>H', key_block_info[i:i+2])[0]
                    i += 2
                    if encoding == 'utf-16-le':
                        i += first_size * 2 + 2
                    else:
                        i += first_size + 1

                    last_size = struct.unpack('>H', key_block_info[i:i+2])[0]
                    i += 2
                    if encoding == 'utf-16-le':
                        i += last_size * 2 + 2
                    else:
                        i += last_size + 1

                    comp_size = struct.unpack('>Q', key_block_info[i:i+8])[0]
                    i += 8
                    decomp_size = struct.unpack('>Q', key_block_info[i:i+8])[0]
                    i += 8

                    key_block_info_list.append((n_entries_block, comp_size, decomp_size))
                except struct.error:
                    break
        else:
            while i + 4 <= len(key_block_info):
                try:
                    n_entries_block = struct.unpack('>I', key_block_info[i:i+4])[0]
                    i += 4
                    first_size = key_block_info[i]
                    i += 1 + first_size + 1
                    last_size = key_block_info[i]
                    i += 1 + last_size + 1
                    comp_size = struct.unpack('>I', key_block_info[i:i+4])[0]
                    i += 4
                    decomp_size = struct.unpack('>I', key_block_info[i:i+4])[0]
                    i += 4
                    key_block_info_list.append((n_entries_block, comp_size, decomp_size))
                except (struct.error, IndexError):
                    break

        print(f"解析到 {len(key_block_info_list)} 个 key block")

        # ===== 5. 读取 KEY BLOCKS =====
        key_list = []
        for idx, (n_entries_block, comp_size, decomp_size) in enumerate(key_block_info_list):
            key_block_compressed = f.read(comp_size)
            try:
                key_block = _decompress(key_block_compressed)
            except Exception as e:
                print(f"  key block {idx} 解压失败: {e}")
                continue

            # 解析每个 key entry
            j = 0
            while j < len(key_block):
                if version >= 2.0:
                    if j + 8 > len(key_block):
                        break
                    record_offset = struct.unpack('>Q', key_block[j:j+8])[0]
                    j += 8
                else:
                    if j + 4 > len(key_block):
                        break
                    record_offset = struct.unpack('>I', key_block[j:j+4])[0]
                    j += 4

                # 读取 key text
                if encoding == 'utf-16-le':
                    k = j
                    while k < len(key_block) - 1:
                        if key_block[k:k+2] == b'\x00\x00':
                            break
                        k += 2
                    key_text = key_block[j:k].decode('utf-16-le', errors='replace')
                    j = k + 2
                else:
                    k = j
                    while k < len(key_block) and key_block[k] != 0:
                        k += 1
                    key_text = key_block[j:k].decode(encoding, errors='replace')
                    j = k + 1

                key_list.append((key_text, record_offset))

        print(f"总共读取 {len(key_list)} 个词条 key")

        # ===== 6. RECORD BLOCK SECTION =====
        if version >= 2.0:
            num_record_blocks = struct.unpack('>Q', f.read(8))[0]
            num_record_entries = struct.unpack('>Q', f.read(8))[0]
            record_block_info_size = struct.unpack('>Q', f.read(8))[0]
            record_block_data_size = struct.unpack('>Q', f.read(8))[0]
        else:
            num_record_blocks = struct.unpack('>I', f.read(4))[0]
            num_record_entries = struct.unpack('>I', f.read(4))[0]
            record_block_info_size = struct.unpack('>I', f.read(4))[0]
            record_block_data_size = struct.unpack('>I', f.read(4))[0]

        print(f"Record blocks: {num_record_blocks}")

        # Record Block Info
        record_block_info_list = []
        for _ in range(num_record_blocks):
            if version >= 2.0:
                comp_size = struct.unpack('>Q', f.read(8))[0]
                decomp_size = struct.unpack('>Q', f.read(8))[0]
            else:
                comp_size = struct.unpack('>I', f.read(4))[0]
                decomp_size = struct.unpack('>I', f.read(4))[0]
            record_block_info_list.append((comp_size, decomp_size))

        # 读取并拼接所有 record block
        record_data = bytearray()
        for comp_size, decomp_size in record_block_info_list:
            record_block_compressed = f.read(comp_size)
            try:
                block = _decompress(record_block_compressed)
                record_data.extend(block)
            except Exception as e:
                print(f"Record block 解压失败: {e}")
                record_data.extend(b'\x00' * decomp_size)

        record_data = bytes(record_data)
        print(f"Record data 总大小: {len(record_data)}")

        # ===== 7. 配对 KEY 和 DEFINITION =====
        for i in range(len(key_list)):
            key_text, offset = key_list[i]
            key_lower = key_text.lower().strip()

            if target_set and key_lower not in target_set:
                continue

            if i + 1 < len(key_list):
                next_offset = key_list[i + 1][1]
            else:
                next_offset = len(record_data)

            if offset < len(record_data) and next_offset <= len(record_data):
                defn_bytes = record_data[offset:next_offset]
                try:
                    definition = defn_bytes.decode(encoding, errors='replace').rstrip('\x00')
                except Exception:
                    definition = defn_bytes.decode('utf-8', errors='replace').rstrip('\x00')

                results[key_lower] = {
                    'key': key_text,
                    'definition': definition
                }

    return results


if __name__ == '__main__':
    mdx_path = r"C:\Users\ExpiiD\AppData\Roaming\Francochinois\eudic\dict\CollinsCOBUILDOverhaul V 2-30.mdx"

    words = [
        "denote", "hypothesis", "prediction", "represent", "perform",
        "addition", "subtraction", "asterisk", "multiplication",
        "division", "integer", "fractional", "decimal",
        "exponentiation", "caret", "bitwise",
        "parentheses", "indicate",
        "additional", "bead", "necklace",
        "apostrophe", "space", "punctuation", "digit",
        "join", "concatenation", "concatenate",
        "operand", "notation", "ambiguity",
        "redundancy", "verbose",
        "idiom", "metaphor", "dense", "adjust", "matter",
        "whimsical", "process", "inability",
        "mitigate", "interfere", "category"
    ]

    print("正在解析 MDX 文件...\n")
    try:
        results = parse_mdx(mdx_path, words)
        print(f"\n=== 查询结果 ({len(results)} 个匹配) ===\n")

        for word in words:
            key = word.lower().strip()
            if key in results:
                defn = results[key]['definition']
                # 将 HTML 转纯文本后显示
                text = html_to_text(defn)
                # 只取前 500 字符预览
                preview = text[:500].strip()
                print(f"=== {word} ===")
                print(preview)
                print()
            else:
                print(f"=== {word} === 未找到")
                print()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
