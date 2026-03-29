#!/bin/bash
# 🐝 m-ia: Gestión Soberana de Nodos P2P
# Nodo Corrientes | Proyecto Mamangá

echo "🛡️ Iniciando m-ia: Transformando Debian en Nodo Inteligente..."

# 1. Optimización de Recursos (para 230MB RAM)
echo "⚙️ Optimizando swap y memoria..."
sudo sysctl -w vm.swappiness=10

# 2. Instalación de herramientas base
echo "📦 Instalando herramientas de auditoría..."
sudo apt update && sudo apt install -y htop curl git net-tools

# 3. Función de Auditoría Rápida
function auditar() {
    echo "📊 Estado del Nodo:"
    free -h
    df -h | grep '^/dev/'
    uptime
}

# 4. Lógica de m-ia (aquí iría la conexión con el modelo de lenguaje)
echo "🧠 m-ia lista para recibir órdenes en el Nodo .248"

auditar
