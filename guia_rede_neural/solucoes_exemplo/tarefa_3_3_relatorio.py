"""Possível solução pedagógica para NNPROJ-12.
Gera uma tabela Markdown a partir dos resultados; o texto científico continua a ser escrito pelo grupo.
"""
import pandas as pd

df = pd.read_csv("benchmark.csv")
melhor = df.sort_values("f1", ascending=False).iloc[0]

with open("resumo_resultados.md", "w", encoding="utf-8") as f:
    f.write("# Resumo dos resultados\n\n")
    f.write(df.to_markdown(index=False))
    f.write("\n\n")
    f.write(
        f"O melhor resultado de F1 foi obtido por **{melhor['modelo']}**, "
        f"com F1 = {melhor['f1']:.3f}. Este resultado deve ser interpretado "
        "em conjunto com as curvas de treino e teste.\n"
    )
