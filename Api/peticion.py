import requests

BASE = "http://localhost:5000"

# 1. Ejemplo de búsqueda secuencial con grid y nombre de modelo
print("\n--- Sequential Search ---")
param_grid = {
    "hidden_layer_sizes": [[5], [10]],
    "activation": ["relu"],
    "solver": ["adam"],
    "alpha": [0.001],
    "max_iter": [50]
}
payload = {"param_grid": param_grid, "model_name": "modelo_seq_demo"}
resp = requests.post(f"{BASE}/sequential-search", json=payload)
print(resp.text)

# 2. Ejemplo de búsqueda paralela con grid y nombre de modelo
print("\n--- Parallel Search ---")
payload = {"param_grid": param_grid, "model_name": "modelo_paralelo_demo"}
resp = requests.post(f"{BASE}/parallel-search", json=payload)
print(resp.text)

# # 3. Listar modelos disponibles en S3
# print("\n--- Listar modelos en S3 ---")
# resp = requests.get(f"{BASE}/list-models")
# print(resp.text)

# # 4. Inferencia con un modelo guardado
# print("\n--- Inferencia ---")
# predict_payload = {
#     "model_name": "modelo_seq_demo",
#     "age": 25,
#     "gender": 1,
#     "education": 3,
#     "country": 2,
#     "ethnicity": 1,
#     "nscore": 0.5,
#     "escore": 0.3,
#     "oscore": 0.2,
#     "ascore": 0.1,
#     "cscore": 0.4,
#     "impulsive": 0.6,
#     "ss": 0.7
# }
# resp = requests.post(f"{BASE}/predict", json=predict_payload)
# print(resp.text)
