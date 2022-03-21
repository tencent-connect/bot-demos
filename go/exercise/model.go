package main

//Config 定义了配置文件的结构
type Config struct {
	AppID uint64 `yaml:"appid"` //机器人的appid
	Token string `yaml:"token"` //机器人的token
}

//WeatherResp 定义了返回当前天气数据的结构
type WeatherResp struct {
	Success    string `json:"success"` //标识请求是否成功，1表示成功，0表示失败
	ResultData Result `json:"result"`  //请求成功时，获取的数据
	Msg        string `json:"msg"`     //请求失败时，失败的原因
}

//FutureWeatherResp 定义了返回未来天气情况的结构
type FutureWeatherResp struct {
	Success     string    `json:"success"` //标识请求是否成功，1表示成功，0表示失败
	ResultDatas []*Result `json:"result"`  //请求成功时，获取的数据
	Msg         string    `json:"msg"`     //请求失败时，失败的原因
}

//AQIRsp 返回的空气质量的数据结构
type AQIRsp struct {
	Success   string    `json:"success"` //标识请求是否成功，1表示成功，0表示失败
	AQIResult AQIResult `json:"result"`  //请求成功时，获取的数据
}

//LifeIndexRsp 生活指数返回数据
type LifeIndexRsp struct {
	Success string             `json:"success"` //标识请求是否成功，1表示成功，0表示失败
	Result  []*LifeIndexResult `json:"result"`  //请求成功时，获取的数据
}

//LifeIndexResult 生活指数的数据，这里只用到了穿衣指数
type LifeIndexResult struct {
	Days           string `json:"days"`                //日期，如2020-03-17
	Week           string `json:"week_1"`              //星期
	ClothIndex     string `json:"lifeindex_ct_typenm"` //穿衣指数标签
	ClothAttr      string `json:"lifeindex_ct_attr"`   //穿衣指数
	ClothRecommend string `json:"lifeindex_ct_dese"`   //穿衣建议
}

//AQIResult 空气质量数据
type AQIResult struct {
	AqiScore  string `json:"aqi_score"`  //AQI指数
	AqiLevid  string `json:"aqi_levid"`  //AQI等级，1级、2级等
	AqiLevnm  string `json:"aqi_levnm"`  //AQI等级，优、良等
	AqiRemark string `json:"aqi_remark"` //注意事项
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
