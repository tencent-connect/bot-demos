<!-- vscode-markdown-toc -->
* 1. [开发前的准备](#)
* 2. [环境搭建](#Node)
* 3. [机器人自动回复普通消息](#-1)
* 4. [获取天气数据](#-2)
* 5. [机器人主动推送消息](#-3)
* 6. [机器人指令回复ark消息](#ark)
* 7. [机器人私信](#-4)
* 8. [使用指令](#-5)
* 9. [最佳实践](#-6)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
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

这里面有两个选项需要注意（标红部分）：**沙箱频道ID** 是指你创建频道的ID，需要注意的是，如果你之前创建的频道人数超过限制，就需要创建另一个频道；**机器人类型**有两种，一种是私域机器人，一种是公域机器人。简单来说，私域机器人只能在你自己的频道使用，而公域机器人可以在所有频道使用。

点击 **提交审核** ，审核完成后就能看到如下界面：

<img width="469" alt="5e92d587-3e99-45b8-a4ff-13b9cf9b1270" src="https://user-images.githubusercontent.com/33934426/156755344-91830840-2178-481e-8013-b54e948446a2.png">

点击 **查看详情** 就可以看到你的 `BotAppID` 、`BotToken` 、`BotSecret` 了，**注意这个信息不要泄露**。

##  2. <a name='Node'></a>环境搭建

### 安装 Node.js

可以在 [官网](http://nodejs.cn/download/) 下载安装 Node.js，建议下载12以上版本。如果你的操作系统为 Linux 或者macOS 也可以参考相应的包管理器安装

**linux**

以 CentOS 为例，可以使用 dnf 包管理器下载 node

```
dnf module install nodejs:12
```

**mac**

macOS 可以使用 homebrew 安装 node

```
brew install node
```

安装完成后可以在命令行输入 `node -v` 指令检验是否安装完成，如果安装成功，会打印出 `Node` 的版本号

### 安装 Yarn

Yarn 是替代 npm 的包管理工具，本教程使用 Yarn 安装依赖。

```
npm install --global yarn
```

### 创建项目

打开命令行工具，进入需要创建工程的目录，执行以下命令

```
mkdir demo
cd demo
yarn init -y
```

### 安装依赖

为了更好的编程体验，本项目使用 TypeScript 编写，另外还使用了以下依赖包：qq-guild-bot（qq机器人 NodeSDK）、axios（网络请求库）、node-cron（定时器）、typescript、ts-node（执行typescript代码）、nodemon（代码改变时自动重启服务））、@types/node（node类型提示）@types/ws（websocket类型提示）、@types/node-cron

```
yarn add qq-guild-bot axios node-cron
yarn add -D typescript ts-node nodemon @types/node @types/ws @types/node-cron
```

##  3. <a name='-1'></a>机器人自动回复普通消息

在项目目录下新建 index.ts，内容如下（APPID和TOKEN要需要替换成自己的机器人，可以在 [机器人后台管理端](https://bot.q.qq.com/#/developer/developer-setting) 查看）

```ts
import { AvailableIntentsEventsEnum, createOpenAPI, createWebsocket, IMessage } from 'qq-guild-bot';

const botConfig = {
    appID: 'APPID', // 申请机器人时获取到的机器人 BotAppID
    token: 'TOKEN', // 申请机器人时获取到的机器人 BotToken
    intents: [AvailableIntentsEventsEnum.AT_MESSAGES], // 事件订阅,用于开启可接收的消息类型
    sandbox: false, // 沙箱支持，可选，默认false. v2.7.0+
};

// 创建 client
const client = createOpenAPI(botConfig);
// 创建 websocket 连接
const ws = createWebsocket(botConfig);

// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    const content = data.msg.content;
    if (content.includes('hello')) {
        client.messageApi.postMessage(data.msg.channel_id, { content: '你好' }).then((res) => {
            console.log(res.data);
        }).catch((err) => {
            console.log(err);
        });
    } 
});
```

修改 package.json，添加 scripts 字段

```
{
  "name": "weather-robot",
  "version": "1.0.0",
  "main": "./index.ts",
  "author": "Next",
  "license": "MIT",
  "scripts": {
    "dev": "npx nodemon ./index.ts"
  },
  "dependencies": {
    "axios": "^0.26.0",
    "qq-guild-bot": "^2.8.2"
  },
  "devDependencies": {
    "@types/node": "^17.0.21",
    "@types/ws": "^8.5.2",
    "nodemon": "^2.0.15",
    "ts-node": "^10.6.0",
    "typescript": "^4.6.2"
  }
}
```

命令行启动服务

```
yarn dev
```

上述步骤完成后就可以测试机器人了。点击频道右上角「...」--->点击「频道设置」--->点击「机器人」--->添加测试机器人。这时在频道内 @机器人 `hello` 指令就可以收到回复了

![0f560a5c8eb091e4d0f1563222f530ef](https://user-images.githubusercontent.com/33934426/156755478-07497508-c95c-4013-b725-c4897b85be10.jpg)

##  4. <a name='-2'></a>获取天气数据

天气机器人最重要的就是提供天气的数据，这里是使用的 `https://www.nowapi.com/api/weather.today` 的Api。

由于需要发起网络请求，需要导入网络请求库 axios

```ts
import axios from 'axios';
```

定义天气数据的对应结构

```ts
interface IWeatherData {
    days: string;                  // 2022-03-03
    week: string;                  // 星期四
    citynm: string;                // 深圳
    temperature: string;           // 25C/18C 
    temperature_curr: string;      // 24C
    humidity: string;              // 59%
    weather: string;               // 多云
    weather_curr: string;          // 晴
    weather_icon: string;          // 地址
    wind: string;                  // 东风
}
```

定义网络请求的方法

```go
// 获取指定城市的天气数据
function getWeatherByCity(city: string) {
    const url = `http://api.k780.com/?app=weather.today&cityNm=${city}&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json`;
    return new Promise<IWeatherData>((resolve, reject) => {
        axios.get(url).then((response) => {
            const data = response.data;
            if (data.success === '1') {
                resolve(data.result);
            } else {
                console.error(data.msg);
                reject(data.msg);
            }
        }).catch((err) => {
            console.log(err);
            reject(err);
        });
    });
}
```

当@机器人`hello`指令时，获取深圳的天气数据并返回

```ts	
// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    const content = data.msg.content;
    if (content.includes('hello')) {
        getWeatherByCity('深圳').then(weatherData => {
            client.messageApi.postMessage(data.msg.channel_id, {
                content: `${weatherData.citynm} ${weatherData.weather} ${weatherData.days} ${weatherData.week}`,
                image: weatherData.weather_icon, // 天气图片
            }).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.log(err);
            });
        });
    }
});
```

效果图如下：

![554f4a6da7c87723084db5f629109cb6](https://user-images.githubusercontent.com/33934426/156755624-1899dcda-ebf2-4666-8d46-be947dca0aa5.jpg)

##  5. <a name='-3'></a>机器人主动推送消息

上面的教程只实现一个简单的获取天气的功能，但是我们做的是天气机器人，希望实现一个报告天气的功能。一般的天气应用都会在一个特定时间给你推送天气通知，在频道机器人中，你可以通过主动消息来实现这个功能。代码如下：

首先导入定时器模块

```ts
import * as cron from 'node-cron';
```

添加定时消息的代码

```go
// 定时推送天气子频道id
let subWeatherChannelID: string;

// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    subWeatherChannelID = data.msg.channel_id;
    // ...
});

//cron表达式由6部分组成，从左到右分别表示 秒 分 时 日 月 星期
//*表示任意值  ？表示不确定值，只能用于星期和日
//这里表示每天15:53分发送消息
cron.schedule('0 53 15 * * ?', () => {
    if (subWeatherChannelID) {
        // 不传 msg_id 代表主动消息
        client.messageApi.postMessage(subWeatherChannelID, { content: '当前天气是：晴天' });
    }
});
```

运行该代码，效果如下图

![fee0801e89409a951567ebbe7d9c4267](https://user-images.githubusercontent.com/33934426/156756498-d0b43ce2-df7a-4029-a09f-7b95947ac7a5.jpg)

##  6. <a name='ark'></a>机器人指令回复ark消息

提供给个人开发者的`Ark`有3种，这里使用 24 号`Ark`。其它`Ark`见[消息模板](https://bot.q.qq.com/wiki/develop/api/openapi/message/message_template.html)

```go
// ...

function createArk24Message(title: string, subtitle: string, desc: string, img?: string) {
    const message = {
        template_id: 24, kv: [
            { key: "#TITLE#", value: title },
            { key: "#SUBTITLE#", value: subtitle },
            { key: "#METADESC#", value: desc },
            { key: "#IMGC#", value: img },
        ]
    };
    return message as any;
}

// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    subWeatherChannelID = data.msg.channel_id;
    const content = data.msg.content;
    if (content.includes('hello')) {
        getWeatherByCity('深圳').then(weatherData => {
            const arkContent = createArk24Message(weatherData.citynm, `${weatherData.days} ${weatherData.week} ${weatherData.weather} ${weatherData.temperature}`, '天气机器人')
            client.messageApi.postMessage(data.msg.channel_id, {
                ark: arkContent,
                msg_id: data.msg.id,
            }).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.log(err);
            });
        });
    }
});
```

效果如下图：

<img width="422" alt="a754879e-7255-4ac3-9c81-247ca556a58d" src="https://user-images.githubusercontent.com/33934426/156756584-8c23eb79-d381-46b9-8470-c30c46d11a16.png">

##  7. <a name='-4'></a>机器人私信

我们希望能提供不同用户不同地方的天气，但是发太多的消息会影响其它的用户。针对这种情况，我们可以通过私信来实现。下面代码中，当我们@机器人hello时收到机器人的私信。

私信中我们不使用ark，代替的而是使用`Embed`。`Embed`也是一种结构化消息，它比ark简单，代码如下：

```go
//获取 Embed
func createEmbed(weather *WeatherResp) *dto.Embed {
	return &dto.Embed{
		Title: weather.ResultData.CityNm + " " + weather.ResultData.Weather,
		Thumbnail: dto.MessageEmbedThumbnail{
			URL: weather.ResultData.WeatherIcon,
		},
		Fields: []*dto.EmbedField{
			{
				Name: weather.ResultData.Days + " " + weather.ResultData.Week,
			},
			{
				Name: "当日温度区间：" + weather.ResultData.Temperature,
			},
			{
				Name: "当前温度：" + weather.ResultData.TemperatureCurr,
			},
			{
				Name: "最高温度：" + weather.ResultData.TempHigh,
			},
			{
				Name: "最低温度：" + weather.ResultData.TempLow,
			},
			{
				Name: "当前湿度：" + weather.ResultData.Humidity,
			},
		},
	}
}
```

发送私信代码如下：

```ts
function createEmbedMessage(title: string, thumbnail: string, items: string[]) {
    const message: Embed = { title, thumbnail: { url: thumbnail }, fields: [] };
    items.forEach(item => {
        message.fields!.push({ name: item });
    });
    return message;
}

// 获取私信场景id，用于发私信消息
async function getDirectMessageGuildID(sourceGuildID: string, authorID: string) {
    const result = await client.directMessageApi.createDirectMessage({ source_guild_id: sourceGuildID, recipient_id: authorID });
    return result.data.guild_id;
}

// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    subWeatherChannelID = data.msg.channel_id;
    const content = data.msg.content;
    if (content.includes('hello')) {
        getWeatherByCity('深圳').then(weatherData => {
            getDirectMessageGuildID(data.msg.guild_id, data.msg.author.id).then(directMessageGuildID => {
                const embedContent = createEmbedMessage(weatherData.citynm, '', [weatherData.days, weatherData.week, weatherData.weather, weatherData.temperature]);
                client.messageApi.postMessage(directMessageGuildID, {
                    embed: embedContent,
                }).then((res) => {
                    console.log(res.data);
                }).catch((err) => {
                    console.log(err);
                });
            });;
        });
    }
});
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

