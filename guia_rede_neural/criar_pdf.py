from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle,
    KeepTogether, Preformatted
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

BASE = Path(__file__).parent
FIG = BASE / "figuras"
SOL = BASE / "solucoes_exemplo"
OUTPUT = BASE.parent / "Guia_Projeto_Rede_Neural.pdf"

# Fonte com suporte robusto a acentos.
font_regular = Path("C:/Windows/Fonts/arial.ttf")
font_bold = Path("C:/Windows/Fonts/arialbd.ttf")
font_mono = Path("C:/Windows/Fonts/consola.ttf")
if font_regular.exists():
    pdfmetrics.registerFont(TTFont("ArialLocal", str(font_regular)))
    pdfmetrics.registerFont(TTFont("ArialLocalBold", str(font_bold)))
    BODY_FONT, BOLD_FONT = "ArialLocal", "ArialLocalBold"
else:
    BODY_FONT, BOLD_FONT = "Helvetica", "Helvetica-Bold"
if font_mono.exists():
    pdfmetrics.registerFont(TTFont("ConsolasLocal", str(font_mono)))
    MONO_FONT = "ConsolasLocal"
else:
    MONO_FONT = "Courier"

PAGE_W, PAGE_H = A4
styles0 = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle("TitleX", parent=styles0["Title"], fontName=BOLD_FONT, fontSize=25,
                            leading=30, textColor=colors.HexColor("#172554"), alignment=TA_CENTER, spaceAfter=18),
    "subtitle": ParagraphStyle("SubtitleX", parent=styles0["Normal"], fontName=BODY_FONT, fontSize=12,
                               leading=17, textColor=colors.HexColor("#475569"), alignment=TA_CENTER),
    "h1": ParagraphStyle("H1X", parent=styles0["Heading1"], fontName=BOLD_FONT, fontSize=18,
                          leading=22, textColor=colors.HexColor("#1e3a8a"), spaceBefore=10, spaceAfter=9),
    "h2": ParagraphStyle("H2X", parent=styles0["Heading2"], fontName=BOLD_FONT, fontSize=14,
                          leading=18, textColor=colors.HexColor("#6d28d9"), spaceBefore=8, spaceAfter=6),
    "h3": ParagraphStyle("H3X", parent=styles0["Heading3"], fontName=BOLD_FONT, fontSize=11.5,
                          leading=15, textColor=colors.HexColor("#0f766e"), spaceBefore=6, spaceAfter=4),
    "body": ParagraphStyle("BodyX", parent=styles0["BodyText"], fontName=BODY_FONT, fontSize=9.4,
                            leading=13.4, alignment=TA_JUSTIFY, textColor=colors.HexColor("#1f2937"), spaceAfter=6),
    "small": ParagraphStyle("SmallX", parent=styles0["BodyText"], fontName=BODY_FONT, fontSize=8,
                             leading=11, textColor=colors.HexColor("#475569"), spaceAfter=4),
    "bullet": ParagraphStyle("BulletX", parent=styles0["BodyText"], fontName=BODY_FONT, fontSize=9.2,
                              leading=13, leftIndent=14, firstLineIndent=-8, bulletIndent=3, spaceAfter=3),
    "note": ParagraphStyle("NoteX", parent=styles0["BodyText"], fontName=BODY_FONT, fontSize=8.8,
                            leading=12.5, backColor=colors.HexColor("#eff6ff"), borderColor=colors.HexColor("#93c5fd"),
                            borderWidth=0.7, borderPadding=7, spaceBefore=5, spaceAfter=7),
    "warn": ParagraphStyle("WarnX", parent=styles0["BodyText"], fontName=BODY_FONT, fontSize=8.8,
                            leading=12.5, backColor=colors.HexColor("#fff7ed"), borderColor=colors.HexColor("#fdba74"),
                            borderWidth=0.7, borderPadding=7, spaceBefore=5, spaceAfter=7),
    "code": ParagraphStyle("CodeX", fontName=MONO_FONT, fontSize=6.6, leading=8.4,
                            textColor=colors.HexColor("#111827"), backColor=colors.HexColor("#f8fafc"),
                            borderColor=colors.HexColor("#cbd5e1"), borderWidth=.5, borderPadding=6,
                            leftIndent=2, rightIndent=2, spaceBefore=4, spaceAfter=7),
}

