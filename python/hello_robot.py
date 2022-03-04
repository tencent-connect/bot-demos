#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import os.path
from typing import Dict

import aiohttp
import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)

    # 根据指令触发不同的推送消息
    if "/推送深圳天气模版消息" in message.content:
        pass

    if "/推送上海天气模版消息" in message.content:
        pass

    if "/推送北京天气模版消息" in message.content:
        pass

    if "/私信推送天气内嵌消息" in message.content:
        qqbot.logger.info("/私信推送天气内嵌消息")
        weather = await get_weather()
        await send_weather_embed_direct_message(weather, message.guild_id, message.author.id)


async def send_weather_embed_direct_message(weather_dict, guild_id, user_id):
    """
    私信推送天气内嵌消息

    :param weather_dict: 天气数据字典
    :param guild_id: 发送私信需要的源频道ID
    """
    dms_api = qqbot.AsyncDmsAPI(t_token, False)
    # 构造消息发送请求数据对象
    embed = MessageEmbed()
    embed.title = weather_dict['result']['citynm'] + " " + weather_dict['result']['weather']
    embed.prompt = "天气消息推送"

    thumbnail = MessageEmbedThumbnail()
    thumbnail.url = weather_dict['result']['weather_icon']
    embed.thumbnail = thumbnail

    fields = []
    field = MessageEmbedField()
    field.name = "当日温度区间：" + weather_dict['result']['temperature']
    fields.append(field)

    field = MessageEmbedField()
    field.name = "当前温度：" + weather_dict['result']['temperature_curr']
    fields.append(field)

    field = MessageEmbedField()
    field.name = "最高温度：" + weather_dict['result']['temp_high']
    fields.append(field)

    field = MessageEmbedField()
    field.name = "最低温度：" + weather_dict['result']['temp_low']
    fields.append(field)

    field = MessageEmbedField()
    field.name = "当前湿度：" + weather_dict['result']['humidity']
    fields.append(field)

    embed.fields = fields

    send = qqbot.MessageSendRequest(embed=embed, content="")
    # 通过api发送回复消息
    direct_message_guild = await dms_api.create_direct_message(CreateDirectMessageRequest(guild_id, user_id))
    await dms_api.post_direct_message(direct_message_guild.guild_id, send)
    qqbot.logger.info("/私信推送天气内嵌消息 成功")


async def get_weather() -> Dict:
    """
    获取天气信息

    :return: 返回天气数据的json对象
    返回示例
    {
    "success":"1",
    "result":{
        "weaid":"1",
        "days":"2022-03-04",
        "week":"星期五",
        "cityno":"beijing",
        "citynm":"北京",
        "cityid":"101010100",
        "temperature":"13℃/-1℃",
        "temperature_curr":"10℃",
        "humidity":"17%",
        "aqi":"98",
        "weather":"扬沙转晴",
        "weather_curr":"扬沙",
        "weather_icon":"http://api.k780.com/upload/weather/d/30.gif",
        "weather_icon1":"",
        "wind":"西北风",
        "winp":"4级",
        "temp_high":"13",
        "temp_low":"-1",
        "temp_curr":"10",
        "humi_high":"0",
        "humi_low":"0",
        "weatid":"31",
        "weatid1":"",
        "windid":"7",
        "winpid":"4",
        "weather_iconid":"30"
        }
    }
    """
    weather_api_url = "http://api.k780.com/?app=weather.today&weaId=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


# async的异步接口的使用示例
if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)

    # 定时推送主动消息
