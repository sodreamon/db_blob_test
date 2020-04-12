from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask import send_file
import io
from PIL import Image

#didnt use
from sqlalchemy.dialects.sqlite import BLOB
import sqlite3
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import base64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Image(db.Model):
    title = db.Column(db.String, primary_key=True)
    image = db.Column(db.LargeBinary)







def toblob(digital_data):
    with open(digital_data, 'rb') as file:
        blobdata = file.read()
    return blobdata

def todigital(digital_path, blob_data):
    with open(digital_path, 'wb') as file:
        digital_path.write(blob_data)
    return digital_path







@app.route('/')
def home():
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/<image_title>')
def image_url(image_title):
    image = Image.query.filter_by(title=image_title).first()
    img_src = image.image
    digital = send_file(io.BytesIO(img_src), attachment_filename='test_image.jpg', mimetype='image/jpeg')
    return digital

@app.route('/', methods=['POST'])
def home_post():
    image = request.files["image"]
    image_path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
    image.save(image_path)
    blob_image = toblob(image_path)
    new_image = Image(image=blob_image, title=secure_filename(image.filename))
    os.remove(image_path)
    db.session.add(new_image)
    db.session.commit()
    return redirect(url_for('home'))






if __name__ == '__main__':
    app.run(debug=True)