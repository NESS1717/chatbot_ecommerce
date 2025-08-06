# Dockerfile para chatbot_ecommerce Flask
FROM python:3.13-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto (ajusta si usas otro)
EXPOSE 80

# Variable de entorno para producción
ENV FLASK_ENV=production

# Comando para ejecutar la app
###CMD ["python", "app.py"]  SOLO PARA LOCAL Y COMENTAR EL SIGUIENTE
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]  
