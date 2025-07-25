from Data import X_train, X_test, y_train, y_test
from flask import Flask, jsonify, request
from flask_cors import CORS
from SequencialSearch import run_sequential_grid_search
from Ray.ParalelDisSearch import run_ray_parallel_grid_search
import ray
import os
import boto3
import joblib
from io import BytesIO



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

# Configuración S3 (ajusta estos valores a tu cuenta)
S3_BUCKET = 'tu-bucket-ml'
S3_REGION = 'us-east-1'
s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/', methods=['GET'])
def hello():
    return "Api en funcionamiento consulta la documentacion para su uso."


# Ruta para ejecutar la búsqueda secuencial
@app.route('/sequential-search', methods=['GET', 'POST'])
def sequential_search():
    # Intentar obtener el grid del cliente
    param_grid = None
    if request.is_json:
        param_grid = request.get_json().get('param_grid')
    if param_grid:
        print("Usando grid enviado por el cliente")
    else:
        print("Usando grid de prueba predefinido")
        param_grid = param_grid_mlp
    if not param_grid:
        return jsonify({'error': 'param_grid es requerido'}), 400
    model_name = request.get_json().get('model_name') if request.is_json else None
    best_params, best_score, best_model = run_sequential_grid_search(X_train.values, y_train.values, param_grid)
    # Guardar modelo en S3 si se proporciona nombre
    if model_name:
        buffer = BytesIO()
        joblib.dump(best_model, buffer)
        buffer.seek(0)
        s3.upload_fileobj(buffer, S3_BUCKET, f"{model_name}.joblib")
        print(f"Modelo guardado en S3 como {model_name}.joblib")
    return f"Mejores parámetros: {best_params}, Mejor score: {best_score:.4f}"

# Ruta para ejecutar la búsqueda paralela
@app.route('/parallel-search', methods=['GET', 'POST'])
def parallel_search():
    # Intentar obtener el grid del cliente
    param_grid = None
    if request.is_json:
        param_grid = request.get_json().get('param_grid')
    if param_grid:
        print("Usando grid enviado por el cliente")
    else:
        print("Usando grid de prueba predefinido")
        param_grid = param_grid_mlp
    if not param_grid:
        return jsonify({'error': 'param_grid es requerido'}), 400
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)
    model_name = request.get_json().get('model_name') if request.is_json else None
    best_params, best_score, best_model = run_ray_parallel_grid_search(X_train.values, y_train.values, param_grid)
    # Guardar modelo en S3 si se proporciona nombre
    if model_name:
        buffer = BytesIO()
        joblib.dump(best_model, buffer)
        buffer.seek(0)
        s3.upload_fileobj(buffer, S3_BUCKET, f"{model_name}.joblib")
        print(f"Modelo guardado en S3 como {model_name}.joblib")
    return f"Mejores parámetros (paralelo): {best_params}, Mejor score: {best_score:.4f}"
# Ruta para inferencia
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    model_name = data.get('model_name')
    features = [
        'age', 'gender', 'education', 'country', 'ethnicity',
        'nscore', 'escore', 'oscore', 'ascore', 'cscore', 'impulsive', 'ss'
    ]
    if not model_name or not all(f in data for f in features):
        return jsonify({'error': 'Faltan datos o nombre de modelo'}), 400
    # Descargar modelo de S3
    buffer = BytesIO()
    try:
        s3.download_fileobj(S3_BUCKET, f"{model_name}.joblib", buffer)
    except Exception as e:
        return jsonify({'error': f'No se pudo descargar el modelo: {str(e)}'}), 404
    buffer.seek(0)
    model = joblib.load(buffer)
    # Preparar input para predicción
    X_input = [[data[f] for f in features]]
    pred = model.predict(X_input)
    return jsonify({'prediction': int(pred[0])})

# Ruta para listar modelos en S3
@app.route('/list-models', methods=['GET'])
def list_models():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        models = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.joblib')]
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
