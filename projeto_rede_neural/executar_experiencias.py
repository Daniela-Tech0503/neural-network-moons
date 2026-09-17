import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from contratos import E01, E02, E03, E04, E05
from experiencias import executar_experiencia, guardar_resultados_csv
from visualizacao import plotar_curvas_loss, plotar_fronteira_decisao

CONFIGURACOES = [E01, E02, E03, E04, E05]


def main():
    raiz = Path(__file__).parent
    pasta_figuras = raiz / "figuras"
    caminho_csv = raiz / "resultados" / "resultados.csv"

    execucoes = []
    for config in CONFIGURACOES:
        print(f"Executando {config.id_experiencia} ({config.dataset}, "
              f"{config.numero_camadas_ocultas}x{config.neuronios_por_camada}, "
              f"{config.ativacao})...")
        execucao = executar_experiencia(config)
        r = execucao.resultado
        print(
            f"  -> accuracy_teste={r.accuracy_teste:.4f} "
            f"loss_teste={r.loss_teste:.4f} "
            f"parametros={r.numero_parametros}"
        )
        execucoes.append(execucao)

    guardar_resultados_csv([e.resultado for e in execucoes], caminho_csv)
    print(f"\nResultados salvos em {caminho_csv}")

    por_id = {e.config.id_experiencia: e for e in execucoes}
    plotar_fronteira_decisao(
        por_id["E01"],
        pasta_figuras / "E01_fronteira_make_moons.png",
    )
    plotar_fronteira_decisao(
        por_id["E05"],
        pasta_figuras / "E05_fronteira_make_circles.png",
    )
    plotar_curvas_loss(
        [por_id["E01"], por_id["E04"]],
        pasta_figuras / "E01_E04_curvas_loss.png",
    )
    print(f"Figuras salvas em {pasta_figuras}")

    print("\nResumo final E01 a E05:")
    print(f"{'ID':<6}{'Dataset':<15}{'Camadas':<9}{'Neuronios':<11}"
          f"{'Ativacao':<10}{'Params':<8}{'Acc':<8}{'Loss'}")
    for e in execucoes:
        r = e.resultado
        print(f"{r.id_experiencia:<6}{r.dataset:<15}{r.numero_camadas_ocultas:<9}"
              f"{r.neuronios_por_camada:<11}{r.ativacao:<10}{r.numero_parametros:<8}"
              f"{r.accuracy_teste:<8.4f}{r.loss_teste:.4f}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
