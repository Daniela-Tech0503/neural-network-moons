"""Possível solução pedagógica para NNPROJ-8."""
from sklearn.datasets import make_circles, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preparar_circulos():
    X, y = make_circles(n_samples=600, noise=0.08, factor=0.45, random_state=42)
    return separar_normalizar(X, y)

def preparar_cancer():
    dados = load_breast_cancer()
    return separar_normalizar(dados.data, dados.target)

def separar_normalizar(X, y):
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    scaler = StandardScaler()
    return scaler.fit_transform(Xtr), scaler.transform(Xte), ytr, yte
