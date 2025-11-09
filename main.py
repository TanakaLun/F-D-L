import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging
import mytime
import traceback
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
webhook_discord_url = os.environ.get('webhookDiscord')
device_info = os.environ.get('DEVICE_INFO_SECRET')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

fgourl.TelegramBotToken = os.environ.get('TGBotToken')
fgourl.TelegramAdminId = os.environ.get('TGAdminId')
fgourl.TelegramTopicId = os.environ.get('TGTopicId')
fgourl.github_token_ = os.environ.get('GithubToken')
fgourl.github_name_ = os.environ.get('GithubName')

def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    try:
        response = requests.get(endpoint, timeout=10).text
        response_data = json.loads(response)
        return response_data['verCode']
    except Exception as e:
        logger.error(f"无法获取最新 verCode: {e}")
        return "2222222"

def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    try:
        response = requests.get(endpoint, timeout=10).text
        response_data = json.loads(response)
        return response_data['appVer']
    except Exception as e:
        logger.error(f"无法获取最新 appVer: {e}")
        return "2.22.2"


def main():
    fgourl.SendTelegramMessage(f'🤖 *FGO 自动登录开始* (UTC+8: {mytime.GetFormattedNowTime()})')

    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets() 
        logger.info(f"成功获取到最新游戏版本: AppVer={fgourl.app_ver_}, VerCode={fgourl.ver_code_}")

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                logger.info(f"\n {'=' * 40} \n [+] 登录账号 \n {'=' * 40} " )
                
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
                instance.gachaTop()

            except Exception as e:
                logger.error(f"处理用户 {userIds[i]} 失败: {e}")
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