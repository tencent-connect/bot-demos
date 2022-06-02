import { AvailableIntentsEventsEnum } from 'qq-guild-bot';
import { Robot } from './robot';
import { WeatherService } from './weather-service';
import * as cron from 'node-cron';

const botConfig = {
    appID: '替换成自己的APPID', // 申请机器人时获取到的机器人 BotAppID
    token: '替换成自己的TOKEN', // 申请机器人时获取到的机器人 BotToken
    intents: [AvailableIntentsEventsEnum.PUBLIC_GUILD_MESSAGES, AvailableIntentsEventsEnum.DIRECT_MESSAGE], // 事件订阅,用于开启可接收的消息类型
    sandbox: false, // 沙箱支持，可选，默认false. v2.7.0+
};

const defaultCity = '深圳';
const weatherService = new WeatherService();
const robot = new Robot(botConfig);
robot.setAtMessagesHandler(message => {
    const content = message.content;
    if (content.includes('/当前天气')) {
        const city = content.split('/当前天气 ')[1];
        weatherService.getWeatherByCity(city).then(data => {
            robot.postMessage(message.channel_id, {
                content: `${data.citynm} ${data.days} ${data.week} ${data.weather} ${data.temperature}`,
                image: data.weather_icon,
                msg_id: message.id,
            });
        }).catch(err => {
            robot.postMessage(message.channel_id, {
                content: `指令错误`,
                msg_id: message.id,
            });
        });
        return;
    }
    if (content.includes('/未来天气')) {
        const city = content.split('/未来天气 ')[1];
        weatherService.getFutureWeatherByCity(city).then(data => {
            const embedContent = Robot.createEmbedMessage(`${city}未来天气：`, '', data.map(item => {
                return `${item.days} ${item.weather} ${item.temperature}`;
            }));
            robot.postMessage(message.channel_id, {
                embed: embedContent,
                msg_id: message.id,
            });
        }).catch(err => {
            robot.postMessage(message.channel_id, {
                content: `指令错误`,
                msg_id: message.id,
            });
        });;
        return;
    }
    if (content.includes('/穿衣指数')) {
        const city = content.split('/穿衣指数 ')[1];
        weatherService.getLifeIndexByCity(city).then(data => {
            const arkContent = Robot.createArk23Message([
                `${city} ${data[0].days} ${data[0].week_1} 穿衣指数`,
                data[0].lifeindex_ct_attr,
                data[0].lifeindex_ct_dese,
            ]);
            robot.postMessage(message.channel_id, {
                ark: arkContent,
                msg_id: message.id,
            });
        }).catch(err => {
            robot.postMessage(message.channel_id, {
                content: `指令错误`,
                msg_id: message.id,
            });
        });;
        return;
    }
    if (content.includes('/空气质量')) { // 私信消息，主动过私信会有每日限制次数
        const city = content.split('/空气质量 ')[1];
        weatherService.getAQIByCity(city).then(data => {
            console.log(data);
            const arkContent = Robot.createArk23Message([
                `${city} 空气质量`,
                data.aqi_levnm,
                data.aqi_remark,
            ]);
            robot.postMessage(message.channel_id, {
                ark: arkContent,
                msg_id: message.id,
            });
        }).catch(err => {
            robot.postMessage(message.channel_id, {
                content: `指令错误`,
                msg_id: message.id,
            });
        });;
        return;
    }
    if (content.includes('/私信天气')) { // 私信消息，主动过私信会有每日限制次数
        const city = content.split('/私信天气 ')[1];
        robot.getDirectMessageGuildID(message.guild_id, message.author.id).then(guildID => {
            weatherService.getWeatherByCity(city).then(data => {
                robot.postDirectMessage(guildID, {
                    content: `${data.citynm} ${data.weather} ${data.temperature}`,
                });
            });
        }).catch(err => {
            robot.postMessage(message.channel_id, {
                content: `指令错误`,
                msg_id: message.id,
            });
        });;
        return;
    }
});

// 每天早上8点给订阅的频道发送天气预报
cron.schedule('0 0 8 * * *', async () => {
    const channelId = await robot.getMyFirstChannelId();
    weatherService.getWeatherByCity(defaultCity).then(data => {
        robot.postDirectMessage(channelId, { content: `${data.citynm} ${data.days} ${data.week} ${data.weather} ${data.temperature}` });
    });
});
