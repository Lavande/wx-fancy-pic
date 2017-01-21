from PIL import Image, ImageEnhance


ok_msg = '你的现场纪念照片已经生成好啦，请访问以下链接查看和保存： '
auto_reply = '嗨！欢迎来玩儿，活动正在进行中！你可以在这里向本公众号发送你拍摄的现场照片，我们会自动生成一张印有“草地音乐·我在现场”的LOMO风格纪念照片～「本消息为自动发送」'

def lomoize (image,darkness,saturation):
	
	(width,height) = image.size

	max = width
	if height > width:
		max = height
	
	mask = Image.open("./lomolive/lomomask.jpg").resize((max,max))

	left = round((max - width) / 2)
	upper = round((max - height) / 2)
	
	mask = mask.crop((left,upper,left+width,upper + height))

#	mask = Image.open('mask_l.png')

	darker = ImageEnhance.Brightness(image).enhance(darkness)	
	saturated = ImageEnhance.Color(image).enhance(saturation)
	lomoized = Image.composite(saturated,darker,mask)
	
	return lomoized

def gen_pic(MediaId):
	pic = Image.open('media/' + MediaId).convert('LA')
#	pic = ImageEnhance.Brightness(pic).enhance(0.35)
	portion = pic.size[0]/pic.size[1]

	if portion < 1:
		#portrait
		if portion <= 0.75:
			pic_w = 960
			pic_h = round(960/portion)
			box = (0,round((pic_h-1280)/2),960,round(pic_h/2+640))

		if portion > 0.75:
			pic_h = 1280
			pic_w = round(1280*portion)
			box = (round((pic_w-960)/2),0,round(pic_w/2+480),1280)

		layer = Image.open('./lomolive/layer_p.png')

	elif portion > 1:
		#landscape
		if portion >= 1.3333:
			pic_h = 960
			pic_w = round(960*portion)
			box = (round((pic_w-1280)/2),0,round(pic_w/2+640),960)

		if portion < 1.3333:
			pic_w = 1280
			pic_h = round(1280/portion)
			box = (0,round((pic_h-960)/2),1280,round(pic_h/2+480))

		layer = Image.open('./lomolive/layer_l.png')

	elif portion == 1:
		#square
		(pic_w,pic_h) = (960,960)
		box = (0,0,960,960)
		layer = Image.open('./lomolive/layer_s.png')

	pic = pic.resize((pic_w, pic_h))
	pic = pic.crop(box)
	pic = lomoize(pic, 0.4, 1)
	pic = pic.convert('RGB')
	pic.paste(layer,(0,0),layer)

	pic.save('media/' + MediaId + '.jpg', quality=95)
