#!/usr/bin/env python3
import psutil
import sys

def stop_streamlit():
    """停止所有 Streamlit 进程"""
    stopped = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'streamlit' in ' '.join(cmdline):
                print(f"找到 Streamlit 进程: {proc.info['pid']}")
                proc.terminate()
                stopped = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if stopped:
        print("已停止 Streamlit 服务")
    else:
        print("未找到运行中的 Streamlit 服务")

if __name__ == "__main__":
    stop_streamlit() 