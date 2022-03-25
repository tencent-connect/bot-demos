from typing import List
from qqbot.model.message import MessageArkObj, MessageArkObjKv


async def create_weather_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value=weather_dict['result']['citynm'] + " " + weather_dict['result']['weather'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当日温度区间：" + weather_dict['result']['temperature'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前温度：" + weather_dict['result']['temperature_curr'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前湿度：" + weather_dict['result']['humidity'])])]
    return obj_list


async def create_future_weather_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value=weather_dict['result'][0]['citynm'] + "未来三天天气预报")]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="明天：" + weather_dict['result'][1]['weather'] + ", " + weather_dict['result'][1]['temperature'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="后天：" + weather_dict['result'][2]['weather'] + ", " + weather_dict['result'][2]['temperature'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="外后天：" + weather_dict['result'][3]['weather'] + ", " + weather_dict['result'][3]['temperature'])])]
    return obj_list


async def create_clothes_ark_obj_list(life_index_dic) -> List[MessageArkObj]:
    obj_list = [
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + life_index_dic['result'][0]['citynm'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="体感：" + life_index_dic['result'][0]['lifeindex_ct_attr'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + life_index_dic['result'][0]['lifeindex_ct_dese'])])]
    return obj_list


async def create_uv_ark_obj_list(life_index_dic) -> List[MessageArkObj]:
    obj_list = [
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + life_index_dic['result'][0]['citynm'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="紫外线指数：" + life_index_dic['result'][0]['lifeindex_uv_attr'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + life_index_dic['result'][0]['lifeindex_uv_dese'])])]
    return obj_list


async def create_aqi_ark_obj_list(aqi_dict) -> List[MessageArkObj]:
    obj_list = [MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="城市：" + aqi_dict['result']['citynm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="空气质量：" + aqi_dict['result']['aqi_levnm'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="PM2.5：" + aqi_dict['result']['aqi_scope'])]),
                MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="建议：" + aqi_dict['result']['aqi_remark'])])]
    return obj_list
