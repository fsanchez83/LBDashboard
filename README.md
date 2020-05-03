# LBDashboard
Create a Power BI Dashboard using your Letterboxd ratings

# ¿Qué es?

Un cuadro de mando en Power BI sobre un dataset de votaciones de pelis extraido de Letterboxd. 

Ejemplo subido aquí: https://app.powerbi.com/view?r=eyJrIjoiNmYxN2FiYjAtMzdiYS00ZmI5LWFjZmUtNzFkOTRmODZiMGMyIiwidCI6ImFmM2E0NDRiLTcwMWItNGVkNi05YzhlLTg0ZGE5MmQ0Zjk2OSIsImMiOjl9

Está creado sobre los datos de mi usuario de Letterboxd (https://letterboxd.com/danielquinn/), pero cambiando los csv de base debería funcionar para los de cualquiera.

# ¿Cómo puedo crear el mío?

1) Se exportan los ficheros de Letterboxd desde esta URL: https://letterboxd.com/settings/data/. De los ficheros que se descargan, hay que quedarse con dos: ratings.csv y diary.csv.

2) Esos ficheros tienen información de qué películas se han valorado, cuándo y la nota que les ha puesto el usuario. Sobre la película, la única información es el título y el año.

3) Se crea un tercer csv con información enriquecida sobre las películas que se han visto. Para ello se utiliza la API de The Movie Data Base. Para hacer eso, basta con ejecutar el script de Python CreateDataset.py. Utiliza Python 3.6 y dos librería: pandas, para la manipulación genérica de datos; y tmdbsimple, un wrapper que facilita y optimiza el uso de la API de TMDB (https://github.com/celiao/tmdbsimple).

4) Una vez se tienen los 3 csv, ya se puede ejecutar el archivo pbix. Para ello, hay que instalarse el Power BI Desktop, que es gratuito (https://powerbi.microsoft.com/es-es/downloads/). El informe, que contiene los datos de los csv importados internamente, se puede ejecutar en local con el propio Desktop, o también en internet con una cuenta gratuita de Power BI (no permite compartirlo con otras personas, ya que eso requiere la licencia de pago, pero sí se puede ejecutar para uno mismo en la nube o hacerlo público en internet).

# ¿Qué tengo que hacer?

1) Poder ejecutar scripts Python, es decir, instalarte Python 3, e instalar las librerías pandas y tmdbsimple: 
    ```
    pip3 install pandas
    pip3 install tmdbsimple
    ```
    
2) Conseguir una API Key de The Movie Database. Para ello:
    2.1) Registrarte y verificar la cuenta: https://www.themoviedb.org/account/signup
    2.2) Hacer login en la cuenta: https://www.themoviedb.org/login
    2.3) En el perfil, Configuración, se llega a la página de la API: https://www.themoviedb.org/settings/api
    2.4) Seguir las instrucciones para obtener la *API KEY*

3) Insertar la *API KEY* obtenida en la línea del código de *CreateDatabase.py* donde se indica, al principio:
    ```
    tmdb.API_KEY = 'INTRODUCE-AQUI-TU-API_KEY'
    ```

4) Instalar Power BI Desktop. Opcionalmente, crear una cuenta para ejecutar el informe en la nube y que esté disponible e internet, ya sea para uno mismo o público.

