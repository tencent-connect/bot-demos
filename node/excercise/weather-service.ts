import axios from 'axios';

// https://www.nowapi.com/api/weather.realtime
const sign = 'b59bc3ef6191eb9f747dd4e83c99f2a4';  // 临时 sign，可能会失效

interface IWeatherData {
    days: string;                  // 2022-03-03
    week: string;                  // 星期四
    citynm: string;                // 深圳
    temperature: string;           // 25C/18C 
    temperature_curr: string;      // 24C
    temp_high: string;             // 最高气温
    temp_low: string;              // 最低气温
    humidity: string;              // 59%
    weather: string;               // 多云
    weather_curr: string;          // 晴
    weather_icon: string;          // 地址
    wind: string;                  // 东风
}

interface ILifeIndexData {         // 生活指数
    days: string;                  // 日期，如2020-03-17
    week_1: string;                // 星期
    lifeindex_ct_typenm: string;   // 穿衣指数标签
    lifeindex_ct_attr: string;     // 穿衣指数
    lifeindex_ct_dese: string;     // 穿衣建议
}

interface IAQIData {                // 空气质量数据
	aqi_scope: string;              // AQI指数
	aqi_levid: string;              // AQI等级，1级、2级等
	aqi_levnm: string;              // AQI等级，优、良等
	aqi_remark: string;             // 注意事项
}

export class WeatherService {

    getWeatherByCity(city: string) {
        const url = `http://api.k780.com/?app=weather.today&cityNm=${encodeURI(city)}&appkey=10003&sign=${sign}&format=json`;
        return new Promise<IWeatherData>((resolve, reject) => {
            axios.get(url).then((response) => {
                const data = response.data;
                if (data.success === '1') {
                    resolve(data.result);
                } else {
                    console.error(data.msg);
                    reject(data.msg);
                }
            }).catch((err) => {
                console.log(err);
                reject(err);
            });
        });
    }

    getFutureWeatherByCity(city: string) {
        const url = `http://api.k780.com/?app=weather.future&cityNm=${encodeURI(city)}&appkey=10003&sign=${sign}&format=json`;
        return new Promise<IWeatherData[]>((resolve, reject) => {
            axios.get(url).then((response) => {
                const data = response.data;
                if (data.success === '1') {
                    resolve(data.result);
                } else {
                    console.error(data.msg);
                    reject(data.msg);
                }
            }).catch((err) => {
                console.log(err);
                reject(err);
            });
        });
    }

    getLifeIndexByCity(city: string) {
        const url = `http://api.k780.com/?app=weather.lifeindex&cityNm=${encodeURI(city)}&appkey=10003&sign=${sign}&format=json`;
        return new Promise<ILifeIndexData[]>((resolve, reject) => {
            axios.get(url).then((response) => {
                const data = response.data;
                if (data.success === '1') {
                    resolve(data.result);
                } else {
                    console.error(data.msg);
                    reject(data.msg);
                }
            }).catch((err) => {
                console.log(err);
                reject(err);
            });
        });
    }

    //获取城市的空气质量
    getAQIByCity(city: string) {
        const url = `http://api.k780.com/?app=weather.pm25&cityNm=${encodeURI(city)}&appkey=10003&sign=${sign}&format=json`;
        return new Promise<IAQIData>((resolve, reject) => {
            axios.get(url).then((response) => {
                const data = response.data;
                if (data.success === '1') {
                    resolve(data.result);
                } else {
                    console.error(data.msg);
                    reject(data.msg);
                }
            }).catch((err) => {
                console.log(err);
                reject(err);
            });
        });
    }

}
