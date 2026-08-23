"""Possível solução pedagógica para NNPROJ-9."""
from itertools import product
from keras import Sequential
from keras.layers import Dense

resultados = []
for numero_camadas, neuronios in product([1, 2, 3, 4], [2, 8, 16, 32, 64]):
    modelo = Sequential()
    modelo.add(Dense(neuronios, input_shape=(2,), activation="tanh"))
    for _ in range(numero_camadas - 1):
        modelo.add(Dense(neuronios, activation="tanh"))
    modelo.add(Dense(1, activation="sigmoid"))
    modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    # histórico = modelo.fit(...)
    # loss, accuracy = modelo.evaluate(...)
    resultados.append({
        "camadas": numero_camadas,
        "neuronios": neuronios,
        "parametros": modelo.count_params(),
    })
