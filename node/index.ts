import { AvailableIntentsEventsEnum, createOpenAPI, createWebsocket, Embed, IMessage } from 'qq-guild-bot';
import axios from 'axios';
import * as cron from 'node-cron';

const botConfig = {
    appID: 'APPID', // 申请机器人时获取到的机器人 BotAppID
    token: 'TOKEN', // 申请机器人时获取到的机器人 BotToken
    intents: [AvailableIntentsEventsEnum.PUBLIC_GUILD_MESSAGES], // 事件订阅,用于开启可接收的消息类型
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
ws.on(AvailableIntentsEventsEnum.PUBLIC_GUILD_MESSAGES, (data: { msg: IMessage }) => {
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