story = []

def P(text, style="body"):
    story.append(Paragraph(text, styles[style]))

def H1(text):
    story.append(Paragraph(text, styles["h1"]))

def H2(text):
    story.append(Paragraph(text, styles["h2"]))

def H3(text):
    story.append(Paragraph(text, styles["h3"]))

def bullet(text):
    story.append(Paragraph("• " + text, styles["bullet"]))

def img(name, width=17*cm, caption=None):
    path = FIG / name
    im = Image(str(path))
    im._restrictSize(width, 11.5*cm)
    story.append(Spacer(1, 4))
    story.append(im)
    if caption:
        story.append(Paragraph(caption, styles["small"]))
    story.append(Spacer(1, 6))

def code(text):
    story.append(Preformatted(text.strip(), styles["code"], maxLineLength=105))

def page():
    story.append(PageBreak())

def section_box(title, simple, technical):
    data = [
        [Paragraph("Em linguagem simples", styles["h3"]), Paragraph("Nome técnico", styles["h3"])],
        [Paragraph(simple, styles["small"]), Paragraph(technical, styles["small"])],
    ]
    t = Table(data, colWidths=[8.2*cm, 8.2*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ("BOX", (0,0), (-1,-1), .6, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0,0), (-1,-1), .4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([Paragraph(title, styles["h2"]), t, Spacer(1, 7)]))

# CAPA
story.append(Spacer(1, 2.4*cm))
story.append(Paragraph("GUIA DO PROJETO DE REDE NEURAL", styles["title"]))
story.append(Paragraph("Leitura do exemplo4.py, aplicações práticas, tarefas do Jira e soluções possíveis", styles["subtitle"]))
story.append(Spacer(1, 1.0*cm))
img("02_arquitetura_221.png", width=16.5*cm)
story.append(Spacer(1, .4*cm))
meta = Table([
    ["Projeto Jira", "NNPROJ — Neural Network Moon Project"],
    ["Equipa", "3 executores + Daniela como reviewer"],
    ["Data de entrega", "26/09/2026"],
    ["Código de partida", "exemplo4.py — aula de 21/08/2026"],
], colWidths=[4.2*cm, 11.7*cm])
meta.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), BODY_FONT), ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#dbeafe")),
    ("BOX", (0,0), (-1,-1), .7, colors.HexColor("#93c5fd")),
    ("INNERGRID", (0,0), (-1,-1), .4, colors.HexColor("#bfdbfe")),
    ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 7),
]))
story.append(meta)
story.append(Spacer(1, .7*cm))
P("<b>Nota pedagógica:</b> as soluções incluídas são exemplos de caminhos possíveis. O objetivo é que o grupo compreenda, execute, compare e justifique as escolhas. Não existe uma única arquitetura correta.", "note")
page()

# ÍNDICE
H1("Índice")
for item in [
    "1. O problema explicado antes da matemática",
    "2. Dicionário: tradução da linguagem técnica",
    "3. Explicação detalhada do exemplo4.py",
    "4. O que o treino está realmente a fazer",
    "5. Aplicabilidade prática e real",
    "6. Plano das tarefas do Jira",
    "7. Possíveis soluções, código e explicação por tarefa",
    "8. Como comparar experiências corretamente",
    "9. Roteiro da reviewer e checklist de entrega",
    "10. Limitações e melhorias do código atual",
]:
    bullet(item)
P("Este guia começa pela intuição. A matemática e o código aparecem depois, quando já sabemos que pergunta cada linha está a tentar responder.", "note")
img("07_roadmap_tarefas.png", width=17*cm, caption="Visão geral das nove tarefas distribuídas pelos três épicos.")
page()

