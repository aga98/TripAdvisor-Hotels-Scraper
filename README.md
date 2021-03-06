# Dataset: Plazas hoteleras en la ciudad de Barcelona

## Descripción
Repositorio correspondiente a la práctica 1 de la asignatura Tipología y ciclo de vida de los datos 
del máster de Ciencia de Datos de la UOC.

En este proyecto se han utilizado técnicas de web scraping mediante Python para recolectar 
datos sobre hoteles de la web Tripadvisor.


## Carpetas y ficheros
- **src**: Contiene los scripts para la recolección de los datos
    - *src/main.py*: Ejecuta el proceso de scraping
    - *src/scraper.py*: Script encargado de realizar el web scraping de los hoteles de Tripadvisor.
    - *src/hotel.py*: Contiene la clase que define la estructura (las variables) del objeto Hotel.
    - *src/hotels_to_csv.py*: Genera el fichero CSV con todos los datos recolectados.
    
- **data**: Contiene el CSV con el dataset resultante del scraping.

- **documents**: Contiene los ficheros .rmd y .pdf con toda la información referente al dataset.

- **drivers**: Carpeta con los drivers que necesita selenium.  Hemos incluido diferentes 
versiones de chromedriver para los diferentes sistemas operativos.


## Para ejecutarlo

### Instalar
```
pip install beautifulsoup4
pip install selenium
pip install pandas
```



o bien

```
pip install -r requirements.txt
```
### Ejecutar
```
cd src
python main.py
```

## Integrantes
Equipo formado por Alberto Giménez Aragón y Maite Gracia Moises.

## DOI

A modo de nota, el dataset publicado en el repositorio Zenodo es una simulación de los datos reales para no infringir las políticas de contenido de la web sobre la que se ha basado la práctica.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4256762.svg)](https://doi.org/10.5281/zenodo.4256762)
