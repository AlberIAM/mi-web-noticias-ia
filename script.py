import urllib.request
import json
import os
import time

try:
    key = os.environ.get("GEMINI_KEY", "").strip()
    
    # Dirección oficial completa en una sola linea limpia
    url = f"https://googleapis.com{key}"
    
    prompt_text = "Busca la noticia mas importante de hoy sobre Inteligencia Artificial o tecnologia. Devuelve exclusivamente un objeto JSON plano con este formato: {\"id\": " + str(int(time.time())) + ", \"titulo\": \"Titular aqui\", \"categoria\": \"ia\", \"img\": \"https://unsplash.com\"}"
    
    body = {"contents": [{"parts": [{"text": prompt_text}]}]}
    data = json.dumps(body).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Limpieza de marcas markdown si las hay
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                lines = lines[1:-1]
            raw_text = "\n".join(lines).strip()

    # Inyección en tu pagina web
    with open("índice.html", "r", encoding="utf-8") as f:
        html = f.read()

    nueva_linea = f"  {raw_text},\n"
    html_modificado = html.replace("const noticiasDB = [", "const noticiasDB = [\n" + nueva_linea)

    with open("índice.html", "w", encoding="utf-8") as f:
        f.write(html_modificado)
    print("Completado con exito.")

except Exception as e:
    print(f"Error detallado: {e}")
    exit(1)
