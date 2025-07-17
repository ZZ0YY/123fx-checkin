# checkin.py
import os
import requests
import json
import time
import notify  # 导入新的推送模块

def main():
    """
    主函数，处理多用户签到逻辑，并在最后调用通知模块。
    """
    cookies_str = os.environ.get('PAN_COOKIES')
    
    if not cookies_str:
        print("❌ 错误：未找到名为 PAN_COOKIES 的环境变量。请在 GitHub Secrets 中设置。")
        notify.send("Pan1.me 签到失败", "错误：未在 GitHub Secrets 中配置 `PAN_COOKIES`。")
        return

    cookies_list = cookies_str.split('&&&')
    print(f"检测到 {len(cookies_list)} 个用户，准备开始签到...")
    
    notification_messages = []  # 用于存储每个用户的签到结果

    for i, cookie in enumerate(cookies_list):
        user_num = i + 1
        print(f"\n--- 🚀 开始为用户 {user_num} 签到 ---")
        
        if not cookie.strip():
            print(f"⚠️ 用户 {user_num} 的 Cookie 为空，已跳过。")
            notification_messages.append(f"👤 **用户 {user_num}:** Cookie 为空，已跳过")
            continue

        url = "https://pan1.me/?my-sign.htm"
        headers = {
            'Accept': 'text/plain, */*; q=0.01', 'Cookie': cookie.strip(), 'Host': 'pan1.me',
            'Origin': 'https://pan1.me', 'Referer': 'https://pan1.me/', 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36 EdgA/137.0.0.0',
        }

        try:
            response = requests.post(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            try:
                result = response.json()
                message = result.get('message', '未知响应')
                if result.get('code') == '0':
                    print(f"✅ 用户 {user_num} 签到成功！信息：{message}")
                    notification_messages.append(f"👤 **用户 {user_num}:** <font color='green'>签到成功</font> - {message}")
                else:
                    print(f"⚠️ 用户 {user_num} 签到提醒：{message}")
                    notification_messages.append(f"👤 **用户 {user_num}:** <font color='orange'>操作提醒</font> - {message}")
            except json.JSONDecodeError:
                message = "响应非JSON (Cookie失效或被拦截?)"
                print(f"❌ 用户 {user_num} 签到失败：{message}")
                notification_messages.append(f"👤 **用户 {user_num}:** <font color='red'>签到失败</font> - {message}")

        except requests.exceptions.RequestException as e:
            error_message = f"网络请求错误: {e}"
            print(f"❌ 用户 {user_num} 签到失败：{error_message}")
            notification_messages.append(f"👤 **用户 {user_num}:** <font color='red'>签到失败</font> - {error_message}")
        
        if i < len(cookies_list) - 1:
            time.sleep(3)

    # --- 所有用户处理完毕，调用通知模块 ---
    final_title = "Pan1.me 签到报告"
    # PushPlus 使用 HTML 标签，Telegram 使用 Markdown，这里用 <br> 换行能兼容两者
    final_content = "<br><br>".join(notification_messages)
    
    notify.send(final_title, final_content)

if __name__ == "__main__":
    main()
