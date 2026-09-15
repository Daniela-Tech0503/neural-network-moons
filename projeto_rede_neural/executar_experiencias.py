from pathlib import Path
from .contratos import E01, E05
from .experiencias import executar_experiencia, guardar_resultados_csv


def main():
    resultados = []

    for config in [E01, E05]:
        print(f"Executando {config.id_experiencia}...")
        execucao = executar_experiencia(config)
        resultados.append(execucao.resultado)

    caminho_csv = Path("resultados/resultados.csv")
    guardar_resultados_csv(resultados, caminho_csv)
    print(f"Resultados salvos em {caminho_csv}")


if __name__ == "__main__":
    main()
