本示例演示被动消息使用方法

## demo运行步骤
- 1.申请[QQ机器人](https://bot.q.qq.com/#/home)，获取 `BotAppID`、`Bot Token`，按照`config.example.yaml`格式，创建`config.yaml`文件，并填入内容，格式参考：

```yaml
appid: 101988888
token: "O2AUl44m1mPu4jKVjAwpNtEpA2Qxxxxx"
```

- 2.配置机器人的语料：
    - 输入：hello
    - 回复：Hello World


- 3.执行
```sh
$ go mod tidy
$ go run .
```

- 4.频道内添加对应的机器人，并在子频道内at机器人，发送`hello`, 会收到机器人返回的`Hello World`

```
@机器人 hello
> Hello World
```
