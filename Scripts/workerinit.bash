#!/bin/bash

# Este script es para los worker nodes en AWS (VPC)

sudo apt update -y
sudo apt upgrade -y

# Instalar Git y Python
sudo apt install -y python3-pip
sudo apt install -y python3-venv
# Clonar el repositorio
cd /home/ubuntu
git clone https://github.com/BayronJDv/Ray-HOptimization.git
cd Ray-HOptimization

cd Api
# Crear un entorno virtual
python3 -m venv venv
# Activar el entorno virtual
source venv/bin/activate
# Instalar las dependencias del proyecto
pip3 install -r requirements.txt
pip3 install ray

cd /home/ubuntu/Ray-HOptimization/Scripts

chmod +x ./rayinit.sh
# Ejecuta rayinit.sh como worker, pasando la IP privada del head
./rayinit.sh worker 10.0.135.156