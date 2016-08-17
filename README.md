# wx-post-generator
微信公众号服务，根据用户发来的照片自动生成海报


基于flask，用python3写的，依赖：
xmltodict, requests, PIL (python imaging library)


#部署方法：

- 先在微信公众号后台配置好开发者相关参数，用wx_verify.py这个脚本验证一下服务器即可绑定。
- 然后根据之前的设置把app.py里的urlbase和token填好。
- layer_title.png和layer_info.png两个文件是海报上的标题和信息对应的图层，自行准备，可以在post_gen这个函数里设定图层放置的位置。
- 可以配合gunicorn和nginx部署，具体方法参看flask官方文档的部署部分。
