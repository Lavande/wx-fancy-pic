import hashlib
from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def wx_verify():
	signature = request.args.get('signature', '')
	timestamp = request.args.get('timestamp', '')
	nonce = request.args.get('nonce', '')
	echostr = request.args.get('echostr', '')
	#PUT YOUR TOKEN HERE
	token = ''
	L = [token, timestamp, nonce]
	L.sort()
	s = L[0] + L[1] + L[2]
	s = s.encode('utf8')
	if hashlib.sha1(s).hexdigest() == signature:
		return echostr
	else:
		return 'Error'
