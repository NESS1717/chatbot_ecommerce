# Dockerfile para chatbot_ecommerce Flask
FROM python:3.13-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 👉 DESCARGA EL MODELO DURANTE EL BUILD
##RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('tiiuae/falcon-7b-instruct'); AutoTokenizer.from_pretrained('tiiuae/falcon-7b-instruct')"

# Dar permisos de ejecución al script
RUN chmod +x startup.sh

# Exponer el puerto (ajusta si usas otro)
####EXPOSE 5000

# Variable de entorno para producción
ENV FLASK_ENV=production


# Comando para ejecutar la app
##CMD ["python", "app.py"] 
##CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]  
CMD ["./startup.sh"]
