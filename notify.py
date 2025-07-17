# notify.py v2
import os
import requests
import json
import re

def _send_pushplus(token, title, content):
    """
    使用 PushPlus 发送通知。
    这个函数保持不变，因为它能正确处理 HTML。
    """
    print("  - 正在尝试使用 PushPlus 推送...")
    url = "http://www.pushplus.plus/send"
    payload = {
        "token": token, "title": title, "content": content, "template": "html"
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        result = response.json()
        if result.get('code') == 200:
            print("    ✅ PushPlus 推送成功！")
        else:
            print(f"    ❌ PushPlus 推送失败：{result.get('msg')}")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ PushPlus 推送网络错误: {e}")

def _send_telegram(tg_bot_token, tg_user_id, title, content):
    """
    使用 Telegram Bot 发送通知。
    函数改造，以正确处理格式转换和转义。
    """
    print("  - 正在尝试使用 Telegram Bot 推送...")
    
    # 1. 格式翻译：将我们自定义的 HTML-like 标签转换为 Markdown
    #    - <font color='xxx'>...</font> -> `...` (行内代码块，醒目且安全)
    #    - <b>...</b> -> *...* (粗体)
    #    - <br> -> \n (换行)
    tg_content = content.replace("<br>", "\n")
    tg_content = re.sub(r"<font color='.*?'>(.*?)</font>", r"`\1`", tg_content)
    tg_content = re.sub(r"<b>(.*?)</b>", r"*\1*", tg_content)
    tg_content = tg_content.replace("**", "*") # 兼容旧格式

    # 2. 字符转义：对所有 MarkdownV2 的保留字符进行转义
    #    官方文档规定的需要转义的字符: _*[]()~`>#+-.=|{}!
    escape_chars = r'_*[]()~`>#+-.=|{}!'
    tg_content = ''.join(['\\' + char if char in escape_chars else char for char in tg_content])
    
    # 3. 构建 payload 并发送
    #    标题也需要转义，以防标题中包含特殊字符
    safe_title = ''.join(['\\' + char if char in escape_chars else char for char in title])
    
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    payload = {
        'chat_id': tg_user_id,
        'text': f"*{safe_title}*\n\n{tg_content}",
        'parse_mode': 'MarkdownV2'
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        result = response.json()
        if result.get('ok'):
            print("    ✅ Telegram Bot 推送成功！")
        else:
            print(f"    ❌ Telegram Bot 推送失败：{result.get('description')}")
            # 打印一些调试信息
            print(f"    - 调试信息：发送的文本内容 -> {payload.get('text')}")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Telegram Bot 推送网络错误: {e}")

# --- 主发送函数 (保持不变) ---
def send(title, content):
    """
    总推送函数，会尝试所有已配置的推送渠道。
    """
    print("\n--- 开始执行推送任务 ---")
    
    pushplus_token = os.environ.get('PUSH_PLUS_TOKEN')
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_user_id = os.environ.get('TG_USER_ID')
    
    has_any_channel = False

    if pushplus_token:
        has_any_channel = True
        _send_pushplus(pushplus_token, title, content)
    
    if tg_bot_token and tg_user_id:
        has_any_channel = True
        _send_telegram(tg_bot_token, tg_user_id, title, content)

    if not has_any_channel:
        print("未配置任何推送渠道，跳过推送。")
    
    print("--- 推送任务执行完毕 ---\n")
