name: Actualizador Automatico de Noticias IA
on:
  schedule:
    # Se ejecuta automaticamente todos los dias a las 8:00 AM
    - cron: '0 8 * * *'
  workflow_dispatch: # Esto te permite activar el robot manualmente cuando quieras

jobs:
  actualizar-noticias:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar repositorio
        uses: actions/checkout@v4

      - name: Consultar noticias con Gemini IA
        id: gemini
        run: |
          # El robot le pide a Gemini la noticia de tecnologia del dia de forma directa
          RESPONSE=$(curl -X POST "https://googleapis.com{{ secrets.GEMINI_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{
              "contents": [{
                "parts": [{
                  "text": "Busca la noticia mas importante de hoy sobre Inteligencia Artificial o tecnologia. Devuelve exclusivamente un objeto JSON plano, sin formato markdown, sin texto explicativo. El formato debe ser: {\"id\": '$(date +%s)', \"titulo\": \"Titular impactante de menos de 60 caracteres\", \"categoria\": \"ia\", \"img\": \"https://unsplash.com\"}"
                }]
              }]
            }')
          
          # Extraemos el texto limpio del JSON
          TEXTO_NOTICIA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].text')
          echo "noticia=$TEXTO_NOTICIA" >> $GITHUB_ENV

      - name: Actualizar el archivo index.html
        run: |
          # Insertamos la nueva noticia dentro de la base de datos de tu index.html
          sed -i "s|const noticiasDB = \[|const noticiasDB = \[\n  $noticia,|" index.html

      - name: Guardar cambios en la Web
        run: |
          git config --global user.name "Robot Noticiero IA"
          git config --global user.email "bot@ia.com"
          git add index.html
          git commit -m "Noticia automatica del dia añadida"
          git push