# 1
H1("1. O problema explicado antes da matemática")
P("O programa recebe pontos com duas coordenadas e tenta decidir a que grupo pertence cada ponto. Os grupos formam duas meias-luas encaixadas. A resposta correta de cada ponto já é conhecida: classe 0 ou classe 1. A rede observa exemplos, erra, corrige os seus parâmetros internos e volta a tentar.")
img("01_dados_duas_luas.png", width=16.5*cm, caption="Cada ponto é uma amostra. A cor é a resposta correta que a rede deve aprender.")
P("Uma linha reta não separa bem estas duas formas. Por isso, o exercício é interessante: obriga o modelo a combinar várias pequenas decisões para formar uma fronteira curva. A camada oculta é precisamente o mecanismo que dá essa flexibilidade.")
section_box("Amostra, característica e classe",
            "Uma amostra é um ponto. As características são as duas coordenadas usadas como pistas. A classe é a resposta azul (0) ou vermelha (1).",
            "X é a matriz de features com forma (n_amostras, 2). Y é o vetor de labels binárias com forma (n_amostras,).")
section_box("O que significa aprender?",
            "Aprender é descobrir valores para os botões internos da rede que façam menos previsões erradas.",
            "Treinar é otimizar pesos e bias minimizando uma função de perda através de gradiente descendente e backpropagation.")

# 2
H1("2. Dicionário: tradução da linguagem técnica")
terms = [
    ("Rede neural", "Um conjunto de pequenas unidades de cálculo ligadas entre si."),
    ("Neurónio", "Uma calculadora: combina entradas, pesos e bias, depois aplica uma função."),
    ("Peso (weight)", "A importância atribuída a uma informação. Peso alto = grande influência."),
    ("Bias ou viés", "Um ajuste adicional que desloca o ponto em que o neurónio muda de opinião."),
    ("Camada oculta", "Etapa intermédia que transforma as pistas para criar decisões não lineares."),
    ("Ativação", "Regra que transforma o resultado de um neurónio. Ex.: sigmoid, tanh, ReLU."),
    ("Forward pass", "Caminho para a frente: dos dados até à previsão."),
    ("Loss", "Número que mede quanto a previsão se afastou da resposta correta."),
    ("Gradiente", "Indicação da direção em que cada parâmetro aumenta mais o erro."),
    ("Backpropagation", "Processo de repartir a responsabilidade do erro pelas ligações da rede."),
    ("Taxa de aprendizagem", "Tamanho do passo usado ao corrigir pesos e bias."),
    ("Época", "Uma passagem de treino pelo conjunto de exemplos."),
    ("Batch", "Grupo de exemplos processado antes de atualizar os parâmetros."),
    ("Acurácia", "Percentagem de previsões classificadas corretamente."),
    ("Overfitting", "Quando o modelo memoriza o treino e piora em dados novos."),
]
table_data = [[Paragraph("Termo", styles["h3"]), Paragraph("Tradução simples", styles["h3"])]]
for a,b in terms:
    table_data.append([Paragraph(a, styles["small"]), Paragraph(b, styles["small"])])
t = Table(table_data, colWidths=[4.2*cm, 12.2*cm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ddd6fe")), ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#94a3b8")),
    ("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#cbd5e1")), ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(t)
page()

# 3
H1("3. Explicação detalhada do exemplo4.py")
H2("3.1 Importações — linhas 1 a 7")
code("""from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras import initializers""")
P("<b>sklearn</b> cria a base de dados; <b>NumPy</b> trabalha com vetores e matrizes; <b>Matplotlib</b> cria o gráfico; <b>Keras</b> constrói a segunda rede, de modo automático. A importação <i>initializers</i> não é usada no código atual e pode ser removida sem alterar o resultado.")

H2("3.2 Criação e visualização dos dados — linhas 9 a 14")
code("""X, Y = datasets.make_moons(100, noise=0.1)
color = ['blue' if k == 0 else 'red' for k in Y]
plt.scatter(X[:, 0], X[:, 1], c=color)
plt.savefig('duas_luas.svg')""")
P("São criados 100 pontos. O parâmetro <b>noise=0.1</b> acrescenta pequenas irregularidades, tornando o problema mais parecido com dados reais. <code>X[:, 0]</code> significa «todas as linhas da primeira coluna»; <code>X[:, 1]</code> significa «todas as linhas da segunda coluna». Y guarda a resposta correta de cada ponto.")
P("O código não define <code>random_state</code>. Portanto, cada execução pode gerar pontos diferentes e resultados diferentes. Para um trabalho comparável, recomenda-se fixar uma seed.", "warn")

