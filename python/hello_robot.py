#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import os.path
import time
from multiprocessing import Process
from typing import Dict, List

import aiohttp
import qqbot
import schedule

from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv, MessageArkObj, MessageArkObjKv

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))
public_channel_id = ""


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息
    content = message.content
    qqbot.logger.info("event %s" % event + ",receive message %s" % content)

    # 根据指令触发不同的推送消息
    if "/天气 " in content:
        split = content.split("/天气 ")
        weather = await get_weather(split[1])
        await send_weather_ark_message(weather, message.channel_id, message.id)

    elif "/私信天气 " in content:
        split = content.split("/私信天气 ")
        weather = await get_weather(split[1])
        await send_weather_embed_direct_message(weather, message.guild_id, message.author.id)

    if "/当前天气 " in content:
        split = content.split("/当前天气 ")
        weather = await get_weather(split[1])
        await send_weather_ark_message(weather, message.channel_id, message.id)

    elif "/未来天气 " in content:
        split = content.split("/未来天气 ")
        future_weather = await get_future_weather(split[1])
        await send_future_weather_ark_message(future_weather, message.channel_id, message.id)

    elif "/空气质量 " in content:
        split = content.split("/空气质量 ")
        aqi_dict = await get_aqi(split[1])
        await send_aqi_ark_message(aqi_dict, message.channel_id, message.id)

    elif "/穿衣指数 " in content:
        split = content.split("/穿衣指数 ")
        weather_life_dict = await get_weather_life_index(split[1])
        await send_clothes_ark_message(weather_life_dict, message.channel_id, message.id)

    elif "/紫外线指数 " in content:
        split = content.split("/紫外线指数 ")
        weather_life_dict = await get_weather_life_index(split[1].strip())
        await send_uv_ark_message(weather_life_dict, message.channel_id, message.id)


async def _create_weather_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value=weather_dict['result']['citynm'] + " " + weather_dict['result']['weather'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当日温度区间：" + weather_dict['result']['temperature'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前温度：" + weather_dict['result']['temperature_curr'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前湿度：" + weather_dict['result']['humidity'])])]
    return obj_list


async def _create_future_weather_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value=weather_dict['result'][0]['citynm'] + "未来三天天气预报")]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="明天：" + weather_dict['result'][1]['weather'] + ", " + weather_dict['result'][1]['temperature'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="后天：" + weather_dict['result'][2]['weather'] + ", " + weather_dict['result'][2]['temperature'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="外后天：" + weather_dict['result'][3]['weather'] + ", " + weather_dict['result'][3]['temperature'])])]
    return obj_list


