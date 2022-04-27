package main

import (
	"context"
	"io/ioutil"
	"log"
	"os"
	"time"

	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/dto/message"
	"github.com/tencent-connect/botgo/openapi"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/event"
	"github.com/tencent-connect/botgo/websocket"

	yaml "gopkg.in/yaml.v2"
)

const (
	ConfigPath       = "config.yaml"  //配置文件名
	GuildCreateEvent = "GUILD_CREATE" //机器人被加入到某个频道的事件

	CmdDirectChatMsg = "/私信天气"
	CmdNowWeather    = "/当前天气"
	CmdFutureWeather = "/未来天气"
	CmdDressingIndex = "/穿衣指数"
	CmdAirQuality    = "/空气质量"
)

var config Config
var api openapi.OpenAPI
var guildId string
var ctx context.Context

func init() {
	content, err := ioutil.ReadFile(ConfigPath)
	if err != nil {
		log.Println("读取配置文件出错， err = ", err)
		os.Exit(1)
	}

	err = yaml.Unmarshal(content, &config)
	if err != nil {
		log.Println("解析配置文件出错， err = ", err)
		os.Exit(1)
	}
	log.Println(config)
}

func main() {
	token := token.BotToken(config.AppID, config.Token) //生成token
	api = botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx = context.Background()
	ws, err := api.WS(ctx, nil, "") //websocket
	if err != nil {
		log.Fatalln("websocket错误， err = ", err)
		os.Exit(1)
	}

	//开启每日9点定时
	timer := cron.New()
	//cron表达式由6部分组成，从左到右分别表示 秒 分 时 日 月 星期
	//*表示任意值  ？表示不确定值，只能用于星期和日
	timer.AddFunc("0 0 9 * * ?", timerHandler)
	timer.Start()

	var atMessage event.ATMessageEventHandler = atMessageEventHandler //@事件处理
	var guildEvent event.GuildEventHandler = guildHandler             //频道事件处理
	intent := websocket.RegisterHandlers(atMessage, guildEvent)           // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent)                   // 启动socket监听
}

//处理 @机器人 的消息
func atMessageEventHandler(event *dto.WSPayload, data *dto.WSATMessageData) error {
	res := message.ParseCommand(data.Content) //去掉@结构和清除前后空格
	log.Println("cmd = " + res.Cmd + " content = " + res.Content)
	cmd := res.Cmd
	content := res.Content

	switch cmd {
	case CmdNowWeather: //获取当前天气
		var webData *WeatherResp = getNowWeatherByCity(content)
		if webData != nil {
			//MsgID 表示这条消息的触发来源，如果为空字符串表示主动消息
			//Ark 传入数据时表示发送的消息是Ark
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForNowWeather(webData)})
		}
	case CmdDirectChatMsg: //私信天气消息到用户
		var webData *WeatherResp = getNowWeatherByCity(content)
		if webData != nil {
			//创建私信会话
			directMsg, err := api.CreateDirectMessage(ctx, &dto.DirectMessageToCreate{
				SourceGuildID: data.GuildID,
				RecipientID:   data.Author.ID,
			})
			if err != nil {
				log.Println("私信创建出错了，err = ", err)
			}
			//发送私信消息
			//Embed 传入数据时表示发送的是 Embed
			api.PostDirectMessage(ctx, directMsg, &dto.MessageToCreate{Embed: createEmbed(webData)})
		}
	case CmdFutureWeather: //获取未来几天的天气状况
		weather := getFutureWeatherByCity(content)
		if weather != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkByFutureWeatherData(weather)})
		}
	case CmdDressingIndex:
		weather := getClothIndexByCity(content)
		if weather != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkByLifeIndex(weather)})
		}
	case CmdAirQuality:
		weather := getAQIByCity(content)
		if weather != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkByAQI(weather)})
		}
	}
	return nil
}

//处理定时事件
func timerHandler() {
	if guildId != "" {
		channels, err := api.Channels(ctx, guildId)
		if err != nil {
			log.Println("获取频道的信息出错，err = ", err)
			return
		}
		var webData *WeatherResp = getNowWeatherByCity("深圳")
		//发送主动消息
		api.PostMessage(ctx, channels[2].ID, &dto.MessageToCreate{MsgID: "", Ark: createArkForNowWeather(webData)})
	}
}

//处理频道相关的事件
func guildHandler(event *dto.WSPayload, data *dto.WSGuildData) error {
	if event.Type == GuildCreateEvent { //当机器人加入频道时，获取频道的id
		guildId = data.ID
		log.Println("guildId = " + data.ID + " guildName = " + data.Name)
	}
	return nil
}

//创建未来天气的ark消息
func createArkByFutureWeatherData(weather *FutureWeatherResp) *dto.Ark {
	list := make([]*dto.ArkObjKV, len(weather.ResultDatas)+1)
	list[0] = NewArkObjKV("desc", "天气预报 "+weather.ResultDatas[0].CityNm)
	for i := 1; i < len(weather.ResultDatas)+1; i++ {
		list[i] = NewArkObjKV("desc", weather.ResultDatas[i-1].Week+" "+weather.ResultDatas[i-1].Weather)
	}
	return NewArk(23, NewArkKObj("#LIST#", list...))
}

//创建穿衣指数的ark消息
func createArkByLifeIndex(weather *LifeIndexRsp) *dto.Ark {
	return NewArk(23,
		NewArkKObj("#LIST#",
			NewArkObjKV("desc", weather.Result[0].ClothIndex+" "+weather.Result[0].Days),
			NewArkObjKV("desc", weather.Result[0].ClothAttr),
			NewArkObjKV("desc", weather.Result[0].ClothRecommend)))
}

//创建空气质量的ark消息
func createArkByAQI(aqi *AQIRsp) *dto.Ark {
	return NewArk(23,
		NewArkKObj("#LIST#",
			NewArkObjKV("desc", "空气质量"),
			NewArkObjKV("desc", "空气等级："+aqi.AQIResult.AqiLevid+" "+aqi.AQIResult.AqiLevnm),
			NewArkObjKV("desc", aqi.AQIResult.AqiRemark)))
}

//获取 Embed
func createEmbed(weather *WeatherResp) *dto.Embed {
	return NewEmbed(weather.ResultData.CityNm+" "+weather.ResultData.Weather, "描述",
		NewMessageEmbedThumbnail(weather.ResultData.WeatherIcon),
		NewField(weather.ResultData.Days+" "+weather.ResultData.Week),
		NewField("当日温度区间："+weather.ResultData.Temperature),
		NewField("当前温度："+weather.ResultData.TemperatureCurr),
		NewField("最高温度："+weather.ResultData.TempHigh),
		NewField("最低温度："+weather.ResultData.TempLow),
	)
}

//创建当前天气的ark消息
func createArkForNowWeather(weather *WeatherResp) *dto.Ark {
	return NewArk(23,
		NewArkKV("#DESC#", "描述"),
		NewArkKV("#PROMPT#", "提示消息"),
		NewArkKObj("#LIST#",
			NewArkObjKV("desc", weather.ResultData.CityNm+" "+weather.ResultData.Weather+" "+weather.ResultData.Days+" "+weather.ResultData.Week),
			NewArkObjKV("desc", "当日温度区间："+weather.ResultData.Temperature),
			NewArkObjKV("desc", "当前温度："+weather.ResultData.TemperatureCurr),
			NewArkObjKV("desc", "当前湿度："+weather.ResultData.Humidity)))
}
