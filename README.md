# 拉勾网爬虫(Scrapy版)

---

### 非Scrapy版本的在这 ---> [here](https://github.com/sunhailin-Leo/LaGou_nonScrapy)

* 使用中有问题的可以提个issue让我改进改进

---

<h3 id="Env">环境和安装方式</h3>

* 开发环境: Win10 x64
* Python版本: Python3.4.4
* Python依赖:
    * Scrapy
    * requests
    * pymongo
    * twisted
    * PyDispatcher

* 安装方式:

```Bash
pip install -r requirements.txt
```

---

<h3 id="GuideForUse">使用帮助及启动方法</h3>

* 启动的时候会有个Warning(可以忽略): ScrapyDeprecationWarning: Module `scrapy.conf` is deprecated, use `crawler.settings` attribute instead


```bash
# scrapy crawl LaGou -a search_name=大数据 --- 已经不用这种方法了

# 根目录下:
python start_spider.py -name 大数据
```

---

<h3 id="Bugs">已知的Bug</h3>

* ~~长时间爬取会进入假死状态~~ (已解决)

---

<h3 id="Future">未来进度</h3>

* ~~修改启动方式~~
* (优先) 增量的方法待完善
* (优先) 定时任务
* 进度监控
* 接入到Gerapy

---

<h3 id="Plus">补充</h3>

* 项目中的lagou_login代码来自 [拉勾网的模拟登录](https://github.com/laichilueng/lagou_login)