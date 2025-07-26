#!/bin/bash

# Obtener IP privada del nodo
PRIVATE_IP=$(hostname -I | awk '{print $1}')

# Si es el nodo HEAD
if [ "$1" == "head" ]; then
    echo "Iniciando nodo HEAD en IP $PRIVATE_IP"
    ray start --head --port=6379 --dashboard-host=0.0.0.0
else
    # El segundo argumento debe ser la IP del head
    if [ -z "$2" ]; then
        echo "Uso: ./setup_ray.sh worker <HEAD_NODE_PRIVATE_IP>"
        exit 1
    fi
    echo "Conectando WORKER al nodo head en $2"
    ray start --address="$2:6379"
fi
