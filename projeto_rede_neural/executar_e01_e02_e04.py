import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib.pyplot as plt

from contratos import E01, E02, E04
from experiencias import executar_experiencia, guardar_resultados_csv


def salvar_curva_loss(execucoes, caminho: Path) -> None:
    plt.figure()
    for execucao in execucoes:
        plt.plot(execucao.historico_loss, label=execucao.config.id_experiencia)
    plt.xlabel("Época")
    plt.ylabel("Loss (treino)")
    plt.title("Curva de loss: tanh (E01) vs ReLU (E04)")
    plt.legend()
    plt.savefig(caminho)


def main():
    execucoes = {}
    for config in [E01, E02, E04]:
        print(f"Executando {config.id_experiencia}...")
        execucao = executar_experiencia(config)
        r = execucao.resultado
        print(
            f"  -> accuracy_teste={r.accuracy_teste:.4f} "
            f"loss_teste={r.loss_teste:.4f} "
            f"parametros={r.numero_parametros}"
        )
        execucoes[config.id_experiencia] = execucao

    raiz = Path(__file__).parent
    caminho_csv = raiz / "resultados" / "resultados.csv"
    guardar_resultados_csv([e.resultado for e in execucoes.values()], caminho_csv)
    print(f"Resultados salvos em {caminho_csv}")

    caminho_curva = raiz / "resultados" / "curva_loss_e01_e04.png"
    salvar_curva_loss([execucoes["E01"], execucoes["E04"]], caminho_curva)
    print(f"Curva de loss (E01 vs E04) salva em {caminho_curva}")


if __name__ == "__main__":
    main()
