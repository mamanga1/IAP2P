#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐝 m-ia: Interfaz de Comandos Inteligente
Nodo Corrientes | Proyecto Mamangá
------------------------------------------
Este script permite administrar el sistema mediante lenguaje natural,
sin comprometer la estabilidad de otros servicios como la radio.
"""
import os, sys, io, json, requests

# Blindaje de encoding para terminales livianas
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 🛡️ CARGA SEGURA: Cada usuario usa su propia API Key
API_KEY = os.getenv("MAMANGA_IA_KEY")
MODELO = "mistralai/mixtral-8x7b-instruct"

if not API_KEY:
    print("\n⚠️  ERROR: No se encontró la variable MAMANGA_IA_KEY.")
    print("Configurala con: export MAMANGA_IA_KEY='tu_clave_aca'\n")
    sys.exit(1)

print("\n🐝 m-ia - ADMINISTRACIÓN SOBERANA (Nodo .248)")
print("Escribí 'salir' para terminar.\n")

messages = [{"role": "system", "content": "Sos m-ia, técnico de Corrientes. Respondé SOLO con el comando de Linux exacto. Sin sermones, sin explicaciones. El comando debe estar en la ÚLTIMA línea."}]

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
            reply = data["choices"][0]["message"]["content"].strip()
            # Limpieza de bloques de código Markdown
            clean_reply = reply.replace("```bash", "").replace("```", "").strip()
            
            # Tomamos la última línea para ejecución
            lineas = clean_reply.split('\n')
            comando = lineas[-1].replace("`", "").replace("$ ", "").strip()
            
            print(f"\nIA 🤖> {clean_reply}\n")
            
            # Filtro de seguridad para ejecución
            if any(c in comando.lower() for c in ["ping", "ls", "apt", "cat", "ssh", "systemctl", "git", "df", "free"]):
                confirmar = input(f"¿Ejecutar '{comando}'? (s/n): ").lower()
                if confirmar == 's':
                    print(f"🚀 Corriendo...\n")
                    os.system(comando)
                    print("\n---")
        else:
            print(f"⚠️ Error de API: {data}")

    except Exception as e:
        print(f"⚠️ Error: {e}")
