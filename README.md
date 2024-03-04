# MovieSuggest
MovieSuggest es un sistema de recomendación de películas.

## Autores:
Lázaro David Alba Ajete

## Detalles técnicos del motor de recomendación:

Como técnica de filtrado de datos, el motor usa el Filtrado Basado en Contenido (Content Based Filtering) más específicamente, Filtrado colaborativo usuario-usuario. Este algoritmo primero encuentra la puntuación de similitud entre los usuarios. Basándose en esta puntuación de similitud, selecciona a los usuarios más similares y recomienda ítems (películas) que les gustaron anteriormente.

Para las predicciones, necesitamos la similitud entre el usuario u y v. Se usa la correlación de Pearson específicamente.

## Cómo ejecutar:

Navega al directorio que contiene tu archivo Python.
```
/MovieSuggest/src/gui/
python ./dashtkinter.py
```

## Posibles mejoras a la implementación:

Si se introduce un usuario y desconocemos la información suficiente sobre las preferencias de este, caemos en un problema conocido como Cold Start o arranque en frío. En este caso, como no tenemos información suficiente para recomendar en el modelo actual, no recomendará nada. Esto puede solucionarse recomendando un top n películas más populares. Además, podríamos explorar otras variantes de filtrado como el colaborativo ítem-ítem y potenciar la solución que tenemos hasta el momento.

## Fuentes de Datos:

Extraídos de Movielens: [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)