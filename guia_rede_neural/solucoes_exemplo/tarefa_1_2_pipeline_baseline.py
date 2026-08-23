"""Possível solução pedagógica para NNPROJ-5."""
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import Sequential
from keras.layers import Dense

X, y = make_moons(n_samples=500, noise=0.15, random_state=42)
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)
scaler = StandardScaler()
X_treino = scaler.fit_transform(X_treino)
X_teste = scaler.transform(X_teste)

modelo = Sequential([
    Dense(8, input_shape=(2,), activation="tanh"),
    Dense(8, activation="tanh"),
    Dense(1, activation="sigmoid"),
])
modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
historico = modelo.fit(
    X_treino, y_treino, validation_split=0.2,
    epochs=150, batch_size=16, verbose=0
)
loss, acc = modelo.evaluate(X_teste, y_teste, verbose=0)
print(f"Acurácia de teste: {acc:.3f}")
