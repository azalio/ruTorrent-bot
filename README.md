# ruTorrent-bot
Telegram bot for adding magnet link to ruTorrent server

Как использовать:
1. Вам нужна машина, которая позволит вам запускать докер.
2. Вам нужен работающий инстанс ruTorrent + rtorrent
Я взял отсюда:
https://github.com/kfei/docktorrent
И запускаю его так:
```commandline
docker run -t \
    -p 31337:80 -p 45566:45566 -p 9527:9527/udp \
    --dns 8.8.8.8 \
    -v [абсолютный путь до папки на хосте]:/rtorrent \
    -e UPLOAD_RATE=1024 \
    -e IP=[ваш внешний IP] \
    --restart always
    docktorrent
```
предварительно собрав его.
При сборке **docktorrent** имеет смысл поменять в **Dockerfile**
логин и пароль доступа к веб-морде ruTorrent.
```commandline
vim Dockerfile
docker build -t docktorrent .
```
После запуска контейнера вы уже можете скачивать торренты.
3. Если вам хочется использовать телеграм-бота для закачки
торрента, то надо:
  * получить токен для своего бота у 
  [BotFather](https://telegram.me/BotFather)
  * склонировать этот репозиторий
  * отредактировать файл `botToken.py_EXAMPLE` и 
  вставить туда этот токен.
  * переименовать его в `botToken.py`
  * собрать контейнер:
  `docker build -t rutorrent-bot .`
  * запустить его:
  ```commandline
docker run --detach \
    --restart always \
    --volume rutorrent_user_info:/usr/src/app/chat_id_file \
    rutorrent-bot
```
  * После этого вы можете настроить бота в телеграме
  следуя инструкции.