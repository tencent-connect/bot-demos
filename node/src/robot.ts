import { createOpenAPI, createWebsocket, IMessage, IOpenAPI, MessageToCreate, AvailableIntentsEventsEnum, GetWsParam, Embed, DirectMessageToCreate } from 'qq-guild-bot';
import { EventEmitter } from 'ws';

export class Robot {

    client: IOpenAPI;
    ws: EventEmitter;

    static createEmbedMessage(title: string, thumbnail: string, items: string[]) {
        const message: Embed = { title, thumbnail: { url: thumbnail }, fields: [] };
        items.forEach(item => {
            message.fields!.push({ name: item });
        });
        return message;
    }

    static createArk24Message(title: string, subtitle: string, desc: string, img?: string) {
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

    constructor(config: GetWsParam) {
        this.client = createOpenAPI(config); // 创建 client
        this.ws = createWebsocket(config); // 创建 websocket 连接
        this.client
    }

    // 监听用户at机器人消息
    setAtMessagesHandler(handler: (message: IMessage) => void) {
        this.ws.on(AvailableIntentsEventsEnum.AT_MESSAGES, (data: any) => {
            console.log('[AT_MESSAGES] 事件接收 :', data);
            handler(data.msg);
        });
    }

    // 监听用户私信机器人消息
    setDirectMessagesHandler(handler: (message: IMessage) => void) {
        this.ws.on(AvailableIntentsEventsEnum.DIRECT_MESSAGE, (data: any) => {
            console.log('[DIRECT_MESSAGE] 事件接收 :', data);
            this.postDirectMessage(data.msg.guild_id, {
                content: '777',
                msg_id: data.msg.id,
            });
            handler(data.msg);
        });
    }

    // 给频道用户发送消息，message 中带 msg_id(回复用户的消息) 为被动消息，不带为主动消息会限制频率
    postMessage(channelID: string, message: MessageToCreate) {
        this.client.messageApi.postMessage(channelID, message).then((res) => {
            console.log(res.data);
        }).catch((err) => {
            console.log(err);
        });
    }

    // 给信息用户发消息
    postDirectMessage(guildID: string, message: MessageToCreate) {
        this.client.directMessageApi.postDirectMessage(guildID, message).then((res) => {
            console.log(res.data);
        }).catch((err) => {
            console.log(err);
        });
    }

    // 获取私信用户场景 id，与频道 id 不同，用于给频道中的用户发主动私信消息
    async getDirectMessageGuildID(sourceGuildID: string, authorID: string) {
        const result = await this.client.directMessageApi.createDirectMessage({ source_guild_id: sourceGuildID, recipient_id: authorID });
        return result.data.guild_id;
    }

}
