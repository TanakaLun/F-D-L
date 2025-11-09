import json
import binascii
import requests
import main
import CatAndMouseGame
import os
import mytime # Added import

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
user_agent_ = 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 5 Build/RD1A.201105.003.A1)'
TelegramBotToken = ''
TelegramAdminId = ''
TelegramTopicId = None


# ==== User Info ====\n
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
    'User-Agent': user_agent_2 if user_agent_2 else user_agent_, # Use user_agent_2 if available, else fallback to user_agent_
    'Accept-Encoding': "deflate, gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Unity-Version': "2022.3.28f1"

}


def NewSession():
    return requests.Session()


def SendTelegramMessage(message: str) -> None:
    """发送消息到配置的 Telegram 群组，支持指定话题/线程。"""
    if not TelegramBotToken or not TelegramAdminId:
        main.logger.warning("Telegram Bot Token 或 Admin ID 未配置，跳过通知。")
        return

    url = f'https://api.telegram.org/bot{TelegramBotToken}/sendMessage'
    payload = {
        'chat_id': TelegramAdminId,
        'text': message,
        'parse_mode': 'Markdown'
    }

    if TelegramTopicId and str(TelegramTopicId).strip().isdigit() and str(TelegramTopicId).strip() != '0':
        try:
            thread_id = int(str(TelegramTopicId).strip())
            payload['message_thread_id'] = thread_id
            main.logger.info(f"发送到 Telegram 话题 {thread_id}")
        except ValueError:
            main.logger.error(f"Telegram Topic ID 无效: {TelegramTopicId}。作为普通消息发送。")
    else:
        main.logger.info("发送到 Telegram 主群组")

    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        main.logger.error(f"发送 Telegram 消息失败: {e}")

def send_telegram_login_report(name: str, uid: str, rewards_data: dict, bonus_data: dict | str) -> None:
    """格式化并发送登录成功报告到 Telegram。"""
    nl = '\n'
    message_parts = []
    message_parts.append(f"🎉 *FGO 登录成功* ({main.fate_region})")
    message_parts.append(f"御主: `{name}` | UID: `{uid}`")
    message_parts.append(f"等级: `{rewards_data.get('lv', 'N/A')}` | 连续登录: `{rewards_data.get('con_login', 'N/A')}`天 | 总登录: `{rewards_data.get('total_login', 'N/A')}`天")
    message_parts.append("-" * 30)
    message_parts.append("*当前资源*")
    message_parts.append(f"🔸 圣晶石: `{rewards_data.get('stone', 'N/A')}`")
    message_parts.append(f"🎫 呼符: `{rewards_data.get('ticket', 'N/A')}`")
    message_parts.append(f"🔋 体力: `{rewards_data.get('now_act', 'N/A')} / {rewards_data.get('act_max', 'N/A')}`")
    message_parts.append(f"🤝 友情点: `{rewards_data.get('total_fp', 'N/A')}`")
    message_parts.append(f"🍎 金屁屁: `{rewards_data.get('ap_recharge', 'N/A')}`")
    message_parts.append(f"💠 绿方块: `{rewards_data.get('mana', 'N/A')}`")
    message_parts.append("-" * 30)

    if bonus_data != "No Bonus":
        message_parts.append("🎁 *登录奖励*")
        message_parts.append(f"*{bonus_data.get('message', '每日奖励')}*")
        item_list = '\n'.join([f"  - {item['name']} x {item['num']}" for item in bonus_data.get('items', [])])
        message_parts.append(f"```\n{item_list}\n```")

        if bonus_data.get('bonus_name'):
            message_parts.append(f"\n*{bonus_data['bonus_name']}*")
            message_parts.append(f"__{bonus_data['bonus_detail']}__")
            camp_item_list = '\n'.join([f"  - {item['name']} x {item['num']}" for item in bonus_data.get('bonus_camp_items', [])])
            message_parts.append(f"```\n{camp_item_list}\n```")

    full_message = nl.join(message_parts)
    SendTelegramMessage(full_message)

def send_telegram_present_report(name: str, item_name: str, count: int) -> None:
    """格式化并发送礼物盒兑换报告到 Telegram。"""
    message = f"🎁 *礼物盒兑换成功* (御主: `{name}`)\n"
    message += f"兑换项目: *{item_name}* x `{count}`"
    SendTelegramMessage(message)

def send_telegram_gacha_report(name: str, gacha_result_text: str) -> None:
    """格式化并发送友情点抽卡报告到 Telegram。"""
    message = f"🎰 *友情点抽卡完成* (御主: `{name}`)\n"
    message += gacha_result_text 
    SendTelegramMessage(message)


def PostReq(s, url, data):
    res = s.post(url, data=data, headers=httpheader, verify=False).json()
    res_code = res['response'][0]['resCode']

    if res_code != '00':
        detail = res['response'][0]['fail']['detail']
        message = f'[ErrorCode: {res_code}]\n{detail}'
        raise Exception(message)

    return res
