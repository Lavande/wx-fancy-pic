# wx-fancy-pic
微信公众号服务，根据用户发来的照片自动生成海报或有趣的照片

基于flask，用python3写的，依赖：
xmltodict, requests, PIL (python imaging library), cv2, numpy

目前支持两种风格的照片生成（见example文件夹里的效果图）：
- lomo现场风格
- 圣诞节风格，通过人脸识别带上圣诞帽，并加上相框

#部署方法：

- 先在微信公众号后台配置好开发者相关参数，主要是服务器的url还有token这两项，在wxverify.py这个脚本里填入你的token，然后验证一下服务器即可绑定，这个步骤只需要一次。
- wxfancypic.py这个文件是主程序，需要在代码开始填写你的服务器url和token才能正常使用，gen_mode有两个选项：'lomolive'和'xmas'，一个是生成lomo现场风格图片，一个是生成圣诞节风格图片。
- lomolive.py和xmas.py是生成图片的主要逻辑，对应lomo现场风格和圣诞节风格，无需改动，wxfancypic.py会根据你的设置自动去调用。
- lomolive和xmas两个文件夹里是生成图片需要的素材，xmas里有个人脸识别的文件，需要cv2这个库来实现。
- 可以配合gunicorn和nginx部署，具体方法参看flask官方文档的部署部分。
