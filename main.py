import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

userIds = os.environ['68218747'].split(',')
authKeys = os.environ['v1HVnH3vFeV4hUsv:e+8QBAAAAAA='].split(',')
secretKeys = os.environ['dWepNQmdlfQx+f3x:e+8QBAAAAAA='].split(',')
webhook_discord_url = os.environ['https://discord.com/api/webhooks/1269161108930035844/RCD-F9CxU8jQV2jRRSDm7LIUnm-OvzN0iX4lY-428z6SeP__JpnaXSzZ0OxaWlc4aHtb']
device_info = os.environ.get('OnePlus PHK110 / Android OS 13 / API-33 (PHK110_11_A.23/T.119565e-24c-14506e)')
user_agent_2 = os.environ.get('Dalvik/2.1.0 (Linux; U; Android 13; PHK110 Build/SKQ1.221012.001)')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

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
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()
        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info(f"\n ======================================== \n [+] 登录账号 \n ======================================== " )

                time.sleep(1)
                instance.topLogin_s()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                instance.lq001()
                instance.lq002()
                time.sleep(2)
                instance.buyBlueApple()
                time.sleep(1)
                instance.lq003()
                time.sleep(1)
                instance.drawFP()


            except Exception as ex:
                logger.error(ex)

if __name__ == "__main__":
    main()

