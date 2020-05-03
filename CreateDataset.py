'''
Created on 30 abr. 2020

@author: fsanchez
'''
# -*- coding: utf-8 -*-

import tmdbsimple as tmdb
import pandas as pd
import os.path

tmdb.API_KEY = 'INTRODUCE-AQUI-TU-API_KEY'

dataset_pelis='dataset_pelis.csv'

# Leer el csv de mis pelis votadas y, si existe, cargar el dataset de info de las pelis para meter las nuevas

lista_ratings=pd.read_csv('ratings.csv')

if os.path.isfile(dataset_pelis):
    lista_dataset=pd.read_csv(dataset_pelis, sep=';')
    last_film=lista_dataset.iloc[-1]['Letterboxd URI']
else:
    last_film='ultimapeliculaquenoexiste'


Atributos_peli = ['Letterboxd URI',"Id_peli", "Titulo", "Popularidad",'Rating','Fecha','Duracion','Pais','Idioma','Presupuesto','Ganancia','Generos','Director','Casting','Guion','Montaje','DOP','Resumen']
df_films = pd.DataFrame(columns = Atributos_peli)

# Se invierte la lista de rating para empezar a insertar desde las ultimas vistas

lista_ratings=lista_ratings.iloc[::-1]


search = tmdb.Search()
contador=0

# Bucle que recorre las pelis vistas hasta llegar a la ultima metida en el dataset

#for index, row in islice(lista_ratings.iterrows(), 1):
for index, row in lista_ratings.iterrows():
    
    contador=contador+1
    letterboxd_uri=row['Letterboxd URI']
    
    if letterboxd_uri == last_film:
        break
    
    # Se lanza una query a TMDB con titulo y anio para averiguar el id de la peli y datos basicos
    
    try:
        response = search.movie(query=row['Name'],year=row['Year'])
        if len(response['results'])<1:
            print('No se encuentra ',row['Name'])
        else:
            id_peli=response['results'][0]['id']
            titulo=response['results'][0]['title']
    
    # Nueva consulta a TMDB para sacar detalles de la pelicula
    
            generos=[]
            movie = tmdb.Movies(response['results'][0]['id'])
            response=movie.info()
            fecha=response['release_date']
            resumen=response['overview']
            popularidad=response['popularity']
            rating=response['vote_average']
            for dic in response['genres']:
                generos.append(dic['name'])
            presupuesto=response['budget']
            ganancia=response['revenue']
            duracion=response['runtime']
            if len(response['production_countries'])>0:
                pais=response['production_countries'][0]['name']
            else:
                pais=[]
            if len(response['spoken_languages'])>0:
                idioma=response['spoken_languages'][0]['name']
            else:
                idioma=[]
    
            director=[]
            guion=[]
            dop=[]
            montaje=[]
            casting=[]

    # Nueva consulta a TMDB para sacar detalles del crew y del reparto

            response = movie.credits()
            
            for dic in response['crew']:
                if dic['job']=='Director':
                    director.append(dic['name'])
                if dic['job']=='Screenplay':
                    guion.append(dic['name'])
                if dic['job']=='Editor':
                    montaje.append(dic['name'])
                if dic['job']=='Director of Photography':
                    dop.append(dic['name'])
            
            for dic in response['cast']:
                casting.append(dic['name'])
            
            lista_peli=[letterboxd_uri,id_peli, titulo,popularidad,rating,fecha,duracion,pais,idioma,presupuesto,ganancia,generos,director,casting,guion,montaje,dop,resumen]

            df_tamanio = len(df_films)
            df_films.loc[df_tamanio] = lista_peli

# Copia de seguridad que se guarda cada 150 pelis por si hubiera algun fallo, no tener que empezar luego de 0

            if contador==150:
                df_films.to_csv('dataset_pelis-dif.csv')
                print(contador)
                contador=0
            
    except UnicodeEncodeError:
        print("Error en el nombre")

# Damos la vuelta al dataframe para guardarlo despues ordenado en el csv

df_films=df_films.iloc[::-1]

if os.path.isfile(dataset_pelis):
    lista_dataset = pd.concat([lista_dataset, df_films], axis=0)
    lista_dataset.to_csv('dataset_pelis.csv', sep=';',index=False)
else:
    df_films.to_csv('dataset_pelis.csv', sep=';',index=False)
     
print('FIN')    

