import cv2, numpy, random
import os
from PIL import Image, ImageDraw


#Prepare the hats for use later
hats = []
hats_portion = []
for i in range(1,8):
	hat = Image.open('./xmas/' + 'hat' + str(i) + '.png')
	hats.append(hat)
	hats_portion.append(hat.size[0]/hat.size[1])
#load photo frames
frame_w = Image.open('./xmas/frame_w.png')
frame_h = Image.open('./xmas/frame_h.png')
frame_s = Image.open('./xmas/frame_s.png')

ok_msg = '你的圣诞节靓照已经生成好啦，请访问以下链接查看，长按图片可保存： '
auto_reply = '嗨！欢迎来玩儿，活动正在进行中！你可以在这里向本公众号发送现场拍摄的照片，我们会自动为照片中的人物带上圣诞帽或鹿角，生成有浓浓圣诞节氛围的照片～「本消息为自动发送」'

def gen_pic(MediaId):

	def get_hat(x,y,w,h):
		#set the probability of every hat
		num = random.randint(1,100)
		if num in range(1,17):
			#hat1
			(hat_num, offset1, offset2, offset3) = (0, 1.2, .05, .67)
		elif num in range(17,33):
			#hat2
			(hat_num, offset1, offset2, offset3) = (1, 1.3, -.4, .62)
		elif num in range(33,49):
			#hat3
			(hat_num, offset1, offset2, offset3) = (2, .9, .05, .8)
		elif num in range(91,101):
			#green hat
			(hat_num, offset1, offset2, offset3) = (3, 1.2, .05, .67)
		elif num in range(49,65):
			#jiao1
			(hat_num, offset1, offset2, offset3) = (4, 1.2, -.1, 1.2)
		elif num in range(65,81):
			#jiao2
			(hat_num, offset1, offset2, offset3) = (5, 1, 0, 1.2)
		elif num in range(81,91):
			#tree
			(hat_num, offset1, offset2, offset3) = (6, .9, .05, 1)
		
		hat_portion = hats_portion[hat_num]
		(hat_w, hat_h) = (int(w*offset1), int(w*offset1/hat_portion))
		print('hat size:',hat_w,hat_h)
		hatter = hats[hat_num].resize((hat_w, hat_h))
	 
		(hat_x, hat_y) = (int(x+w*offset2), int(y-hat_h*offset3))
		hat_pos = (hat_x, hat_y)
		print('hat at:',hat_x,hat_y)
		
		return (hatter, hat_pos)
	
	
	def std_size(imagePath):
		pic = Image.open(imagePath)
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
	
		elif portion == 1:
			#square
			(pic_w,pic_h) = (960,960)
			box = (0,0,960,960)
	
		pic = pic.resize((pic_w, pic_h))
		pic = pic.crop(box)
		return pic
	
	
	def facedet(pil_image):
	#input an PIL Image object and output a list of positions of faces
	
		# Create the haar cascade
		cascPath = './xmas/haarcascade_frontalface_default.xml'
		faceCascade = cv2.CascadeClassifier(cascPath)
	
		# Read the image
		#image = cv2.imread(imagePath)
		#pil_image = std_size(imagePath)
		image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
		# Detect faces in the image
		faces = faceCascade.detectMultiScale(
		    gray,
		    scaleFactor=1.2,
		    minNeighbors=5,
		    minSize=(50, 60),
		    flags=cv2.CASCADE_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
		#for (x, y, w, h) in faces:
		#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
		#cv2.imwrite(o_path, image)
		return faces
	

	imagePath = os.path.join('media', MediaId)
	o_path = os.path.join('media', MediaId + '.jpg')
	image = std_size(imagePath)
	faces = facedet(image)
	for (x,y,w,h) in faces:
		print('face at:',x,y,w,h)
		#draw = ImageDraw.Draw(image)
		#draw.rectangle([(x, y), (x+w, y+h)])

		(hatter,hat_pos) = get_hat(x,y,w,h)

		image.paste(hatter, hat_pos, hatter)

	#add photo to the frame
	portion = image.size[0]/image.size[1]
	if portion > 1:
		image.paste(frame_w, (0,0), frame_w)
	elif portion < 1:
		image.paste(frame_h, (0,0), frame_h)
	else:
		image.paste(frame_s, (0,0), frame_s)

	image.save(o_path)
