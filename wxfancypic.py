from flask import Flask,request,render_template,url_for,send_file
from werkzeug.contrib.fixers import ProxyFix
import hashlib
import xmltodict
import subprocess
import time


##BASIC SETTINGS##
#set the server's url here
urlbase = 'http://'
#set your token here
token = ''
#currently 2 options: xmas and lomolive (as in xmas.py and lomolive.py)
gen_mode = 'xmas'


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


if gen_mode == 'xmas':
	import xmas
	ok_msg = xmas.ok_msg
	auto_reply = xmas.auto_reply
elif gen_mode == 'lomolive':
	import lomolive
	ok_msg = lomolive.ok_msg
	auto_reply = lomolive.auto_reply


def Isfromwx(request):
	signature = request.args.get('signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	#echostr = request.args.get('echostr', '')
	L = [token, timestamp, nonce]
	L.sort()
	s = L[0] + L[1] + L[2]
	s = s.encode('utf8')
	if hashlib.sha1(s).hexdigest() == signature:
		return True
	else:
		return False


def xml_msg(user, msg, fromuser):
	'''format the raw message into xml'''

	template = '''
<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{3}]]></FromUserName>
<CreateTime>{1}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''
	return template.format(user, int(time.time()), msg, fromuser)




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
				subprocess.call(['wget', PicUrl, '-O', 'media/' + MediaId])
				if gen_mode == 'xmas':
					xmas.gen_pic(MediaId)
				elif gen_mode == 'lomolive':
					lomolive.gen_pic(MediaId)
				
				result_url = urlbase + url_for('pic', MediaId=MediaId)
				msg = ok_msg + result_url
				xml = xml_msg(FromUserName, msg, me)
				print(xml)
				return xml

			else:
				#save user's text msg into a file as a backup
				if MsgType == 'text':
					with open('user_msg', 'a') as f: f.write(str(d)+'\n')

				#default auto-reply if we received a non-image message
				msg = auto_reply
				xml = xml_msg(FromUserName, msg, me)
				return xml

	#show a blank page for website visitors
	if request.method == 'GET':
		return 'nothing'


@app.route('/pic/<MediaId>')
def pic(MediaId):
	'''generates the web page that contains the picture'''
	mediaurl = url_for('media', filename=MediaId+'.jpg')
	return render_template('pic.html', pic_path=mediaurl)


@app.route('/media/<filename>')
def media(filename):
	'''returns the media file (i.e., the picture)'''
	path = 'media/' + filename
	return send_file(path)

