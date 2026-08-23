from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from sklearn.datasets import make_moons
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

OUT = Path(__file__).parent / "figuras"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 15,
    "axes.labelsize": 11,
})

# Dados reprodutíveis.
X, y = make_moons(n_samples=300, noise=0.16, random_state=42)

# 1. Dados das duas luas.
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(X[y == 0, 0], X[y == 0, 1], c="#2563eb", label="Classe 0 (azul)", edgecolor="white", s=45)
ax.scatter(X[y == 1, 0], X[y == 1, 1], c="#dc2626", label="Classe 1 (vermelha)", edgecolor="white", s=45)
ax.set_title("Base de dados make_moons: duas classes entrelaçadas")
ax.set_xlabel("Característica x₀ (posição horizontal)")
ax.set_ylabel("Característica x₁ (posição vertical)")
ax.legend()
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "01_dados_duas_luas.png", dpi=180)
plt.close(fig)

# 2. Arquitetura 2-2-1.
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
positions = {
    "x0": (1.5, 4.1), "x1": (1.5, 1.9),
    "h0": (5.0, 4.1), "h1": (5.0, 1.9),
    "out": (8.5, 3.0),
}
colors = {"input": "#dbeafe", "hidden": "#fef3c7", "output": "#dcfce7"}
for source in ("x0", "x1"):
    for target in ("h0", "h1"):
        ax.add_patch(FancyArrowPatch(positions[source], positions[target], arrowstyle="->", mutation_scale=12, color="#64748b", lw=1.5))
for source in ("h0", "h1"):
    ax.add_patch(FancyArrowPatch(positions[source], positions["out"], arrowstyle="->", mutation_scale=12, color="#64748b", lw=1.5))
for key, label, group in [
    ("x0", "x₀", "input"), ("x1", "x₁", "input"),
    ("h0", "neurónio 0", "hidden"), ("h1", "neurónio 1", "hidden"),
    ("out", "probabilidade\ny₂", "output")]:
    x0, y0 = positions[key]
    circ = Circle((x0, y0), .65, facecolor=colors[group], edgecolor="#334155", lw=2, zorder=3)
    ax.add_patch(circ); ax.text(x0, y0, label, ha="center", va="center", fontsize=11, zorder=4)
ax.text(1.5, 5.35, "Entrada\n2 valores", ha="center", fontsize=13, weight="bold")
ax.text(5.0, 5.35, "Camada oculta\n2 neurónios", ha="center", fontsize=13, weight="bold")
ax.text(8.5, 5.35, "Saída\n1 neurónio", ha="center", fontsize=13, weight="bold")
ax.text(3.2, .55, "Cada seta representa um peso: quanto uma informação influencia a seguinte.", ha="center", fontsize=10)
ax.text(7.8, .55, "Os bias deslocam os limites de decisão.", ha="center", fontsize=10)
ax.set_title("Arquitetura da rede manual do exemplo4.py: 2 → 2 → 1", pad=10, fontsize=16, weight="bold")
fig.tight_layout()
fig.savefig(OUT / "02_arquitetura_221.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# 3. Modelo antes/depois usando MLP do sklearn para visualização equivalente.
Xs = StandardScaler().fit_transform(X)
Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=.25, random_state=42, stratify=y)
model = MLPClassifier(hidden_layer_sizes=(8, 8), activation="tanh", solver="sgd", learning_rate_init=.08,
                      max_iter=1, warm_start=True, random_state=7)
model.partial_fit(Xtr, ytr, classes=np.array([0, 1]))
initial_score = accuracy_score(yte, model.predict(Xte))
xx, yy = np.meshgrid(np.linspace(Xs[:,0].min()-.7, Xs[:,0].max()+.7, 350),
                     np.linspace(Xs[:,1].min()-.7, Xs[:,1].max()+.7, 350))
grid = np.c_[xx.ravel(), yy.ravel()]
initial_prob = model.predict_proba(grid)[:,1].reshape(xx.shape)
losses = [model.loss_]
for _ in range(399):
    model.partial_fit(Xtr, ytr)
    losses.append(model.loss_)
final_score = accuracy_score(yte, model.predict(Xte))
final_prob = model.predict_proba(grid)[:,1].reshape(xx.shape)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, zz, title in [
    (axes[0], initial_prob, f"Antes do treino\nacurácia de teste ≈ {initial_score:.1%}"),
    (axes[1], final_prob, f"Depois do treino\nacurácia de teste ≈ {final_score:.1%}")]:
    ax.contourf(xx, yy, zz, levels=np.linspace(0,1,21), cmap="RdBu_r", alpha=.65)
    ax.contour(xx, yy, zz, levels=[.5], colors="black", linewidths=2)
    ax.scatter(Xs[y==0,0], Xs[y==0,1], c="#2563eb", edgecolor="white", s=28)
    ax.scatter(Xs[y==1,0], Xs[y==1,1], c="#dc2626", edgecolor="white", s=28)
    ax.set_title(title); ax.set_xlabel("x₀ normalizado"); ax.set_ylabel("x₁ normalizado")
fig.suptitle("A fronteira preta é a regra aprendida pela rede", fontsize=16, weight="bold")
fig.tight_layout()
fig.savefig(OUT / "03_fronteira_antes_depois.png", dpi=180)
plt.close(fig)

# 4. Curva de aprendizagem.
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot(losses, color="#7c3aed", lw=2.3)
ax.set_title("Curva de aprendizagem: o erro diminui durante o treino")
ax.set_xlabel("Época")
ax.set_ylabel("Loss (medida de erro)")
ax.grid(alpha=.25)
ax.annotate("No início a rede erra mais", xy=(5, losses[5]), xytext=(65, losses[5]+.12),
            arrowprops=dict(arrowstyle="->", color="#475569"))
