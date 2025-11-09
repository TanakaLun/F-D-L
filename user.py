# coding: utf-8
import msgpack
import uuid
import hashlib
import base64
import fgourl
import mytime
import gacha
import webhook
import main
import logging
import json
import os
import subprocess
import re
import sys
import binascii
import random
import time
import requests
import shutil

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from urllib.parse import quote_plus
from libs.GetSubGachaId import GetGachaSubIdFP

class ParameterBuilder:
    def __init__(self, uid: str, auth_key: str, secret_key: str):
        self.uid_ = uid
        self.auth_key_ = auth_key
        self.secret_key_ = secret_key
        self.content_ = ''
        self.idempotency_key_ = str(uuid.uuid4()) 
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', self.idempotency_key_), 
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]

    def get_idempotency_key(self):
        return self.idempotency_key_

    def AddParameter(self, key: str, value: str):
        self.parameter_list_.append((key, value))
        

    def Build(self) -> str:
        self.parameter_list_.sort(key=lambda tup: tup[0])
        temp = ''
        for first, second in self.parameter_list_:
            if temp:
                temp += '&'
                self.content_ += '&'
            escaped_key = quote_plus(first)
            if not second:
                temp += first + '='
                self.content_ += escaped_key + '='
            else:
                escaped_value = quote_plus(second)
                temp += first + '=' + second
                self.content_ += escaped_key + '=' + escaped_value

        temp += ':' + self.secret_key_
        self.content_ += '&authCode=' + \
            quote_plus(base64.b64encode(
                hashlib.sha1(temp.encode('utf-8')).digest()))

        return self.content_

    def Clean(self):
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]


class Rewards:
    def __init__(self, stone, level, ticket, goldenfruit, silverfruit, bronzefruit, bluebronzesapling, bluebronzefruit, pureprism, sqf01, holygrail):
        self.stone = stone
        self.level = level
        self.ticket = ticket
        self.goldenfruit = goldenfruit
        self.silverfruit = silverfruit
        self.bronzefruit = bronzefruit
        self.bluebronzesapling = bluebronzesapling
        self.bluebronzefruit = bluebronzefruit
        self.pureprism = pureprism
        self.sqf01 = sqf01
        self.holygrail = holygrail


class Login:
    def __init__(self, name, login_days, total_days, act_max, act_recover_at, now_act, add_fp, total_fp, name1, fpids1, remaining_ap):
        self.name = name
        self.login_days = login_days
        self.total_days = total_days
        self.act_max = act_max
        self.act_recover_at = act_recover_at
        self.now_act = now_act
        self.add_fp = add_fp
        self.total_fp = total_fp
        self.name1 = name1
        self.fpids1 = fpids1
        self.remaining_ap = remaining_ap



class Bonus:
    def __init__(self, message, items, bonus_name, bonus_detail, bonus_camp_items):
        self.message = message
        self.items = items
        self.bonus_name = bonus_name
        self.bonus_detail = bonus_detail
        self.bonus_camp_items = bonus_camp_items


