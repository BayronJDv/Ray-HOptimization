import requests

BASE = "http://localhost:5000"


# Ejemplo de búsqueda secuencial y paralela con predicción
print("\n--- Sequential Search & Predict ---")
param_grid = {
    "hidden_layer_sizes": [[5], [10]],
    "activation": ["relu"],
    "solver": ["adam"],
    "alpha": [0.001],
    "max_iter": [50]
}
payload = {
    "param_grid": param_grid,
    "age": 25,
    "gender": 1,
    "education": 3,
    "country": 2,
    "ethnicity": 1,
    "nscore": 0.5,
    "escore": 0.3,
    "oscore": 0.2,
    "ascore": 0.1,
    "cscore": 0.4,
    "impulsive": 0.6,
    "ss": 0.7
}
resp = requests.post(f"{BASE}/sequential-search", json=payload)
print(resp.text)

# print("\n--- Parallel Search & Predict ---")
# resp = requests.post(f"{BASE}/parallel-search", json=payload)
# print(resp.text)
