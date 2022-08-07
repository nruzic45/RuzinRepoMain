import pandas
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.metrics import mean_squared_error
from tensorflow import keras
from tensorflow.keras import layers

from data_normalize import normalize_data

akt = 'relu'
aktIz = 'relu'
opti = 'Adam'
epoha = 50
lr = 0.01


def neural_model(x: pandas.DataFrame, y: pandas.DataFrame, num_of_layers: int, epoha: int, lr: float, akt: str,
                 aktIz: str,output_size:int):

    '''modelN = keras.Sequential([
        layers.Dense(units=512, activation=akt),
        layers.Dense(units=256, activation=akt),
        layers.Dense(units=256, activation=akt),
        layers.Dense(13, activation=aktIz),

    ])'''

    inputs = keras.Input(shape=(len(x.columns)))
    t = inputs
    for i in range(num_of_layers):
        t = layers.Dense(units=512, activation=akt)(t)
    outputs = layers.Dense(output_size, activation=aktIz)(t)
    model = keras.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        #loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False,),
        loss='mae',
        #loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        # metrics=["accuracy"]
        metrics=[
            keras.metrics.Accuracy()
            #keras.metrics.F1Score()
        ]

    )

    izlaz = model.fit(
        x, y,
        batch_size=64,
        epochs=epoha,
    )

    return model
