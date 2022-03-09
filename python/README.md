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

最后，在`demo`文件夹下创建一个名为 `robot.py` 的文件：

- 在Linux和mac上，你需要使用 `touch robot.py` 创建一个名为 `robot.py` 的文件。
- 在windows上，你可以右键-->创建txt文件-->重命名为`robot.py`

##  3. <a name='-1'></a>机器人自动回复普通消息

在Linux和mac上你需要使用 `vim robot.py` 编辑`robot.py` 文件，键盘输入 `i` ,把文件变成可编辑状态，复制粘贴下面代码。`esc` 键退出，键盘输入 `:wq` 保持退出。

在windows上，你需要使用文本编辑器打开文件，并复制粘贴下面的代码，`ctrl+s`保存文件。

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import aiohttp
import qqbot

from qqbot.core.util.yaml_util import YamlUtil

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
