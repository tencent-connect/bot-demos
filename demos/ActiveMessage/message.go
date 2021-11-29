// 主动消息示例：天气预报
// 运行后 主动向子频道推送天气预报消息
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
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
	// 获取频道列表
	guilds, err := api.MeGuilds(ctx)
	if err != nil {
		log.Fatalln("%+v, err:%v", guilds, err)
	}
	fmt.Println("guilds:", guilds[0])

	// 获取子频道列表
	channels, err := api.Channels(ctx, guilds[0].ID)
	if err != nil {
		log.Fatalln("%+v, err:%v", channels, err)
	}

	// 向所用子频道推送主动消息 （仅示意 线上不要这么做。。。。）
	for key, value := range channels {
		if value.ChannelValueObject.Type == 0 { // 子频道
			fmt.Println("channels: ", key, value.ID, value.ChannelValueObject.Name, value.ChannelValueObject.Type)
			// 主动消息推送
			api.PostMessage(ctx, value.ID, &dto.MessageToCreate{Content: getWeather()})
		}
	}

}

// ==========以下，获取北京的天气信息==========
type WeatherDate struct {
	Days         string // "例如：20211128"
	Week         string //"例如：星期日"
	Citynm       string //"城市名"
	Weather      string //"例如：多云转阴"
	Temperature  string //"例如：10℃/2℃"
	Weather_curr string //"例如：霾"
	Wind         string //"例如：西南风"
	Winp         string //"例如：1级"
}
type WeatherResult struct {
	Success string
	Result  WeatherDate
}

func getWeather() string {
	// https://www.nowapi.com/api/weather.today
	resp, err := http.Get("http://api.k780.com/?app=weather.today&weaId=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json")
	if err != nil {
		log.Fatalln("天气预报接口请求异常")
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln("天气预报接口数据异常")
	}

	var weatherRes WeatherResult
	if err = json.Unmarshal(body, &weatherRes); err != nil {
		fmt.Printf("Unmarshal err, %v\n", err)
		return ""
	}

	fmt.Println("")
	fmt.Println("body", string(body))
	fmt.Println("")
	fmt.Println("weatherRes: ", weatherRes)

	var weather = weatherRes.Result
	var res = "【主动消息示例】天气预报：" + weather.Days + " " + weather.Week + ", " + weather.Citynm + ", 天气：" + weather.Weather + ", " + weather.Wind + " " + weather.Winp
	fmt.Println("")
	fmt.Println("res: ", res)

	return res
	// fmt.Println("")
	// fmt.Println(string(body))
}
