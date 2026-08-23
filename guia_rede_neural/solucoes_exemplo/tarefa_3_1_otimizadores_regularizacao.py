"""Possível solução pedagógica para NNPROJ-10."""
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD, Adam
from keras.regularizers import l2

def criar_modelo(otimizador="adam", usar_regularizacao=True):
    regularizador = l2(1e-4) if usar_regularizacao else None
    modelo = Sequential([
        Dense(32, input_shape=(2,), activation="relu", kernel_regularizer=regularizador),
        Dropout(0.20 if usar_regularizacao else 0.0),
        Dense(16, activation="relu", kernel_regularizer=regularizador),
        Dense(1, activation="sigmoid"),
    ])
    opt = Adam(learning_rate=1e-3) if otimizador == "adam" else SGD(
        learning_rate=0.05, momentum=0.9
    )
    modelo.compile(optimizer=opt, loss="binary_crossentropy", metrics=["accuracy"])
    return modelo
