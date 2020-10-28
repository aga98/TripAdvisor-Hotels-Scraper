# Dataset: Plazas hoteleras en la ciudad de Barcelona

#### Alberto Giménez y Maite Gracia

##### Estructura del proyecto:
- **src**: Contiene los  scripts
    - *main.py*: Script principal del proyecto
    - *scraper.py*: Script encargado de realizar el web scraping de los hoteles de Tripadvisor.
    - *hotel.py*: Script donde se define la clase Hotel
    - *hotels_to_csv.py*: Script que exporta los hoteles extraidos a CSV.
    
- **data**: Contiene el CSV con el dataset resultante del scraping.

- **documents**: Contiene el archivo PDF con las respuestas y otros ficheros necesarios.

- **drivers**: Carpeta con los drivers que necesita selenium. 
Hemos incluido diferentes versiones de chromedriver para los diferentes sistemas operativos.

##### Ejecución:
1. Instalar las librerías necesarias: `pip install -r requirements.txt`
2. Ir a la carpeta **src**: `cd src`
3. Ejecutar el _main.py_: `python main.py`   