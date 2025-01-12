#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from typing import List, Dict, Any
import requests
import json
from dotenv import load_dotenv
import re

# 加载.env文件
load_dotenv()

class GoogleSearch:
    def __init__(self, api_key: str, search_engine_id: str):
        """初始化Google搜索客户端
        
        Args:
            api_key: Google API密钥
            search_engine_id: 自定义搜索引擎ID
        """
        print(f"初始化搜索客户端...")
        print(f"API密钥: {api_key[:10]}...")
        print(f"搜索引擎ID: {search_engine_id}")
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = 'https://www.googleapis.com/customsearch/v1'

    def build_payload(self, query: str, start: int = 1, num: int = 10, 
                     date_restrict: str = None, **params) -> Dict:
        """构建搜索请求参数
        
        Args:
            query: 搜索关键词
            start: 起始结果索引
            num: 返回结果数量（1-10）
            date_restrict: 日期限制（例如：'m1'表示一个月内，'w2'表示两周内），None表示不限制
            **params: 其他参数，可以包括：
                     - hl: 界面语言（例如：zh-CN）
                     - gl: 地理位置偏好（例如：cn）
                     - safe: 安全搜索设置
                     - sort: 排序方式
                     - filter: 是否过滤相似结果
                     - cr: 国家限制
                     - lr: 语言限制
                     - rights: 使用权限过滤
                     - exactTerms: 精确匹配的词
                     - excludeTerms: 排除的词
                     
        Returns:
            请求参数字典
        """
        payload = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'start': start,
            'num': min(num, 10),
            'rsz': 'filtered_cse',  # 结果过滤
            'safe': 'off',  # 默认关闭安全搜索
            'filter': '1',  # 开启重复过滤
        }
        
        if date_restrict:
            payload['dateRestrict'] = date_restrict
            
        # 添加其他可选参数
        optional_params = [
            'hl', 'gl', 'safe', 'sort', 'cr', 'lr', 
            'rights', 'exactTerms', 'excludeTerms'
        ]
        
        for param in optional_params:
            if param in params and params[param] is not None:
                payload[param] = params[param]
                
        return payload

    def make_request(self, payload: Dict) -> Dict:
        """发送搜索请求
        
        Args:
            payload: 请求参数
            
        Returns:
            API响应JSON
        """
        try:
            response = requests.get(self.base_url, params=payload)
            if response.status_code != 200:
                print(f"请求失败: HTTP {response.status_code}")
                print(f"错误信息: {response.text}")
                raise Exception('Request failed')
            return response.json()
        except Exception as e:
            print(f"请求出错: {str(e)}")
            raise

    def search(self, query: str, total_results: int = 10, date_restrict: str = None, hl: str = None, gl: str = None, sort: str = None, safe: str = None, filter: str = None, cr: str = None, lr: str = None, rights: str = None, exactTerms: str = None, excludeTerms: str = None) -> List[Dict[str, Any]]:
        """执行Google搜索
        
        Args:
            query: 搜索关键词
            total_results: 需要返回的总结果数量
            date_restrict: 日期限制，None表示不限制时间
            hl: 界面语言
            gl: 搜索区域偏好
            sort: 排序方式
            safe: 安全搜索设置
            filter: 是否过滤相似结果
            cr: 国家限制
            lr: 语言限制
            rights: 使用权限过滤
            exactTerms: 精确匹配的词
            excludeTerms: 排除的词
            
        Returns:
            搜索结果列表
        """
        try:
            print(f"\n执行搜索: {query}")
            print(f"请求总结果数量: {total_results}")
            print(f"日期限制: {date_restrict}")
            
            all_items = []
            remainder = total_results % 10
            pages = (total_results // 10) + (1 if remainder > 0 else 0)
            
            for i in range(pages):
                start = i * 10 + 1
                if i == pages - 1 and remainder > 0:
                    num = remainder
                else:
                    num = 10
                    
                print(f"\n获取第 {i+1}/{pages} 页结果...")
                print(f"起始索引: {start}, 数量: {num}")
                
                payload = self.build_payload(
                    query=query,
                    start=start,
                    num=num,
                    date_restrict=date_restrict,
                    hl=hl,
                    gl=gl,
                    sort=sort,
                    safe=safe,
                    filter=filter,
                    cr=cr,
                    lr=lr,
                    rights=rights,
                    exactTerms=exactTerms,
                    excludeTerms=excludeTerms
                )
                
                result = self.make_request(payload)
                
                if 'items' in result:
                    items = result['items']
                    print(f"本页获取到 {len(items)} 条结果")
                    
                    for item in items:
                        all_items.append({
                            'title': item.get('title', ''),
                            'link': item.get('link', ''),
                            'snippet': item.get('snippet', ''),
                            'displayLink': item.get('displayLink', ''),
                            'pagemap': item.get('pagemap', {}),
                            'kind': item.get('kind', ''),
                            'htmlTitle': item.get('htmlTitle', ''),
                            'htmlSnippet': item.get('htmlSnippet', ''),
                            'formattedUrl': item.get('formattedUrl', ''),
                            'htmlFormattedUrl': item.get('htmlFormattedUrl', '')
                        })
                else:
                    print("本页没有找到结果")
                    break
                    
            return all_items
            
        except Exception as e:
            print(f"搜索时发生错误: {str(e)}")
            return []

def clean_filename(filename: str) -> str:
    """清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='Google搜索工具')
    parser.add_argument('query', help='搜索查询')
    parser.add_argument('-n', '--num-results', type=int, default=10,
                      help='返回结果总数量（默认10条）')
    parser.add_argument('-d', '--date-restrict',
                      help='日期限制 (例如: m1=一个月内, w2=两周内)，默认不限制')
    parser.add_argument('-k', '--api-key', help='Google API密钥')
    parser.add_argument('-s', '--search-engine-id', help='搜索引擎ID')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--sort', help='排序方式 (relevance或date)')
    parser.add_argument('--hl', default='zh-CN', help='界面语言 (默认: zh-CN)')
    parser.add_argument('--gl', help='地理位置偏好 (例如: cn)')
    parser.add_argument('--safe', default='off', help='安全搜索设置 (默认: off)')
    parser.add_argument('--filter', default='1', help='是否过滤相似结果 (默认: 1)')
    parser.add_argument('--cr', help='国家限制 (例如: countryUS)')
    parser.add_argument('--lr', help='语言限制 (例如: lang_zh-CN)')
    parser.add_argument('--rights', help='使用权限过滤')
    parser.add_argument('--exact', help='精确匹配的词')
    parser.add_argument('--exclude', help='排除的词')
    args = parser.parse_args()

    # 获取API密钥和搜索引擎ID（优先使用命令行参数，其次使用环境变量）
    api_key = args.api_key or os.getenv('GOOGLE_API_KEY')
    search_engine_id = args.search_engine_id or os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    print(f"\n环境检查:")
    print(f"GOOGLE_API_KEY 环境变量: {'已设置' if os.getenv('GOOGLE_API_KEY') else '未设置'}")
    print(f"GOOGLE_SEARCH_ENGINE_ID 环境变量: {'已设置' if os.getenv('GOOGLE_SEARCH_ENGINE_ID') else '未设置'}")
    print(f"最终使用的API密钥: {api_key[:10] if api_key else 'None'}...")
    print(f"最终使用的搜索引擎ID: {search_engine_id if search_engine_id else 'None'}")
    if args.sort:
        print(f"排序方式: {args.sort}")

    if not api_key or not search_engine_id:
        print("\n错误：需要提供Google API密钥和搜索引擎ID")
        print("可以通过命令行参数(-k, -s)或环境变量(GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID)提供")
        return

    # 创建搜索客户端并执行搜索
    searcher = GoogleSearch(api_key, search_engine_id)
    results = searcher.search(
        query=args.query,
        total_results=args.num_results,
        date_restrict=args.date_restrict,
        sort=args.sort,
        hl=args.hl,
        gl=args.gl,
        safe=args.safe,
        filter=args.filter,
        cr=args.cr,
        lr=args.lr,
        rights=args.rights,
        exactTerms=args.exact,
        excludeTerms=args.exclude
    )

    # 格式化输出
    output = {
        'query': args.query,
        'num_results': len(results),
        'date_restrict': args.date_restrict,
        'results': results
    }
    
    # 输出结果
    if args.output:
        # 如果没有指定文件扩展名，添加.json
        output_path = args.output if args.output.endswith('.json') else f"{args.output}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_path}")
    else:
        print("\n搜索结果:")
        print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main() 