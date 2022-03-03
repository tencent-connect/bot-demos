package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/openapi"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	yaml "gopkg.in/yaml.v2"
)

type Config struct {
	AppID uint64 `yaml:"appid"`
	Token string `yaml:"token"`
}

type WeatherResp struct {
	Success string `json:"success"`
	ResultData Result `json:"result"`
	Msg string `json:"msg"`
}

type Result struct {
	Days string `json:"days"`
	Week string `json:"week"`
	CityNm string `json:"citynm"`
	Temperature string `json:"temperature"`
	TemperatureCurr string `json:"temperature_curr"`
	Humidity string `json:"humidity"`
	Weather string `json:"weather"`
	Wind string `json:"wind"`
	Winp string `json:"winp"`
	TempHigh string `json:"temp_high"`
	TempLow string `json:"temp_low"`
	WeatherIcon string `json:"weather_icon"`
}

const (
   configPath       = "config.yaml"
   guildCreateEvent = "GUILD_CREATE"

   commandShenZhen = "> /深圳"
   commandShangHai = "> /上海"
   commandBeiJin = "> /北京"
   commandDirectChatMsg = "> /私信推送"
   commandWeatherProgrammer = "> /全国天气小程序"

   cityShenZhen = "深圳"
   cityShangHai = "上海"
   cityBeiJin = "北京"
)

var config Config
var api openapi.OpenAPI
var guildId string
var ctx context.Context

func init() {
	content, err := ioutil.ReadFile(configPath)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	err = yaml.Unmarshal(content, &config)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}
	log.Println(config)
}



func main() {
	token := token.BotToken(config.AppID, config.Token)
	api = botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx = context.Background()
	timer := cron.New()
	ws, err := api.WS(ctx, nil, "")
	log.Printf("%+v, err:%v", ws, err)
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
	}

	timer.AddFunc("0 0 9 * * ?", timerHandler)
	timer.Start()

	var atMessage websocket.ATMessageEventHandler = atMessageEventHandler
	var guildEvent websocket.GuildEventHandler = guildHandler

	intent := websocket.RegisterHandlers(atMessage, guildEvent)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
}

//处理 @机器人 的消息
func atMessageEventHandler(event *dto.WSPayload, data *dto.WSATMessageData) error {
	// 打印一些值 供参考 无实际作用
	fmt.Println(event.Data)
	fmt.Println(data.GuildID, data.ChannelID, data.Content)
	fmt.Println(data.Author.ID, data.Author.Username)

	// 发被动消息到频道
	if strings.HasSuffix(data.Content, commandShenZhen) {
		var webData *WeatherResp = getWeatherByCity(cityShenZhen)
		if webData != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	} else if strings.HasSuffix(data.Content, commandBeiJin) {
		var webData *WeatherResp = getWeatherByCity(cityBeiJin)
		if webData != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	} else if strings.HasSuffix(data.Content, commandShangHai) {
		var webData *WeatherResp = getWeatherByCity(cityShangHai)
		if webData != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	} else if strings.HasSuffix(data.Content, commandDirectChatMsg) {
		var webData *WeatherResp = getWeatherByCity(cityShenZhen)
		if webData != nil {
			directMsg, err := api.CreateDirectMessage(ctx, &dto.DirectMessageToCreate{
				SourceGuildID: data.GuildID,
				RecipientID: data.Author.ID,
			})
			if err != nil {
				log.Println("私信创建出错了，err = " , err)
			}
			api.PostDirectMessage(ctx, directMsg, &dto.MessageToCreate{Embed: createEmbed(webData)})
		}
	} else if strings.HasSuffix(data.Content, commandWeatherProgrammer) {

	}

	return nil
}

func timerHandler()  {
	if guildId != "" {
		channels, err := api.Channels(ctx, guildId)
		if err != nil {
			log.Println(err)
			return
		}
		var webData *WeatherResp = getWeatherByCity(cityShenZhen)
		api.PostMessage(ctx, channels[2].ID, &dto.MessageToCreate{MsgID: "", Ark: createArkForTemplate23(webData)})
	}
}

func getWeatherByCity(cityName string) *WeatherResp {
	url := "http://api.k780.com/?app=weather.today&cityNm="+ cityName +"&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalln("天气预报接口请求异常, err = ", err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln("天气预报接口数据异常, err = ", err)
	}
	var weatherData WeatherResp
	err = json.Unmarshal(body, &weatherData)
	if err != nil {
		log.Fatalln("解析数据异常 err = ", err, body)
	}

	if weatherData.Success != "1" {
		log.Fatalln("返回数据问题 err = ", weatherData.Msg)
		return nil
	}
   return &weatherData
}

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

func createArkForTemplate23(weather *WeatherResp) *dto.Ark {
	return &dto.Ark{
		TemplateID: 23,
		KV: createArkKvArray(weather),
	}
}

func createArkKvArray(weather *WeatherResp) []*dto.ArkKV {
	akvArray := make([]*dto.ArkKV, 3)
	akvArray[0] = &dto.ArkKV{
		Key: "#DESC#",
		Value: "描述",
	}
	akvArray[1] = &dto.ArkKV{
		Key: "#PROMPT#",
		Value: "#PROMPT#",
	}
	akvArray[2] = &dto.ArkKV{
		Key: "#LIST#",
		Obj: createArkObjArray(weather),
	}
	return akvArray
}

func createArkObjArray(weather *WeatherResp) []*dto.ArkObj {
	objectArray := make([]*dto.ArkObj, 7)
	objectArkArray := make([]*dto.ArkObjKV, 1)
	objectArkArray[0] = &dto.ArkObjKV{
		Key: "desc",
		Value: weather.ResultData.Days + " " + weather.ResultData.Week,
	}
	objectArray = []*dto.ArkObj{
		{
			[]*dto.ArkObjKV{
				{
					Key: "desc",
					Value: weather.ResultData.CityNm + " " + weather.ResultData.Weather + " " + weather.ResultData.Days + " " + weather.ResultData.Week,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key: "desc",
					Value: "当日温度区间：" + weather.ResultData.Temperature,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key: "desc",
					Value: "当前温度：" + weather.ResultData.TemperatureCurr,
				},
			},
		},
		{
			[]*dto.ArkObjKV{
				{
					Key: "desc",
					Value: "当前湿度：" + weather.ResultData.Humidity,
				},
			},
		},
	}
	return objectArray
}

func guildHandler(event *dto.WSPayload, data *dto.WSGuildData) error {
	if event.Type == guildCreateEvent {
		guildId = data.ID
		log.Println("guildId = " + data.ID + " guildName = " + data.Name)
	}
	return nil
}