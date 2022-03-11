package main

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/dto/message"
	"github.com/tencent-connect/botgo/openapi"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"

	yaml "gopkg.in/yaml.v2"
)

//Config 定义了配置文件的结构
type Config struct {
	AppID uint64 `yaml:"appid"` //机器人的appid
	Token string `yaml:"token"` //机器人的token
}

//WeatherResp 定义了返回天气数据的结构
type WeatherResp struct {
	Success    string `json:"success"` //标识请求是否成功，0表示成功，1表示失败
	ResultData Result `json:"result"`  //请求成功时，获取的数据
	Msg        string `json:"msg"`     //请求失败时，失败的原因
}

//Result 定义了具体天气数据结构
type Result struct {
	Days            string `json:"days"`             //日期，例如2022-03-01
	Week            string `json:"week"`             //星期几
	CityNm          string `json:"citynm"`           //城市名
	Temperature     string `json:"temperature"`      //当日温度区间
	TemperatureCurr string `json:"temperature_curr"` //当前温度
	Humidity        string `json:"humidity"`         //湿度
	Weather         string `json:"weather"`          //天气情况
	Wind            string `json:"wind"`             //风向
	Winp            string `json:"winp"`             //风力
	TempHigh        string `json:"temp_high"`        //最高温度
	TempLow         string `json:"temp_low"`         //最低温度
	WeatherIcon     string `json:"weather_icon"`     //气象图标
}

const (
	ConfigPath       = "config.yaml"  //配置文件名
	GuildCreateEvent = "GUILD_CREATE" //机器人被加入到某个频道的事件

	CommandShenZhen          = "深圳"
	CommandShangHai          = "上海"
	CommandBeiJin            = "北京"
	CommandDirectChatMsg     = "私信推送"
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

	var atMessage websocket.ATMessageEventHandler = atMessageEventHandler //@事件处理
	var guildEvent websocket.GuildEventHandler = guildHandler             //频道事件处理
	intent := websocket.RegisterHandlers(atMessage, guildEvent)           // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent)                   // 启动socket监听
}

//处理 @机器人 的消息
func atMessageEventHandler(event *dto.WSPayload, data *dto.WSATMessageData) error {
	res := message.ETLInput(data.Content) //去掉@结构和清除前后空格
	if strings.HasPrefix(res, "/") {      //去掉/
		res = strings.Replace(res, "/", "", 1)
	}
	
	switch res {
	case CommandShenZhen, CommandBeiJin, CommandShangHai:
		var webData *WeatherResp = getWeatherByCity(res)
		if webData != nil {
			//MsgID 表示这条消息的触发来源，如果为空字符串表示主动消息
			//Ark 传入数据时表示发送的消息是Ark
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	case CommandDirectChatMsg: //私信深圳的天气消息到用户
		var webData *WeatherResp = getWeatherByCity(CommandShenZhen)
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
		var webData *WeatherResp = getWeatherByCity(CommandShenZhen)
		//发送主动消息
		api.PostMessage(ctx, channels[2].ID, &dto.MessageToCreate{MsgID: "", Ark: createArkForTemplate23(webData)})
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

//获取对应城市的天气数据
func getWeatherByCity(cityName string) *WeatherResp {
	url := "http://api.k780.com/?app=weather.today&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalln("天气预报接口请求异常, err = ", err)
		return nil
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln("天气预报接口数据异常, err = ", err)
		return nil
	}
	var weatherData WeatherResp
	err = json.Unmarshal(body, &weatherData)
	if err != nil {
		log.Fatalln("解析数据异常 err = ", err, body)
		return nil
	}
	if weatherData.Success != "1" {
		log.Fatalln("返回数据问题 err = ", weatherData.Msg)
		return nil
	}
	return &weatherData
}

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
				Name:  "当日温度区间：" + weather.ResultData.Temperature,
				Value: "test",
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
		},
	}
}

//获取23号的Ark
func createArkForTemplate23(weather *WeatherResp) *dto.Ark {
	return &dto.Ark{
		TemplateID: 23,
		KV:         createArkKvArray(weather),
	}
}

//创建Ark需要的ArkKV数组
func createArkKvArray(weather *WeatherResp) []*dto.ArkKV {
	akvArray := make([]*dto.ArkKV, 3)
	akvArray[0] = &dto.ArkKV{
		Key:   "#DESC#",
		Value: "描述",
	}
	akvArray[1] = &dto.ArkKV{
		Key:   "#PROMPT#",
		Value: "提示消息",
	}
	akvArray[2] = &dto.ArkKV{
		Key: "#LIST#",
		Obj: createArkObjArray(weather),
	}
	return akvArray
}

//创建ArkKV需要的ArkObj数组
func createArkObjArray(weather *WeatherResp) []*dto.ArkObj {
	objectArray := []*dto.ArkObj{
		{
			[]*dto.ArkObjKV{
				{
					Key:   "desc",
					Value: weather.ResultData.CityNm + " " + weather.ResultData.Weather + " " + weather.ResultData.Days + " " + weather.ResultData.Week,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key:   "desc",
					Value: "当日温度区间：" + weather.ResultData.Temperature,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key:   "desc",
					Value: "当前温度：" + weather.ResultData.TemperatureCurr,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key:   "desc",
					Value: "当前湿度：" + weather.ResultData.Humidity,
				},
			},
		},
	}
	return objectArray
}
