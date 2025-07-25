#Aqui se realiza la carga y preparacion de los datos

from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split, StratifiedKFold


# --- 1. Cargar y preparar los datos ---
# fetch dataset
drug_consumption_quantified = fetch_ucirepo(id=373)

# data (as pandas dataframes)
X = drug_consumption_quantified.data.features
y = drug_consumption_quantified.data.targets

# Binarizar: CL0 y CL1 = No usuario (0), CL2+ = Usuario (1)
y_binary = y['cannabis'].apply(lambda x: 0 if x in ['CL0', 'CL1', 'CL2'] else 1)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
)
