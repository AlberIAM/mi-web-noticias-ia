import urllib.request
import json
import os
import time

try:
    # 1. Consultar a Gemini IA de forma directa y segura
    key = os.environ.get("GEMINI_KEY", "")
    url = f"https://googleapis.com{key}"
    
    prompt = "Busca la noticia mas importante de hoy sobre Inteligencia Artificial o tecnologia. Devuelve exclusivamente un objeto JSON plano, sin formato markdown, sin texto explicativo. El formato debe ser exactamente: {\"id\": " + str(int(time.time())) + ", \"titulo\": \"Tu titular impactante aki\", \"categoria\": \"ia\", \"img\": \"https://unsplash.com\"}"
    
    data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Limpiar bloques markdown si la IA los añade
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

    # 2. Leer archivo índice.html e inyectar la noticia
    with open("índice.html", "r", encoding="utf-8") as f:
        html = f.read()

    nueva_linea = f"  {raw_text},\n"
    html_modificado = html.replace("const noticiasDB = [", "const noticiasDB = [\n" + nueva_linea)

    with open("índice.html", "w", encoding="utf-8") as f:
        f.write(html_modificado)
        print("Web actualizada con éxito.")

except Exception as e:
    print(f"Error en el proceso: {e}")
    exit(1)
