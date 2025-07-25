# --- Implementación Paralela con Ray de la busqueda de hiperparámetros ---
import ray
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
import itertools
import time
from sklearn.model_selection import StratifiedKFold


@ray.remote
def train_and_evaluate_mlp(X_train_data, y_train_data, params, cv_folds=5, random_state=123):
    # Asegúrate de que los datos se manejen correctamente como NumPy arrays dentro de la función remota
    # Si X_train_data y y_train_data se pasaron directamente, ya son NumPy arrays.
    
    fold_scores = []
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    
    for train_idx, val_idx in skf.split(X_train_data, y_train_data):
        X_fold_train, X_fold_val = X_train_data[train_idx], X_train_data[val_idx]
        y_fold_train, y_fold_val = y_train_data[train_idx], y_train_data[val_idx]

        model = MLPClassifier(**params, random_state=random_state)
        model.fit(X_fold_train, y_fold_train)
        
        y_pred = model.predict(X_fold_val)
        fold_scores.append(accuracy_score(y_fold_val, y_pred))
        
    mean_fold_score = sum(fold_scores) / len(fold_scores)
    return mean_fold_score, params

def run_ray_parallel_grid_search(X_train, y_train, param_grid, cv_folds=5):
    keys = param_grid.keys()
    param_combinations = list(itertools.product(*param_grid.values()))

    print(f"Iniciando búsqueda paralela (Ray) con {len(param_combinations)} combinaciones...")
    start_time = time.time()

    # Enviar cada combinación como una tarea remota de Ray
    futures = [train_and_evaluate_mlp.remote(X_train, y_train, dict(zip(keys, combo)), cv_folds)
               for combo in param_combinations]

    results = []
    
    # Process results as they become available for better user experience
    while len(futures) > 0:
        ready_futures, remaining_futures = ray.wait(futures, num_returns=1)
        if ready_futures:
            result = ray.get(ready_futures[0])
            results.append(result)
            futures = remaining_futures
            print(f"  Tarea completada. Quedan {len(remaining_futures)} tareas.")
        else:
            # Should not happen if futures list is not empty
            print("No hay tareas listas aún...")
            time.sleep(1) # Wait a bit before retrying

    best_score = -1
    best_params = None
    
    for score, params in results:
        if score > best_score:
            best_score = score
            best_params = params

    end_time = time.time()
    print(f"\nBúsqueda paralela (Ray) finalizada en {end_time - start_time:.2f} segundos.")
    
    # Entrenar el mejor modelo con los mejores hiperparámetros en todo el conjunto de entrenamiento
    best_model = MLPClassifier(**best_params, random_state=123)
    best_model.fit(X_train, y_train)

    
    #aqui se deberia guardar ese modelo para su uso posterior

    return best_params, best_score, best_model