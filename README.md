# 使い方
※Macの場合はターミナル、Windowsの場合はコマンドプロンプトで  
docker-compose.ymlがあるディレクトリをカレントディレクトリにしてください。 

## 前提条件
Dockerが使用可能

## 起動

```
docker-compose up -d --build
```

## 停止

```
docker-compose down --rmi all --volumes --remove-orphans
```
