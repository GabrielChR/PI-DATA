<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL ** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

## Desarrollo de ETL y EDA

Se usaron las bases de dato de Steam - [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) Archivos en formato json los cuales se descomprimieron. y se extrajeron datos necesarios para la solución de nuestras consultas.

Se realiza el mapeo para poder hace más eficiente la búsqueda de nuestros datos importantes como también se hace el análisis mediante gráficos, análisis de sentimiento, entre otros tipos de correlaciones 
<p align="center">
<img src="https://github.com/HX-PRomero/PI_ML_OPS/raw/main/src/DiagramaConceptualDelFlujoDeProcesos.png"  height=500>
</p>

## CONTENIDO DE LA API

La API satisface estas consultas:


--PlayTimeGenre( genero : str ): Devuelve el año con mas horas jugadas para dicho género ingresado.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género Action" : 2012}

--UserForGenre( genero : str ): Devuelve el usuario que acumula más horas jugadas para el género ingresado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género Action" : 154930493, "Horas jugadas":[{Año: 2010, Horas: 31.033333333333335}, {Año: 2011, Horas: 2899.2}, {Año: 2012, Horas: 10556.883333333333},{Año: 2013, Horas:  111424.81666666667}]}

--UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

--UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

--sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

La API, el cual esta en [Render](https://render.com/docs/free#free-web-services) contiene 5 funciones y un sistema de recomendacion por item_id el cual fue solicitado
--recomendacion de juego(product_id : int)
El sistema de recomendacion nos retornara 5 juegos similares, con respecto al juego que buscamos mediante el product_id

## LINKS
 + Repositorio de (GITHUB) : https://github.com/GabrielChR/PI-DATA
 + Link de Render : https://gabriel-pi-data1.onrender.com
 + Video : https://youtu.be/S5KGGME8Bow
