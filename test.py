from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import tensorflow as tf
import pandas as pd

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

model = tf.keras.models.load_model("diabetes_model.h5")
app = Flask(__name__)


@app.route("/")
def upload_f():
    return render_template("upload.html")


import keras

# keras.preprocessing
def finds():
    # for key in request.form:
    # if key.startswith('values.'):
    # id_ = key.partition('.')[-1]
    values = []
    numeric_values = []
    values.append(request.form.get("Pregnancies"))
    values.append(request.form.get("Glucose"))
    values.append(request.form.get("BloodPressure"))
    values.append(request.form.get("SkinThickness"))
    values.append(request.form.get("Insulin"))
    values.append(request.form.get("BMI"))
    values.append(request.form.get("DiabetesPedigreeFunction"))
    values.append(request.form.get("Age"))
    for value in values:
        numeric_values.append(float(value))

    numeric_values = np.asarray(numeric_values)
    df = pd.DataFrame(
        [
            pd.Series(
                [
                    numeric_values[0],
                    numeric_values[1],
                    numeric_values[2],
                    numeric_values[3],
                    numeric_values[4],
                    numeric_values[5],
                    numeric_values[6],
                    numeric_values[7],
                ]
            )
        ]
    )

    pred = model.predict(df)
    if pred[0][0] < 0:
        return "no diabetic"
    else:
        return "diabetic"
    return pred


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        val = finds()
        return render_template("pred.html", ss=val)


if __name__ == "__main__":
    app.run()
