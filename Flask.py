import os
import cv2
import numpy as np
import threading
from flask import Flask, request
from pyngrok import ngrok

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
port = 5000
# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

# ... Update inbound traffic via APIs to use the public-facing ngrok URL


# Define Flask routes
def cnn(photo):

    frame=photo  # Requestten gelen resim olacak  requestren string olarak gelecek  resimi jpeg

    from keras.models import load_model
    model = load_model('model.h5') # Eğittiğimiz model load
    label_dict = {0:'ercan', 1:'ezgi', 2:'Onur'}
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100,100))

    for(x,y,w,h) in faces:
      face_img = gray[y:y+h, x:x+w]
      resized = cv2.resize(face_img, (224,224))
      normalized=resized/255.
      reshaped=np.reshape(normalized, (1,224,224,1))
      result=model.predict(reshaped)
      label=np.argmax(result,axis=1)[0]
      cv2.rectangle(frame,(x,y),(x+w,y+h),(218,7,222),2)
      cv2.putText(frame,label_dict[label], (x, y-10), cv2.FONT_HERSHEY_COMPLEX,0.8,(240,14,172))


    return f'{label_dict[label]}'                # Hangi kişi olduğunu return ediyor


@app.route('/photo',methods=['POST'])
def upload_photo():
  photo = cv2.imdecode(np.fromstring(request.files.get('file').read(),np.uint8),cv2.IMREAD_UNCHANGED)
  return cnn(photo)


# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": True}).start()