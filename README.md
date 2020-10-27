# P1-WebScraping

## Descripción
Repositorio correspondiente a la práctica 1 de la asignatura Tipología y ciclo de vida de los datos del máster de Ciencia de Datos de la UOC.

En este proyecto se han utilizado técnicas de web scraping mediante Python para recolectar datos sobre hoteles de la web Tripadvisor.

## Ficheros
El repositorio contiene dos carpetas, analysis, dónde se pueden encontrar los ficheros .rmd y pdf con toda la información referente al dataset. Y la carpeta src que contiene los archivos .py para la creación del dataset con los siguientes scrips:

- src/main: ejecuta el proceso de scraping 
- src/scraper: contiene el código para la recolección de los datos
- src/hotel: contiene la clase que define la estructura (las variables) del objeto hotel
- src/hotels_to_csv: genera el fichero csv con todos los datos recolectados

## Para ejecutarlo

### Instalar
```
pip install beautifulsoup4
pip install selenium
pip install pandas
```

### Ejecutar
```
python main.py
```

## Integrantes
Equipo formado por Alberto Giménez Aragón y Maite Gracia Moises.
