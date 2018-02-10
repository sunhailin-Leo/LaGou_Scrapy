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

* 安装方式:

```Bash
pip install -r requirements.txt
```

---

<h3 id="GuideForUse">使用帮助</h3>

* -a 接的是参数名（之后会修改启动方式）

```bash
# 根目录下
scrapy crawl LaGou -a search_name=大数据
```

---

<h3 id="Future">未来进度</h3>

* 修改启动方式
* 进度监控
* 接入到Gerapy

---

<h3 id="Plus">补充</h3>

* 项目中的lagou_login代码来自 [拉勾网的模拟登录](https://github.com/laichilueng/lagou_login)