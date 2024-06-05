# Uso de la imagen base de Alpine
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /flight_scraping

# Copia el contenido actual del directorio al contenedor en /app
COPY . /flight_scraping

RUN pip --no-cache-dir install -r requirements.txt

# Ejecuta el script
CMD ["python", "./main.py"]