H2("3.3 A função sigmoid — linhas 17 a 18")
code("""def sigmoid(x):
    return 1 / (1 + np.exp(-x))""")
P("A sigmoid comprime qualquer número para o intervalo entre 0 e 1. Isso permite tratar a saída como um grau de confiança. Exemplo: 0,92 pode ser interpretado como forte confiança na classe 1. O limite de 0,5 converte esse valor contínuo numa decisão 0 ou 1.")
P("Tecnicamente, a derivada usada depois é <code>sigmoid(x) * (1 - sigmoid(x))</code>. O código já possui a saída y, por isso escreve simplesmente <code>y * (1-y)</code>.")

H2("3.4 run_neural_net: apenas prever — linhas 21 a 39")
P("Esta função executa o caminho para a frente. Ela não aprende e não altera pesos. Recebe um ponto e os parâmetros já existentes, calcula os dois neurónios ocultos, calcula o neurónio de saída e devolve a classe prevista.")
code("""s00 = w0[0, 0] * x[0]
s01 = w0[0, 1] * x[1]
s02 = s00 + s01
v0 = s02 + b0[0]
y0 = sigmoid(v0)""")
P("Tradução linha a linha: multiplicar a primeira coordenada pelo primeiro peso; multiplicar a segunda pelo segundo peso; somar as duas contribuições; acrescentar o bias; passar o resultado pela sigmoid. O segundo neurónio oculto repete a mesma receita com outros pesos.")
code("""v2 = y0 * w1[0] + y1 * w1[1] + b1[0]
y2 = sigmoid(v2)
return 1 if y2 > 0.5 else 0""")
P("O neurónio final combina as duas opiniões intermédias. Se a confiança na classe 1 ultrapassar 50%, devolve 1; caso contrário, devolve 0.")
img("02_arquitetura_221.png", width=16.6*cm)

H2("3.5 neural_net: prever, medir o erro e calcular correções — linhas 42 a 103")
P("A primeira metade repete o forward pass, mas mantém todos os valores intermédios necessários para calcular o erro e os gradientes.")
code("""e = y2 - d
L = 1/2 * (e ** 2)""")
P("<code>d</code> é a resposta desejada. <code>e</code> é a diferença entre a previsão e essa resposta. A loss quadrática torna o erro sempre positivo e penaliza mais os erros grandes. O fator 1/2 é usado porque simplifica a derivada: a derivada de 1/2 × e² é e.")
P("Na segunda metade, o código percorre mentalmente a rede no sentido contrário. Começa no erro da saída e calcula quanto cada peso e bias contribuiu para esse erro. Isso é backpropagation.")
code("""grad_v2 = e * y2 * (1 - y2)
grad_w1[0] = grad_v2 * y0
grad_w1[1] = grad_v2 * y1""")
P("A primeira linha mede quanto o valor anterior à sigmoid da saída deve mudar. As linhas seguintes medem a responsabilidade dos pesos que ligam os neurónios ocultos à saída. O mesmo raciocínio continua até chegar aos pesos ligados às duas entradas.")

H2("3.6 main: inicialização, treino e avaliação — linhas 105 a 154")
code("""w0 = np.random.rand(2, 2)
w1 = np.random.rand(2)
b0 = np.random.rand(2)
b1 = np.random.rand(1)
taxa = 0.1""")
P("A rede começa com opiniões aleatórias. A taxa 0,1 controla a força de cada correção. Se for demasiado alta, a rede pode saltar de um lado para o outro; se for demasiado baixa, pode aprender muito lentamente.")
code("""for i in range(10000):
    ...
    for k in range(100):
        g_w0, g_b0, g_w1, g_b1, L = neural_net(...)
        grad_w0 += g_w0
        ...
    w0 -= taxa * grad_w0""")
P("Em cada uma das 10.000 épocas, o código calcula os gradientes das 100 amostras e soma-os. Depois atualiza os parâmetros uma vez. Isso é batch gradient descent.")
P("A soma dos gradientes não é dividida por 100. Logo, a dimensão da atualização cresce com o número de amostras. Uma versão mais estável usaria a média dos gradientes ou uma taxa menor.", "warn")