完善`index.ts`代码，同时增加了如下功能：

- 机器人通过天气api拉取默认城市（深圳）的天气，每天主动推送模版消息
- 机器人通过指令选择“深圳、上海、北京”时，被动推送模版消息
- 机器人通过指令选择“私信推送”时，被动推送私信的天气内嵌消息（建议改成注册需要推送消息）
- 机器人通过指令选择“全国天气小程序”，打开天气小程序

代码如下：

```ts
import { AvailableIntentsEventsEnum, createOpenAPI, createWebsocket, Embed, IMessage } from 'qq-guild-bot';
import axios from 'axios';
import * as cron from 'node-cron';

const botConfig = {
    appID: 'APPID', // 申请机器人时获取到的机器人 BotAppID
    token: 'TOKEN', // 申请机器人时获取到的机器人 BotToken
    intents: [AvailableIntentsEventsEnum.AT_MESSAGES], // 事件订阅,用于开启可接收的消息类型
    sandbox: false, // 沙箱支持，可选，默认false. v2.7.0+
};

interface IWeatherData {
    days: string;                  // 2022-03-03
    week: string;                  // 星期四
    citynm: string;                // 深圳
    temperature: string;           // 25C/18C 
    temperature_curr: string;      // 24C
    humidity: string;              // 59%
    weather: string;               // 多云
    weather_curr: string;          // 晴
    weather_icon: string;          // 地址
    wind: string;                  // 东风
}

// 创建 client
const client = createOpenAPI(botConfig);
// 创建 websocket 连接
const ws = createWebsocket(botConfig);
// 定时推送天气子频道id
let subWeatherChannelID: string;

// 获取指定城市的天气数据
function getWeatherByCity(city: string) {
    const url = `http://api.k780.com/?app=weather.today&cityNm=${city}&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json`;
    return new Promise<IWeatherData>((resolve, reject) => {
        axios.get(url).then((response) => {
            const data = response.data;
            if (data.success === '1') {
                resolve(data.result);
            } else {
                console.error(data.msg);
                reject(data.msg);
            }
        }).catch((err) => {
            console.log(err);
            reject(err);
        });
    });
}

