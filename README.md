

## Getting Started

Get set up locally in three steps:

### I. Environment Variables

Replace the values in **.env.example** with your values and rename this file to **.env**:

* `FLASK_APP`: Entry point of your application (should be `run.py`).
* `FLASK_ENV`: The environment to run your app in (either `development` or `production`).
* `SECRET_KEY`: Randomly generated string of characters used to encrypt your app's data.
* `SQLALCHEMY_DATABASE_URI`: Connection URI of a SQL database.
* `TIMEZONE`: Local time zone.
* `ANTMEDIA_URI`: Antmedia URI.
* `ANTMEDIA_USER`: Antmedia user.
* `ANTMEDIA_PASSWORD`: Antmedia password.
* `CELERY_BROKER_URL`: Celery broker URL used to store queue data.
* `TELEGRAM_BOT_CHAT_API_URL`: Telegram bot chat url to push alerting.
* `TELEGRAM_BOT_TOKEN`: Telegram bot token.
* `TELEGRAM_BOT_CHATID`:  Telegram bot chat id.
* `TELEGRAM_TAG`: Telegram tag.

example:

```shell
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=yoursecretkey
DB_ENGINE=mysql
DB_USERNAME=root
DB_PASS=example
DB_HOST=103.143.207.30
DB_PORT=3306
DB_NAME=headend
TIMEZONE=Asia/Ho_Chi_Minh
ANTMEDIA_URI=http://103.171.92.145:5080
ANTMEDIA_USER=evglive
ANTMEDIA_PASSWORD=a3692eb7a85cf072d85309370f1c2f6c
# CELERY_BROKER_URL=amqp://admin:admin@103.143.207.30:5672
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_EVENT_WORKERS=event_handle_worker_1,event_handle_worker_2,event_handle_worker_3
TELEGRAM_BOT_CHAT_API_URL=https://api.telegram.org/bot1812784603:AAEHvW3c9frw8ae7K5e5ZWAYxIY7ZctHJzM/sendMessage
TELEGRAM_BOT_TOKEN=1812784603:AAEHvW3c9frw8ae7K5e5ZWAYxIY7ZctHJzM
TELEGRAM_BOT_CHATID=-586472083
TELEGRAM_TAG=DEV-HEADEND-CONTROLLER-ANTMEDIA
```
### II. Installation

