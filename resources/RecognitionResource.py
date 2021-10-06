import librosa
import tensorflow as tf
import pandas as pd
from pickle import load
from mycroft_bus_client import MessageBusClient, Message
from flask import request
from flask_restful import Resource
from utils.utils import audio_to_features, scalling_data, predict_classe, pcm2float
from Model_MySQL import User, Skills

import io
import base64
import numpy as np
import scipy.io.wavfile as wav
import json
# LOAD MODEL AND SCALER
mlp = tf.keras.models.load_model("/home/raul/Desktop/va-user-authentication-dev/model/model_mlp.h5")
scaler = load(open('/home/raul/Desktop/va-user-authentication-dev/model/scaler.pkl', 'rb'))


class RecognitionResource(Resource):
    def get(self):
        audio,sr = librosa.load("/home/raul/Desktop/va-user-authentication-dev/scripts/NOIZEUS/user2/sp05.wav")
        #audio,sr = librosa.load("/home/raul/Downloads/Voz 047.wav")
        data_speech = pd.DataFrame(audio_to_features(audio,sr))
        data_speech = scalling_data(data_speech, scaler)

        # Predict
        user_id = predict_classe(mlp, data_speech)
        print(user_id)
        print(user_id[0].item())

        user = User.query.filter_by(id=user_id[0].item()+1).first()
        skill = Skills.query.filter_by(tag='CreateService').first()

        roles = user.roles
        # Check authorization & response
        for role in roles:
            print(role)
            for ski in role.skills:
                print(ski.id)
                if ski.id == skill.id:
                    return "Ok " + user.username + " ! The Service is created."

        return "Sorry " + user.username + ", you don't have permission for that!"

    def post(self):
        data = request.get_json(force=True)

        #_, speech = wav.read(io.BytesIO(base64.b64decode(data['audio'].encode('ascii'))))
        _,speech = wav.read(io.BytesIO(base64.b64decode(data['audio'].encode('ascii'))))

        # Data processing
        data_speech = pd.DataFrame(audio_to_features(pcm2float(speech.astype(np.int16)), 16000))
        data_speech = scalling_data(data_speech, scaler)

        # Predict
        user_id = predict_classe(mlp, data_speech)


        user = User.query.filter_by(id=user_id[0].item()+1).first()
        if(user is None):
            d={
                "id":2,
                "user_name":None
            }
            print("User not recognize")
            return d
        skill = Skills.query.filter_by(tag=data['tag']).first()
        roles = user.roles

        # Check authorization & response
        for role in roles:
            print(role)
            for ski in role.skills:
                print(ski.id)
                if ski.id == skill.id:
                    print(user.username)
                    d={
                        "id":1,
                        "user_name":user.username
                    }
                    return d
        d={
            "id":0,
            "user_name":user.username
        }
        return d
