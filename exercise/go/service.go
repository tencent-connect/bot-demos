package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
)

//获取当前对应城市的天气数据
func getNowWeatherByCity(cityName string) *WeatherResp {
	url := "http://api.k780.com/?app=weather.today&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	body := getNetworkData(url)
	if body == nil {
		return nil
	}
	var weatherData WeatherResp
	err := json.Unmarshal(body, &weatherData)
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

//获取城市未来几天的天气信息
func getFutureWeatherByCity(cityName string) *FutureWeatherResp {
	url := "http://api.k780.com/?app=weather.future&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	body := getNetworkData(url)
	if body == nil {
		return nil
	}
	var weather FutureWeatherResp
	err := json.Unmarshal(body, &weather)
	if err != nil {
		log.Fatalln("解析数据异常 err = ", err, body)
		return nil
	}
	if weather.Success != "1" {
		log.Fatalln("返回数据问题 err = ", weather.Msg)
		return nil
	}
	return &weather
}

//获取城市的空气质量
func getAQIByCity(cityName string) *AQIRsp {
	url := "http://api.k780.com/?app=weather.pm25&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	body := getNetworkData(url)
	if body == nil {
		return nil
	}
	var weather AQIRsp
	err := json.Unmarshal(body, &weather)
	if err != nil {
		log.Fatalln("解析数据异常 err = ", err, body)
		return nil
	}
	if weather.Success != "1" {
		log.Fatalln("返回数据问题")
		return nil
	}
	return &weather
}

//获取穿衣指数的信息
func getClothIndexByCity(cityName string) *LifeIndexRsp {
	url := "http://api.k780.com/?app=weather.lifeindex&cityNm=" + cityName + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
	body := getNetworkData(url)
	if body == nil {
		return nil
	}
	var weather LifeIndexRsp
	err := json.Unmarshal(body, &weather)
	if err != nil {
		log.Fatalln("解析数据异常 err = ", err, body)
		return nil
	}
	if weather.Success != "1" {
		log.Fatalln("返回数据问题")
		return nil
	}
	return &weather
}

//获取网络请求的数据
func getNetworkData(url string) []byte {
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
	return body
}
