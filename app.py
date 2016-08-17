from flask import Flask,request,render_template,url_for,send_file
import hashlib
import requests
import xmltodict,json
import subprocess
import time
from PIL import Image
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

#PUT YOUR DOMAIN NAME or IP HERE
urlbase = 'http://'
#SET your token which has been specified in the wx panel
token = ''


def Isfromwx(request):
	global token
	signature = request.args.get('signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	echostr = request.args.get('echostr', '')
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

def gen_post(MediaId):
	post = Image.open('media/' + MediaId)
	(post_w, post_h) = post.size
	print('post size ' + str(post.size))
	if post_w/post_h > 1:
	        #only for landscape layout
		title = Image.open('layer_title.png')
		title_w = int(post_w * .7)
		title_h = int(title_w/title.size[0] * title.size[1])
		title = title.resize((title_w,title_h))
		post.paste(title, (int((post_w-title_w)/2),int(.45*post_h-title_h/2)), title)

		info = Image.open('layer_info.png')
		info_w = int(post_w * .56)
		info_h = int(info_w/info.size[0] * info.size[1])
		info = info.resize((info_w,info_h))
		post.paste(info, (int((post_w-info_w)/2),int(.95*post_h-info_h)), info)

		post.save('media/' + MediaId + '.jpg', quality=95)
		return True
	else:		
		#size not supported
		return False


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

			if MsgType == 'image':
				MediaId = d['xml']['MediaId']
				PicUrl = d['xml']['PicUrl']
				#only useful when you access media API
				#f = open('./access_token', 'r')
				#access_token = f.readline()
				#access_token = json.loads(access_token)['access_token']
				subprocess.call(['wget', PicUrl, '-O', 'media/' + MediaId])

				gen_status = gen_post(MediaId)
				if gen_status:
					result_url = urlbase + url_for('pic', MediaId=MediaId)
					msg = '你的专属海报已经生成好啦，请访问以下链接查看和保存： ' + result_url
					xml = xml_msg(FromUserName, msg, me)
					print(xml)
					return xml
				else:
					msg = '不好意思，目前仅支持横版的照片，请换一张试试呢！'
					xml = xml_msg(FromUserName, msg, me)
					return xml
			else:
				if MsgType == 'text':
					#save text msg from users
					with open('user_msg', 'a') as f:
						f.write(str(d)+'\n')
				msg = '8月活动出炉，这次有个新玩法，在这里给本公众号发一张图片（需要是横版的），会帮你生成一张你的专属海报哦！「本消息为自动发送」'
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
