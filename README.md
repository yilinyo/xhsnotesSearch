## 简单的 小红书📕 关键词 搜索笔记 Python爬虫小程序 



##### 	✨爬取过程

​	**微信小程序版小红书接口查询 笔记id列表 --> 通过笔记id列表 web 爬取笔记内容（可获取标题、内容、图片视频地址、点赞、转发评论数、笔记所属用户信息等）-->选择保存 笔记链接 ，标题，内容到CSV文件**

##### 	✨使用须知

1. 需要对电脑微信 小红书小程序抓包 获取 Authorization 值，微信3.6.018 版本比较适合抓包可以直接抓到，新版本微信不太容易抓建议使用我提供的 微信版本 抓包。
2. 支持关键词检索 并 保存到当前 目录 的csv文件，文件名默认检索名。
3. 在Windows 环境测试下 发现小红书会对短期 请求页面 做限制，所以程序不保证爬取到所有检索到笔记的内容，但能保证获取所有检索到的笔记id号，可自行配置 ip池或更换设备或时间爬取。
4. 需要引入的Python 包

```python
import csv
import hashlib
from urllib import parse
import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
```

5. 运行数据说明

```

if __name__ == "__main__":
# 参数
# 检索关键字
keyName = "Python爬虫"
# 微信小程序 小红书header 认证头 小程序自行 抓包Authorization ，是一串 wxmp.xxxxxxxx的数据
authorization = ""
# 排序方式可选  general：综合排序 (默认)，或hot_desc：热度排序
sortedWay = "general"

# 执行函数

idList = getlistByName(keyName, authorization, sortedWay)

toCsv(getInfo(idList), keyName)
```

##### ✨效果

![image-20230413173426590](https://yilin-1307688338.cos.ap-nanjing.myqcloud.com/blog/image-20230413173426590.png)



![image-20230413173525235](https://yilin-1307688338.cos.ap-nanjing.myqcloud.com/blog/image-20230413173525235.png)

##### ✨参考

[lighthookyu/xhs-mini-spider: 小红书小程序版本爬虫 (github.com)](https://github.com/lighthookyu/xhs-mini-spider)
