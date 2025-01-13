#!/usr/bin/env python3
import pyperclip
import webbrowser
from urllib.parse import quote
import subprocess
import os
import sys

def main():
    # 获取剪贴板内容
    url = pyperclip.paste().strip()
    
    # 验证是否是URL
    if not url.startswith(('http://', 'https://')):
        print("剪贴板内容不是有效的URL")
        sys.exit(1)
    
    # 编码URL
    encoded_url = quote(url)
    
    # 构建Streamlit应用URL
    streamlit_url = f'http://localhost:8501?url={encoded_url}'
    
    # 检查Streamlit是否已经运行
    try:
        import requests
        requests.get('http://localhost:8501')
    except:
        # 如果Streamlit未运行，启动它
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        subprocess.Popen(['poetry', 'run', 'streamlit', 'run', 'app_web.py'], 
                        cwd=current_dir,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    
    # 打开浏览器
    webbrowser.open(streamlit_url)

if __name__ == "__main__":
    main() 