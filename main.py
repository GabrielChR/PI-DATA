from fastapi import FastAPI, HTTPException
import pandas as pd
import fastparquet
import dask.dataframe as dd
import dask
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title='API Realizado por Gabriel Chumbes Rueda ')

@app.get("/")
async def read_root():
    return {" PROYECTO INDIVIDUAL DE DATA               INGRESAR AL LINK: https://gabriel-pi-data1.onrender.com/docs       LINK DE GITHUB : https://github.com/GabrielChR/PI-DATA"}

@app.get('/about/')
async def about():
    return {'Proyecto individual Data Science'}

@app.get('/PlayTimeGenre/{genero}')
async def PlayTimeGenre(genero: str):
    try:
        steamGames = pd.read_csv('DATOS PROCESADOS/df_datagames.csv')
        df_desanidadaItem = pd.read_parquet('DATOS PROCESADOS/items.parquet')
        steamGames.drop(columns=['playtime_forever'], inplace=True)

        genero_filtrado = steamGames[steamGames['genres'].apply(lambda x: genero.title() in x)]

        if genero_filtrado.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos para el género {genero}")

        merged_df = pd.merge(genero_filtrado, df_desanidadaItem, on='item_id')

        if merged_df.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos de horas jugadas para el género {genero}")

        merged_df['playtime_forever'] = merged_df['playtime_forever'] / 60

        max_hours_year = merged_df.groupby('release_date')['playtime_forever'].sum().idxmax()

        max_hours_year = str(max_hours_year)

        return {"Año de lanzamiento con más horas jugadas para el Género " + genero: max_hours_year}
    
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error al cargar los archivos de datos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/UserForGenre/{genero}')
async def UserForGenre(genero:str):
    try:
        df_games = pd.read_csv('DATOS PROCESADOS/df_datagames.csv')
        df_reviews = pd.read_csv('DATOS PROCESADOS/reviews.csv')


        condition = df_games['genres'].apply(lambda x: genero in x)
        juegos_genero = df_games[condition]

        df_merged = df_reviews.merge(juegos_genero, on='item_id')

        df_merged['playtime_forever'] = df_merged['playtime_forever'] / 60

        df_merged = df_merged[df_merged['posted'] >= 100]

        df_merged['Año'] = df_merged['posted']

        horas_por_usuario = df_merged.groupby(['user_id', 'Año'])['playtime_forever'].sum().reset_index()
        if not horas_por_usuario.empty:
            usuario_max_horas = horas_por_usuario.groupby('user_id')['playtime_forever'].sum().idxmax()
            usuario_max_horas = horas_por_usuario[horas_por_usuario['user_id'] == usuario_max_horas]
        else:
            usuario_max_horas = None

        acumulacion_horas = horas_por_usuario.groupby(['Año'])['playtime_forever'].sum().reset_index()
        acumulacion_horas = acumulacion_horas.rename(columns={'Año': 'Año', 'playtime_forever': 'Horas'})

        resultado = {
            "Usuario con más horas jugadas para " + genero: usuario_max_horas.to_dict(orient='records'),
            "Horas jugadas": acumulacion_horas.to_dict(orient='records')
        }

        return resultado

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error al cargar los archivos de datos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/UsersRecommend/{anio}')  
async def UsersRecommend(año:int):
    try:
        df_reviews = pd.read_csv('DATOS PROCESADOS/reviews.csv')
        df_item = pd.read_parquet('DATOS PROCESADOS/items.parquet')

        reviews_filtradas = df_reviews[(df_reviews['posted'] == año) & (df_reviews['recommend'] == True) & (df_reviews['sentiment_analysis'] >= 1)]

        if reviews_filtradas.empty:
            raise Exception(f"No hay datos para el año {año} con los filtros especificados.")

        df_merged = reviews_filtradas.merge(df_item, on='item_id')

        recomendaciones_por_juego = df_merged.groupby('item_name')['recommend'].sum().reset_index()

        if recomendaciones_por_juego.empty:
            raise Exception(f"No hay juegos recomendados para el año {año} con los filtros especificados.")

        top_juegos_recomendados = recomendaciones_por_juego.nlargest(3, 'recommend')

        resultado = [{"Puesto 1": top_juegos_recomendados.iloc[0]['item_name']},
                    {"Puesto 2": top_juegos_recomendados.iloc[1]['item_name']},
                    {"Puesto 3": top_juegos_recomendados.iloc[2]['item_name']}]

        return resultado

    except FileNotFoundError:
        raise Exception("No se pudo cargar uno o más archivos de datos. Verifica la existencia de los archivos en las rutas especificadas.")

    except Exception as e:
        raise Exception(f"Se produjo un error inesperado: {str(e)}")
    
@app.get('/Sentiment_analysis/{anio}')
async def sentiment_analysis(año:int):
    try:
        steamGames = pd.read_csv('DATOS PROCESADOS/df_datagames.csv')
        df_reviews = pd.read_csv('DATOS PROCESADOS/reviews.csv')

        juegos_año = steamGames[steamGames['release_date'] == año]
        
        if juegos_año.empty:
            raise Exception(f"No hay datos para el año {año} con los filtros especificados.")

        df_merged = df_reviews.merge(juegos_año, left_on='item_id', right_on='item_id')

        resultados = {
            'Negative': len(df_merged[df_merged['sentiment_analysis'] == 0]),
            'Neutral': len(df_merged[df_merged['sentiment_analysis'] == 1]),
            'Positive': len(df_merged[df_merged['sentiment_analysis'] == 2])
        }

        return resultados
    except FileNotFoundError:
        raise Exception("No se pudo cargar uno o más archivos de datos. Verifica la existencia de los archivos en las rutas especificadas.")

    except Exception as e:
        raise Exception(f"Se produjo un error inesperado: {str(e)}")
    
@app.get("/recomendacion_juego/{product_id}")
async def recomendacion_juego(product_id: int):
    try:
        steamGames = pd.read_csv('DATOS PROCESADOS/steam_games.csv')

        target_game = steamGames[steamGames['item_id'] == product_id]

        if target_game.empty:
            return {"message": "No se encontró el juego de referencia."}

        target_game_tags_and_genres = ' '.join(target_game['tags'].fillna('').astype(str) + ' ' + target_game['genres'].fillna('').astype(str))

        tfidf_vectorizer = TfidfVectorizer()

        chunk_size = 100   
        similarity_scores = None

        for chunk in pd.read_csv('DATOS PROCESADOS/steam_games.csv', chunksize=chunk_size):
            chunk_tags_and_genres = chunk['tags'].fillna('').astype(str) + ' ' + chunk['genres'].fillna('').astype(str)
            games_to_compare = [target_game_tags_and_genres] + chunk_tags_and_genres.tolist()

            tfidf_matrix = tfidf_vectorizer.fit_transform(games_to_compare)

            if similarity_scores is None:
                similarity_scores = cosine_similarity(tfidf_matrix)
            else:
                similarity_scores = cosine_similarity(tfidf_matrix)

        if similarity_scores is not None:
            similar_games_indices = similarity_scores[0].argsort()[::-1]

            num_recommendations = 5
            recommended_games = steamGames.loc[similar_games_indices[1:num_recommendations + 1]]

            return recommended_games[['app_name']].to_dict(orient='records')

        return {"message": "No se encontraron juegos similares."}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
