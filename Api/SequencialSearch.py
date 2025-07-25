from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
import itertools
import time
from sklearn.model_selection import StratifiedKFold


def run_sequential_grid_search(X_train, y_train, param_grid, cv_folds=5):
    best_score = -1
    best_params = None
    best_model = None

    keys = param_grid.keys()
    param_combinations = list(itertools.product(*param_grid.values()))

    print(f"Iniciando búsqueda secuencial con {len(param_combinations)} combinaciones...")
    start_time = time.time()

    for i, combo_values in enumerate(param_combinations):
        current_params = dict(zip(keys, combo_values))
        
        fold_scores = []
        # StratifiedKFold es crucial para clasificacion con clases desbalanceadas
        skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
            X_fold_train, X_fold_val = X_train[train_idx], X_train[val_idx]
            y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]

            # Usar MLPClassifier
            model = MLPClassifier(**current_params, random_state=123)
            model.fit(X_fold_train, y_fold_train)
            
            y_pred = model.predict(X_fold_val)
            fold_scores.append(accuracy_score(y_fold_val, y_pred))
            
        mean_fold_score = sum(fold_scores) / len(fold_scores)
        
        if mean_fold_score > best_score:
            best_score = mean_fold_score
            best_params = current_params
            
            # Entrenar el mejor modelo con todos los datos de entrenamiento
            best_model_candidate = MLPClassifier(**best_params, random_state=123)
            best_model_candidate.fit(X_train, y_train)
            best_model = best_model_candidate

        if (i + 1) % 5 == 0 or (i + 1) == len(param_combinations): # Imprimir cada 5 para datasets más grandes
            print(f"  Completadas {i+1}/{len(param_combinations)} combinaciones. Mejor score actual: {best_score:.4f}")

    end_time = time.time()
    print(f"\nBúsqueda secuencial finalizada en {end_time - start_time:.2f} segundos.")
    return best_params, best_score, best_model