H2("3.7 A versão Keras — linhas 156 a 165")
code("""model = Sequential()
model.add(Dense(5, input_dim=2, activation='relu'))
model.add(Dense(5, activation='tanh'))
model.add(Dense(1, activation='sigmoid'))
opt = SGD(learning_rate=taxa)
model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])
model.fit(X, Y, epochs=100, verbose=False, batch_size=5)
acc = model.evaluate(X, Y)""")
P("Keras executa automaticamente as multiplicações, as ativações, o backpropagation e as atualizações. Esta rede é 2 → 5 → 5 → 1, portanto é diferente da rede manual 2 → 2 → 1. A comparação atual não isola uma única mudança.")
P("Para classificação binária, <code>binary_crossentropy</code> costuma ser uma escolha mais adequada do que erro quadrático. Além disso, o código avalia no mesmo conjunto usado no treino e não imprime o resultado de <code>model.evaluate</code>. Para medir generalização, deve separar treino e teste.", "warn")

# 4
H1("4. O que o treino está realmente a fazer")
img("05_ciclo_treino.png", width=17*cm)
P("O treino não guarda uma regra escrita por uma pessoa. Ele ajusta números. Depois de muitas correções, esses números combinam-se para produzir uma fronteira que separa as classes. A linha preta abaixo é essa regra aprendida.")
img("03_fronteira_antes_depois.png", width=17*cm, caption="Experiência reproduzível equivalente: a acurácia de teste passou de cerca de 64% para 97,3%.")
img("04_curva_aprendizagem.png", width=15.5*cm)
P("Uma loss descendente é um bom sinal, mas não basta. Devemos acompanhar também a loss de validação/teste. Se a loss de treino continuar a cair enquanto a de validação sobe, o modelo pode estar a memorizar os exemplos.")

