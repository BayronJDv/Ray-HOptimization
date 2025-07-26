
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
  Ray/
    ParalelDisSearch.py # Búsqueda paralela/distribuida con Ray
Client/                 # Frontend (React + Vite)
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

   - **/sequential-search** (POST): Realiza búsqueda secuencial de hiperparámetros y predicción.
   - **/parallel-search** (POST): Igual que el anterior pero usando Ray para búsqueda paralela.
     - Body ejemplo (para ambos):
       ```json
       {
         "param_grid": {
           "hidden_layer_sizes": [[5], [10]],
           "activation": ["relu"],
           "solver": ["adam"],
           "alpha": [0.001],
           "max_iter": [50]
         },
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
     - Respuesta ejemplo:
       ```json
       {
         "best_params": { ... },
         "best_score": 0.85,
         "search_time": 12.34,
         "prediction": 1
       }
       ```

4. Puedes ver ejemplos de uso de los endpoints en el archivo `Api/peticion.py`.

---

## Ejecución rápida con Docker

Si prefieres no instalar dependencias manualmente, puedes correr la API directamente usando la imagen publicada en Docker Hub:

```sh
docker run -p 5000:5000 bayronj/rayapi
```

Esto levantará la API en http://localhost:5000 lista para recibir peticiones.


