"""Possível solução pedagógica para NNPROJ-4.
Generaliza uma camada densa e ativações sem alterar exemplo4.py.
"""
import numpy as np

class DenseManual:
    def __init__(self, entradas, saidas, seed=42):
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 0.3, size=(entradas, saidas))
        self.b = np.zeros(saidas)

    def forward(self, X):
        self.X = X
        return X @ self.W + self.b

    def backward(self, grad_saida):
        self.grad_W = self.X.T @ grad_saida / len(self.X)
        self.grad_b = grad_saida.mean(axis=0)
        return grad_saida @ self.W.T

    def atualizar(self, taxa):
        self.W -= taxa * self.grad_W
        self.b -= taxa * self.grad_b

class TanhManual:
    def forward(self, Z):
        self.Y = np.tanh(Z)
        return self.Y

    def backward(self, grad_saida):
        return grad_saida * (1 - self.Y ** 2)
