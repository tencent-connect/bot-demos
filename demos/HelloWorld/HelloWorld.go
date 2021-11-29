// 被动消息示例
// 客户端At机器人并传入 hello，  则收到机器人回复： Hello World
package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"time"

	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	yaml "gopkg.in/yaml.v2"
)

var conf struct {
	AppID uint64 `yaml:"appid"`
	Token string `yaml:"token"`
}

func init() {
	content, err := ioutil.ReadFile("../config.yaml")
	if err != nil {
		log.Println("read conf failed")
		os.Exit(1)
	}
	if err := yaml.Unmarshal(content, &conf); err != nil {
		log.Println(err)
		os.Exit(1)
	}
	log.Println(conf)
}

func main() {
	token := token.BotToken(conf.AppID, conf.Token)
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	ws, err := api.WS(ctx, nil, "")
	log.Printf("%+v, err:%v", ws, err)
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
	}

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {
		// 打印一些值 供参考 无实际作用
		fmt.Println(event.Data)
		fmt.Println(data.GuildID, data.ChannelID, data.Content)
		fmt.Println(data.Author.ID, data.Author.Username)

		// 发被动消息到频道
		if strings.HasSuffix(data.Content, "> hello") { // 如果at机器人并输入 hello 则回复 Hello World 。需要后台配置语料 否则回复不了
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Content: "Hello World"})
		} else { // 否则回复提示信息 需要申请发Ark消息权限
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: &dto.Ark{
				TemplateID: 23, KV: []*dto.ArkKV{
					{Key: "#LIST#", Obj: []*dto.ArkObj{
						{ObjKV: []*dto.ArkObjKV{{Key: "desc", Value: "试试输入 hello"}}},
					}},
				}}})
		}

		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听

}
