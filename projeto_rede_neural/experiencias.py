import os
import random
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf

from contratos import (
    ConfiguracaoExperiencia,
    ExecucaoExperiencia,
    ResultadoExperiencia,
)
from dados import preparar_dados
from modelos import criar_modelo


def fixar_seeds(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    tf.config.experimental.enable_op_determinism()


def executar_experiencia(config: ConfiguracaoExperiencia) -> ExecucaoExperiencia:
    fixar_seeds(config.seed)

    dados = preparar_dados(config)
    modelo = criar_modelo(config, dados.X_treino.shape[1])

    history = modelo.fit(
        dados.X_treino,
        dados.y_treino,
        epochs=config.epocas,
        batch_size=config.batch_size,
        verbose=0,
    )

    loss, accuracy = modelo.evaluate(dados.X_teste, dados.y_teste, verbose=0)

    resultado = ResultadoExperiencia(
        id_experiencia=config.id_experiencia,
        dataset=config.dataset,
        numero_camadas_ocultas=config.numero_camadas_ocultas,
        neuronios_por_camada=config.neuronios_por_camada,
        ativacao=config.ativacao,
        numero_parametros=int(modelo.count_params()),
        accuracy_teste=float(accuracy),
        loss_teste=float(loss),
    )

    return ExecucaoExperiencia(
        config=config,
        dados=dados,
        modelo=modelo,
        historico_loss=[float(v) for v in history.history["loss"]],
        resultado=resultado,
    )


def guardar_resultados_csv(
    resultados: list[ResultadoExperiencia], caminho: Path
) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    df_novos = pd.DataFrame([vars(r) for r in resultados])
    df_novos = df_novos.rename(
        columns={
            "id_experiencia": "experiencia",
            "numero_camadas_ocultas": "camadas_ocultas",
            "numero_parametros": "parametros",
        }
    )

    if caminho.exists():
        df_existente = pd.read_csv(caminho)
        df_final = pd.concat([df_existente, df_novos])
        df_final = df_final.drop_duplicates(subset=["experiencia"], keep="last")
    else:
        df_final = df_novos

    df_final = df_final.sort_values("experiencia")
    df_final.to_csv(caminho, index=False, float_format="%.6f")
