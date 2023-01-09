'''
Created on 30 abr. 2020

@author: fsanchez
'''
# -*- coding: utf-8 -*-

import tmdbsimple as tmdb
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup
import sys
import os.path

tmdb.API_KEY = '8a079fd45df94dd519bfa7220af2414d'

# Leer la lista básica de pelis

# filmid_whitelist=pd.read_csv('filmid_whitelist')
# whitelist=filmid_whitelist[['Title','Year']]
lista_basica = pd.read_csv('ratings.csv')
lista_con_id = pd.read_csv('ratings_con_id.csv')
exclusiones = pd.read_csv('exclusiones.csv', sep=';')

Atributos_peli = ["Letterboxd URI","tmdb_type","Id_peli", "Titulo", "Popularidad", 'Rating', 'Fecha', 'Duracion', 'Pais', 'Idioma',
                  'Presupuesto', 'Ganancia', 'Generos', 'Director', 'Casting', 'Guion', 'Montaje', 'DOP', 'Resumen']
df_films = pd.DataFrame(columns=Atributos_peli)

search = tmdb.Search()
contador = 0


def get_tmdb_id(url):
    page = rq.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        literal = soup.find_all("a", {"data-track-action": "TMDb"})[0].get('href').split('themoviedb.org/')[1].split(
            '/')
        tmdb_type = literal[0]
        tmdb_id = literal[1]
    except:
        tmdb_type = 0
        tmdb_id = 0
    return tmdb_type, tmdb_id


# Mezclo las dos listas en una, que tendra NaN en las nuevas pelis


lista_merged = lista_basica.merge(lista_con_id, 'left', on="Letterboxd URI")
lista_nuevas = lista_merged[lista_merged['tmdb_id'].isnull()]
lista_nuevas = lista_nuevas.rename(columns={"Name_x": "Name","Date_x":"Date","Year_x":"Year","Rating_x": "Rating"})

lista_nuevas_id = lista_nuevas.copy()

for index, row in lista_nuevas.iterrows():
    # Obtener con scraping el tipo de film (tv o movie) y el id de tmdb
    tmdb_type, tmdb_id = get_tmdb_id(row['Letterboxd URI'])
    lista_nuevas_id.loc[index, 'tmdb_type'] = tmdb_type
    lista_nuevas_id.loc[index, 'tmdb_id'] = tmdb_id
    print(row['Name'])

lista_con_id = lista_con_id.append(lista_nuevas_id)

lista_con_id.to_csv('ratings_con_id.csv', index=False)

pelis_con_error = []

dataset_inicial = pd.read_csv('dataset_pelis.csv', sep=';')

dataset_nuevas = pd.merge(dataset_inicial,lista_con_id,left_on=['Id_peli','Titulo'],right_on=['tmdb_id','Name'],how="outer",indicator=True)
dataset_nuevas = dataset_nuevas[dataset_nuevas['_merge'] == 'right_only']
dataset_nuevas_exc = pd.merge(dataset_nuevas,exclusiones,left_on=['tmdb_id'],right_on=['tmdb_id'],how="outer",indicator='exists')
dataset_nuevas_exc = dataset_nuevas_exc[dataset_nuevas_exc['_merge'] == 'right_only']
dataset_nuevas_exc = dataset_nuevas_exc[dataset_nuevas_exc['exists'] == 'left_only']
dataset_nuevas_pelis = dataset_nuevas_exc.copy()
dataset_nuevas_pelis = dataset_nuevas_pelis.rename(columns={"Name_x": "Name","tmdb_type_y":"tmdb_type","Letterboxd URI_y":"Letterboxd URI","Rating_y": "Rating"})

print("")
print("EXTRAE DATOS NUEVAS PELIS:")
# for index, row in islice(lista_ratings.iterrows(), 1):
for index, row in dataset_nuevas_pelis.iterrows():
    print(row['Name'])

    # Se lanza una query a TMDB con titulo y anio para averiguar el id de la peli y datos basicos

    try:
        # Consulta a TMDB para sacar detalles de la pelicula
        generos = []
        ## Si la película está en la lista blanca, cojo el id manualmente ###
        # if whitelist.isin([row['Title'], row['Year']]).any().all():
        #    id_peli=filmid_whitelist.loc[(filmid_whitelist['Title'] == row['Title']) & (filmid_whitelist['Year'] == row['Year']),'Id'].item()
        #    tipo = filmid_whitelist.loc[(filmid_whitelist['Title'] == row['Title']) & (filmid_whitelist['Year'] == row['Year']),'Type'].item()
        #    print(row['Title']+' - Pelicula de la lista blanca con id: '+str(id_peli))
        #####################################################################
        if row['tmdb_type'] == "movie":
            movie = tmdb.Movies(row['tmdb_id'])
            response = movie.info()
            presupuesto = response['budget']
            ganancia = response['revenue']
            duracion = response['runtime']
        else:
            movie = tmdb.TV(row['tmdb_id'])
            response = movie.info()
            presupuesto = 0
            ganancia = 0
            duracion = 0

        director = []
        guion = []
        dop = []
        montaje = []
        casting = []

        response = movie.info()
        # fecha = response['release_date']
        fecha = row['Year']
        resumen = response['overview']
        popularidad = response['popularity']
        rating = response['vote_average']
        if row['tmdb_type'] == 'tv':
            try:
                director = []
                director.append(response['created_by'][0]['name'])
            except IndexError:
                director = []
        for dic in response['genres']:
            generos.append(dic['name'])

        if len(response['production_countries']) > 0:
            pais = response['production_countries'][0]['name']
        else:
            pais = []
        if len(response['spoken_languages']) > 0:
            idioma = response['spoken_languages'][0]['name']
        else:
            idioma = []

            # Nueva consulta a TMDB para sacar detalles del crew y del reparto

        response = movie.credits()
        for dic in response['crew']:
            if dic['job'] == 'Director':
                director.append(dic['name'])
            if dic['job'] == 'Screenplay':
                guion.append(dic['name'])
            if dic['job'] == 'Editor':
                montaje.append(dic['name'])
            if dic['job'] == 'Director of Photography':
                dop.append(dic['name'])
        for dic in response['cast']:
            casting.append(dic['name'])

        lista_peli = [row['Letterboxd URI'],row['tmdb_type'],row['tmdb_id'], row['Name'], popularidad, rating, fecha, duracion, pais, idioma,
                      presupuesto, ganancia, generos, director, casting, guion, montaje, dop, resumen]
        df_tamanio = len(dataset_inicial)
        dataset_inicial.loc[df_tamanio] = lista_peli

    except:
        print("Error en el nombre")
        pelis_con_error.append(row['Name'])

dataset_inicial.to_csv('dataset_pelis.csv', sep=';', index=False)

df_pelis_con_error = pd.DataFrame(pelis_con_error, columns=['titulo'])
df_pelis_con_error.to_csv('pelis_con_error.csv', sep=';', index=False)

print('FIN')