function createArk24Message(title: string, subtitle: string, desc: string, img?: string) {
    const message = {
        template_id: 24, kv: [
            { key: "#TITLE#", value: title },
            { key: "#SUBTITLE#", value: subtitle },
            { key: "#METADESC#", value: desc },
            { key: "#IMGC#", value: img },
        ]
    };
    return message as any;
}

function createEmbedMessage(title: string, thumbnail: string, items: string[]) {
    const message: Embed = { title, thumbnail: { url: thumbnail }, fields: [] };
    items.forEach(item => {
        message.fields!.push({ name: item });
    });
    return message;
}

// 获取私信场景id，用于发私信消息
async function getDirectMessageGuildID(sourceGuildID: string, authorID: string) {
    const result = await client.directMessageApi.createDirectMessage({ source_guild_id: sourceGuildID, recipient_id: authorID });
    return result.data.guild_id;
}

function postWeatherToChannel(city: string, fromMessage: IMessage) {
    getWeatherByCity('深圳').then(weatherData => {
        const embedContent = createEmbedMessage(weatherData.citynm, '', [weatherData.days, weatherData.week, weatherData.weather, weatherData.temperature]);
        client.messageApi.postMessage(fromMessage.channel_id, {
            embed: embedContent,
        }).then((res) => {
            console.log(res.data);
        }).catch((err) => {
            console.log(err);
        });
    });
}

