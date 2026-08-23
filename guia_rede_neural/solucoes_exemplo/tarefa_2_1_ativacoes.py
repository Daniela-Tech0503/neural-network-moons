"""Possível solução pedagógica para NNPROJ-7."""
from keras import Sequential
from keras.layers import Dense, Activation, LeakyReLU


def criar_modelo(ativacao="relu"):
    # A camada Dense é igual em todas as experiências.
    # Apenas a função de ativação é alterada.
    modelo = Sequential()
    modelo.add(Dense(16, input_shape=(2,)))

    if ativacao == "leaky_relu":
        modelo.add(LeakyReLU(negative_slope=0.1))
    else:
        modelo.add(Activation(ativacao))

    modelo.add(Dense(1, activation="sigmoid"))
    modelo.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return modelo


for nome in ["relu", "tanh", "elu", "leaky_relu"]:
    modelo = criar_modelo(nome)
    # Treinar sempre com o mesmo split e seed para uma comparação justa.
    print(nome, modelo.count_params())
