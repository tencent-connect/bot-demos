* 1. [开发前的准备](#)
* 2. [Python环境搭建](#Python)
* 3. [机器人自动回复普通消息](#-1)
* 4. [获取天气数据](#-2)
* 5. [机器人主动推送消息](#-3)
* 6. [机器人指令回复ark消息](#ark)
* 7. [机器人私信](#-4)
* 8. [使用指令](#-5)
* 9. [最佳实践](#-6)


##  1. <a name=''></a>开发前的准备

如下图，点击 [频道机器人开发官网](https://bot.q.qq.com/open) ，在官网页面点击 **立即注册**

<img width="1606" alt="ff729f2e-1ce8-4fa7-b364-2be0d2ca18c3" src="https://user-images.githubusercontent.com/33934426/156754545-5f873fa9-68c4-4f07-ae2e-d7085516349e.png">

有两种主体类型，可以根据自己的实际情况进行选择，这里介绍个人开发者的流程，企业详细流程见 [企业主体入驻
](https://bot.q.qq.com/wiki/#_2-%E4%BC%81%E4%B8%9A%E4%B8%BB%E4%BD%93%E5%85%A5%E9%A9%BB)

<img width="911" alt="f377e842-b6ef-47f1-8eac-1b88733e9ad8" src="https://user-images.githubusercontent.com/33934426/156754613-b18d6a58-52d2-4302-915d-004f6edd3e0f.png">

目前个人开发者还在内测中，需要点击如下图的 [频道机器人个体开发者邀请问卷](https://docs.qq.com/form/page/DSlZjZ0dPc0llT3d0?_w_tencentdocx_form=1#/fill-detail) 进行申请

<img width="903" alt="b93b8cb6-0361-4b58-a2d7-3c456d294076" src="https://user-images.githubusercontent.com/33934426/156754657-d0ebc699-64b0-4ee4-9dea-358fe837b160.png">

提交完成后，需要等待审核。如果审核通过，就会发送邮件到你的邮箱。

<img width="613" alt="06eedc81-fee4-4b5f-b862-781dd5ef4bba" src="https://user-images.githubusercontent.com/33934426/156754731-5077b76c-3dd2-4138-992b-fed862011f3f.png">

收到邀请码后就可以点击 **下一步** 进入登陆页面

<img width="910" alt="0c627f76-d7c1-4834-9ca8-c2a75cd6306e" src="https://user-images.githubusercontent.com/33934426/156754845-006b7a14-bc37-4a82-9033-fa133c0fd07b.png">

在完成邮箱、手机号等认证后，就可以进入 QQ机器人管理界面，如下图所示：

<img width="1620" alt="1145ae87-951b-4d55-9f41-7a0d313f73f6" src="https://user-images.githubusercontent.com/33934426/156754890-3dc06db0-1c17-49ab-8495-803fc6145b2a.png">

点击 **生成BotAppID** 进入机器人配置界面（如下图）：

<img width="1385" alt="adf8c879-dc38-43f1-887a-265ed0db496e" src="https://user-images.githubusercontent.com/33934426/156755041-11c3935f-0e80-4846-acb6-bc04f02e1677.png">

这里面有两个选项需要注意（标红部分）：**沙箱频道ID** 是指你创建的频道的ID，需要注意的是，如果你之前创建的频道人数超过限制，就需要创建另一个频道；**机器人类型**有两种，一种是私域机器人，一种是公域机器人。简单来说，私域机器人只能在你自己的频道使用，而公域机器人可以在所有频道使用。

点击 **提交审核** ，审核完成后就能看到如下界面：

<img width="469" alt="5e92d587-3e99-45b8-a4ff-13b9cf9b1270" src="https://user-images.githubusercontent.com/33934426/156755344-91830840-2178-481e-8013-b54e948446a2.png">

点击 **查看详情** 就可以看到你的 `BotAppID` 、`BotToken` 、`BotSecret` 了，**注意这个信息不要泄露**。


现在，点击频道右上角「...」--->点击「频道设置」--->点击「机器人」--->添加测试机器人，就可以将机器人添加到自己的频道了。不过此时机器人还没有任何的功能，下面手把手教你用 python 写一个机器人服务

##  2. <a name='Python'></a>Python环境搭建

### 安装Python3

**linux**

在命令行依次输入如下命令来下载 `Python3`
   ```
   sudo apt-get install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt-get update
   sudo apt-get install python3.8
   ```

在命令行输入 `python --version` 指令检验是否安装完成，如果安装成功，会打印出 `python` 的版本号
   ```
   python --version
   ```

**mac**

先打开 Terminal，安装 Homebrew。（可先用 `brew -v` 查看是否已经安装 Homebrew）
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   ```

安装 Homebrew 后，将 Homebrew 目录插入到 `PATH` 环境变量顶部。你可以通过在 `~/.profile` 文件底部添加以下行来执行此操作
   ```
   export PATH="/usr/local/opt/python/libexec/bin:$PATH"
   ```

现在，可以用 Homebrew 安装 `Python3` 了
   ```
   brew install python
   ```

在命令行输入 python --version 指令检验是否安装完成，如果安装成功，会打印出 python 的版本号
   ```
   python --version
   ```

**windows**

在 https://www.python.org/downloads/windows/ 下载 executable installer （一般选 64-bit 的），下载完成后，运行 exe 安装包即可

*注意：* 记得勾选 `Add Python 3.x to Path` 选项

安装成功后，打开命令提示符窗口，输入 `python`，如果安装成功，会打印出 `python` 的版本号
   ```
   C:\> python
   ```

### 安装机器人 SDK

```bash
pip install qq-bot
```

同时，由于需要读取 `yaml` 文件的内容，我们也需要安装 `pyyaml`
```bash
pip install pyyaml
```

### 创建项目

创建一个 demo 项目文件夹

```
mkdir demo
cd demo
```

接着，在`demo`文件夹下创建名为 `config.yaml` 的配置文件，填入自己的 `BotAppID` 和 `Bot token`，内容类似下面所示。 也可直接下载 github 仓库里的`config.example.yaml` 文件，然后自己修改后缀名和内容

    ``` bash
    token:
    appid: "123"
    token: "xxxx"
    ```

接着，在`demo`文件夹下创建一个名为 `robot.py` 的文件：

- 在Linux和mac上，你需要使用 `touch robot.py` 创建一个名为 `robot.py` 的文件。
- 在windows上，你可以右键-->创建txt文件-->重命名为`robot.py`

最后，打开 `python` 文件，在开头导入相关的包：

在Linux和mac上你需要使用 `vim robot.py` 编辑`robot.py` 文件，键盘输入 `i` ,把文件变成可编辑状态，复制粘贴下面代码。`esc` 键退出，键盘输入 `:wq` 保持退出。

在windows上，你需要使用文本编辑器打开文件，并复制粘贴下面的代码，`ctrl+s`保存文件。

```Python
import asyncio
import json
import os.path
import threading
from typing import Dict, List

import aiohttp
import qqbot

from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv, MessageArkObj, MessageArkObjKv

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))
```


##  3. <a name='-1'></a>机器人自动回复普通消息

在 `python`文件中添加如下代码

```py
async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)

    # 发送消息告知用户
    message_to_send = qqbot.MessageSendRequest(content="你好", msg_id=message.id)
    await msg_api.post_message(message.channel_id, message_to_send)


# async的异步接口的使用示例
if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)
```

保存完代码，在命令行输入 `python3 robot.py` 运行机器人。 这时在频道内 @机器人 `hello` 指令就可以收到回复了

![0f560a5c8eb091e4d0f1563222f530ef](https://user-images.githubusercontent.com/33934426/156755478-07497508-c95c-4013-b725-c4897b85be10.jpg)


##  4. <a name='-2'></a>获取天气数据

天气机器人最重要的就是提供天气的数据，这里是使用的 `https://www.nowapi.com/api/weather.today` 的Api。

首先，在文件中添加用于获取天气数据的函数

```python
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
```

然后，修改 `_message_handler`函，调用 `get_weather` 函数并发送天气

```python
async def _message_handler(event, message: qqbot.Message):
    .
    .
    .
    # 发送消息告知用户
    weather_dict = await get_weather("深圳")
    weather_desc = weather_dict['result']['citynm'] + " " 
        + weather_dict['result']['weather'] + " " 
        + weather_dict['result']['days'] + " " 
        + weather_dict['result']['week']
    message_to_send = qqbot.MessageSendRequest(msg_id=message.id, content=weather_desc, image=weather_dict['result']['weather_icon'])
    await msg_api.post_message(message.channel_id, message_to_send)
```

效果图如下：

![554f4a6da7c87723084db5f629109cb6](https://user-images.githubusercontent.com/33934426/156755624-1899dcda-ebf2-4666-8d46-be947dca0aa5.jpg)

##  5. <a name='-3'></a>机器人主动推送消息

上面的教程只实现一个简单的获取天气的功能，但是我们做的是天气机器人，希望实现一个报告天气的功能。一般的天气应用都会在一个特定时间给你推送天气通知，在频道机器人中，你可以通过主动消息来实现这个功能。代码如下：

添加定时发送消息的函数

```python
async def send_weather_message_by_time():
    """
    任务描述：每天推送一次普通天气消息
    """
    # 获取天气数据
    weather_dict = await get_weather("深圳")
    # 获取频道列表都取首个频道的首个子频道推送
    user_api = qqbot.AsyncUserAPI(t_token, False)
    guilds = await user_api.me_guilds()
    guilds_id = guilds[0].id
    channel_api = qqbot.AsyncChannelAPI(t_token, False)
    channels = await channel_api.get_channels(guilds_id)
    channels_id = channels[0].id
    qqbot.logger.info("channelid %s" % channel_id)
    # 推送消息
    weather = "当前天气是：" + weather_dict['result']['weather']
    send = qqbot.MessageSendRequest(content=weather)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channels_id, send)
    # 如果需要每天都执行，加上下面两句
    t = threading.Timer(100, await send_weather_message_by_time)
    t.start()
```

在 `__main__` 中添加执行 `send_weather_message_by_time()` 的语句

```python
if __name__ == "__main__":
    .
    .
    .
    # 定时推送主动消息
    send_weather_message_by_time()
```

运行该代码，效果如下图

![fee0801e89409a951567ebbe7d9c4267](https://user-images.githubusercontent.com/33934426/156756498-d0b43ce2-df7a-4029-a09f-7b95947ac7a5.jpg)

##  6. <a name='ark'></a>机器人指令回复ark消息

提供给个人开发者的`Ark`有3种，这里使用 24 号`Ark`。其它`Ark`见[消息模板](https://bot.q.qq.com/wiki/develop/api/openapi/message/message_template.html)

先添加发送ark的函数

```python
async def _create_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value=weather_dict['result']['citynm'] + " " + weather_dict['result']['weather'] +  " " + weather_dict['result']['days'] + " " + weather_dict['result']['week'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当日温度区间：" + weather_dict['result']['temperature'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前温度：" + weather_dict['result']['temperature_curr'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前湿度：" + weather_dict['result']['humidity'])])]
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
              MessageArkKv(key="#LIST#", obj=await _create_ark_obj_list(weather_dict))]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    await msg_api.post_message(channel_id, send)
```

再修改 `_message_handler`函数发送ark

```python
async def _message_handler(event, message: qqbot.Message):
    """
      .
      .
      .
    # 发送消息告知用户
    weather = await get_weather("深圳")
    await send_weather_ark_message(weather, message.channel_id, message.id)
```

效果如下图:

<img width="422" alt="a754879e-7255-4ac3-9c81-247ca556a58d" src="https://user-images.githubusercontent.com/33934426/156756584-8c23eb79-d381-46b9-8470-c30c46d11a16.png">

##  7. <a name='-4'></a>机器人私信

我们希望能提供不同用户不同地方的天气，但是发太多的消息会影响其它的用户。针对这种情况，我们可以通过私信来实现。下面代码中，当我们@机器人hello时收到机器人的私信。

私信中我们不使用ark，而是使用`Embed`。`Embed`也是一种结构化消息，它比ark简单，发送 `Embed` 的函数如下：

```python
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
```

修改 `_message_handler`函数，使他不再发送 `Ark` ，而是在私信里给你发送 `Embed` 

```python

async def _message_handler(event, message: qqbot.Message):
    """
      .
      .
      .
    # 发送消息告知用户
    weather = await get_weather("深圳")
    await send_weather_embed_direct_message(weather, message.guild_id, message.author.id)
```

效果图如下：

![01DDC2277EE8A0EE699C8049E38806A7](https://user-images.githubusercontent.com/33934426/156757976-99464dae-485b-459d-b5b2-dcddbb701746.jpg)

##  8. <a name='-5'></a>使用指令

每次@机器人输入指令太麻烦了，有没有简单的方式呢？机器人提供了指令配置，当你输入`/`时就会产出你配置的指令面板。配置方式如下：

<img width="1364" alt="44579997-4462-4a70-a54a-27e919452c89" src="https://user-images.githubusercontent.com/33934426/156758327-bd196a2a-a412-4a86-a64b-e7969b6aa27f.png">
<img width="1367" alt="ac4d256d-3e31-4e18-9fd2-5a87e4d550a3" src="https://user-images.githubusercontent.com/33934426/156758368-5fb6496f-2ca6-4872-9997-6ebab0181230.png">

配置好后，当我们输入`/`时，就可以看到配置的面板了

<img width="442" alt="150f1d0d-a34b-4c19-ac14-8dea8afe6171" src="https://user-images.githubusercontent.com/33934426/156758394-8f54b0aa-b932-4993-9da7-e26b2abfb9bc.png">

>需要注意，点击指令后输入的内容增加了一个`/`，上面的例子就变成了 `@天气机器人-测试中 /天气`

##  9. <a name='-6'></a>最佳实践

上面已经叙述了机器人的各种功能，下面可以通过修改 `_message_handler` 的逻辑，把这些功能都整合起来：

- 机器人通过天气api拉取默认城市（深圳）的天气，每天主动推送模版消息
- 机器人通过指令选择“深圳、上海、北京”时，被动推送模版消息
- 机器人通过指令选择“私信推送”时，被动推送私信的天气内嵌消息（建议改成注册需要推送消息）
- 机器人通过指令选择“全国天气小程序”，打开天气小程序

修改完成之后的代码如下：

```python
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
    if "/推送深圳天气" in message.content:
        weather = await get_weather("深圳")
        await send_weather_ark_message(weather, message.channel_id, message.id)

    if "/推送上海天气" in message.content:
        weather = await get_weather("上海")
        await send_weather_ark_message(weather, message.channel_id, message.id)

    if "/推送北京天气" in message.content:
        weather = await get_weather("北京")
        await send_weather_ark_message(weather, message.channel_id, message.id)

    if "/私信推送天气" in message.content:
        weather = await get_weather("北京")
        await send_weather_embed_direct_message(weather, message.guild_id, message.author.id)
```

完整代码看 [天气机器人-Python实现版](https://github.com/tencent-connect/bot-demos/tree/master/python)