function postWeatherToDirectMessage(city: string, fromMessage: IMessage) {
    getWeatherByCity(city).then(weatherData => {
        getDirectMessageGuildID(fromMessage.guild_id, fromMessage.author.id).then(directMessageGuildID => {
            const embedContent = createEmbedMessage(weatherData.citynm, '', [weatherData.days, weatherData.week, weatherData.weather, weatherData.temperature]);
            client.messageApi.postMessage(directMessageGuildID, {
                embed: embedContent,
            }).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.log(err);
            });
        });;
    });
}

// 注册用户 at 机器人消息事件
ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: { msg: IMessage }) => {
    subWeatherChannelID = data.msg.channel_id;
    const content = data.msg.content;
    if (content.includes('深圳')) {
        postWeatherToChannel('深圳', data.msg);
        return;
    }
    if (content.includes('北京')) {
        postWeatherToChannel('北京', data.msg);
        return;
    }
    if (content.includes('上海')) {
        postWeatherToChannel('上海', data.msg);
        return;
    }
    if (content.includes('/私信推送')) {
        postWeatherToDirectMessage('深圳', data.msg);
        return;
    }
    if (content.includes('/全国天气小程序')) {
        // TODO:
    }
});

//cron表达式由6部分组成，从左到右分别表示 秒 分 时 日 月 星期
//*表示任意值  ？表示不确定值，只能用于星期和日
//这里每天9点发送消息
cron.schedule('0 0 9 * * ?', () => {
    if (subWeatherChannelID) {
        getWeatherByCity('深圳').then(weatherData => {
            const embedContent = createEmbedMessage(weatherData.citynm, '', [weatherData.days, weatherData.week, weatherData.weather, weatherData.temperature]);
            client.messageApi.postMessage(subWeatherChannelID, {
                embed: embedContent,
            }).then((res) => {
                console.log(res.data);
            }).catch((err) => {
                console.log(err);
            });
        });;
    }
});
```

完整代码看 [天气机器人-Node实现版](https://github.com/tencent-connect/bot-demos/tree/master/node)