async def _create_clothes_ark_obj_list(life_index_dic) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + life_index_dic['result'][0]['citynm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="体感：" + life_index_dic['result'][0]['lifeindex_ct_attr'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + life_index_dic['result'][0]['lifeindex_ct_dese'])])]
    return obj_list


async def _create_uv_ark_obj_list(life_index_dic) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + life_index_dic['result'][0]['citynm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="紫外线指数：" + life_index_dic['result'][0]['lifeindex_uv_attr'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + life_index_dic['result'][0]['lifeindex_uv_dese'])])]
    return obj_list


async def _create_aqi_ark_obj_list(aqi_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + aqi_dict['result']['citynm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="空气质量：" + aqi_dict['result']['aqi_levnm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="PM2.5：" + aqi_dict['result']['aqi_scope'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + aqi_dict['result']['aqi_remark'])])]
    return obj_list


async def send_weather_ark_message(weather_dict, channel_id, message_id):
    """
    被动回复-子频道推送模版消息

    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param weather_dict:天气消息
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [MessageArkKv(key="#DESC#", value="描述"),
              MessageArkKv(key="#PROMPT#", value="提示消息"),
              MessageArkKv(key="#LIST#", obj=await _create_weather_ark_obj_list(weather_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


async def send_weather_embed_direct_message(weather_dict, guild_id, user_id):
    """
    被动回复-私信推送天气内嵌消息

    :param user_id: 用户ID
    :param weather_dict: 天气数据字典
    :param guild_id: 发送私信需要的源频道ID
    """
    # 构造消息发送请求数据对象
    embed = MessageEmbed()
    embed.title = weather_dict['result']['citynm'] + " " + weather_dict['result']['weather']
    embed.prompt = "天气消息推送"
    # 构造内嵌消息缩略图
    thumbnail = MessageEmbedThumbnail()
    thumbnail.url = weather_dict['result']['weather_icon']
    embed.thumbnail = thumbnail
    # 构造内嵌消息fields
    embed.fields = [MessageEmbedField(name="当日温度区间：" + weather_dict['result']['temperature']),
                    MessageEmbedField(name="当前温度：" + weather_dict['result']['temperature_curr']),
                    MessageEmbedField(name="最高温度：" + weather_dict['result']['temp_high']),
                    MessageEmbedField(name="最低温度：" + weather_dict['result']['temp_low']),
                    MessageEmbedField(name="当前湿度：" + weather_dict['result']['humidity'])]

    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(embed=embed, content="")
    dms_api = qqbot.AsyncDmsAPI(t_token, False)
    direct_message_guild = await dms_api.create_direct_message(CreateDirectMessageRequest(guild_id, user_id))
    await dms_api.post_direct_message(direct_message_guild.guild_id, send)
    qqbot.logger.info("/私信推送天气内嵌消息 成功")


async def send_clothes_ark_message(life_index_dict, channel_id, message_id):
    """
    被动回复-子频道推送穿衣指数

    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param life_index_dict:天气消息
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [MessageArkKv(key="#DESC#", value="描述"),
              MessageArkKv(key="#PROMPT#", value="提示消息"),
              MessageArkKv(key="#LIST#", obj=await _create_clothes_ark_obj_list(life_index_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


async def send_uv_ark_message(life_index_dict, channel_id, message_id):
    """
    被动回复-子频道推送紫外线指数

    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param life_index_dict:天气消息
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [MessageArkKv(key="#DESC#", value="描述"),
              MessageArkKv(key="#PROMPT#", value="提示消息"),
              MessageArkKv(key="#LIST#", obj=await _create_uv_ark_obj_list(life_index_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


async def send_aqi_ark_message(aqi_dict, channel_id, message_id):
    """
    被动回复-子频道推送 PM2.5 空气质量指数

    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param aqi_dict:空气质量数据
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [MessageArkKv(key="#DESC#", value="描述"),
              MessageArkKv(key="#PROMPT#", value="提示消息"),
              MessageArkKv(key="#LIST#", obj=await _create_aqi_ark_obj_list(aqi_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


async def send_future_weather_ark_message(future_weather_dict, channel_id, message_id):
    """
    被动回复-子频道推送未来三天天气

    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param future_weather_dict:空气质量数据
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [MessageArkKv(key="#DESC#", value="描述"),
              MessageArkKv(key="#PROMPT#", value="提示消息"),
              MessageArkKv(key="#LIST#", obj=await _create_future_weather_ark_obj_list(future_weather_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


async def get_weather(city_name: str) -> Dict:
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
    weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_future_weather(city_name: str) -> Dict:
    """
    获取未来几天的天气信息

    :return: 返回天气数据的json对象
    返回示例(返回值过长,部分省略)
    {
        "success": "1",
        "result": [{
            "weaid": "1",
            "days": "2014-07-30",
            "week": "星期三",
            "cityno": "beijing",
            "citynm": "北京",
            "cityid": "101010100",
            "temperature": "23℃/11℃", /*温度*/
            "humidity": "0%/0%", /*湿度,后期气像局未提供,如有需要可使用weather.today接口 */
            "weather": "多云转晴",
            "weather_icon": "http://api.k780.com/upload/weather/d/1.gif", /*气象图标(白天) 全部气象图标下载*/
            "weather_icon1": "http://api.k780.com/upload/weather/d/0.gif", /*气象图标(夜间) 全部气象图标下载*/
            "wind": "微风", /*风向*/
            "winp": "小于3级", /*风力*/
            "temp_high": "31", /*最高温度*/
            "temp_low": "24", /*最低温度*/
            "humi_high": "0", /*湿度栏位已不再更新*/
            "humi_low": "0",/*湿度栏位已不再更新*/
            "weatid": "2", /*白天天气ID，可对照weather.wtype接口中weaid*/
            "weatid1": "1", /*夜间天气ID，可对照weather.wtype接口中weaid*/
            "windid": "1", /*风向ID(暂无对照表)*/
            "winpid": "2" /*风力ID(暂无对照表)*/
            "weather_iconid": "1", /*气象图标编号(白天),对应weather_icon 1.gif*/
            "weather_iconid1": "0" /*气象图标编号(夜间),对应weather_icon1 0.gif*/
        },
    ......
    """
    weather_api_url = "http://api.k780.com/?app=weather.future&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_weather_life_index(citi_name: str) -> Dict:
    """
    获取生活指数

    :return: 返回天气数据的json对象
    返回示例
    {
    success: "1",
    result: {
        2017-04-17: {
            weaid: "1",
            days: "2017-04-17",
            week_1: "星期一",
            simcode: "beijing",
            citynm: "北京",
            cityid: "101010100",
            lifeindex_uv_id: "101",
            lifeindex_uv_typeno: "uv",
            lifeindex_uv_typenm: "紫外线指数",
            lifeindex_uv_attr: "弱",
            lifeindex_uv_dese: "辐射较弱，涂擦SPF12-15、PA+护肤品。",
            lifeindex_gm_id: "111",
            lifeindex_gm_typeno: "gm",
            lifeindex_gm_typenm: "感冒指数",
            lifeindex_gm_attr: "少发",
            lifeindex_gm_dese: "无明显降温，感冒机率较低。",
            lifeindex_ct_id: "108",
            lifeindex_ct_typeno: "ct",
            lifeindex_ct_typenm: "穿衣指数",
            lifeindex_ct_attr: "较舒适",
            lifeindex_ct_dese: "建议穿薄外套或牛仔裤等服装。",
            lifeindex_xc_id: "112",
            lifeindex_xc_typeno: "xc",
            lifeindex_xc_typenm: "洗车指数",
            lifeindex_xc_attr: "较适宜",
            lifeindex_xc_dese: "无雨且风力较小，易保持清洁度。",
            lifeindex_yd_id: "114",
            lifeindex_yd_typeno: "yd",
            lifeindex_yd_typenm: "运动指数",
            lifeindex_yd_attr: "较适宜",
            lifeindex_yd_dese: "风力稍强，推荐您进行室内运动。",
            lifeindex_kq_id: "109",
            lifeindex_kq_typeno: "kq",
            lifeindex_kq_typenm: "空气污染扩散指数",
            lifeindex_kq_attr: "良",
            lifeindex_kq_dese: "气象条件有利于空气污染物扩散。"
        },
    ...
    """
    weather_api_url = "http://api.k780.com/?app=weather.lifeindex&cityNm=" + citi_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=weather_api_url,
            timeout=5
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_aqi(citi_name: str) -> Dict:
    """
    获取空气质量（aqi）数据

    :return: 返回空气质量数据的json对象
    返回示例
    {
    success: "1",
    result: {
        "success": "1",
        "result": {
        "weaid": "180",
        "cityno": "gdzhongshan",
        "citynm": "中山",
        "cityid": "101281701",
        "aqi": "18",
        "aqi_scope": "0-50",
        "aqi_levid": "1",
        "aqi_levnm": "优",
        "aqi_remark": "参加户外活动呼吸清新空气"
    }
    """
    weather_api_url = "http://api.k780.com/?app=weather.pm25&cityNm=" + citi_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=weather_api_url,
            timeout=5
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


def set_schedule_task():
    schedule.every(10).seconds.do(send_weather_message_by_time)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_weather_message_by_time():
    """
    任务描述：每天推送一次普通天气消息
    """
    loop = asyncio.get_event_loop()
    token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])

    # 获取频道列表，取首个频道的首个子频道推送
    global public_channel_id
    if not public_channel_id:
        user_api = qqbot.AsyncUserAPI(token, False)
        guild_id = loop.run_until_complete(user_api.me_guilds())[0].id
        channel_api = qqbot.AsyncChannelAPI(token, False)
        public_channel_id = loop.run_until_complete(channel_api.get_channels(guild_id))[0].id

    # 获取天气数据
    weather_dict = loop.run_until_complete(get_weather("深圳"))
    # 推送消息
    content = "当日温度区间：" + weather_dict['result']['temperature']
    send = qqbot.MessageSendRequest(content=content)
    msg_api = qqbot.AsyncMessageAPI(token, False)
    loop.run_until_complete(msg_api.post_message("2568610", send))


# async的异步接口的使用示例
if __name__ == "__main__":
    # 定时推送主动消息
    Process(target=set_schedule_task).start()
    # @机器人后推送被动消息
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)
