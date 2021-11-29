本示例演示被动消息使用方法

## demo运行步骤

- 1.配置机器人的语料：
    - 输入：hello
    - 回复：Hello World


- 2.执行
```sh
$ go mod tidy
$ go run .
```

- 3.频道内添加对应的机器人，并在子频道内at机器人，发送`hello`, 会收到机器人返回的`Hello World`

```
@机器人 hello
> Hello World
```
