# 开发前的准备

如下图，点击 [频道机器人开发官网](https://bot.q.qq.com/open) ，在官网页面点击 **立即注册** 

![注册界面](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/ff729f2e-1ce8-4fa7-b364-2be0d2ca18c3.png)

有两种主体类型，可以根据自己的实际情况进行选择，这里介绍个人开发者的流程，企业详细流程见 [企业主体入驻
](https://bot.q.qq.com/wiki/#_2-%E4%BC%81%E4%B8%9A%E4%B8%BB%E4%BD%93%E5%85%A5%E9%A9%BB)

![个人开发者](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/f377e842-b6ef-47f1-8eac-1b88733e9ad8.png)

目前个人开发者还在内测中，需要点击如下图的 [频道机器人个体开发者邀请问卷](https://docs.qq.com/form/page/DSlZjZ0dPc0llT3d0?_w_tencentdocx_form=1#/fill-detail) 就行申请

![频道机器人个体开发者邀请问卷](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/b93b8cb6-0361-4b58-a2d7-3c456d294076.png)

提交完成后，需要等待审核。如果审核通过，就会发送邮件到你的邮箱。

![发送邮件到你的邮箱](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/06eedc81-fee4-4b5f-b862-781dd5ef4bba.png)

收到邀请码后就可以点击 **下一步** 进入登陆页面

![登陆页面](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/0c627f76-d7c1-4834-9ca8-c2a75cd6306e.png)

在完成邮箱、手机号等认证后，就可以进入 QQ机器人管理界面，如下图所示：

![QQ机器人管理界面](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/1145ae87-951b-4d55-9f41-7a0d313f73f6.png)

点击 **生成BotAppID** 进入机器人配置界面（如下图）：

![机器人配置界面](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/5e92d587-3e99-45b8-a4ff-13b9cf9b1270.png)

这里面有两个选项需要注意（标红部分）：**沙箱频道ID** 是指你创建频道的ID，需要注意的是，如果你之前创建的频道人数超过限制，就需要创建另一个频道；**机器人类型**有两种，一种是私域机器人，一种是公域机器人。简单来说，私域机器人只能在你自己的频道使用，而公域机器人可以在所有频道使用。

点击 **提交审核** ，审核完成后就能看到如下界面：

![](https://github.com/lichukuan/bot-demos/blob/personal/add_go_demo/images/adf8c879-dc38-43f1-887a-265ed0db496e.png)

点击 **查看详情** 就可以看到你的 `BotAppID` 、`BotToken` 、`BotSecret` 了，**注意这个信息不要泄露**。


# Go环境搭建

在命令行输入如下命令来下载 `Go` 语言压缩包

```
wget https://dl.google.com/go/go1.17.7.linux-amd64.tar.gz
```

解压缩到指定目录，这样 `Go` 语言就安装好了

```
sudo tar -xzf go1.17.7.linux-amd64.tar.gz -C /usr/local
```

在命令行输入 `go version` 指令检验是否安装完成，如果安装成功，会打印出 `Go` 的版本号

```
[root@VM-155-69-centos ~]# go version
go version go1.17.7 linux/amd64
```

使用下面命令创建一个 `demo` 项目，并初始化

```
mkdir demo
cd demo
go mod init demo
```

# 机器人自动回复普通消息

使用 `mkdir robot.go` 创建一个 `robot.go` 的文件。使用 `vim robot.go` 编辑`robot.go` 文件，键盘输入 `i` ,把文件变成可编辑状态，复制粘贴下面代码。`esc` 键退出，键盘输入 `:wq` 保持退出。

```go
package main

import (
	"context"
	"log"
	"os"
	"strings"
	"time"

	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
)

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	ws, err := api.WS(ctx, nil, "") //websocket
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
		os.Exit(1)
	}

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {

		if strings.HasSuffix(data.Content, "> hello") { // 如果at机器人并输入 hello 则回复 你好。
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Content: "你好"})
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
}
```

由于上面的代码使用了机器人的sdk，需要先下载下来，命令如下：

```
go get github.com/tencent-connect/botgo
```

上述步骤完成后就可以使用 `go run robot.go` 命令运行代码。如图，这时在频道内 @机器人 `hello` 指令就可以收到回复了

![]()

# 获取天气数据

天气机器人最重要的就是提供天气的数据，这里是使用的 `https://www.nowapi.com/api/weather.today` 的Api。代码如下：

```
package main

import (
	"context"
	"encoding/json"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

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

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	ws, err := api.WS(ctx, nil, "") //websocket
	if err != nil {
		log.Fatalln("websocket错误， err = ", err)
		os.Exit(1)
	}
	
	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {
		if strings.HasSuffix(data.Content, "> hello") {
			weatherData := getWeatherByCity("深圳")
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID,
				Content: weatherData.ResultData.CityNm + " " + weatherData.ResultData.Weather + " " + weatherData.ResultData.Days + " " + weatherData.ResultData.Week,
				Image: weatherData.ResultData.WeatherIcon,//天气图片
			})
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
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
```
效果图如下：

![]()

# 机器人主动推送消息

上面的教程只实现一个简单的获取天气的功能，但是我们做的是天气机器人，希望实现一个报告天气的功能。一般的天气应用都会在一个特定时间给你推送天气通知，在频道机器人中，你可以通过主动消息来实现这个功能。代码如下：

```
package main

import (
	"context"
	"encoding/json"
	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

var channelId = "" //保存子频道的id

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

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	timer := cron.New()
	ws, err := api.WS(ctx, nil, "") //websocket
	if err != nil {
		log.Fatalln("websocket错误， err = ", err)
		os.Exit(1)
	}

	var activeMsgPush = func() {
		if channelId != "" {
			//MsgID 为空字符串表示主动消息
			api.PostMessage(ctx, channelId, &dto.MessageToCreate{MsgID: "", Content: "当前天气是：晴天"})
		}
	}
	//cron表达式由6部分组成，从左到右分别表示 秒 分 时 日 月 星期
	//*表示任意值  ？表示不确定值，只能用于星期和日
	//这里表示每天15:53分发送消息
	timer.AddFunc("0 53 15 * * ?", activeMsgPush) 
	timer.Start()

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {
		channelId = data.ChannelID
		if strings.HasSuffix(data.Content, "> hello") {
			weatherData := getWeatherByCity("深圳")
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID,
				Content: weatherData.ResultData.CityNm + " " + weatherData.ResultData.Weather + " " + weatherData.ResultData.Days + " " + weatherData.ResultData.Week,
				Image:   weatherData.ResultData.WeatherIcon, //天气图片
			})
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
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
```

由于在代码使用了 `cron` 来实现定时功能，需要下载对应的依赖。

```
go get github.com/robfig/cron
```

运行该代码，效果如下图

![]()

# 机器人指令回复ark消息

提供给个人开发者的`Ark`有3种，这里使用 23 号`Ark`。其它`Ark`见[消息模板](https://bot.q.qq.com/wiki/develop/api/openapi/message/message_template.html)

```go
package main

import (
	"context"
	"encoding/json"
	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

var channelId = "" //保存子频道的id

type WeatherResp struct {
	Success    string `json:"success"` //标识请求是否成功，0表示成功，1表示失败
	ResultData Result `json:"result"`  //请求成功时，获取的数据
	Msg        string `json:"msg"`     //请求失败时，失败的原因
}

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

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	timer := cron.New()
	ws, err := api.WS(ctx, nil, "")//websocket
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
		os.Exit(1)
	}

	var activeMsgPush = func() {
		if channelId != "" {
			weatherData := getWeatherByCity("深圳")
			api.PostMessage(ctx, channelId, &dto.MessageToCreate{MsgID: "", Ark: createArkForTemplate23(weatherData)})
		}
	}

	timer.AddFunc("0 0 9 * * ?", activeMsgPush) //每天九点发送消息
	timer.Start()

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {
		channelId = data.ChannelID
		if strings.HasSuffix(data.Content, "> hello") {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Content: "你好"})
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
}

func getWeatherByCity(cityName string) *WeatherResp {
	url := "http://api.k780.com/?app=weather.today&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
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

func createArkForTemplate23(weather *WeatherResp) *dto.Ark {
	return &dto.Ark{
		TemplateID: 23,
		KV:         createArkKvArray(weather),
	}
}

func createArkKvArray(weather *WeatherResp) []*dto.ArkKV {
	akvArray := make([]*dto.ArkKV, 3)
	akvArray[0] = &dto.ArkKV{
		Key:   "#DESC#",
		Value: "描述",
	}
	akvArray[1] = &dto.ArkKV{
		Key:   "#PROMPT#",
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
		Key:   "desc",
		Value: weather.ResultData.Days + " " + weather.ResultData.Week,
	}
	objectArray = []*dto.ArkObj{
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
```

效果如下图：

![]()

# 机器人指令回复embed消息

```
package main

import (
	"context"
	"encoding/json"
	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"
)

var channelId = ""

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

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	timer := cron.New()
	ws, err := api.WS(ctx, nil, "")
	log.Printf("%+v, err:%v", ws, err)
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
	}

	var activeMsgPush = func() {
		if channelId != "" {
			weatherData := getWeatherByCity("深圳")
			api.PostMessage(ctx, channelId, &dto.MessageToCreate{MsgID: "", Ark: createArkForTemplate23(weatherData)})
		}
	}

	timer.AddFunc("0 0 9 * * ?", activeMsgPush)//每天九点发送消息
	timer.Start()

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {

		channelId = data.ChannelID
		if strings.HasSuffix(data.Content, "> hello") {//发送embed消息
			var webData *WeatherResp = getWeatherByCity("深圳")
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Embed: createEmbed(webData)})
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
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
```


效果如下图

![]()

# 机器人私信

我们希望能提供不同用户不同地方的天气，但是发太多的消息会影响其它的用户。针对这种情况，我们可以通过私信来实现。下面代码中，当我们@机器人hello时收到机器人的私信。

```
package main

import (
	"context"
	"encoding/json"
	"github.com/robfig/cron"
	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/dto"
	"github.com/tencent-connect/botgo/token"
	"github.com/tencent-connect/botgo/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"
)

var channelId = ""

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

func main() {
	token := token.BotToken(你的appid, "你的token")
	api := botgo.NewOpenAPI(token).WithTimeout(3 * time.Second)
	ctx := context.Background()
	timer := cron.New()
	ws, err := api.WS(ctx, nil, "")
	log.Printf("%+v, err:%v", ws, err)
	if err != nil {
		log.Printf("%+v, err:%v", ws, err)
	}

	var activeMsgPush = func() {
		if channelId != "" {
			weatherData := getWeatherByCity("深圳")
			api.PostMessage(ctx, channelId, &dto.MessageToCreate{MsgID: "", Ark: createArkForTemplate23(weatherData)})
		}
	}

	timer.AddFunc("0 0 9 * * ?", activeMsgPush)//每天九点发送消息
	timer.Start()

	var atMessage websocket.ATMessageEventHandler = func(event *dto.WSPayload, data *dto.WSATMessageData) error {
		channelId = data.ChannelID
		if strings.HasSuffix(data.Content, "> hello") { //发送私信消息
			var webData *WeatherResp = getWeatherByCity("深圳")
			if webData != nil {
				directMsg, err := api.CreateDirectMessage(ctx, &dto.DirectMessageToCreate{
					SourceGuildID: data.GuildID,
					RecipientID:   data.Author.ID,
				})
				if err != nil {
					log.Println("私信创建出错了，err = ", err)
				}
				api.PostDirectMessage(ctx, directMsg, &dto.MessageToCreate{Embed: createEmbed(webData)})
			}
		}
		return nil
	}

	intent := websocket.RegisterHandlers(atMessage)     // 注册socket消息处理
	botgo.NewSessionManager().Start(ws, token, &intent) // 启动socket监听
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
```

效果图如下：

![]()

# 使用指令

每次@机器人输入指令太麻烦了，有没有简单的方式呢？机器人提供了指令配置，当你输入`/`时就会产出你配置的指令面板。配置方式如下：

![]()

![]()

配置好后，当我们输入`/`时，就可以看到配置的面板了

![]()

>需要注意，点击指令后输入的内容增加了一个`/`，上面的例子就变成了 `@天气机器人-测试中 /天气`

# 最佳实践

创建`config.yaml`文件保存配置信息，代码如下：

```
appid: 你的appid //注意要加空格
token: "你的token"
```

在`robot.go`文件中添加解析代码，同时增加了如下功能：

- 机器人通过天气api拉取默认城市（深圳）的天气，每天主动推送模版消息
- 机器人通过指令选择“深圳、上海、北京”时，被动推送模版消息
- 机器人通过指令选择“私信推送”时，被动推送私信的天气内嵌消息（建议改成注册需要推送消息）
- 机器人通过指令选择“全国天气小程序”，打开天气小程序

代码如下：

```
package main

import (
	"context"
	"encoding/json"
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

	CommandShenZhen          = "> /深圳"
	CommandShangHai          = "> /上海"
	CommandBeiJin            = "> /北京"
	CommandDirectChatMsg     = "> /私信推送"
	CommandWeatherProgrammer = "> /全国天气小程序"

	CityShenZhen = "深圳"
	CityShangHai = "上海"
	CityBeiJin   = "北京"
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
		log.Printf("%+v, err:%v", ws, err)
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
	if strings.HasSuffix(data.Content, CommandShenZhen) { //发送深圳的天气消息到频道
		var webData *WeatherResp = getWeatherByCity(CityShenZhen)
		if webData != nil {
			//MsgID 表示这条消息的触发来源，如果为空字符串表示主动消息
			//Ark 传入数据时表示发送的消息是Ark
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Embed: createEmbed(webData)})
		}
	} else if strings.HasSuffix(data.Content, CommandBeiJin) { //发送北京的天气消息到频道
		var webData *WeatherResp = getWeatherByCity(CityBeiJin)
		if webData != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	} else if strings.HasSuffix(data.Content, CommandShangHai) { //发送上海的天气消息到频道
		var webData *WeatherResp = getWeatherByCity(CityShangHai)
		if webData != nil {
			api.PostMessage(ctx, data.ChannelID, &dto.MessageToCreate{MsgID: data.ID, Ark: createArkForTemplate23(webData)})
		}
	} else if strings.HasSuffix(data.Content, CommandDirectChatMsg) { //私信深圳的天气消息到用户
		var webData *WeatherResp = getWeatherByCity(CityShenZhen)
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
	} else if strings.HasSuffix(data.Content, CommandWeatherProgrammer) {

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
		var webData *WeatherResp = getWeatherByCity(CityShenZhen)
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
			{
				Name:  "当前湿度：" + weather.ResultData.Humidity,
				Value: "https://bot.q.qq.com/wiki/develop/api/openapi/message/template/embed_message.html",
			},
			{
				Value: "test1",
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
	objectArray := make([]*dto.ArkObj, 7)
	objectArkArray := make([]*dto.ArkObjKV, 1)
	objectArkArray[0] = &dto.ArkObjKV{
		Key:   "desc",
		Value: weather.ResultData.Days + " " + weather.ResultData.Week,
	}
	objectArray = []*dto.ArkObj{
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
```

完整代码看 [天气机器人-Go实现版]()









