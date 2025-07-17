# notify.py
import os
import requests
import json

def _send_pushplus(token, title, content):
    """
    使用 PushPlus 发送通知。
    这是一个私有函数，由 send() 调用。
    """
    print("  - 正在尝试使用 PushPlus 推送...")
    url = "http://www.pushplus.plus/send"
    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)
        result = response.json()
        if result.get('code') == 200:
            print("    ✅ PushPlus 推送成功！")
            return True
        else:
            print(f"    ❌ PushPlus 推送失败：{result.get('msg')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"    ❌ PushPlus 推送网络错误: {e}")
        return False

def _send_telegram(tg_bot_token, tg_user_id, title, content):
    """
    使用 Telegram Bot 发送通知。
    这是一个私有函数，由 send() 调用。
    """
    print("  - 正在尝试使用 Telegram Bot 推送...")
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    # 将 Markdown V2 的特殊字符进行转义
    # . - + ! { } ( ) | # > < =
    safe_content = content.replace('.', '\\.').replace('-', '\\-').replace('+', '\\+') \
                          .replace('!', '\\!').replace('{', '\\{').replace('}', '\\}') \
                          .replace('(', '\\(').replace(')', '\\)').replace('|', '\\|') \
                          .replace('#', '\\#').replace('>', '\\>').replace('<', '\\<') \
                          .replace('=', '\\=')

    payload = {
        'chat_id': tg_user_id,
        'text': f"*{title}*\n\n{safe_content}",
        'parse_mode': 'MarkdownV2'
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)
        result = response.json()
        if result.get('ok'):
            print("    ✅ Telegram Bot 推送成功！")
            return True
        else:
            print(f"    ❌ Telegram Bot 推送失败：{result.get('description')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Telegram Bot 推送网络错误: {e}")
        return False

# --- 主发送函数 ---
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
        
    # 在这里可以继续添加其他推送渠道的判断
    # if other_token:
    #     _send_other(...)

    if not has_any_channel:
        print("未配置任何推送渠道，跳过推送。")
    
    print("--- 推送任务执行完毕 ---\n")
