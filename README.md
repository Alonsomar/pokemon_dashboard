# Pokémon Dashboard
_Alonso Valdés, Visualización Avanzada, UCM - Máster Data Science, Big Data & Business Analytics._

Este proyecto implementa una aplicación web usando Dash para visualización de datos.
La app se utiliza para generar distintos gráficos y comparativas de estadísticas de pokemones.
- [VISITA EL DASHBOARD](https://pokemon.alonsovaldes.com)

## Fuentes de información
- [Imágenes de cada pokemon - Github](https://github.com/HybridShivam/Pokemon/tree/master)
- [Estadísticas de cada pokemon - Kaggle](https://www.kaggle.com/datasets/abcsds/pokemon)

Tanto las imágenes como las estadísticas se cruzan a través del número del pokemon (ID)

## Estructura del Proyecto
- `app.py`: Script principal que inicia la aplicación.
- `layout.py`: Contiene el diseño de la interfaz de la aplicación.
- `plot_utils.py`: Funciones utilitarias para la generación de gráficos.
- `assets/`: Carpeta con archivos estáticos necesarios para la app:
  - Estilos CSS.
  - Imágenes de pokemon.
  - Script para el fondo, utilizando librería P5. 
  - Favicon.
- `data/`: Carpeta que contiene los datos de pokemon utilizados por la aplicación.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar la aplicación.

## Instalación

1. Copia los archivos en una carpeta.
    ```bash
    git clone https://github.com/Alonsomar/pokemon-dashboard.git
    ```
2. En esa carpeta crea un entorno virtual:
   ```sh
   python -m venv venv
   ```
3. Activa el entorno virtual:
     ```sh
     venv\Scripts\activate
     ```
4. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación, usa el siguiente comando:
```sh
python app.py
```

La aplicación estará disponible en el puerto por defecto `http://127.0.0.1:8050/`.


## Demostración
![](https://raw.githubusercontent.com/Alonsomar/pokemon_dashboard/main/captures/main_page.PNG)
![](https://raw.githubusercontent.com/Alonsomar/pokemon_dashboard/main/captures/scatter_plot.PNG)
![](https://raw.githubusercontent.com/Alonsomar/pokemon_dashboard/main/captures/violin_plot.PNG)

## Contribución
Si deseas contribuir, por favor realiza un fork del repositorio y crea un pull request.

## Licencia
Este proyecto está licenciado bajo MIT License.
