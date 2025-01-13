#!/usr/bin/env python3
import sys
import json
import struct
import subprocess
import os
import logging
import time

# 设置日志记录
logging.basicConfig(
    filename=os.path.expanduser('~/indieto_collector.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 记录启动信息
logging.info("="*50)
logging.info("Native host script started")
logging.info(f"Script path: {os.path.abspath(__file__)}")
logging.info(f"Working directory: {os.getcwd()}")
logging.info(f"Python version: {sys.version}")
logging.info(f"Environment: {os.environ}")
logging.info("="*50)

def get_message():
    """从标准输入读取消息"""
    try:
        logging.info("Waiting for message...")
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            logging.info("No message received")
            return None
        message_length = struct.unpack('=I', raw_length)[0]
        logging.info(f"Message length: {message_length}")
        message = sys.stdin.buffer.read(message_length)
        decoded_message = json.loads(message)
        logging.info(f"Received message: {decoded_message}")
        return decoded_message
    except Exception as e:
        logging.error(f"Error reading message: {str(e)}", exc_info=True)
        return None

def send_message(message):
    """向标准输出写入消息"""
    try:
        logging.info(f"Sending message: {message}")
        encoded = json.dumps(message).encode('utf-8')
        sys.stdout.buffer.write(struct.pack('=I', len(encoded)))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()
        logging.info("Message sent successfully")
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}", exc_info=True)

def start_streamlit(url=None):
    """启动 Streamlit"""
    try:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 运行管理脚本
        manage_script = os.path.join(current_dir, 'scripts', 'manage_streamlit.py')
        result = subprocess.run(
            ['python3', manage_script],
            capture_output=True,
            text=True,
            cwd=current_dir
        )
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response['status'] in ['running', 'started']:
                    logging.info(f"Streamlit status: {response['message']}")
                    return True, None
                else:
                    logging.error(f"Error starting Streamlit: {response['message']}")
                    return False, response['message']
            except json.JSONDecodeError:
                logging.error("Failed to parse manage script output")
                return False, "Internal error"
        else:
            logging.error(f"Manage script failed: {result.stderr}")
            return False, result.stderr
            
    except Exception as e:
        logging.error(f"Error starting Streamlit: {str(e)}", exc_info=True)
        return False, str(e)

def main():
    logging.info("Native host main function started")
    while True:
        message = get_message()
        if message is None:
            logging.info("No message, exiting")
            break
            
        if message.get('action') == 'start_streamlit':
            success, error = start_streamlit(message.get('url'))
            if success:
                send_message({"status": "success"})
            else:
                send_message({"status": "error", "message": error})

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Main function error: {str(e)}", exc_info=True)
        sys.exit(1) 