ax.annotate("Depois os ajustes tornam-se menores", xy=(350, losses[350]), xytext=(180, losses[350]+.13),
            arrowprops=dict(arrowstyle="->", color="#475569"))
fig.tight_layout()
fig.savefig(OUT / "04_curva_aprendizagem.png", dpi=180)
plt.close(fig)

# 5. Tradução visual do ciclo de aprendizagem.
fig, ax = plt.subplots(figsize=(11, 4.5)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 5)
steps = [
    (1.3, "1. Receber\nos dados", "#dbeafe"),
    (4.2, "2. Fazer\nprevisão", "#fef3c7"),
    (7.1, "3. Medir\no erro", "#fee2e2"),
    (10.0, "4. Ajustar\npesos", "#dcfce7"),
]
for x0, text, color in steps:
    box = FancyBboxPatch((x0-.9, 1.7), 1.8, 1.5, boxstyle="round,pad=0.12", facecolor=color, edgecolor="#334155", lw=1.8)
    ax.add_patch(box); ax.text(x0, 2.45, text, ha="center", va="center", fontsize=12, weight="bold")
for a, b in zip(steps[:-1], steps[1:]):
    ax.add_patch(FancyArrowPatch((a[0]+.95,2.45),(b[0]-.95,2.45),arrowstyle="->",mutation_scale=16,lw=2,color="#64748b"))
ax.add_patch(FancyArrowPatch((10,1.55),(1.3,1.55),connectionstyle="arc3,rad=-.32",arrowstyle="->",mutation_scale=16,lw=2,color="#7c3aed"))
ax.text(5.65,.38,"Repetir muitas vezes: a rede aprende por tentativa, erro e correção",ha="center",fontsize=12,color="#6d28d9",weight="bold")
ax.set_title("O ciclo de treino em linguagem simples", fontsize=17, weight="bold")
fig.tight_layout()
fig.savefig(OUT / "05_ciclo_treino.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# 6. Aplicações reais: classificação binária com fronteiras não lineares.
fig, ax = plt.subplots(figsize=(11, 6)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 7)
items = [
    (2.2,5.1,"Fraude bancária","normal ou suspeita","#dbeafe"),
    (6.0,5.1,"Manutenção industrial","máquina saudável ou risco","#fef3c7"),
    (9.8,5.1,"Saúde","resultado benigno ou suspeito","#dcfce7"),
    (3.8,2.1,"Cibersegurança","acesso legítimo ou ataque","#fee2e2"),
    (8.2,2.1,"Qualidade industrial","produto aprovado ou defeituoso","#ede9fe"),
]
for x0,y0,title,subtitle,color in items:
    box=FancyBboxPatch((x0-1.45,y0-.72),2.9,1.44,boxstyle="round,pad=.14",facecolor=color,edgecolor="#334155",lw=1.5)
    ax.add_patch(box); ax.text(x0,y0+.17,title,ha="center",va="center",fontsize=11.5,weight="bold")
    ax.text(x0,y0-.28,subtitle,ha="center",va="center",fontsize=9.5,color="#475569")
ax.text(6,6.55,"O mesmo princípio: observar características e escolher entre duas classes",ha="center",fontsize=16,weight="bold")
ax.text(6,.55,"No exemplo das luas, as características são coordenadas. No mundo real, podem ser valores financeiros, sensores, exames ou padrões de rede.",ha="center",fontsize=10.5,wrap=True)
fig.tight_layout()
fig.savefig(OUT / "06_aplicacoes_reais.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# 7. Roadmap das tarefas Jira.
fig, ax = plt.subplots(figsize=(12, 6.2)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 8)
columns = [
    (2.1,"ÉPICO 1\nCompreender e organizar",["1.1 Rede manual modular","1.2 Dados + baseline Keras","1.3 Fronteira de decisão"],"#dbeafe"),
    (6.0,"ÉPICO 2\nExperimentar alterações",["2.1 Funções de ativação","2.2 Novas bases de dados","2.3 Camadas e neurónios"],"#fef3c7"),
    (9.9,"ÉPICO 3\nComparar e comunicar",["3.1 Otimizadores/regularização","3.2 Métricas e benchmarks","3.3 Relatório final"],"#dcfce7"),
]
for x0,title,items,color in columns:
    box=FancyBboxPatch((x0-1.6,1),3.2,5.7,boxstyle="round,pad=.15",facecolor=color,edgecolor="#334155",lw=1.8)
    ax.add_patch(box); ax.text(x0,6.05,title,ha="center",va="center",fontsize=12.5,weight="bold")
    for i,item in enumerate(items):
        y0=4.75-i*1.25
        ax.text(x0,y0,"• "+item,ha="center",va="center",fontsize=10.5)
for x1,x2 in [(3.75,4.35),(7.65,8.25)]:
    ax.add_patch(FancyArrowPatch((x1,3.85),(x2,3.85),arrowstyle="->",mutation_scale=18,lw=2,color="#64748b"))
ax.text(6,.35,"Daniela: reviewer — verifica entendimento, resultados, justificações e qualidade da entrega.",ha="center",fontsize=11,weight="bold",color="#6d28d9")
ax.set_title("Mapa do projeto NNPROJ",fontsize=17,weight="bold")
fig.tight_layout()
fig.savefig(OUT / "07_roadmap_tarefas.png", dpi=180, bbox_inches="tight")
plt.close(fig)

print(f"Figuras criadas em: {OUT}")
print(f"Acurácia antes: {initial_score:.4f}; depois: {final_score:.4f}; loss final: {losses[-1]:.6f}")
