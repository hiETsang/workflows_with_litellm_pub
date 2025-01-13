#!/usr/bin/env python3
import sys
import subprocess
import os
import time
import json
import socket

def is_port_in_use(port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def ensure_single_streamlit():
    """确保只有一个 Streamlit 实例在运行"""
    if is_port_in_use(8501):
        return {"status": "running", "message": "Streamlit is already running"}
    
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 设置 poetry 路径
    poetry_path = "/opt/anaconda3/bin/poetry"
    
    try:
        # 启动 Streamlit
        cmd = [poetry_path, 'run', 'streamlit', 'run', 'app_web.py', '--server.headless', 'true']
        process = subprocess.Popen(
            cmd,
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, 'PATH': f"/opt/anaconda3/bin:{os.environ.get('PATH', '')}"},
            start_new_session=True
        )
        
        # 等待服务启动
        for _ in range(20):
            if is_port_in_use(8501):
                return {"status": "started", "message": "Streamlit started successfully"}
            time.sleep(0.5)
        
        # 如果启动失败，获取错误信息
        stdout, stderr = process.communicate(timeout=1)
        error_msg = stderr.decode() if stderr else "Unknown error"
        return {"status": "error", "message": f"Failed to start Streamlit: {error_msg}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = ensure_single_streamlit()
    print(json.dumps(result)) 