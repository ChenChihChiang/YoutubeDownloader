from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g
from pytube import YouTube
import os
#import urllib.parse as up

app = Flask(__name__)

dirpath = os.path.join(app.root_path,'download')

@app.route('/')
def index():
	filename = request.args.get('filename')
	resolutions0 = request.args.get('resolutions0')
	resolutions1 = request.args.get('resolutions1')
	url = request.args.get('url')
	
	return render_template('index.html', filename=filename, resolutions0=resolutions0, resolutions1=resolutions1, url=url)

@app.route('/done')
def done():
	filename = request.args.get('filename')
	return render_template('done.html', filename=filename)

@app.route('/index', methods=['POST'])
def backindex():
	return render_template('index.html')


@app.route('/sumbit', methods=['POST'])
def post_sumbit():
	yt = YouTube()
	url = request.form.get('url')
	yt.url = url
	#video = yt.get('mp4', '360p')
	filename = yt.filename


	#for i in range(0,len(yt.videos)):
	#	print(resolutions[i])

	resolutions = yt.filter('mp4')

	#print (len(resolutions))

	#print(yt.filter('mp4')[-1])

	#print (resolutions)
	#resolutions0 = str(resolutions[0])
	#resolutions1 = str(resolutions[1])
	#resolutions2 = str(yt.videos[2])
	
	#print (resolutions0)
	#print (resolutions1)
	#print (resolutions2)
	


	#print (yt)
	#print (filename)
	#a = yt.get_videos()
	#print (type(a))

	#return redirect(url_for('index', filename=filename))

	if len(resolutions) == 2:
		resolutions0 = str(resolutions[0])
		resolutions1 = str(resolutions[1])
		return redirect(url_for('index',url=url, filename=filename, resolutions0=resolutions0, resolutions1=resolutions1))
	else:
		resolutions0 = str(resolutions[0])
		return redirect(url_for('index',url=url, filename=filename, resolutions0=resolutions0))

@app.route('/download', methods=['POST'])
def post_download():
	yt = YouTube()
	url = request.form.get('url')
	yt.url = url

	pixel = request.form.get('pixel')
	video = yt.get('mp4', pixel)
	
	filename = yt.filename

	if os.path.exists("./download/"+filename+".mp4"):
		os.remove("./download/"+filename+".mp4")
	
	video.download('./download')

	#os.rename("./download/"+filename+".mp4", "./download/1.mp4")
	##return redirect(url_for('done', filename=filename))
	#return redirect(url_for('downloader', filename="1.mp4"))

	#filename = filename.encode('uft-8')
	#filename = filename.decode('latin1')
	filename = filename+".mp4"
	#filename = filename.encode('Big5')

	#filename=filename.encode("latin-1","ignore")

	#print (filename)
	return send_from_directory(dirpath,filename,as_attachment=True)

	#filename = up.quote(filename)
	#return redirect(url_for('downloader', filename=filename))

@app.route('/downloader/<filename>')
def downloader(filename):

	#filename = up.unquote(filename)
	#filename = filename.encode('utf8')
	filename = filename+".mp4"
	#print (filename)

	#filename = up.unquote(filename)
	return send_from_directory(dirpath,filename,as_attachment=True)
    #os.remove("./download/1.mp4")

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9000,debug=True)
