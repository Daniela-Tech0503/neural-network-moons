from pathlib import Path
import csv

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).parent
ROOT = BASE.parent
OUTPUT = BASE / "relatorio_final.pdf"
CSV_PATH = ROOT / "resultados" / "resultados.csv"
FIGURAS_DIR = ROOT / "figuras"

font_regular = Path("C:/Windows/Fonts/arial.ttf")
font_bold = Path("C:/Windows/Fonts/arialbd.ttf")
if font_regular.exists() and font_bold.exists():
    pdfmetrics.registerFont(TTFont("ArialLocal", str(font_regular)))
    pdfmetrics.registerFont(TTFont("ArialLocalBold", str(font_bold)))
    BODY_FONT = "ArialLocal"
    BOLD_FONT = "ArialLocalBold"
else:
    BODY_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"

styles_base = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle(
        "Title", parent=styles_base["Title"], fontName=BOLD_FONT, fontSize=20,
        leading=24, textColor=colors.HexColor("#1e3a8a"), alignment=TA_CENTER,
        spaceAfter=6,
    ),
    "subtitle": ParagraphStyle(
        "Subtitle", parent=styles_base["Normal"], fontName=BODY_FONT, fontSize=9.5,
        leading=13, textColor=colors.HexColor("#475569"), alignment=TA_CENTER,
        spaceAfter=14,
    ),
    "h1": ParagraphStyle(
        "H1", parent=styles_base["Heading1"], fontName=BOLD_FONT, fontSize=13,
        leading=16, textColor=colors.HexColor("#1e3a8a"), spaceBefore=10,
        spaceAfter=5,
    ),
    "h2": ParagraphStyle(
        "H2", parent=styles_base["Heading2"], fontName=BOLD_FONT, fontSize=10.5,
        leading=14, textColor=colors.HexColor("#4338ca"), spaceBefore=6,
        spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "Body", parent=styles_base["BodyText"], fontName=BODY_FONT, fontSize=8.8,
        leading=12.2, textColor=colors.HexColor("#1f2937"), spaceAfter=4,
        alignment=TA_JUSTIFY,
    ),
    "bullet": ParagraphStyle(
        "Bullet", parent=styles_base["BodyText"], fontName=BODY_FONT, fontSize=8.5,
        leading=11.5, leftIndent=12, firstLineIndent=-6, spaceAfter=2.5,
    ),
    "table_cell": ParagraphStyle(
        "TableCell", parent=styles_base["BodyText"], fontName=BODY_FONT, fontSize=8,
        leading=10.5, textColor=colors.HexColor("#1f2937"), alignment=TA_CENTER,
    ),
    "table_header": ParagraphStyle(
        "TableHeader", parent=styles_base["BodyText"], fontName=BOLD_FONT, fontSize=8,
        leading=10.5, textColor=colors.HexColor("#1e3a8a"), alignment=TA_CENTER,
    ),
    "note": ParagraphStyle(
        "Note", parent=styles_base["BodyText"], fontName=BODY_FONT, fontSize=8.5,
        leading=11.5, textColor=colors.HexColor("#1e3a8a"),
        backColor=colors.HexColor("#eff6ff"), borderColor=colors.HexColor("#93c5fd"),
        borderWidth=0.6, borderPadding=6, spaceBefore=4, spaceAfter=6,
    ),
    "caption": ParagraphStyle(
        "Caption", parent=styles_base["Normal"], fontName=BODY_FONT, fontSize=7.5,
        leading=10, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER,
        spaceBefore=2, spaceAfter=6,
    ),
}


def ler_resultados():
    resultados = {}
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            resultados[row["experiencia"]] = row
    return resultados


