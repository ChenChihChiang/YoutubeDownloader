from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g
from pytube import YouTube
import os

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

	filename = yt.filename

	resolutions = yt.filter('mp4')

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

	filename = filename+".mp4"

	return send_from_directory(dirpath,filename,as_attachment=True)

@app.route('/downloader/<filename>')
def downloader(filename):

	filename = filename+".mp4"

	return send_from_directory(dirpath,filename,as_attachment=True)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9000,debug=True)
