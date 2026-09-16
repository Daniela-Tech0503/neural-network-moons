import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from contratos import E01, E02, E03, E04, E05
from dados import preparar_dados
from modelos import criar_modelo
from experiencias import executar_experiencia


def testar():
    dados = preparar_dados(E01)
    assert dados.X_treino.shape == (375, 2)
    assert dados.X_teste.shape == (125, 2)
    assert dados.y_treino.shape == (375,)
    assert dados.y_teste.shape == (125,)

    modelo = criar_modelo(E01, numero_features=2)
    assert modelo.input_shape == (None, 2)
    assert modelo.output_shape == (None, 1)
    assert modelo.count_params() > 0

    assert E02.neuronios_por_camada != E01.neuronios_por_camada
    assert E03.numero_camadas_ocultas != E01.numero_camadas_ocultas
    assert E04.ativacao != E01.ativacao
    assert E05.dataset != E01.dataset

    # Este teste falhará se não houver tensorflow
    execucao = executar_experiencia(E01)
    assert 0.0 <= execucao.resultado.accuracy_teste <= 1.0
    assert execucao.resultado.loss_teste >= 0.0
    assert len(execucao.historico_loss) == E01.epocas
    print("Testes de fundação passaram!")


if __name__ == "__main__":
    testar()
