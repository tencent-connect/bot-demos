import axios from 'axios';

// https://www.nowapi.com/api/weather.realtime
const host = 'http://api.k780.com/';
const sign = 'b59bc3ef6191eb9f747dd4e83c99f2a4';  // 临时 sign，可能会失效
const appkey = '10003';

interface IWeatherData {
    days: string;                  // 2022-03-03
    week: string;                  // 星期四
    citynm: string;                // 深圳
    temperature: string;           // 25C/18C 
    temperature_curr: string;      // 24C
    humidity: string;              // 59%
    weather: string;               // 多云
    weather_curr: string;          // 晴
    weather_icon: string;          // 地址
    wind: string;                  // 东风
}

export class WeatherService {

    cityMap: { [key: string]: string } = {}; // 城市映射天气id { cityName: weatherId }

    constructor() {
        this.initCityMap();
    }

    initCityMap() {
        axios.get(host, {
            params: {
                app: 'weather.city',
                areaType: 'cn',
                appkey: appkey,
                sigƒn: sign,
                format: 'json',
            },
        }).then((response) => {
            const data = response.data;
            if (data.success === '1') {
                const list = data.result.dtList;
                Object.keys(list).forEach((key) => {
                    const item = list[key];
                    this.cityMap[item.cityNm] = item.weaId;
                });
            } else {
                console.error(data.msg);
            }
        }).catch((err) => {
            console.log(err);
        });
    }

    getWeatherID(city: string) {
        return this.cityMap[city];
    }

    getWeatherData(city: string) {
        return new Promise<IWeatherData>((resolve, reject) => {
            const weatherID = this.getWeatherID(city);
            if (!weatherID) {
                console.error('未找到weatherID');
            }
            axios.get(host, {
                params: {
                    app: 'weather.today',
                    weaId: weatherID,
                    appkey: appkey,
                    sign: sign,
                    format: 'json',
                },
            }).then((response) => {
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
