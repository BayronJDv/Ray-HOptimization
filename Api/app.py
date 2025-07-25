from Data import X_train, X_test, y_train, y_test
from flask import Flask, jsonify, request
from flask_cors import CORS
from SequencialSearch import run_sequential_grid_search
import ray
import importlib.util
import os

# Cargar el módulo con nombre no estándar usando importlib
ray_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ray/Paralel&DisSearch.py'))
spec = importlib.util.spec_from_file_location('paralel_search', ray_module_path)
paralel_search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paralel_search)

#hiperparametros para el grid search temporales
param_grid_mlp = {
    'hidden_layer_sizes': [(12, 7), (15, 10, 5)], # Diferentes arquitecturas de capas ocultas
    'activation': ['relu', 'tanh'],                          # Función de activación
    'solver': ['adam', 'sgd'],                               # Algoritmo para optimización de pesos
    'alpha': [ 0.001, 0.01],                          # Parámetro de regularización L2
    'max_iter': [50,100,200]                                   # Número máximo de iteraciones
}
    

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return "Api en funcionamiento consulta la documentacion para su uso."


# Ruta para ejecutar la búsqueda secuencial
@app.route('/sequential-search', methods=['GET', 'POST'])
def sequential_search():
    param_grid = param_grid_mlp  # Usar el grid predefinido para pruebas
    if not param_grid:
        return jsonify({'error': 'param_grid es requerido'}), 400
    best_params, best_score, _ = run_sequential_grid_search(X_train.values, y_train.values, param_grid)
    return f"Mejores parámetros: {best_params}, Mejor score: {best_score:.4f}"

# Ruta para ejecutar la búsqueda paralela
@app.route('/parallel-search', methods=['GET', 'POST'])
def parallel_search():
    param_grid = param_grid_mlp  # Usar el grid predefinido para pruebas
    if not param_grid:
        return jsonify({'error': 'param_grid es requerido'}), 400
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)
    best_params, best_score, _ = paralel_search.run_ray_parallel_grid_search(X_train.values, y_train.values, param_grid)
    return f"Mejores parámetros (paralelo): {best_params}, Mejor score: {best_score:.4f}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