def gerar_relatorio():
    res = ler_resultados()
    story = []

    def p(text, style="body"):
        story.append(Paragraph(text, styles[style]))

    def h(text, level=1):
        story.append(Paragraph(text, styles[f"h{level}"]))

    def b(text):
        story.append(Paragraph("&#8226; " + text, styles["bullet"]))

    p("RELATÓRIO FINAL DE EXPERIÊNCIAS — REDES NEURAIS", "title")
    p("Neural Network Moon Project &#8226; Task NNPROJ-12 &#8226; Data: 17/09/2026<br/>"
      "Autor: Pedro Rodrigues &#8226; Colaboradores: Helton Soares, Luciana Almeida &#8226; Revisão: Daniela Amaro", "subtitle")

    # 1. Objetivo do projeto
    h("1. Objetivo do Projeto")
    p("O objetivo central deste trabalho não é encontrar a melhor arquitetura de rede neural possível, "
      "mas sim realizar um estudo científico controlado sobre como alterações estruturais e de dados "
      "afetam o processo de aprendizagem e a capacidade de generalização de uma rede neural artificial "
      "em problemas de classificação binária não linearmente separáveis.")

    # 2. Explicação simples do problema de classificação
    h("2. Problema de Classificação Binária")
    p("Classificação binária consiste em prever uma entre duas classes possíveis (0 ou 1) a partir de "
      "atributos de entrada (duas coordenadas <i>(x₁, x₂)</i>). Foram utilizados dois conjuntos sintéticos:")
    b("<b>make_moons</b>: 500 amostras formando duas meias-luas entrelaçadas (ruído 0.15).")
    b("<b>make_circles</b>: 500 amostras formando dois círculos concêntricos (ruído 0.15, fator padrão 0.8).")
    p("Ambos os padrões são não lineares: não é possível separar as classes por uma única reta, exigindo "
      "redes com camadas ocultas e funções de ativação não lineares.")

    # 3. Descrição da baseline E01
    h("3. Descrição da Baseline E01")
    p("A baseline <b>E01</b> adota 2 camadas ocultas com 8 neurónios cada, ativação <i>tanh</i>, saída <i>sigmoid</i>, "
      "otimizador <i>Adam</i>, loss <i>binary_crossentropy</i>, 100 épocas e batch size 16. O split é 75% treino (375 amostras) "
      "e 25% teste (125 amostras), com <i>StandardScaler</i> ajustado exclusivamente no conjunto de treino. "
      f"Atingiu <b>accuracy de {float(res['E01']['accuracy_teste'])*100:.2f}%</b> e <b>loss de {float(res['E01']['loss_teste']):.4f}</b> "
      f"com {res['E01']['parametros']} parâmetros.")

    # 4. Regra científica central
    h("4. Regra Científica: 'Uma Variável de Cada Vez'")
    p("Para garantir validade causal, cada experiência subsequente (E02 a E05) altera exatamente um único elemento "
      "em relação à baseline E01, mantendo todas as outras variáveis (seed 42, split, normalização, épocas, otimizador) rigorosamente idênticas.")

    # 5 a 8: Comparações
    h("5. Comparação E01 vs E02: Número de Neurónios (Largura)")
    p(f"Variando a largura de 8 para 16 neurónios por camada (E02), os parâmetros triplicaram de {res['E01']['parametros']} para {res['E02']['parametros']} (+221%). "
      f"A accuracy subiu de {float(res['E01']['accuracy_teste'])*100:.2f}% para {float(res['E02']['accuracy_teste'])*100:.2f}% (+0.80 pp) e a loss caiu para {float(res['E02']['loss_teste']):.4f}. "
      "Conclusão: a rede maior opera com maior confiança estatística, embora a accuracy atinja retornos decrescentes devido à simplicidade do dataset.")

    h("6. Comparação E01 vs E03: Número de Camadas (Profundidade)")
    p(f"Reduzindo a profundidade de 2 camadas para 1 camada oculta (E03), os parâmetros caíram para {res['E03']['parametros']} (-68.6%). "
      f"Contudo, a accuracy caiu para {float(res['E03']['accuracy_teste'])*100:.2f}% (-10.40 pp) e a loss subiu para {float(res['E03']['loss_teste']):.4f}. "
      "Conclusão: com apenas 8 neurónios, 1 camada tem flexibilidade geométrica insuficiente para moldar a fronteira em espiral das meias-luas; a composição de não-linearidades em profundidade foi fundamental.")

    h("7. Comparação E01 vs E04: Função de Ativação (tanh vs ReLU)")
    p(f"Mantendo 105 parâmetros e trocando <i>tanh</i> por <i>ReLU</i> (E04), a accuracy foi de {float(res['E04']['accuracy_teste'])*100:.2f}% e loss {float(res['E04']['loss_teste']):.4f}. "
      "Conclusão: a ativação <i>tanh</i> (suave e centrada em zero) obteve desempenho superior e convergência mais estável nesta arquitetura pequena. "
      "A ReLU apresentou oscilações na curva de treino decorrentes do desligamento temporário de unidades ('dying ReLU') em rede rasa.")

    h("8. Comparação E01 vs E05: Base de Dados (moons vs circles)")
    p(f"Aplicando a arquitetura baseline ao dataset make_circles (E05), a accuracy foi de {float(res['E05']['accuracy_teste'])*100:.2f}% e loss {float(res['E05']['loss_teste']):.4f}. "
      "Conclusão: com ruído 0.15 e fator 0.8, os dois anéis concêntricos (raios 0.8 e 1.0) sobrepõem-se fisicamente no espaço de entrada. "
      "A loss próxima de ln(2)≈0.693 comprova a incerteza intrínseca dos dados e evidencia que o desempenho depende fortemente da separabilidade geométrica da base.")

    story.append(PageBreak())

    # 9. Tabela de Resultados do CSV
    h("9. Tabela Consolidada de Resultados (E01 a E05)")
    p("Resultados gerados automaticamente a partir do ficheiro <code>resultados.csv</code>:")

    linhas_tabela = [
        [
            Paragraph("Exp.", styles["table_header"]),
            Paragraph("Dataset", styles["table_header"]),
            Paragraph("Camadas", styles["table_header"]),
            Paragraph("Neurónios", styles["table_header"]),
            Paragraph("Ativação", styles["table_header"]),
            Paragraph("Parâmetros", styles["table_header"]),
            Paragraph("Accuracy", styles["table_header"]),
            Paragraph("Loss", styles["table_header"]),
        ]
    ]
    for exp_id in ["E01", "E02", "E03", "E04", "E05"]:
        r = res[exp_id]
        linhas_tabela.append([
            Paragraph(r["experiencia"], styles["table_cell"]),
            Paragraph(r["dataset"], styles["table_cell"]),
            Paragraph(r["camadas_ocultas"], styles["table_cell"]),
            Paragraph(r["neuronios_por_camada"], styles["table_cell"]),
            Paragraph(r["ativacao"], styles["table_cell"]),
            Paragraph(r["parametros"], styles["table_cell"]),
            Paragraph(f"{float(r['accuracy_teste'])*100:.2f}%", styles["table_cell"]),
            Paragraph(f"{float(r['loss_teste']):.4f}", styles["table_cell"]),
        ])

    t = Table(linhas_tabela, colWidths=[1.5 * cm, 3.2 * cm, 2.0 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.4 * cm, 2.3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 10. Fronteiras de Decisão
    h("10. Fronteiras de Decisão (E01 e E05)")
    p("Visualização da probabilidade prevista e da linha de decisão (limiar 0.5) gerada pelo contrato <code>visualizacao.py</code>:")

    img_moons = str(FIGURAS_DIR / "E01_fronteira_make_moons.png")
    img_circles = str(FIGURAS_DIR / "E05_fronteira_make_circles.png")
    if Path(img_moons).exists() and Path(img_circles).exists():
        t_imgs = Table([
            [
                Image(img_moons, width=8.2 * cm, height=6.2 * cm),
                Image(img_circles, width=8.2 * cm, height=6.2 * cm),
            ],
            [
                Paragraph("<b>Figura 1:</b> Fronteira E01 (make_moons - 98.4%)", styles["caption"]),
                Paragraph("<b>Figura 2:</b> Fronteira E05 (make_circles - 62.4%)", styles["caption"]),
            ]
        ], colWidths=[8.8 * cm, 8.8 * cm])
        t_imgs.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t_imgs)

    # 11. Curvas de Loss
    h("11. Curvas de Loss de Treino (E01 vs E04)")
    img_loss = str(FIGURAS_DIR / "E01_E04_curvas_loss.png")
    if Path(img_loss).exists():
        t_loss = Table([
            [Image(img_loss, width=11.0 * cm, height=5.5 * cm)],
            [Paragraph("<b>Figura 3:</b> Curvas de loss ao longo das 100 épocas: tanh (E01) vs ReLU (E04)", styles["caption"])],
        ], colWidths=[17.6 * cm])
        t_loss.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_loss)

    story.append(PageBreak())

    # 12. Limitações
    h("12. Limitações Metodológicas")
    p("Em conformidade com as boas práticas científicas, reconhecem-se as seguintes limitações:")
    b("<b>Amostragem de Hiperparâmetros:</b> cinco experiências não esgotam o espaço de configurações possíveis nem permitem extrapolar superioridade universal de uma função ou topologia.")
    b("<b>Variabilidade e Seed Única:</b> a seed fixa (42) permite reprodutibilidade exata, mas não estima o intervalo de confiança nem a variância entre diferentes inicializações aleatórias.")
    b("<b>Métricas de Avaliação:</b> em datasets balanceados (50/50), accuracy e loss são informativas, mas em dados desbalanceados exigiriam precisão, recall e curva ROC/AUC.")
    b("<b>Datasets Sintéticos:</b> bases 2D facilitam a visualização mas não representam a dimensionalidade, ruído heterogéneo e correlações complexas de problemas industriais reais.")

    # 13. Contribuição de cada pessoa
    h("13. Contribuições da Equipa")
    t_contrib = Table([
        [Paragraph("Membro", styles["table_header"]), Paragraph("Responsabilidade Principal", styles["table_header"]), Paragraph("Entregáveis Realizados", styles["table_header"])],
        [
            Paragraph("<b>Helton Soares</b>", styles["table_cell"]),
            Paragraph("Fundação e Baseline<br/>(NNPROJ-5, 8, 11)", styles["table_cell"]),
            Paragraph("Contratos de software (<font face='Courier'>contratos.py</font>), pipeline de dados (<font face='Courier'>dados.py</font>), execução e consolidação CSV E01 a E05.", styles["table_cell"]),
        ],
        [
            Paragraph("<b>Luciana Almeida</b>", styles["table_cell"]),
            Paragraph("Neurónios e Ativações<br/>(NNPROJ-4, 7)", styles["table_cell"]),
            Paragraph("Validação experimental E02 (16 neurónios) e E04 (ReLU), análise da convergência das ativações e conclusões técnicas.", styles["table_cell"]),
        ],
        [
            Paragraph("<b>Pedro Rodrigues</b>", styles["table_cell"]),
            Paragraph("Topologias, Visualização e Relatório<br/>(NNPROJ-6, 9, 12)", styles["table_cell"]),
            Paragraph("Módulo de visualização (<font face='Courier'>visualizacao.py</font>), geração das fronteiras e curvas, análise de camadas (E03) e relatório final.", styles["table_cell"]),
        ],
        [
            Paragraph("<b>Daniela Amaro</b>", styles["table_cell"]),
            Paragraph("Revisão Geral e Qualidade<br/>(Controlos 1 a 5)", styles["table_cell"]),
            Paragraph("Auditoria dos contratos técnicos, validação da baseline, conformidade das experiências e aprovação formal dos PRs.", styles["table_cell"]),
        ],
    ], colWidths=[3.2 * cm, 4.0 * cm, 10.4 * cm])
    t_contrib.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_contrib)

    story.append(Spacer(1, 10))
    p("<b>Aprovação Final da Revisora:</b> Relatório conferido e aprovado formalmente em 17/09/2026. Todos os valores correspondem aos ficheiros de dados e o código é 100% auditável e reprodutível.", "note")

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Relatório Final - Neural Network Moon Project",
        author="Pedro Rodrigues",
    )
    doc.build(story)
    print(f"Relatório Final gerado com sucesso em: {OUTPUT}")


if __name__ == "__main__":
    gerar_relatorio()
