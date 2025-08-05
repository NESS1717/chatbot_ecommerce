# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para que pueda accederse a Flask
EXPOSE 5000

# Variable opcional de entorno
ENV FLASK_ENV=production

# Comando para iniciar tu aplicación Flask
CMD ["python", "app.py"]
