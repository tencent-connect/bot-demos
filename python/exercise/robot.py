#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path
import time
from multiprocessing import Process

import qqbot
import schedule

from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv

from ark_builder import *
from weather_info_getter import *

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
              MessageArkKv(key="#LIST#", obj=await create_weather_ark_obj_list(weather_dict))]
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
              MessageArkKv(key="#LIST#", obj=await create_clothes_ark_obj_list(life_index_dict))]
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
              MessageArkKv(key="#LIST#", obj=await create_uv_ark_obj_list(life_index_dict))]
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
              MessageArkKv(key="#LIST#", obj=await create_aqi_ark_obj_list(aqi_dict))]
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
              MessageArkKv(key="#LIST#", obj=await create_future_weather_ark_obj_list(future_weather_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)


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

