from tensorflow.keras import Sequential, layers, Model
from .contratos import ConfiguracaoExperiencia


def criar_modelo(config: ConfiguracaoExperiencia, numero_features: int) -> Model:
    model = Sequential()
    model.add(layers.Input(shape=(numero_features,)))

    # Camadas ocultas
    for _ in range(config.numero_camadas_ocultas):
        model.add(layers.Dense(config.neuronios_por_camada, activation=config.ativacao))

    # Camada de saída
    model.add(layers.Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model
