import { AvailableIntentsEventsEnum } from 'qq-guild-bot';
import { Robot } from './robot';
import { WeatherService } from './weather-service';
import * as cron from 'node-cron';

const botConfig = {
    appID: process.env.ROBOT_ID as string, // 申请机器人时获取到的机器人 BotAppID
    token: process.env.ROBOT_TOKEN as string, // 申请机器人时获取到的机器人 BotToken
    intents: [AvailableIntentsEventsEnum.AT_MESSAGES, AvailableIntentsEventsEnum.DIRECT_MESSAGE], // 事件订阅,用于开启可接收的消息类型
    sandbox: false, // 沙箱支持，可选，默认false. v2.7.0+
};

const defaultCity = '深圳';
let subWeatherChannelID: string;

const weatherService = new WeatherService();
const robot = new Robot(botConfig);
robot.setAtMessagesHandler(message => {
    const content = message.content;
    if (content.includes('订阅天气')) { // 订阅天气
        subWeatherChannelID = message.channel_id;
        robot.postMessage(message.channel_id, {
            content: '订阅成功',
            msg_id: message.id,
        });
        return;
    }
    if (content.includes('/深圳天气')) { // 文字消息
        weatherService.getWeatherData('深圳').then(data => {
            robot.postMessage(message.channel_id, {
                content: `${data.citynm} ${data.days} ${data.week} ${data.weather} ${data.temperature}`,
                image: '',
            });
        });
        return;
    }
    if (content.includes('/上海天气')) { // embed 消息
        weatherService.getWeatherData('上海').then(data => {
            const replyMessage = Robot.createEmbedMessage(data.citynm, '', [data.days, data.week, data.weather, data.temperature]);
            robot.postMessage(message.channel_id, {
                embed: replyMessage
            });
        });
        return;
    }
    if (content.includes('/北京天气')) { // ark 消息
        weatherService.getWeatherData('北京').then(data => {
            const replyMessage = Robot.createArk24Message(data.citynm, `${data.days} ${data.week} ${data.weather} ${data.temperature}`, '天气机器人');
            robot.postMessage(message.channel_id, {
                ark: replyMessage
            });
        });
        return;
    }
    if (content.includes('/私信天气')) { // 私信消息，主动过私信会有每日限制次数
        robot.getDirectMessageGuildID(message.guild_id, message.author.id).then(guildID => {
            weatherService.getWeatherData(defaultCity).then(data => {
                robot.postDirectMessage(guildID, {
                    content: `${data.citynm} ${data.weather} ${data.temperature}`,
                });
            });
        });
        return;
    }
});

// 每天早上8点给订阅的频道发送天气预报
cron.schedule('0 0 8 * * *', () => {
    if (subWeatherChannelID) {
        weatherService.getWeatherData(defaultCity).then(data => {
            robot.postDirectMessage(subWeatherChannelID, { content: `${data.citynm} ${data.days} ${data.week} ${data.weather} ${data.temperature}` });
        });
    }
});
