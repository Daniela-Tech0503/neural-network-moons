import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from projeto_rede_neural.contratos import E01
from projeto_rede_neural.dados import preparar_dados
from projeto_rede_neural.modelos import criar_modelo
from projeto_rede_neural.experiencias import executar_experiencia


def testar():
    dados = preparar_dados(E01)
    assert dados.X_treino.shape == (375, 2)
    assert dados.X_teste.shape == (125, 2)

    modelo = criar_modelo(E01, numero_features=2)
    assert modelo.count_params() > 0

    # Este teste falhará se não houver tensorflow
    execucao = executar_experiencia(E01)
    assert 0.0 <= execucao.resultado.accuracy_teste <= 1.0
    assert execucao.resultado.loss_teste >= 0.0
    assert len(execucao.historico_loss) == E01.epocas
    print("Testes de fundação passaram!")


if __name__ == "__main__":
    testar()
