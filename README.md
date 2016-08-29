# wx-post-generator
微信公众号服务，根据用户发来的照片自动生成海报


基于flask，用python3写的，依赖：
xmltodict, requests, PIL (python imaging library)


#部署方法：

- 先在微信公众号后台配置好开发者相关参数，用wx_verify.py这个脚本验证一下服务器即可绑定。
- postgen.py是用于生成海报的，模板是layer_title.png和layer_info.png两个文件，实际使用请自行准备，可以在post_gen这个函数里设定调整图层放置的位置。
- livepic.py是用于生成现场lomo风格纪念照片的，模板是layer_l.png, layer_p.png, layer_s.png三个文件，分别为横版、竖版、正方形。
- postgen.py和livepic,py其实大量代码是重复的，我只是没整合在一起，实际使用根据需求选择运行一个即可，然后根据之前微信后台的设置把代码里面的urlbase和token填好。
- 可以配合gunicorn和nginx部署，具体方法参看flask官方文档的部署部分。
