import json
import binascii
import requests
import main
import CatAndMouseGame
import os

requests.urllib3.disable_warnings()
session = requests.Session()
session.verify = False

# ===== Game's parameters =====
app_ver_ = ''
data_ver_ = 0
date_ver_ = 0
ver_code_ = ''
asset_bundle_folder_ = ''
data_server_folder_crc_ = 0
server_addr_ = 'https://game.fate-go.jp'
github_token_ = ''
github_name_ = ''

TelegramBotToken = ''
TelegramChatId = ''
TelegramTopicId = None


# ==== User Info ====
def set_latest_assets():
    global app_ver_, data_ver_, date_ver_, asset_bundle_folder_, data_server_folder_crc_, ver_code_, server_addr_

    region = main.fate_region

    # Set Game Server Depends of region

    if region == "NA":
        server_addr_ = "https://game.fate-go.us"

    # Get Latest Version of the data!
    version_str = main.get_latest_appver()
    #main.logger.info(f"vv{version_str}")

    response = requests.get(
        server_addr_ + '/gamedata/top?appVer=' + version_str).text
    response_data = json.loads(response)["response"][0]["success"]

    # Set AppVer, DataVer, DateVer
    app_ver_ = version_str
    data_ver_ = response_data['dataVer']
    date_ver_ = response_data['dateVer']
    ver_code_ = main.get_latest_verCode()

    #main.logger.info(f"ver{ver_code_}")

    # Use Asset Bundle Extractor to get Folder Name
    assetbundle = CatAndMouseGame.getAssetBundle(response_data['assetbundle'])
    get_folder_data(assetbundle)


def get_folder_data(assetbundle):
    global asset_bundle_folder_, data_server_folder_crc_

    asset_bundle_folder_ = assetbundle['folderName']
    data_server_folder_crc_ = binascii.crc32(
        assetbundle['folderName'].encode('utf8'))

# ===== End =====

user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')

httpheader = {
    'User-Agent': user_agent_2,
    'Accept-Encoding': "deflate, gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Unity-Version': "2022.3.28f1"

}


def NewSession():
    return requests.Session()

def SendTelegramMessage(message: str) -> None:
    """发送消息到配置的 Telegram 群组，支持指定话题/线程。"""
    if not TelegramBotToken or not TelegramChatId:
        print("Telegram Bot Token 或 Chat ID 未配置，跳过通知。")
        main.logger.warning("Telegram Bot Token 或 Chat ID 未配置，跳过通知。")
        return

    url = f'https://api.telegram.org/bot{TelegramBotToken}/sendMessage'
    payload = {
        'chat_id': TelegramChatId,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    if TelegramTopicId and TelegramTopicId.strip() != '' and TelegramTopicId.strip() != '0':
        try:
            # message_thread_id 必须是整数
            thread_id = int(TelegramTopicId.strip())
            payload['message_thread_id'] = thread_id
            main.logger.info(f"发送到群组 {TelegramChatId} 的话题 {thread_id}")
        except ValueError:
            main.logger.error(f"Telegram Topic ID 无效: {TelegramTopicId}。作为普通消息发送。")
    else:
        main.logger.info(f"发送到群组 {TelegramChatId} (无话题指定)")

    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        main.logger.error(f"发送 Telegram 消息失败: {e}")


def PostReq(s, url, data):
    res = s.post(url, data=data, headers=httpheader, verify=False).json()
    res_code = res['response'][0]['resCode']

    if res_code != '00':
        detail = res['response'][0]['fail']['detail']
        message = f'[ErrorCode: {res_code}]\n{detail}'
        raise Exception(message)

    return res
