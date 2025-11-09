import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging
import mytime # Added mytime import for the start message
import traceback # Added traceback import for detailed error logs

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
webhook_discord_url = os.environ['webhookDiscord']
device_info = os.environ.get('DEVICE_INFO_SECRET')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

# ⬇️ 修正/新增 Telegram 环境变量加载 ⬇️
fgourl.TelegramBotToken = os.environ.get('TGBotToken')
fgourl.TelegramAdminId = os.environ.get('TGAdminId')
fgourl.TelegramTopicId = os.environ.get('TGTopicId')

# 原始文件中的其他 env vars 保持不变
fgourl.ver_code_ = os.environ['verCode']
fgourl.github_token_ = os.environ['GithubToken']
fgourl.github_name_ = os.environ['GithubName']
UA = os.environ['UserAgent']
if UA != 'nullvalue':
    fgourl.user_agent_ = UA
# ⬆️ 修正/新增 Telegram 环境变量加载 ⬆️


def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']
    
def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['appVer']


def main():
    fgourl.SendTelegramMessage(f'🤖 *FGO 自动登录开始* (UTC+8: {mytime.GetFormattedNowTime()})')

    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()
        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                logger.info(f"\n {'=' * 40} \n [+] 登录账号 \n {'=' * 40} " )
                
                # 登录和操作，这些方法已在 user.py 中更新以发送详细 Telegram 报告
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(0.5)
                instance.lq001()
                time.sleep(0.5)
                instance.Present()
                time.sleep(0.5)
                instance.lq002()
                time.sleep(2)
                instance.buyBlueApple()
                time.sleep(1)
                instance.lq003()
                time.sleep(1)
                instance.drawFP()
                time.sleep(1)
                instance.gachaTop() # 现在已在 user.py 中修复

            except Exception as e:
                logger.error(f"处理用户 {userIds[i]} 失败: {e}")
                # 出现错误时，发送错误消息到 Telegram，包含详细堆栈信息
                error_trace = traceback.format_exc()
                fgourl.SendTelegramMessage(
                    f'❌ *账号处理失败*\n用户ID: `{userIds[i]}`\n错误: `{e}`\n\n*详细追踪*:\n```\n{error_trace}\n```'
                )

        fgourl.SendTelegramMessage(f'✅ *FGO 自动登录结束* (处理 {userNums} 个账号)')
    else:
        logger.error(f"配置错误: 用户ID/AuthKey/SecretKey数量不匹配。")
        fgourl.SendTelegramMessage(f'🚨 *配置错误*\n请检查 GitHub Secrets 中 `userIds`, `authKeys`, `secretKeys` 的数量是否一致。')

if __name__ == '__main__':
    main()