```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

Get up and running with `make deploy`:

```shell
$ git clone https://github.com/imt/headend.git
$ cd headend
$ make install
``` 



### III. Run in development

Running API with `make run`:

```shell
(.venv)$ make run
```

Install RabbitMQ docker:

```shell
docker run -d -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq:3-management
```

If You want to Redis:

```shell
docker run -p 6379:6379 -d redis
```

Running scheduler jobs with Celery:

```shell
celery -A run.celery beat
celery -A run.celery worker --loglevel=info
```

### IV> AntMedia mp4 files


```shell
-rw-r--r-- 1 root root 10223664 Jun 12 12:29 jTXNUFmxtfeW1655036890355-2022-06-12_12-29-03.431.mp4.tmp_extension
-rw-r--r-- 1 root root  2359344 Jun 12 12:29 jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.312_720p1500kbps.mp4.tmp_extension
-rw-r--r-- 1 root root  3932208 Jun 12 12:29 jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.314_1080p2000kbps.mp4.tmp_extension
-rw-r--r-- 1 root root      229 Jun 12 12:29 jTXNUFmxtfeW1655036890355.m3u8
-rw-r--r-- 1 root root  2862300 Jun 12 12:29 jTXNUFmxtfeW1655036890355_0000.ts
-rw-r--r-- 1 root root  2899336 Jun 12 12:29 jTXNUFmxtfeW1655036890355_0001.ts
-rw-r--r-- 1 root root  2900276 Jun 12 12:29 jTXNUFmxtfeW1655036890355_0002.ts
-rw-r--r-- 1 root root      528 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps.m3u8
-rw-r--r-- 1 root root   801632 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0000.ts
-rw-r--r-- 1 root root   667024 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0001.ts
-rw-r--r-- 1 root root   668716 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0002.ts
-rw-r--r-- 1 root root   673980 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0003.ts
-rw-r--r-- 1 root root   674168 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0004.ts
-rw-r--r-- 1 root root   566444 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0005.ts
-rw-r--r-- 1 root root   181608 Jun 12 12:29 jTXNUFmxtfeW1655036890355_1080p2000kbps0006.ts
-rw-r--r-- 1 root root      521 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps.m3u8
-rw-r--r-- 1 root root   460788 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0000.ts
-rw-r--r-- 1 root root   440296 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0001.ts
-rw-r--r-- 1 root root    66552 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0002.ts
-rw-r--r-- 1 root root   409652 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0003.ts
-rw-r--r-- 1 root root   400816 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0004.ts
-rw-r--r-- 1 root root    60160 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0005.ts
-rw-r--r-- 1 root root   413412 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0006.ts
-rw-r--r-- 1 root root   328812 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0007.ts
-rw-r--r-- 1 root root    12220 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0008.ts
-rw-r--r-- 1 root root   104716 Jun 12 12:29 jTXNUFmxtfeW1655036890355_720p1500kbps0009.ts
-rw-r--r-- 1 root root      428 Jun 12 12:29 jTXNUFmxtfeW1655036890355_adaptive.m3u8
```

__Hook scripts when mp4 recording finished__

```shell
2022-06-12 12:29:49,179 [vert.x-worker-thread-2] INFO  io.antmedia.muxer.RecordMuxer - File: /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.314_1080p2000kbps.mp4.tmp_extension exist: false
2022-06-12 12:29:49,179 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - running muxer finish script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-03.431.mp4
2022-06-12 12:29:49,191 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - completing script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-03.431.mp4 with return value 0
2022-06-12 12:29:49,191 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - running muxer finish script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.312_720p1500kbps.mp4
2022-06-12 12:29:49,195 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - completing script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.312_720p1500kbps.mp4 with return value 0
2022-06-12 12:29:49,195 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - running muxer finish script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.314_1080p2000kbps.mp4
2022-06-12 12:29:49,207 [vert.x-worker-thread-2] INFO  i.a.AntMediaApplicationAdapter - completing script: /opt/ams_app_finished.sh  /usr/local/antmedia/webapps/NewAPP2022106/streams/jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.314_1080p2000kbps.mp4 with return value 0
2022-06-12 12:29:49,391 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - POST Response Status:: 200
2022-06-12 12:29:49,392 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - Running notify hook url:https://api-dev-headend.ekycglobal.com/api/v1/webhook-stream-event?api_key=yoursecretkey stream id: jTXNUFmxtfeW1655036890355 action:liveStreamEnded vod name:null vod id:null
2022-06-12 12:29:49,460 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - POST Response Status:: 200
2022-06-12 12:29:49,460 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - Running notify hook url:https://api-dev-headend.ekycglobal.com/api/v1/webhook-stream-event?api_key=yoursecretkey stream id: jTXNUFmxtfeW1655036890355 action:vodReady vod name:jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.312_720p1500kbps vod id:213033878005290164804390
2022-06-12 12:29:49,533 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - POST Response Status:: 200
2022-06-12 12:29:49,533 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - Running notify hook url:https://api-dev-headend.ekycglobal.com/api/v1/webhook-stream-event?api_key=yoursecretkey stream id: jTXNUFmxtfeW1655036890355 action:vodReady vod name:jTXNUFmxtfeW1655036890355-2022-06-12_12-29-04.314_1080p2000kbps vod id:374959214356542068571049
2022-06-12 12:29:49,601 [vert.x-eventloop-thread-6] INFO  i.a.AntMediaApplicationAdapter - POST Response Status:: 200
```

Pipeline event: mp4 recording finished => running muxer finish script => Running notify hook url.



