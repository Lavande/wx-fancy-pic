from flask import Flask,request,render_template,url_for,send_file
import hashlib
import requests
import xmltodict,json
import subprocess
import time
from PIL import Image,ImageEnhance,ImageColor
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

urlbase = 'http://115.159.206.102'


def Isfromwx(request):
	signature = request.args.get('signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	echostr = request.args.get('echostr', '')
	token = 'r45g46h5n8kyfujf56thdj67k578kh'
	L = [token, timestamp, nonce]
	L.sort()
	s = L[0] + L[1] + L[2]
	s = s.encode('utf8')
	if hashlib.sha1(s).hexdigest() == signature:
		return True
	else:
		return False

def xml_msg(user, msg, fromuser):
	template = '''
<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{3}]]></FromUserName>
<CreateTime>{1}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''
	return template.format(user, int(time.time()), msg, fromuser)

def lomoize (image,darkness,saturation):
	
	(width,height) = image.size

	max = width
	if height > width:
		max = height
	
	mask = Image.open("lomomask.jpg").resize((max,max))

	left = round((max - width) / 2)
	upper = round((max - height) / 2)
	
	mask = mask.crop((left,upper,left+width,upper + height))

	darker = ImageEnhance.Brightness(image).enhance(darkness)	
	saturated = ImageEnhance.Color(image).enhance(saturation)
	lomoized = Image.composite(saturated,darker,mask)
	
	return lomoized

def gen_pic(MediaId):
	pic = Image.open('media/' + MediaId).convert('LA')
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

		layer = Image.open('layer_p.png')

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

		layer = Image.open('layer_l.png')

	elif portion == 1:
		#square
		(pic_w,pic_h) = (960,960)
		box = (0,0,960,960)
		layer = Image.open('layer_s.png')

	pic = pic.resize((pic_w, pic_h))
	pic = pic.crop(box)
	pic = lomoize(pic, 0.5, 1)
	pic = pic.convert('RGB')
	pic.paste(layer,(0,0),layer)

	pic.save('media/' + MediaId + '.jpg', quality=95)


@app.route('/', methods=['POST', 'GET'])
def get_msg():
	if Isfromwx(request):
		if request.method == 'POST':
			d = request.data
			d = str(d, 'utf-8')
			d = xmltodict.parse(d)
			FromUserName = d['xml']['FromUserName']
			MsgType = d['xml']['MsgType']
			me = d['xml']['ToUserName']
			#print(str(d))

			if MsgType == 'image':
				MediaId = d['xml']['MediaId']
				PicUrl = d['xml']['PicUrl']
				#f = open('./access_token', 'r')
				#token = f.readline()
				#token = json.loads(token)['access_token']
				subprocess.call(['wget', PicUrl, '-O', 'media/' + MediaId])

				gen_pic(MediaId)
				result_url = urlbase + url_for('pic', MediaId=MediaId)
				msg = '你的现场纪念照片已经生成好啦，请访问以下链接查看和保存： ' + result_url
				xml = xml_msg(FromUserName, msg, me)
				print(xml)
				return xml

			else:
				if MsgType == 'text':
					#save msg
					with open('user_msg', 'a') as f:
						f.write(str(d)+'\n')
				msg = '嗨！欢迎来玩儿，活动正在进行中！你可以在这里向本公众号发送你拍摄的现场照片，我们会自动生成一张印有“草地音乐·我在现场”的LOMO风格纪念照片～「本消息为自动发送」'
				xml = xml_msg(FromUserName, msg, me)
				return xml

	if request.method == 'GET':
		return 'nothing'

@app.route('/pic/<MediaId>')
def pic(MediaId):
	mediaurl = url_for('media', filename=MediaId+'.jpg')
	return render_template('pic.html', pic_path=mediaurl)

@app.route('/media/<filename>')
def media(filename):
	path = 'media/' + filename
	return send_file(path)
