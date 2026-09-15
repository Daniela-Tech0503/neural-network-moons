from dataclasses import dataclass
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import Model


@dataclass(frozen=True)
class ConfiguracaoExperiencia:
    id_experiencia: str
    dataset: str
    numero_amostras: int
    ruido: float
    numero_camadas_ocultas: int
    neuronios_por_camada: int
    ativacao: str
    seed: int = 42
    percentagem_teste: float = 0.25
    epocas: int = 100
    batch_size: int = 16


@dataclass
class DadosPreparados:
    X_treino: np.ndarray
    X_teste: np.ndarray
    y_treino: np.ndarray
    y_teste: np.ndarray
    scaler: StandardScaler


@dataclass(frozen=True)
class ResultadoExperiencia:
    id_experiencia: str
    dataset: str
    numero_camadas_ocultas: int
    neuronios_por_camada: int
    ativacao: str
    numero_parametros: int
    accuracy_teste: float
    loss_teste: float


@dataclass
class ExecucaoExperiencia:
    config: ConfiguracaoExperiencia
    dados: DadosPreparados
    modelo: Model
    historico_loss: list[float]
    resultado: ResultadoExperiencia


# Configurações oficiais
E01 = ConfiguracaoExperiencia(
    id_experiencia="E01",
    dataset="make_moons",
    numero_amostras=500,
    ruido=0.15,
    numero_camadas_ocultas=2,
    neuronios_por_camada=8,
    ativacao="tanh",
)

E02 = ConfiguracaoExperiencia(
    id_experiencia="E02",
    dataset="make_moons",
    numero_amostras=500,
    ruido=0.15,
    numero_camadas_ocultas=2,
    neuronios_por_camada=16,
    ativacao="tanh",
)

E03 = ConfiguracaoExperiencia(
    id_experiencia="E03",
    dataset="make_moons",
    numero_amostras=500,
    ruido=0.15,
    numero_camadas_ocultas=1,
    neuronios_por_camada=8,
    ativacao="tanh",
)

E04 = ConfiguracaoExperiencia(
    id_experiencia="E04",
    dataset="make_moons",
    numero_amostras=500,
    ruido=0.15,
    numero_camadas_ocultas=2,
    neuronios_por_camada=8,
    ativacao="relu",
)

E05 = ConfiguracaoExperiencia(
    id_experiencia="E05",
    dataset="make_circles",
    numero_amostras=500,
    ruido=0.15,
    numero_camadas_ocultas=2,
    neuronios_por_camada=8,
    ativacao="tanh",
)
