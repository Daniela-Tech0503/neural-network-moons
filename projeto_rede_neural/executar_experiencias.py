import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from contratos import E01, E05
from experiencias import executar_experiencia, guardar_resultados_csv


def main():
    resultados = []

    for config in [E01, E05]:
        print(f"Executando {config.id_experiencia}...")
        execucao = executar_experiencia(config)
        r = execucao.resultado
        print(
            f"  -> accuracy_teste={r.accuracy_teste:.4f} "
            f"loss_teste={r.loss_teste:.4f} "
            f"parametros={r.numero_parametros}"
        )
        resultados.append(r)

    raiz = Path(__file__).parent
    caminho_csv = raiz / "resultados" / "resultados.csv"
    guardar_resultados_csv(resultados, caminho_csv)
    print(f"Resultados salvos em {caminho_csv}")


if __name__ == "__main__":
    main()
