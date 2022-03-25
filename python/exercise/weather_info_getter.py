import json
from typing import Dict

import aiohttp


async def get_weather(city_name: str) -> Dict:
    """
    获取天气信息

    :return: 返回天气数据的json对象
    返回示例
    {
    "success":"1",
    "result":{
        "weaid":"1",
        "days":"2022-03-04",
        "week":"星期五",
        "cityno":"beijing",
        "citynm":"北京",
        "cityid":"101010100",
        "temperature":"13℃/-1℃",
        "temperature_curr":"10℃",
        "humidity":"17%",
        "aqi":"98",
        "weather":"扬沙转晴",
        "weather_curr":"扬沙",
        "weather_icon":"http://api.k780.com/upload/weather/d/30.gif",
        "weather_icon1":"",
        "wind":"西北风",
        "winp":"4级",
        "temp_high":"13",
        "temp_low":"-1",
        "temp_curr":"10",
        "humi_high":"0",
        "humi_low":"0",
        "weatid":"31",
        "weatid1":"",
        "windid":"7",
        "winpid":"4",
        "weather_iconid":"30"
        }
    }
    """
    weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_future_weather(city_name: str) -> Dict:
    """
    获取未来几天的天气信息

    :return: 返回天气数据的json对象
    返回示例(返回值过长,部分省略)
    {
        "success": "1",
        "result": [{
            "weaid": "1",
            "days": "2014-07-30",
            "week": "星期三",
            "cityno": "beijing",
            "citynm": "北京",
            "cityid": "101010100",
            "temperature": "23℃/11℃", /*温度*/
            "humidity": "0%/0%", /*湿度,后期气像局未提供,如有需要可使用weather.today接口 */
            "weather": "多云转晴",
            "weather_icon": "http://api.k780.com/upload/weather/d/1.gif", /*气象图标(白天) 全部气象图标下载*/
            "weather_icon1": "http://api.k780.com/upload/weather/d/0.gif", /*气象图标(夜间) 全部气象图标下载*/
            "wind": "微风", /*风向*/
            "winp": "小于3级", /*风力*/
            "temp_high": "31", /*最高温度*/
            "temp_low": "24", /*最低温度*/
            "humi_high": "0", /*湿度栏位已不再更新*/
            "humi_low": "0",/*湿度栏位已不再更新*/
            "weatid": "2", /*白天天气ID，可对照weather.wtype接口中weaid*/
            "weatid1": "1", /*夜间天气ID，可对照weather.wtype接口中weaid*/
            "windid": "1", /*风向ID(暂无对照表)*/
            "winpid": "2" /*风力ID(暂无对照表)*/
            "weather_iconid": "1", /*气象图标编号(白天),对应weather_icon 1.gif*/
            "weather_iconid1": "0" /*气象图标编号(夜间),对应weather_icon1 0.gif*/
        },
    ......
    """
    weather_api_url = "http://api.k780.com/?app=weather.future&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_weather_life_index(citi_name: str) -> Dict:
    """
    获取生活指数

    :return: 返回天气数据的json对象
    返回示例
    {
    success: "1",
    result: {
        2017-04-17: {
            weaid: "1",
            days: "2017-04-17",
            week_1: "星期一",
            simcode: "beijing",
            citynm: "北京",
            cityid: "101010100",
            lifeindex_uv_id: "101",
            lifeindex_uv_typeno: "uv",
            lifeindex_uv_typenm: "紫外线指数",
            lifeindex_uv_attr: "弱",
            lifeindex_uv_dese: "辐射较弱，涂擦SPF12-15、PA+护肤品。",
            lifeindex_gm_id: "111",
            lifeindex_gm_typeno: "gm",
            lifeindex_gm_typenm: "感冒指数",
            lifeindex_gm_attr: "少发",
            lifeindex_gm_dese: "无明显降温，感冒机率较低。",
            lifeindex_ct_id: "108",
            lifeindex_ct_typeno: "ct",
            lifeindex_ct_typenm: "穿衣指数",
            lifeindex_ct_attr: "较舒适",
            lifeindex_ct_dese: "建议穿薄外套或牛仔裤等服装。",
            lifeindex_xc_id: "112",
            lifeindex_xc_typeno: "xc",
            lifeindex_xc_typenm: "洗车指数",
            lifeindex_xc_attr: "较适宜",
            lifeindex_xc_dese: "无雨且风力较小，易保持清洁度。",
            lifeindex_yd_id: "114",
            lifeindex_yd_typeno: "yd",
            lifeindex_yd_typenm: "运动指数",
            lifeindex_yd_attr: "较适宜",
            lifeindex_yd_dese: "风力稍强，推荐您进行室内运动。",
            lifeindex_kq_id: "109",
            lifeindex_kq_typeno: "kq",
            lifeindex_kq_typenm: "空气污染扩散指数",
            lifeindex_kq_attr: "良",
            lifeindex_kq_dese: "气象条件有利于空气污染物扩散。"
        },
    ...
    """
    weather_api_url = "http://api.k780.com/?app=weather.lifeindex&cityNm=" + citi_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=weather_api_url,
            timeout=5
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


async def get_aqi(citi_name: str) -> Dict:
    """
    获取空气质量（aqi）数据

    :return: 返回空气质量数据的json对象
    返回示例
    {
    success: "1",
    result: {
        "success": "1",
        "result": {
        "weaid": "180",
        "cityno": "gdzhongshan",
        "citynm": "中山",
        "cityid": "101281701",
        "aqi": "18",
        "aqi_scope": "0-50",
        "aqi_levid": "1",
        "aqi_levnm": "优",
        "aqi_remark": "参加户外活动呼吸清新空气"
    }
    """
    weather_api_url = "http://api.k780.com/?app=weather.pm25&cityNm=" + citi_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=weather_api_url,
            timeout=5
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj
