# wx-post-generator
微信公众号服务，根据用户发来的照片自动生成海报

>基于flask，可以配合gunicorn和nginx部署。
>
>先在微信公众号后台配置好开发者相关参数，然后把app.py里的urlbase和token填好。
>
>layer_title.png和layer_info.png两个文件是海报上的标题和信息对应的图层，自行准备，可以在post_gen这个函数里设定图层放置的位置。
