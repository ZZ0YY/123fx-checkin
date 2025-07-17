# Pan1.me 自动签到脚本

一个基于 GitHub Actions 的全自动签到脚本，支持多用户和多种消息推送渠道。

## ✨ 主要功能

- **多用户支持**：通过环境变量一次性配置多个账号。
- **模块化推送**：将通知功能分离，轻松扩展新渠道。
- **已支持渠道**：
  - [PushPlus](http://www.pushplus.plus/)
  - [Telegram Bot](https://core.telegram.org/bots)
- **安全可靠**：所有敏感信息均通过 GitHub Secrets 加密存储。
- **详细日志**：签到过程和结果清晰可见。

## 🚀 使用方法

1.  **Fork 仓库**：点击本仓库右上角的 **Fork** 按钮。
2.  **设置 Secrets**：进入你 Fork 的仓库，点击 **Settings** > **Secrets and variables** > **Actions**，然后点击 **New repository secret** 创建以下变量。
3.  **启用 Actions**：点击仓库上方的 **Actions** 标签，并按提示启用工作流。

### 环境变量 (Secrets)

| Secret 名称       | 说明                                                                                                                                              | 是否必需 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `PAN_COOKIES`     | **你的身份凭证**。多个账号的 Cookie 请用 `&&&` 分隔。                                                                                             | **是**   |
| `PUSH_PLUS_TOKEN` | [PushPlus](http://www.pushplus.plus/) 的 Token，用于推送消息。                                                                                     | 否       |
| `TG_BOT_TOKEN`    | Telegram 机器人的 Token。需和 `TG_USER_ID` 配合使用。在 Telegram 中向 `@BotFather` 申请。                                                           | 否       |
| `TG_USER_ID`      | 你的 Telegram User ID。需和 `TG_BOT_TOKEN` 配合使用。在 Telegram 中向 `@userinfobot` 发送消息获取。                                                  | 否       |

**`PAN_COOKIES` 示例 (两个用户):**
`bbs_sid=user1_cookie...&&&bbs_sid=user2_cookie...`

### 手动运行

你可以在 Actions 页面，选择 "Pan1.me Auto Check-in"，然后点击 "Run workflow" 来立即测试。

## 🔧 扩展新推送渠道

要添加新的推送渠道 (例如 Bark, Discord)，你只需要：
1.  在 `notify.py` 文件中，仿照 `_send_pushplus` 添加一个新的私有函数 `_send_new_channel()`。
2.  在 `send()` 主函数中，添加对新渠道 Token 的检测和函数调用。
3.  在 `.github/workflows/auto_checkin.yml` 的 `env` 部分添加新的 `secrets`。
