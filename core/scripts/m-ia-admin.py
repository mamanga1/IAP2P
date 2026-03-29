#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐝 m-ia v2.0 - Cerebro de Administración Soberana
Proyecto Mamangá | Nodo Corrientes
----------------------------------------------
Este script permite administrar servidores Debian mediante lenguaje natural.
La IA detecta comandos faltantes y ofrece instalarlos automáticamente.
"""

import os, sys, io, json, requests

# Blindaje de encoding para terminales de bajos recursos
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# CONFIGURACIÓN
# Se recomienda usar variable de entorno: export MAMANGA_IA_KEY='tu_llave'
API_KEY = os.getenv("MAMANGA_IA_KEY", "TU_API_KEY_AQUI")
MODELO = "mistralai/mixtral-8x7b-instruct"

def ejecutar_m_ia():
    print("\n🐝 m-ia - ADMINISTRACIÓN SOBERANA (Nodo .248)")
    print("Escribí 'salir' para terminar.\n")

    # Instrucción de sistema para mantener la IA enfocada en comandos
    messages = [{"role": "system", "content": "Sos una terminal Linux. Respondé ÚNICAMENTE con el comando solicitado. Sin explicaciones, sin texto extra. Solo el comando."}]

    while True:
        try:
            user_input = input("Vos 🧉> ").strip()
            if user_input.lower() in ["salir", "exit", "q"]: 
                print("¡Chau socio!")
                break
            
            messages.append({"role": "user", "content": user_input})
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": MODELO, "messages": messages}
            )
            
            data = response.json()
            if "choices" in data:
                # Limpieza de la respuesta
                reply = data["choices"][0]["message"]["content"].strip()
                reply = reply.replace("```bash", "").replace("```", "").strip()
                
                # Extraemos el comando (última línea para evitar ruidos)
                cmd = reply.split('\n')[-1].replace("`", "").replace("$ ", "").strip()
                
                print(f"\nIA 🤖> {reply}\n")
                
                # Filtro de seguridad: Ejecuta si detecta comandos conocidos o instalaciones
                whitelist = ["ping", "ls", "apt", "cat", "ssh", "systemctl", "df", "free", "htop", "ip", "uname", "nmap", "whois", "nikto"]
                if any(c in reply.lower() for c in whitelist) or "install" in reply.lower():
                    confirmar = input(f"¿Ejecutar '{cmd}'? (s/n): ").lower()
                    if confirmar == 's':
                        print(f"🚀 Corriendo...\n")
                        os.system(cmd)
                        print("\n---")
            else:
                print(f"⚠️ Error de API: {data}")

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    ejecutar_m_ia()