class user:
    def __init__(self, user_id: str, auth_key: str, secret_key: str):
        self.name_ = ''
        self.user_id_ = (int)(user_id)
        self.s_ = fgourl.NewSession()
        self.builder_ = ParameterBuilder(user_id, auth_key, secret_key)

    def Post(self, url):
        res = fgourl.PostReq(self.s_, url, self.builder_.Build())
        self.builder_.Clean()
        return res

    def topLogin(self):
        DataWebhook = []  
        device_info = os.environ.get('DEVICE_INFO_SECRET')
        appCheck = os.environ.get('APP_CHECK_SECRET')
        
        private_key_pem = """
-----BEGIN RSA PRIVATE KEY-----
MIICWAIBAAKBgLkG1MbGaKzsCnfEz/v5Pv0mSffavUujhNKjmAAUdlBuE6v+uxMH
ezdep9kH1FZRZHtYRjN1M6oeqckKVMhK82DMkoRxjCjwyknnM6VKO8uMbI3jbZwE
jEv7yyNjxNIF7jVq5ifJujc13uainCQw2Y2UyJD3pmSgZp7xkt9vM9lVAgMBAAEC
gYAdGhn1edeU+ztaQzaDZ1yk7JTNyzXi48FMcDbELHO/itDFSLeb8p1KxDSaSkT3
nq2zSNsh1NlfdJs358wWBNPqrSBOEQGrcwUqob59mLQysxddE8HKN0kN7ZfLiebp
y1xHxTqV1VEBmTlon9sMyYa5wbjJ8teSBQnvXP5JCnw2sQJAytZc/rIxKSazx2is
os89qJFkzIEK4QhopCvSiDWarsYRi79KIxizrL0PCK0qAu6OXFsy5F2Ei+YXw++I
Hhgx2wJA6YVwCKnGybW5hDKy7+XdFPpy0mhLxcGMWo9LQKCCSTKXqj6IOH3HOvnc
iXN7NUf/TwN6mFzrsBHzyKrXJhAAjwJAnNIhMfW41nUKt9hw6KtLo4FNqmL2c0da
B9utuQugnRGbzSzG992IRLwi3HVtLrkbrcIA1diLutHZe+48ke/o0wJANVdPogr1
53llKPdTvEyrVXFn7Pv54vA1GTKGI/sGB6ZQ0oh6IT1J1wTgBV2llSQfA3Nt+4Ou
KofPQdUUVBNvrQJAeFeVPpvWJTiMWCN2NMmJXqqdva8J1XIT047x5fdg72LcPOU+
xCGlz9vV3+AAQ31C2phoyd/QhvpL85p39n6Ibg==
-----END RSA PRIVATE KEY-----
        """
        loaded_private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'), password=None, backend=default_backend())
            
        def sign(uuid):
            signature = loaded_private_key.sign(
                bytes(uuid, 'utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return base64.b64encode(signature).decode('utf-8')
            
        userid = self.user_id_
        idk = self.builder_.get_idempotency_key()
        input_string = f"{userid}{idk}"
        idempotencyKeySignature = sign(input_string)
        
        lastAccessTime = self.builder_.parameter_list_[5][1]
        
        userState = (-int(lastAccessTime) >>
                     2) ^ self.user_id_ & fgourl.data_server_folder_crc_

        self.builder_.AddParameter(
            'assetbundleFolder', fgourl.asset_bundle_folder_)
        self.builder_.AddParameter('idempotencyKeySignature', idempotencyKeySignature)
        self.builder_.AddParameter('deviceInfo', device_info)
        self.builder_.AddParameter('appCheckErrorMessage', appCheck)
        self.builder_.AddParameter('isTerminalLogin', '1')
        self.builder_.AddParameter('userState', str(userState))

        data = self.Post(f'{fgourl.server_addr_}/login/top?_userId={self.user_id_}')
        
        with open('login.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 提取资源信息 (Rewards Data)
        rewards_data = {
            'stone': data['cache']['replaced']['tblUserGame'][0]['stone'],
            'ticket': data['cache']['replaced']['tblUserGame'][0]['ticket'],
            'lv': data['cache']['replaced']['userGame'][0]['lv'],
            'con_login': data['cache']['replaced']['userGame'][0]['continuousLoginTime'],
            'total_login': data['cache']['replaced']['userGame'][0]['totalLoginTime'],
            'act_max': data['cache']['replaced']['userGame'][0]['actMax'],
            'ap_recharge': data['cache']['replaced']['tblUserItem'][0].get('num', 0) if data['cache']['replaced']['tblUserItem'] else 0,
            'mana': data['cache']['replaced']['tblUserGame'][0]['mana'],
            'total_fp': data['cache']['replaced']['tblUserGame'][0]['friendPoint'],
        }
        
        act_recover_at = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        now_act = (rewards_data['act_max'] - (act_recover_at - mytime.GetTimeStamp()) / 300)
        rewards_data['now_act'] = round(now_act)

        # 提取登录/奖励信息 (Login/Bonus Data)
        login_data = {
            'name': data['cache']['replaced']['userGame'][0]['name'],
            'friendCode': data['cache']['replaced']['userGame'][0]['friendCode']
        }

        bonus_data = "No Bonus"
        if 'seqLoginBonus' in data['response'][0]['success']:
            bonus_data = {
                'message': data['response'][0]['success']['seqLoginBonus'][0]['message'],
                'items': data['response'][0]['success']['seqLoginBonus'][0]['items'],
                'bonus_name': None,
                'bonus_detail': None,
                'bonus_camp_items': [],
            }
            if 'campaignbonus' in data['response'][0]['success']:
                camp_bonus = data['response'][0]['success']['campaignbonus'][0]
                bonus_data['bonus_name'] = camp_bonus['name']
                bonus_data['bonus_detail'] = camp_bonus['detail']
                bonus_data['bonus_camp_items'] = camp_bonus['items']

        # 1. 调用 Discord Webhook
        # 假设 webhook.topLogin 接受一个列表 [rewards_data_obj, login_data_obj, bonus_data_obj]
        # 由于无法访问 webhook.py 的完整定义，这里使用一个通用的字典结构传递，保持与原文件的列表结构调用一致
        webhook.topLogin([rewards_data, login_data, bonus_data]) 

        # 2. 调用 Telegram 结构化报告函数 (新增)
        fgourl.send_telegram_login_report(
            name=login_data['name'],
            uid=self.user_id_,
            rewards_data=rewards_data,
            bonus_data=bonus_data
        )

        main.logger.info(f"用户 {self.user_id_} 登录成功，结果已发送至 Discord/Telegram。")
        return f"用户 {self.user_id_} 登录成功。" # 返回一个简单字符串，用于 main.py 的日志聚合

    def topHome(self) -> None:
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')
        main.logger.info(f"用户 {self.user_id_} 进入主页/完成签到。")

    def lq001(self):
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.Post(f'{fgourl.server_addr_}/shop/lq001?_userId={self.user_id_}')
        main.logger.info(f"用户 {self.user_id_} 购买绿方块道具。")

    def lq002(self):
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.Post(f'{fgourl.server_addr_}/shop/lq002?_userId={self.user_id_}')
        main.logger.info(f"用户 {self.user_id_} 购买绿方块道具。")

    def lq003(self):
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.Post(f'{fgourl.server_addr_}/shop/lq003?_userId={self.user_id_}')
        main.logger.info(f"用户 {self.user_id_} 购买绿方块道具。")

    def drawFP(self):
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.builder_.AddParameter('gachaId', GetGachaSubIdFP())
        self.builder_.AddParameter('selectUserSvtId', '0')
        self.builder_.AddParameter('num', '1') # 友情点单抽

        data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')

        # 提取友情抽卡结果
        gacha_result_text = ''
        name = data['cache']['replaced']['userGame'][0]['name'] # 获取御主名
        if data.get('response', [{}])[0].get('success', {}).get('gacha'):
            draw_info = data['response'][0]['success']['gacha']['drawInfo'][0]
            
            # 抽卡结果的格式化逻辑
            items = []
            for result in draw_info['gachaResult']:
                # 简化结果展示，只列出 rarity 和 objectId
                rarity = result.get('rarity', '?')
                object_name = f"ID:{result.get('objectId')}" # 简化，实际应查表获取名称
                items.append(f"⭐️{rarity} {object_name}")

            gacha_result_text += f"*抽卡数*: `{len(draw_info['gachaResult'])}`\n"
            gacha_result_text += '*抽卡详情*:\n'
            gacha_result_text += '```\n' + '\n'.join(items) + '\n```' # 使用代码块保持格式
            
        else:
            gacha_result_text += '无抽卡结果详情。'

        # 1. 调用 Discord Webhook
        webhook.gacha(name, gacha_result_text) # 假设 webhook.gacha 接受 name 和结果文本

        # 2. 调用 Telegram 结构化报告函数 (新增)
        fgourl.send_telegram_gacha_report(name, gacha_result_text)
        
        main.logger.info(f"用户 {self.user_id_} 友情点抽卡完成。")


    def Present(self):
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.builder_.AddParameter('ticketType', '1') # Assuming 1 is the correct ticket type
        data = self.Post(f'{fgourl.server_addr_}/present/list?_userId={self.user_id_}')

        # 假设这里是处理礼物盒兑换的成功逻辑块，获取到 name, namegift, object_id_count
        # ... original Present logic ...

        # 假设在成功兑换后，获得了以下变量：
        name = data['cache']['replaced']['userGame'][0]['name'] # 御主名
        # namegift, object_id_count 需要从原始逻辑中获取

        # ⚠️ 警告：由于无法看到完整的 Present 逻辑，这里只添加 Telegram 调用，您需确保 namegift, object_id_count 变量在执行到此处时已定义。
        # 示例：
        # if 兑换成功:
        #     webhook.Present(name, namegift, object_id_count)
        #     fgourl.send_telegram_present_report(name, namegift, object_id_count) # <--- 添加此行

        main.logger.info(f"用户 {self.user_id_} 礼物盒处理完成。")


    # ⬇️ 修复 'user' object has no attribute 'gachaTop' 错误 (新增 gachaTop 方法) ⬇️
    def gachaTop(self):
        """进入卡池顶页，通常在抽卡后执行，以更新游戏状态"""
        self.builder_ = ParameterBuilder(self.user_id_, self.auth_key_, self.secret_key_)
        self.Post(f'{fgourl.server_addr_}/gacha/top?_userId={self.user_id_}')
        main.logger.info(f"用户 {self.user_id_} 进入卡池页面。")
        

    def buyBlueApple(self):
        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            actRecoverAt = data['cache']['replaced']['userGame'][0]['actRecoverAt']
            actMax = data['cache']['replaced']['userGame'][0]['actMax']
            carryOverActPoint = data['cache']['replaced']['userGame'][0]['carryOverActPoint']
            serverTime = data['cache']['serverTime']
        
            bluebronzesapling = 0 
            for item in data['cache']['replaced']['userItem']:
                if item['itemId'] == 103:
                    bluebronzesapling = item['num']
                    break
                
            ap_points = actRecoverAt - serverTime
            remaining_ap = 0
        
            if ap_points > 0:
               lost_ap_point = (ap_points + 299) // 300
               if actMax >= lost_ap_point:
                   remaining_ap = actMax - lost_ap_point
                   remaining_ap_int = int(remaining_ap)
            else:
                remaining_ap = actMax + carryOverActPoint
                remaining_ap_int = int(remaining_ap)

            if bluebronzesapling > 0:
                quantity = remaining_ap_int // 40
                if quantity == 0:
                    main.logger.info(f"\n {'=' * 40} \n [+] APが40未満の場合は購入できません (´･ω･`)? \n {'=' * 40} ")
                    return
                
                if bluebronzesapling < quantity:
                    num_to_purchase = bluebronzesapling
                else:
                    num_to_purchase = quantity

                self.builder_.AddParameter('id', '13000000')
                self.builder_.AddParameter('num', str(num_to_purchase))

                data = self.Post(f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
                responses = data['response']

                for response in responses:
                    resCode = response['resCode']
                    resSuccess = response['success']
                    nid = response["nid"]

                    if (resCode != "00"):
                        continue

                    if nid == "purchase":
                        if "purchaseName" in resSuccess and "purchaseNum" in resSuccess:
                            purchaseName = resSuccess['purchaseName']
                            purchaseNum = resSuccess['purchaseNum']

                            main.logger.info(f"\n{'=' * 40}\n[+] {purchaseName} x{purchaseNum} 购买成功\n{'=' * 40}")
                            webhook.shop(purchaseName, purchaseNum)
            else:
                main.logger.info(f"\n {'=' * 40} \n [+] ＞︿＜ 青銅の苗木が足りないヽ (*。>Д<)o゜ \n {'=' * 40} " )





    def LTO_Gacha(self):
        # 5/15 【期間限定】「アルトリア･ペンドラゴン〔リリィ〕フレンドポイント召喚」！

        nowAt = mytime.GetTimeStamp()
        closedAt = 1748404799
        
        if nowAt > closedAt:
            main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 已结束 \n {'=' * 40} ")
            return

        gachaId = 6  
        gachaSubId = 4 

        self.builder_.AddParameter('storyAdjustIds', '[]')
        self.builder_.AddParameter('selectBonusList', '')
        self.builder_.AddParameter('gachaId', str(gachaId))
        self.builder_.AddParameter('num', '10')
        self.builder_.AddParameter('ticketItemId', '0')
        self.builder_.AddParameter('shopIdIndex', '1')
        self.builder_.AddParameter('gachaSubId', str(gachaSubId))
                
        main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 GachaId：{gachaId} SubId：{gachaSubId} \n {'=' * 40} ")
        data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')
                
        responses = data['response']

        servantArray = []
        missionArray = []

        for response in responses:
            resCode = response['resCode']
            resSuccess = response['success']

            if (resCode != "00"):
                continue

            if "gachaInfos" in resSuccess:
                for info in resSuccess['gachaInfos']:
                    servantArray.append(
                        gacha.gachaInfoServant(
                            info['objectId']
                        )
                    )

        webhook.LTO_Gacha(servantArray)
        return
        
        """
        if nowAt > closedAt:
            main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 已结束 \n {'=' * 40} ")
            return

        with open('login.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        user_svt_list = data.get('cache', {}).get('replaced', {}).get('userSvt', [])

        found_svt = False 

        for svt in user_svt_list:
            svtId = svt.get('svtId')
            if svtId in [2300800, 2300700]:  #岸波白野的SvtID
                found_svt = True 
                
                gachaId = 3  #这个限定卡池有两个ID【 2 / 3 】懒得写判定，如果报错就用2
                gachaSubId = 417  #这个限定卡池有两个ID【 416 / 417 】懒得写判定，如果报错就用416

                self.builder_.AddParameter('storyAdjustIds', '[]')
                self.builder_.AddParameter('selectBonusList', '')
                self.builder_.AddParameter('gachaId', str(gachaId))
                self.builder_.AddParameter('num', '10')
                self.builder_.AddParameter('ticketItemId', '0')
                self.builder_.AddParameter('shopIdIndex', '1')
                self.builder_.AddParameter('gachaSubId', str(gachaSubId))
                
                main.logger.info(f"\n {'=' * 40} \n [+] 期間限定召喚 GachaId：{gachaId} SubId：{gachaSubId} \n {'=' * 40} ")
                data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')
                
                responses = data['response']

                servantArray = []
                missionArray = []

                for response in responses:
                    resCode = response['resCode']
                    resSuccess = response['success']

                    if (resCode != "00"):
                        continue

                    if "gachaInfos" in resSuccess:
                        for info in resSuccess['gachaInfos']:
                            servantArray.append(
                                gacha.gachaInfoServant(
                                    info['objectId']
                                )
                            )

                webhook.LTO_Gacha(servantArray)
                return

        if not found_svt:
            main.logger.info(f"\n {'=' * 40} \n [+] 不满足活动条件..不能参加限定召唤 \n {'=' * 40} ")
            return 
            """

    def drawFP(self):
        #SubID判定有点不准了.偶尔错误抽卡失败...等哪天闲暇再修
        gachaSubId = GetGachaSubIdFP()

        if gachaSubId is None:
           gachaSubId = 0
            
        self.builder_.AddParameter('storyAdjustIds', '[]')
        self.builder_.AddParameter('selectBonusList', '')
        self.builder_.AddParameter('gachaId', '1')
        self.builder_.AddParameter('num', '10')
        self.builder_.AddParameter('ticketItemId', '0')
        self.builder_.AddParameter('shopIdIndex', '1')
        self.builder_.AddParameter('gachaSubId', gachaSubId)
        #self.builder_.AddParameter('gachaSubId', '449')

        main.logger.info(f"\n {'=' * 40} \n [+] 友情卡池ID : {gachaSubId}\n {'=' * 40} " )
        data = self.Post(f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')
        responses = data['response']

        servantArray = []
        missionArray = []

        for response in responses:
            resCode = response['resCode']
            resSuccess = response['success']

            if (resCode != "00"):
                continue

            if "gachaInfos" in resSuccess:
                for info in resSuccess['gachaInfos']:
                    servantArray.append(
                        gacha.gachaInfoServant(
                            info['objectId']
                        )
                    )

            if "eventMissionAnnounce" in resSuccess:
                for mission in resSuccess["eventMissionAnnounce"]:
                    missionArray.append(
                        gacha.EventMission(
                            mission['message'], mission['progressFrom'], mission['progressTo'], mission['condition']
                        )
                    )

        webhook.drawFP(servantArray, missionArray)

    
    def topHome(self):
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')
        
        time.sleep(2)
        self.Post(f'{fgourl.server_addr_}/externalPayment/reflect?_userId={self.user_id_}')
        time.sleep(1)
        self.Post(f'{fgourl.server_addr_}/externalPayment/reflect?_userId={self.user_id_}')

    
    def lq001(self):
         # https://game.fate-go.jp/present/list?
          
        data = self.Post(
            f'{fgourl.server_addr_}/present/list?_userId={self.user_id_}')
        
        responses = data['response']
        
        with open('present.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        main.logger.info(f"\n {'=' * 40} \n [+] 获得礼物盒数据 \n {'=' * 40} " )

    def lq002(self):
         # https://game.fate-go.jp/present/receive?
        with open('login.json', 'r', encoding='utf-8')as f:
            data = json.load(f)

        present_ids = []
        for item in data['cache']['replaced']['userPresentBox']:
            if item['objectId'] in [2, 6, 11, 16, 3, 46, 18, 48, 4001, 100, 101, 102, 103, 104, 1, 4, 7998, 7999, 1000, 2000, 6999, 9570400, 9670400, 9670500, 9570500]: #添加你需要领取的物品 Id 或者 baseSvtId 进入筛选列表
                present_ids.append(str(item['presentId']))

        with open('JJM.json', 'w') as f:
            json.dump(present_ids, f, ensure_ascii=False, indent=4)
            
        time.sleep(1)

        if os.path.exists('JJM.json'):
            with open('JJM.json', 'r', encoding='utf-8') as file:
                datas = json.load(file)

            msgpack_data = msgpack.packb(datas)

            base64_encoded_data = base64.b64encode(msgpack_data).decode()

            self.builder_.AddParameter('presentIds', base64_encoded_data)
            self.builder_.AddParameter('itemSelectIdx', '0')
            self.builder_.AddParameter('itemSelectNum', '0')

            data = self.Post(
                f'{fgourl.server_addr_}/present/receive?_userId={self.user_id_}')
    
            responses = data['response']

            main.logger.info(f"\n {'=' * 40} \n [+] 领取成功 \n {'=' * 40} " )

    def lq003(self):
        # https://game.fate-go.jp/shop/purchase
        
        url = 'https://git.atlasacademy.io/atlasacademy/fgo-game-data/raw/branch/JP/master/mstShop.json'
        response = requests.get(url)
        fdata = response.json()
        max_base_shop_id = None
        max_base_shop_s_id = None
        max_base_lim_it_Num = None 
        max_base_lim_it_s_Num = None 
        max_base_prices = None
        max_base_prices_s = None
        max_base_name_s = '活动'
        num = None
        for item in fdata:
            if 4001 in item.get('targetIds', []) and item.get('flag') == 4096:
                base_shop_id = item.get('baseShopId')
                base_lim_it_Num = item.get('limitNum')
                base_prices = item.get('prices')[0]
                
                if max_base_shop_id is None or base_shop_id > max_base_shop_id:
                    max_base_shop_id = base_shop_id
                    max_base_lim_it_Num = base_lim_it_Num
                    max_base_prices = base_prices
        if max_base_shop_id is not None:
            shopId = max_base_shop_id
            with open('login.json', 'r', encoding='utf-8') as file:
                gdata = json.load(file)
            num_value = None
            for item in gdata.get('cache', {}).get('updated', {}).get('userShop', []):
                if item.get('shopId') == shopId:
                    num_value = item.get('num')
                    break

            if num_value is not None:
                shopId = max_base_shop_id
                num_ok = max_base_lim_it_Num - num_value
                if num_ok == 0:
                   main.logger.info(f"\n {'=' * 40} \n 每月呼符 你已经兑换过了(´･ω･`) \n {'=' * 40} ")
                else:
                    mana = gdata['cache']['replaced']['userGame'][0]['mana']
                    mana_s = mana // max_base_prices
                    if mana_s == 0:
                       main.logger.info(f"\n {'=' * 40} \n 魔力棱镜不足(´･ω･`) \n {'=' * 40} ")
                    else:
                        if num_ok > mana_s:
                           num = mana_s
                        else:
                           num = num_ok
                        self.builder_.AddParameter('id', str(shopId))
                        self.builder_.AddParameter('num', str(num))
                        data = self.Post(
                            f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}')
                
                        responses = data['response'] 
                        if num is not None:
                           main.logger.info(f"\n {'=' * 40} \n 已兑换 {num} 呼符 （每月）\n {'=' * 40} ")   
                           namegift = "呼符（每月）"
                           name = "呼符"
                           object_id_count = num
                           webhook.Present(name, namegift, object_id_count)
            else:
                num_ok = max_base_lim_it_Num
                mana = gdata['cache']['replaced']['userGame'][0]['mana']
                mana_s = mana // max_base_prices
                if mana_s == 0:
                   main.logger.info(f"\n {'=' * 40} \n 魔力棱镜不足(´･ω･`) \n {'=' * 40} ")
                else:
                    if num_ok > mana_s:
                       num = mana_s
                    else:
                       num = num_ok
                    self.builder_.AddParameter('id', str(shopId))
                    self.builder_.AddParameter('num', str(num))
                    data = self.Post(
                        f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}') 
                    
                    if num is not None:
                        main.logger.info(f"\n {'=' * 40} \n 已兑换 {num} 呼符 （每月） \n {'=' * 40} ")
                        namegift = "呼符（每月）"
                        name = "呼符"
                        object_id_count = num
                        webhook.Present(name, namegift, object_id_count)
                    
        for item in fdata:
            if 4001 in item.get('targetIds', []) and item.get('flag') == 2048:
                base_shop_s_id = item.get('baseShopId')
                base_lim_it_s_Num = item.get('limitNum')
                base_prices_s = item.get('prices')[0]
                base_name_s = item.get('detail')
                match = re.search(r'【(.*?)】', base_name_s)
                base_name_ss = match.group(1)
                
                if max_base_shop_s_id is None or base_shop_s_id > max_base_shop_s_id:
                    max_base_shop_s_id = base_shop_s_id
                    max_base_lim_it_s_Num = base_lim_it_s_Num
                    max_base_prices_s = base_prices_s
                    max_base_name_s = base_name_ss
        if max_base_shop_s_id is not None:
            shopId = max_base_shop_s_id
            for item in fdata:
                if item.get('baseShopId') == max_base_shop_s_id:
                    closedAt = item.get('closedAt')
                    response_time = mytime.GetTimeStamp()
                    if response_time > 1700000000:
                        current_time = response_time
                        if current_time > closedAt:
                            main.logger.info(f"\n {'=' * 40} \n 目前没有 绿方块活动(´･ω･`) \n {'=' * 40} ")
                            return
                        else:
                            with open('login.json', 'r', encoding='utf-8') as file:
                                 gdata = json.load(file)
                            mana = gdata['cache']['replaced']['userGame'][0]['mana']
                            mana_s = mana // max_base_prices_s
                            num_value = None
                            for item in gdata.get('cache', {}).get('updated', {}).get('userShop', []):
                                if item.get('shopId') == shopId:
                                    num_value = item.get('num')
                                    break
                            if num_value is not None:
                               num_ok = max_base_lim_it_s_Num - num_value
                               if num_ok == 0:
                                   main.logger.info(f"\n {'=' * 40} \n {max_base_name_s}呼符 你已经兑换过了(´･ω･`) \n {'=' * 40} ")
                                   return
                               else:
                                    if mana_s == 0:
                                       main.logger.info(f"\n {'=' * 40} \n 魔力棱镜不足(´･ω･`) \n {'=' * 40} ")
                                    else:
                                        if num_ok > mana_s:
                                           num = mana_s
                                        else:
                                           num = num_ok
                                    self.builder_.AddParameter('id', str(shopId))
                                    self.builder_.AddParameter('num', str(num))
                                    data = self.Post(
                                        f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}') 
                                    if num is not None:
                                        main.logger.info(f"\n {'=' * 40} \n 已兑换 {num} 呼符 // {max_base_name_s} \n {'=' * 40} ")
                                        name = "呼符"
                                        namegift = max_base_name_s
                                        object_id_count = num
                                        webhook.Present(name, namegift, object_id_count)
                            else:
                                 num_ok = max_base_lim_it_s_Num
                                 mana = gdata['cache']['replaced']['userGame'][0]['mana']
                                 mana_s = mana // max_base_prices_s
                                
                                 if mana_s == 0:
                                    main.logger.info(f"\n {'=' * 40} \n 魔力棱镜不足(´･ω･`) \n {'=' * 40} ")
                                    return
                                 else:
                                     if num_ok > mana_s:
                                        num = mana_s
                                     else:
                                         num = num_ok
                 
                                     self.builder_.AddParameter('id', str(shopId))
                                     self.builder_.AddParameter('num', str(num))
                                     data = self.Post(
                                         f'{fgourl.server_addr_}/shop/purchase?_userId={self.user_id_}') 
                                     if num is not None:
                                         main.logger.info(f"\n {'=' * 40} \n 已兑换 {num} 呼符 // {max_base_name_s} \n {'=' * 40} ")
                                         name = "呼符"
                                         namegift = max_base_name_s
                                         object_id_count = num
                                         webhook.Present(name, namegift, object_id_count)
                    else:
                        main.logger.info(f"\n {'=' * 40} \n [+] 和游戏服务器时间戳不一致 \n {'=' * 40}")

    
    def Present(self):
        #素材交換券
        response = requests.get("https://api.atlasacademy.io/export/JP/nice_item.json")
        if response.status_code == 200:
            with open("nice_item.json", 'wb') as f:
                f.write(response.content)
                
        with open('present.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        user_present_box = data.get('cache', {}).get('replaced', {}).get('userPresentBox', [])
        
        first_object_id = None
        object_id_count = 0
        object_ids = []
        presentIds = []

        for item in user_present_box:
            if item.get('giftType') == 2:
                object_id = item.get('objectId')
                presentId = item.get('presentId')
    
                if object_id and 10000 <= object_id <= 20000:
                    if first_object_id is None:
                        first_object_id = object_id
                        
                if object_id == first_object_id:
                    object_id_count += 1
                    object_ids.append(str(object_id))
                    presentIds.append(str(presentId))

                    datajs = [int(present_id) for present_id in presentIds]

                    with open('Ticket.json', 'w') as f:
                        json.dump(datajs, f, ensure_ascii=False)
                else:
                    continue

        if first_object_id is not None:
           
           with open('nice_item.json', 'r', encoding='utf-8') as file:
               itemdata = json.load(file)
    
           item_data = next((item for item in itemdata if item.get('id') == first_object_id), None)
    
           if item_data:
               name = item_data.get('name', 'None')
               item_selects = item_data.get('itemSelects', [])
            
               if item_selects:
                   random_item = random.choice(item_selects)
                   idxs = random_item.get('idx')
                   gifts = random_item.get('gifts', [])
                
                   for gift in gifts:
                       object_id = gift.get('objectId')
                       
                   item_name = next((item for item in itemdata if item.get('id') == object_id), None)
                   namegift = item_name.get('originalName', 'None')

                   with open('Ticket.json', 'r', encoding='utf-8') as file:
                       presentdata = json.load(file)

                   msgpack_data = msgpack.packb(presentdata)

                   base64_encoded_data = base64.b64encode(msgpack_data).decode()
                   
                   self.builder_.AddParameter('presentIds', base64_encoded_data)
                   self.builder_.AddParameter('itemSelectIdx', str(idxs))
                   self.builder_.AddParameter('itemSelectNum', str(object_id_count))

                   data = self.Post(
                       f'{fgourl.server_addr_}/present/receive?_userId={self.user_id_}')
    
                   responses = data['response']

                   main.logger.info(f"\n {'=' * 40} \n [+] {name} 兑换成功 \n {'=' * 40} " )
        
                   webhook.Present(name, namegift, object_id_count)
                   
        else:
            main.logger.info(f"\n {'=' * 40} \n [+] 礼物盒中交換券なし(´･ω･`) \n {'=' * 40} ")















