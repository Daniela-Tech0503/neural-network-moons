import pandas as pd
import numpy as np
import tensorflow as tf
from pathlib import Path
from .contratos import (
    ConfiguracaoExperiencia,
    ExecucaoExperiencia,
    ResultadoExperiencia,
)
from .dados import preparar_dados
from .modelos import criar_modelo


def executar_experiencia(config: ConfiguracaoExperiencia) -> ExecucaoExperiencia:
    # Fixar seeds
    np.random.seed(config.seed)
    tf.random.set_seed(config.seed)

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
        numero_parametros=modelo.count_params(),
        accuracy_teste=accuracy,
        loss_teste=loss,
    )

    return ExecucaoExperiencia(
        config=config,
        dados=dados,
        modelo=modelo,
        historico_loss=history.history["loss"],
        resultado=resultado,
    )


def guardar_resultados_csv(
    resultados: list[ResultadoExperiencia], caminho: Path
) -> None:
    # Garantir pasta
    caminho.parent.mkdir(parents=True, exist_ok=True)

    df_novos = pd.DataFrame([vars(r) for r in resultados])
    # Renomear colunas para o padrão do relatório
    df_novos = df_novos.rename(
        columns={
            "numero_camadas_ocultas": "camadas_ocultas",
            "numero_parametros": "parametros",
            "accuracy_teste": "accuracy_teste",
            "loss_teste": "loss_teste",
        }
    )

    if caminho.exists():
        df_existente = pd.read_csv(caminho)
        df_final = pd.concat([df_existente, df_novos])
        # Remover duplicadas mantendo a última atualização
        df_final = df_final.drop_duplicates(subset=["id_experiencia"], keep="last")
    else:
        df_final = df_novos

    df_final = df_final.sort_values("id_experiencia")
    df_final.to_csv(caminho, index=False)
