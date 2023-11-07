import io

from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
# model.add(tf.keras.layers.Dense(128, activation='relu'))
# model.add(tf.keras.layers.Dense(128, activation='relu'))
# model.add(tf.keras.layers.Dense(10, activation='softmax'))
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#
# model.fit(x_train, y_train, epochs=9)
#
# model.save('handwritten.model2')


app = FastAPI()
origins = ["*"]  # Możesz dostosować te źródła do swoich potrzeb

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model('handwritten.model2')


(loss, accuracy) = model.evaluate(x_test, y_test)
# print(loss)
# # ok. 0.094
# print(accuracy)
# # ok.99%
@app.get("/loss")
async def accuracy():
    return {"loss": loss}
@app.post("/")
async def predict(file: UploadFile):

    image_bytes = await file.read()

    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)

    new_size = (28, 28)
    img = cv2.resize(img, new_size)

    # przygotowanie obrazu do prognozowania
    img = np.invert(img)
    img = np.array([img])

    prediction = model.predict(img)
    predicted_class = int(np.argmax(prediction))

    return {"prediction": predicted_class }