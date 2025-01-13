#!/usr/bin/env python3
import sys
import json
import struct

def send_message(message):
    """模拟扩展发送消息"""
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('=I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def get_message():
    """接收本地主机的响应"""
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length)
    return json.loads(message)

def main():
    # 发送测试消息
    test_message = {"action": "start_streamlit"}
    send_message(test_message)
    
    # 接收响应
    response = get_message()
    print(f"Response: {response}")

if __name__ == "__main__":
    main() 