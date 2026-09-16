from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from contratos import ConfiguracaoExperiencia, DadosPreparados


def preparar_dados(config: ConfiguracaoExperiencia) -> DadosPreparados:
    if config.dataset == "make_moons":
        X, y = make_moons(
            n_samples=config.numero_amostras,
            noise=config.ruido,
            random_state=config.seed,
        )
    elif config.dataset == "make_circles":
        X, y = make_circles(
            n_samples=config.numero_amostras,
            noise=config.ruido,
            random_state=config.seed,
        )
    else:
        raise ValueError(f"Dataset não suportado: {config.dataset}")

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=config.percentagem_teste, stratify=y, random_state=config.seed
    )

    scaler = StandardScaler()
    X_treino = scaler.fit_transform(X_treino)
    X_teste = scaler.transform(X_teste)

    return DadosPreparados(
        X_treino=X_treino,
        X_teste=X_teste,
        y_treino=y_treino,
        y_teste=y_teste,
        scaler=scaler,
    )
