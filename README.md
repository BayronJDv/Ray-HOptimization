
# Comparación de Infraestructuras Paralelas y Distribuidas en ML con Ray

## Intención del Proyecto
Este proyecto busca comparar el rendimiento y eficiencia de infraestructuras de cómputo paralelas y distribuidas en problemas de machine learning, específicamente en la optimización de hiperparámetros de modelos. Se utiliza el framework Ray para implementar y evaluar búsquedas de hiperparámetros tanto de forma secuencial como paralela/distribuida, permitiendo analizar ventajas y desventajas de cada enfoque.

## Estructura de Archivos

```
Api/
  app.py                # API Flask principal
  Data.py               # Carga y preparación de datos
  SequencialSearch.py   # Búsqueda secuencial de hiperparámetros
  peticion.py           # Ejemplo de petición a la API
Client/                 # Frontend (React + Vite)
Ray/
  ParalelDisSearch.py   # Búsqueda paralela/distribuida con Ray
```

## Instrucciones de Uso de la API

1. Instala las dependencias del backend:
   ```
   pip install -r requirements.txt
   pip install ray  # Ray no está en requirements.txt porque puede dar problemas en Windows
   ```

2. Inicia la API:
   ```
   cd Api
   python app.py
   ```

3. Endpoints disponibles:

   - **/sequential-search** (POST): Realiza búsqueda secuencial de hiperparámetros y puede guardar el modelo en S3.
     - Body ejemplo:
       ```json
       {
         "param_grid": {
           "hidden_layer_sizes": [[5], [10]],
           "activation": ["relu"],
           "solver": ["adam"],
           "alpha": [0.001],
           "max_iter": [50]
         },
         "model_name": "modelo_seq_demo"
       }
       ```

   - **/parallel-search** (POST): Igual que el anterior pero usando Ray para búsqueda paralela.
     - Body igual al anterior, cambiando el endpoint.

   - **/list-models** (GET): Lista los modelos `.joblib` disponibles en el bucket S3.

   - **/predict** (POST): Realiza inferencia usando un modelo guardado en S3.
     - Body ejemplo:
       ```json
       {
         "model_name": "modelo_seq_demo",
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
       ```

4. Puedes ver ejemplos de uso de todos los endpoints en el archivo `Api/peticion.py`.

---

```