# 5
H1("5. Aplicabilidade prática e real")
img("06_aplicacoes_reais.png", width=17*cm)
P("O exercício das luas é uma simplificação de um problema real: <b>classificação binária</b>. Recebemos várias características e escolhemos entre duas categorias. No mundo real há mais variáveis, mais ruído, custos de erro diferentes e obrigações de explicabilidade.")
applications = [
    ("Fraude bancária", "valor, localização, hora, dispositivo, histórico", "transação normal ou suspeita", "bloquear uma operação legítima também tem custo"),
    ("Manutenção preditiva", "temperatura, vibração, pressão, corrente", "funcionamento saudável ou risco de falha", "um falso negativo pode causar avaria"),
    ("Triagem de saúde", "medições clínicas e resultados de exames", "baixo risco ou caso a investigar", "a rede apoia; não substitui decisão clínica"),
    ("Cibersegurança", "frequência de acesso, origem, padrão de pedidos", "atividade legítima ou potencial ataque", "os padrões mudam com o tempo"),
    ("Qualidade industrial", "medidas, sensores, imagem da peça", "produto aprovado ou defeituoso", "é necessário controlar iluminação e calibração"),
]
data = [["Aplicação", "Características", "Classes", "Cuidado real"]] + applications
t = Table([[Paragraph(str(c), styles["small"]) for c in row] for row in data], colWidths=[3*cm,4.7*cm,4.4*cm,4.4*cm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ccfbf1")), ("FONTNAME",(0,0),(-1,0),BOLD_FONT),
    ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#94a3b8")), ("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#cbd5e1")),
    ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(t)
P("A forma das duas luas não representa literalmente fraude ou doença. Ela demonstra uma ideia: a relação entre características e resposta pode ser curva e complexa, e uma rede neural consegue aprender relações que uma única linha reta não consegue.", "note")

# 6
H1("6. Plano das tarefas do Jira")
P("O projeto foi dividido em três fases: compreender e organizar; experimentar alterações; comparar e comunicar. Cada tarefa deve terminar com código executável, resultados guardados e uma explicação que outra pessoa consiga reproduzir.")
img("07_roadmap_tarefas.png", width=17*cm)

jira_tasks = [
("NNPROJ-4 — Rede manual modular", "Luciana", "Transformar cálculos fixos numa estrutura reutilizável.", "A rede aceita dimensões configuráveis; gradientes verificados; comparação com o original."),
("NNPROJ-5 — Pipeline e baseline Keras", "Helton", "Separar treino/teste, normalizar e criar referência justa.", "Seed fixa; sem fuga de dados; métricas de treino e teste registadas."),
("NNPROJ-6 — Fronteira de decisão", "Pedro", "Mostrar visualmente o que a rede aprendeu.", "Gráficos antes/depois e legenda clara para o limite 0,5."),
("NNPROJ-7 — Ativações", "Luciana", "Comparar sigmoid, tanh, ReLU, LeakyReLU e ELU.", "Uma variável alterada de cada vez; tabela e curvas de convergência."),
("NNPROJ-8 — Novos datasets", "Helton", "Testar círculos e uma base real.", "Pré-processamento adequado; métricas e limitações explicadas."),
("NNPROJ-9 — Topologias", "Pedro", "Variar camadas e neurónios.", "Número de parâmetros, desempenho e sinais de overfitting comparados."),
("NNPROJ-10 — Otimizadores/regularização", "Luciana", "Comparar SGD, momentum, Adam, L2 e dropout.", "Mesmos dados/seeds; curvas treino-validação; conclusão justificada."),
("NNPROJ-11 — Benchmark", "Helton", "Consolidar accuracy, precision, recall, F1, loss e tempo.", "CSV/tabela reproduzível e definição das métricas."),
("NNPROJ-12 — Relatório", "Pedro", "Organizar pergunta, método, resultados e conclusão.", "Texto revisto por Daniela; figuras numeradas; resultados rastreáveis."),
]
data = [["Tarefa", "Executor", "Pergunta", "Pronto quando..."]]
for row in jira_tasks:
    data.append(list(row))
t = Table([[Paragraph(str(c), styles["small"]) for c in row] for row in data], colWidths=[4.1*cm,2.6*cm,4.3*cm,5.5*cm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#dbeafe")), ("FONTNAME",(0,0),(-1,0),BOLD_FONT),
    ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#94a3b8")), ("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#cbd5e1")),
    ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(t)
page()

# 7 soluções
H1("7. Possíveis soluções, código e explicação por tarefa")
P("Os exemplos abaixo são esqueletos pedagógicos. Devem ser executados, completados, comentados e adaptados pela equipa. Os ficheiros correspondentes estão na pasta guia_rede_neural/solucoes_exemplo.", "note")

solutions = [
("NNPROJ-4 — Modularizar a rede manual", "tarefa_1_1_rede_manual_modular.py",
 "Criar objetos para a camada densa e para a ativação. Assim, a dimensão deixa de estar presa a exatamente dois neurónios.",
 "DenseManual.forward guarda X porque o backward precisará dele. O operador @ é multiplicação matricial. No backward, X.T @ grad_saida calcula como cada peso influenciou o erro. atualizar aplica gradiente descendente."),
("NNPROJ-5 — Pipeline e baseline", "tarefa_1_2_pipeline_baseline.py",
 "Separar dados antes de normalizar. O StandardScaler aprende apenas no treino e transforma treino/teste com a mesma regra.",
 "stratify preserva a proporção das classes. validation_split acompanha dados não usados nas atualizações. binary_crossentropy é a loss habitual para uma saída sigmoid binária."),
("NNPROJ-6 — Fronteira de decisão", "tarefa_1_3_fronteira_decisao.py",
 "Criar uma grelha de pontos imaginários, pedir uma previsão para cada ponto e pintar o plano segundo a probabilidade.",
 "meshgrid constrói a grelha. contourf pinta regiões. contour desenha a linha em que probabilidade = 0,5, isto é, a fronteira de decisão."),
("NNPROJ-7 — Funções de ativação", "tarefa_2_1_ativacoes.py",
 "Construir o mesmo modelo várias vezes, alterando somente a ativação.",
 "A comparação deve manter seed, split, número de camadas, neurónios, épocas e otimizador. Caso contrário, não saberemos qual alteração causou a diferença."),
("NNPROJ-8 — Novas bases", "tarefa_2_2_novos_datasets.py",
 "Criar funções de preparação com a mesma interface para círculos e para breast cancer.",
 "A base real tem muitas características, portanto o input_shape do Keras deve ser X_treino.shape[1], e não 2. A fronteira 2D só é diretamente aplicável a duas características."),
("NNPROJ-9 — Camadas e neurónios", "tarefa_2_3_topologias.py",
 "Percorrer combinações de profundidade e largura, treinando e guardando resultados numa tabela.",
 "count_params mede a complexidade. Mais parâmetros podem melhorar a flexibilidade, mas também aumentar tempo e overfitting. A seleção deve usar validação, não o teste final."),
("NNPROJ-10 — Otimizadores e regularização", "tarefa_3_1_otimizadores_regularizacao.py",
 "Criar uma função que devolve variantes controladas do modelo.",
 "Momentum acumula direção; Adam adapta o tamanho dos passos; L2 penaliza pesos grandes; dropout desliga aleatoriamente unidades durante o treino. Regularização deve ser avaliada pela diferença treino-validação."),
("NNPROJ-11 — Benchmark", "tarefa_3_2_benchmark.py",
 "Executar cada modelo da mesma forma e devolver um dicionário de métricas.",
 "Accuracy mede acertos totais; precision pergunta quantos positivos previstos eram corretos; recall pergunta quantos positivos reais foram encontrados; F1 equilibra precision e recall."),
("NNPROJ-12 — Relatório", "tarefa_3_3_relatorio.py",
 "Ler o CSV do benchmark e gerar uma tabela Markdown para reduzir erros de transcrição.",
 "O script automatiza a tabela, mas não substitui a interpretação. O grupo deve explicar por que um modelo funcionou melhor, quais limitações existem e se a diferença é consistente."),
]

for idx, (title, filename, approach, explanation) in enumerate(solutions, 1):
    H2(f"7.{idx} {title}")
    P("<b>Ideia:</b> " + approach)
    source = (SOL / filename).read_text(encoding="utf-8")
    code(source)
    P("<b>Como ler este código:</b> " + explanation)
    P(f"<b>Verificação sugerida:</b> executar {filename}, guardar resultados e comparar com uma baseline usando a mesma seed e o mesmo split.", "small")
    if idx in (3,6):
        page()

# 8
H1("8. Como comparar experiências corretamente")
P("Uma experiência científica tenta responder a uma pergunta controlada. Se mudarmos dataset, ativação, arquitetura, épocas e otimizador ao mesmo tempo, não conseguimos atribuir o resultado a uma causa.")
for b in [
    "Fixar random_state e, quando possível, seeds do NumPy e TensorFlow.",
    "Usar o mesmo split treino/validação/teste para modelos comparados.",
    "Normalizar usando apenas estatísticas do treino.",
    "Alterar uma variável de cada vez ou declarar claramente um desenho fatorial.",
    "Executar várias seeds e apresentar média e desvio-padrão, não apenas a melhor execução.",
    "Não escolher o modelo olhando repetidamente para o teste; usar validação para escolhas e teste uma vez no fim.",
    "Guardar arquitetura, parâmetros, tempo, curvas e versão das bibliotecas.",
]:
    bullet(b)
H2("Tabela mínima recomendada")
data = [
    ["Experiência","Dataset","Topologia","Ativação","Otimizador","Val. acc","Teste acc","F1","Tempo"],
    ["E01","moons","2-5-5-1","relu/tanh","SGD","...","...","...","..."],
    ["E02","moons","2-8-8-1","tanh","Adam","...","...","...","..."],
]
t = Table([[Paragraph(c,styles["small"]) for c in row] for row in data], colWidths=[1.65*cm]*9, repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#fef3c7")),("FONTNAME",(0,0),(-1,0),BOLD_FONT),
    ("BOX",(0,0),(-1,-1),.5,colors.HexColor("#94a3b8")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#cbd5e1")),
    ("VALIGN",(0,0),(-1,-1),"TOP"),("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(t)

# 9
H1("9. Roteiro da reviewer e checklist de entrega")
H2("Perguntas que Daniela pode fazer em cada revisão")
for b in [
    "Que pergunta esta experiência tenta responder?",
    "O que foi mantido constante e o que foi alterado?",
    "O teste usa dados que o modelo nunca viu durante o treino?",
    "A conclusão é apoiada por números e gráficos?",
    "O resultado pode ser reproduzido com seed, dependências e instruções?",
    "O código está explicado pelo autor, ou foi apenas copiado?",
    "Há sinais de overfitting? Como foram identificados?",
    "Quais erros seriam mais graves numa aplicação real: falsos positivos ou falsos negativos?",
]:
    bullet(b)
H2("Checklist final")
checks = [
    "Código original preservado e nova versão identificada.",
    "README com instalação e execução no VS Code/Jupyter.",
    "Treino, validação e teste separados.",
    "Seeds e versões registadas.",
    "Pelo menos uma alteração de arquitetura/ativação/dataset bem justificada.",
    "Gráficos com título, eixos, legenda e fonte dos dados.",
    "Tabela comparativa com métricas.",
    "Discussão de limitações e aplicações reais.",
    "Contribuições dos quatro membros declaradas.",
    "Revisão final antes de 26/09/2026.",
]
for x in checks:
    bullet("☐ " + x)

# 10
H1("10. Limitações e melhorias do código atual")
limitations = [
("Sem seed", "Resultados mudam entre execuções.", "Definir random_state e np.random.seed."),
("Treino e avaliação nos mesmos 100 pontos", "A acurácia pode parecer melhor do que a generalização real.", "Criar treino/validação/teste."),
("Gradientes somados, não promediados", "A atualização depende do número de amostras.", "Dividir gradientes por len(X) ou usar mini-batches."),
("Manual e Keras com arquiteturas diferentes", "A comparação não é controlada.", "Comparar topologias equivalentes primeiro."),
("MSE na classificação Keras", "Pode convergir de forma menos adequada.", "Testar binary_crossentropy e justificar."),
("Resultado Keras não impresso", "A avaliação fica invisível.", "Imprimir loss e accuracy ou guardar no benchmark."),
("Poucas métricas", "Accuracy pode esconder tipos de erro.", "Adicionar matriz de confusão, precision, recall e F1."),
("Código fixo em dois neurónios", "Dificulta experiências de topologia.", "Modularizar camadas e dimensões."),
]
data=[["Limitação","Por que importa","Melhoria"]]+[list(x) for x in limitations]
t=Table([[Paragraph(c,styles["small"]) for c in row] for row in data],colWidths=[4.3*cm,6.1*cm,6.1*cm],repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#fee2e2")),("FONTNAME",(0,0),(-1,0),BOLD_FONT),
    ("BOX",(0,0),(-1,-1),.6,colors.HexColor("#94a3b8")),("INNERGRID",(0,0),(-1,-1),.3,colors.HexColor("#cbd5e1")),
    ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(t)
P("Conclusão: o exemplo4.py é valioso porque expõe a matemática escondida pelas bibliotecas. O projeto torna-se mais forte quando preserva essa compreensão e, em seguida, introduz práticas reais: dados separados, experiências controladas, métricas adequadas, visualizações e interpretação.", "note")

# Apêndice de artefactos
H1("Apêndice — Ficheiros produzidos")
for b in [
    "Guia_Projeto_Rede_Neural.pdf — este documento.",
    "guia_rede_neural/figuras — gráficos e diagramas gerados.",
    "guia_rede_neural/gerar_figuras.py — script reproduzível das figuras.",
    "guia_rede_neural/solucoes_exemplo — nove soluções pedagógicas separadas.",
]:
    bullet(b)
P("Os exemplos Keras foram verificados sintaticamente, mas requerem TensorFlow/Keras instalado no ambiente em que forem executados. As imagens empíricas deste guia foram geradas com scikit-learn para permitir validação no ambiente atual.", "warn")


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.line(2*cm, 1.45*cm, PAGE_W-2*cm, 1.45*cm)
    canvas.setFont(BODY_FONT, 7.5)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(2*cm, 1.0*cm, "Guia do Projeto de Rede Neural — NNPROJ")
    canvas.drawRightString(PAGE_W-2*cm, 1.0*cm, f"Página {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=1.7*cm, leftMargin=1.7*cm,
    topMargin=1.7*cm, bottomMargin=1.8*cm,
    title="Guia do Projeto de Rede Neural",
    author="Daniela Amaro e equipa — material pedagógico",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
