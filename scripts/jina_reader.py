#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from dotenv import load_dotenv
from urllib.parse import quote
from typing import Optional, Dict, Any

# 加载环境变量
load_dotenv()

class JinaReader:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('JINA_API_KEY')
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found. Please set it as an environment variable or pass it directly.")
        
        self.base_headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'X-Retain-Images': 'none',
            'X-With-Links-Summary': 'true'
        }
        self.base_url = 'https://r.jina.ai/'

    def read_url(self, url: str, retain_images: bool = False, with_links_summary: bool = True) -> Dict[str, Any]:
        """
        读取网页内容
        :param url: 要读取的网页URL
        :param retain_images: 是否保留图片
        :param with_links_summary: 是否包含链接摘要
        :return: 网页内容和元数据
        """
        # 确保URL是完整的
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 构建完整的URL
        full_url = f"{self.base_url}{quote(url)}"

        # 构建headers
        headers = self.base_headers.copy()
        headers['X-Retain-Images'] = 'all' if retain_images else 'none'
        headers['X-With-Links-Summary'] = str(with_links_summary).lower()

        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"读取失败: {str(e)}", file=sys.stderr)
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text}", file=sys.stderr)
            return {}

def main():
    parser = argparse.ArgumentParser(description='使用Jina AI读取网页内容')
    parser.add_argument('url', help='要读取的网页URL')
    parser.add_argument('-k', '--api-key', help='Jina API密钥（也可通过JINA_API_KEY环境变量设置）')
    parser.add_argument('-o', '--output', help='输出文件路径（可选，默认输出到控制台）')
    parser.add_argument('--retain-images', action='store_true', help='是否保留图片')
    parser.add_argument('--no-links-summary', action='store_false', dest='with_links_summary', help='不包含链接摘要')
    args = parser.parse_args()

    try:
        reader = JinaReader(api_key=args.api_key)
        content = reader.read_url(args.url, args.retain_images, args.with_links_summary)
        
        if args.output:
            # 如果指定了输出文件，写入文件
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"内容已保存到: {args.output}")
        else:
            # 否则输出到控制台
            print(content)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 