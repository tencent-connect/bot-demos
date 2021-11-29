
## 主动推送消息demo运行步骤
- 1.申请[QQ机器人](https://bot.q.qq.com/#/home)，获取 `BotAppID`、`Bot Token`，按照`config.example.yaml`格式，创建`config.yaml`文件，并填入内容，格式参考：

```yaml
appid: 101984888
token: "O2AUl44m1mPu4jKVjAwpNtEpA2QWXXXX"
```


- 2.执行
```sh
$ go mod tidy
$ go run .
```

- 3.频道内添加对应的机器人，在运行此程序后 会收到天气预报推送 示意：

```
 机器人小天：
【主动消息示例】天气预报：2021-11-28 星期日, 北京, 天气：阴, 东北风 1级
```
