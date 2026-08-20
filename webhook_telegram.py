import os
import logging
import requests
from typing import Optional

logger = logging.getLogger("FGO Daily Login.Telegram")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_TOPIC_ID = os.environ.get("TELEGRAM_TOPIC_ID")

# 如果未配置 token 或 chat_id，则禁用 Telegram 通知
TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)


def _send_telegram_message(text: str) -> None:
    """发送 Telegram 消息，失败时记录日志但不抛出异常"""
    if not TELEGRAM_ENABLED:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    if TELEGRAM_TOPIC_ID:
        payload["message_thread_id"] = int(TELEGRAM_TOPIC_ID)

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.warning(f"Telegram 发送失败 (HTTP {resp.status_code}): {resp.text[:200]}")
    except Exception as e:
        logger.warning(f"Telegram 发送异常: {e}")


def top_login(data: list) -> None:
    """发送登录结果到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    rewards = data[0]
    login = data[1]
    bonus = data[2]

    lines = [
        f"<b>FGO登录系统 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        f"👤 御主名: {login.name1}",
        f"🔢 朋友ID: {login.fpids1}",
        f"⭐ 等级: {rewards.level}",
        f"🎫 呼符: {rewards.ticket}",
        f"💎 圣晶石: {rewards.stone}",
        f"🧩 圣晶片: {rewards.sqf01}",
        f"🍎 金苹果: {rewards.goldenfruit}",
        f"🍏 银苹果: {rewards.silverfruit}",
        f"🥔 铜苹果: {rewards.bronzefruit}",
        f"🫐 蓝苹果: {rewards.bluebronzefruit}",
        f"🌱 蓝苹果树苗: {rewards.bluebronzesapling}",
        f"📅 连续登录: {login.login_days} 天",
        f"📆 累计登录: {login.total_days} 天",
        f"⬜ 白方块: {rewards.pureprism}",
        f"🤝 友情点: {login.total_fp}",
        f"➕ 今日友情点: +{login.add_fp}",
        f"⚡ 当前AP: {login.remaining_ap}",
        f"🏆 圣杯: {rewards.holygrail}",
    ]

    if bonus != "No Bonus":
        lines.append("")
        lines.append(f"<b>🎁 {bonus.message}</b>")
        for item in bonus.items:
            lines.append(f"  • {item}")
        if bonus.bonus_name:
            lines.append("")
            lines.append(f"<b>🎉 {bonus.bonus_name}</b>")
            lines.append(f"  {bonus.bonus_detail}")
            for item in bonus.bonus_camp_items:
                lines.append(f"  • {item}")

    _send_telegram_message("\n".join(lines))


def shop(item: str, quantity: str) -> None:
    """发送商店购买通知到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    lines = [
        f"<b>FGO自动购物系统 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        f"🛒 购买成功",
        f"  • 商品: {item}",
        f"  • 数量: {quantity}",
        f"  • 消耗AP: {40 * int(quantity)}",
    ]
    _send_telegram_message("\n".join(lines))


def draw_fp(servants: list, missions: list) -> None:
    """发送友情抽卡通知到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    lines = [
        f"<b>FGO自动抽卡系统 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        "🎴 完成当日免费友情抽卡",
    ]

    if missions:
        lines.append("")
        lines.append("<b>📋 任务进度</b>")
        for m in missions:
            lines.append(f"  • {m.message}: {m.progressTo}/{m.condition}")

    if servants:
        lines.append("")
        lines.append("<b>✨ 抽卡结果</b>")
        lines.append(f"  {', '.join(servants)}")

    _send_telegram_message("\n".join(lines))


def lto_gacha(servants: list) -> None:
    """发送限定抽卡通知到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    lines = [
        f"<b>FGO限定抽卡 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        "🌟 完成限定友情抽卡",
    ]
    if servants:
        lines.append("")
        lines.append("<b>✨ 抽卡结果</b>")
        lines.append(f"  {', '.join(servants)}")

    _send_telegram_message("\n".join(lines))


def free_gacha(servants: list) -> None:
    """发送每日免费单抽通知到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    lines = [
        f"<b>FGO每日免费单抽 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        "🎯 完成每日免费单抽",
    ]
    if servants:
        lines.append("")
        lines.append("<b>✨ 抽卡结果</b>")
        lines.append(f"  {', '.join(servants)}")

    _send_telegram_message("\n".join(lines))


def present(name: str, namegift: str, count: int) -> None:
    """发送礼物兑换通知到 Telegram"""
    if not TELEGRAM_ENABLED:
        return

    lines = [
        f"<b>FGO兑换系统 - {os.environ.get('fate_region', 'JP')}</b>",
        "",
        "🎁 兑换成功",
        f"  • 物品: {name}",
        f"  • 来源: {namegift}",
        f"  • 数量: x{count}",
    ]
    _send_telegram_message("\n".join(lines))
