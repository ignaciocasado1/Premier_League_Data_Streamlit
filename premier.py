import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from IPython.display import Audio
import seaborn as sns

# Importamos el DF y las Columnas
df = pd.read_csv('premier_data.csv')


df['90s'] = df['minutes']/90

calc_elements = ['goals', 'assists', 'points']

for each in calc_elements:
    df[f'{each}_p90'] = df[each] / df['90s']

positions = list(df['position'].drop_duplicates())
teams = list(df['team'].drop_duplicates())

# Create a sidebar and add a selectbox to it
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Seleccione la Página:", ["Historia", "Análisis de Dataframe","Análisis de Precios", "Análisis de Minutos Jugados", "Agradecimientos"])

# Show different contents based on the selected page
if page == "Historia":
    # Titulo
    st.title("Historia del Fútbol")
     # Enlace a LinkedIn
    st.markdown("[Ignacio Casado](https://www.linkedin.com/in/ignacio-casado-ternero-a397991bb/)")

    st.image('descarga_campo.jpeg', caption=None, width=None, use_column_width=True)


    st.write('El fútbol es un deporte de equipo que se juega con un balón y dos equipos de once jugadores cada uno. El objetivo del juego es anotar más goles que el equipo contrario mediante el uso de los pies. El juego se juega en un campo rectangular con dos áreas de gol en cada extremo. Los jugadores tratan de pasar el balón a sus compañeros de equipo y avanzar hacia el área de gol del equipo contrario, mientras intentan evitar que el equipo contrario anote goles. El equipo que anota más goles al final del partido gana.')
    st.empty()
    st.write('El fútbol es uno de los deportes más populares en el mundo y se juega en casi todos los países. Se celebra una gran cantidad de competiciones de fútbol, incluyendo ligas nacionales, copas nacionales e internacionales y torneos de selecciones nacionales. Las cinco grandes ligas de fútbol son la Premier League de Inglaterra, La Liga de España, la Bundesliga de Alemania, la Serie A de Italia y la Ligue 1 de Francia. La Premier League es considerada como una de las ligas de fútbol más competitivas y emocionantes del mundo, atrayendo a algunos de los mejores jugadores y equipos de todo el mundo. Es famosa por su atmósfera de juego y su gran rivalidad entre los equipos.')
    st.empty()
    st.write('Además de las competiciones mencionadas anteriormente, también hay competiciones a nivel continental como la Liga de Campeones de la UEFA y la Liga Europa de la UEFA. Estas competiciones reúnen a los mejores equipos de Europa para competir por el título continental. La Liga de Campeones es considerada como la competición de clubes más importante del mundo, y es muy codiciada por los equipos y los aficionados.')
    
    st.title("Historia de la Premier League")

    # Imagen
    st.image('Barclays.jpeg', caption=None, width=None, use_column_width=True)
    audio_file = 'NEW Premier League 202122 Matchday Intro.mp3'
    st.audio(audio_file)

    # Parrafos
    st.write("La Premier League es la liga de fútbol más importante de Inglaterra y una de las más importantes a nivel mundial. Fue fundada en 1992, después de que los clubes de la primera división de la Football League decidieran romper su relación con la organización que llevaba ese nombre y crear una liga independiente. La nueva liga se llamó Premier League, y desde entonces ha sido el escenario de algunos de los mejores equipos y jugadores de fútbol del mundo.", width='45%')
    st.empty()
    st.write("A lo largo de su historia, la Premier League ha sido dominada por algunos equipos, especialmente Manchester United, Chelsea, Arsenal y Manchester City. Estos equipos han ganado la mayoría de los títulos de liga desde su creación. A pesar de esto, en los últimos años, se ha visto un cambio en el panorama de la liga, con el surgimiento de nuevos equipos como Leicester City, que ganó su primer título en 2016, y Liverpool, que ganó su primer título en 2019, después de 30 años de espera. Además, en los últimos años también ha habido un aumento en la competencia entre los equipos, lo que ha llevado a una liga más emocionante y difícil de predecir.", width='45%')
    st.empty()
    st.write('Dentro de todas las temporadas que se han disputado en la Premier League hay una que resalta por su signofocativa rareza y es la temporada 20/21, la cual resalta debido a que tuvo que hacer frente a una pandemia y vio afectada su forma de ser llevada dráticamente. Es por ello por lo que vamos a poder analizar al detalle el desempeño que tuvieron los jugadores bajo estas inesperadas circunstancias')

    st.markdown('##### Equipos que Conforman la Temporada 2020/2021')
    st.image('equipos.jpg', caption=None, width=None, use_column_width=True)
    teams = ['Arsenal', 'Aston Villa', 'Brighton & Hove Albion', 'Burnley', 'Chelsea',
         'Crystal Palace', 'Everton', 'Leeds United', 'Leicester City', 'Liverpool',
         'Manchester City', 'Manchester United', 'Newcastle United', 'Norwich City',
         'Southampton', 'Tottenham Hotspur', 'Watford', 'West Ham United', 'Wolves']

    selected_team = st.selectbox('Lista con lo equipos que participaron en la temporada 20/21:', teams)

elif page == "Análisis de Dataframe":
    st.markdown('### Dataframe de Jugadores')

    search_query = st.text_input("Inserte el nombre de un jugador si lo quiere ver específicamente:")

    if search_query:
        filtered_df = df.loc[df["name"].str.contains(search_query, case=False, na=False)]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df.sort_values('points', ascending=False).reset_index(drop=True))

    st.markdown('### Matriz de Correlación')

    corr = df.corr()

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

    # Add slider to adjust the size of the plot
    plot_width = st.slider("Ancho de la gráfica", min_value=100, max_value=1000, value=500, step=100)
    plot_height = st.slider("Alto de la gráfica", min_value=100, max_value=1000, value=500, step=100)

    fig.set_size_inches(plot_width/100, plot_height/100)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

elif page == "Análisis de Precios":
    # Sidebar - title & filters
    st.sidebar.markdown('### Data Filters')
    position_choice = st.sidebar.multiselect(
        'Elija la Posición de los Jugadores:', positions, default=positions)
    teams_choice = st.sidebar.multiselect(
        "Equipos:", teams, default=teams)
    price_choice = st.sidebar.slider(
        'Precio Máximo:', min_value=4.0, max_value=15.0, step=.5, value=15.0)

    df = df[df['position'].isin(position_choice)]
    df = df[df['team'].isin(teams_choice)]
    df = df[df['cost'] < price_choice]

# Main - charts
    st.markdown('### Precio vs 20/21 Puntos')

    st.vega_lite_chart(df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'cost', 'type': 'quantitative'},
        'y': {'field': 'points', 'type': 'quantitative'},
        'color': {'field': 'position', 'type': 'nominal'},
        'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
    },
    'width': 700,
    'height': 400,
    })

    st.markdown('### Goles/Partido vs Asistencias/Partido')

    st.vega_lite_chart(df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'goals_p90', 'type': 'quantitative'},
        'y': {'field': 'assists_p90', 'type': 'quantitative'},
        'color': {'field': 'position', 'type': 'nominal'},
        'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
    },
    'width': 700,
    'height': 400,
    })

    st.markdown('### Promedio de Precio de los Jugadores por Equipo')
    # Agrupar datos por equipo y posición y obtener el promedio de coste
    grouped = df.groupby(['team', 'position'])['cost'].mean()
    grouped = grouped.reset_index()

    # Crear gráfica de barras
    st.bar_chart(grouped, x="team", y="cost")



elif page == 'Análisis de Minutos Jugados':

    st.markdown('### Relación de Minutos Jugados con Posición')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    def create_pie_chart(df, positions):
        grouped = df[df["position"].isin(positions)].groupby("position")["minutes"].sum()
        plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%')
        plt.axis('equal')
        st.pyplot()

    st.markdown('### Jugadores con Más Partidos Disputados')
    st.write('Seleccione el Nº de Jugadores a Mostrar y Pulse Update Ranking:')

    #players = pd.read_csv('/Users/ignaciocasado/Desktop/VD Steramlit/premier_data.csv')
    players = df

    def show_ranking(n):
        players_sorted = players.sort_values('minutes', ascending=False)
        top_players = players_sorted.head(n)
        st.write(top_players[['name', 'minutes']])

    #st.sidebar.title("Options")
    number_of_players = st.sidebar.slider("Seleccione el nº de jugadores: \n(Sólo para los Jugadores con más Partidos)", min_value=1, max_value=30, value=10)

    #st.write("Ranking of Players by Minutes Played:")
    #show_ranking(number_of_players)

    if st.button("Update Ranking"):
        show_ranking(number_of_players)

    st.write("Complete Data")
    st.write(players)
        
    #df = pd.read_csv('/Users/ignaciocasado/Desktop/VD Steramlit/premier_data.csv')

    positions = df["position"].unique().tolist()
    selected_positions = st.multiselect("Elija la Posición:", positions)
    create_pie_chart(df, selected_positions)

elif page == "Agradecimientos":
    st.title("Conclusiones")
    audio_file_1 = 'Samba Do Brasil-Ey Macalena.mp3'
    st.audio(audio_file_1)
    st.write('La página que ha creado es una herramienta que permite visualizar información de un dataframe de jugadores de fútbol. La idea principal es proporcionar una forma rápida y fácil de ver y analizar los datos relevantes, como el coste, el equipo y la posición de los jugadores.')
    st.write('En términos de mejoras, hay varias opciones que podría considerar para aumentar la funcionalidad de su página. Una opción es agregar una búsqueda interactiva de jugadores, lo que permitiría a los usuarios filtrar la información por nombre o posición. Además, podría agregar gráficos adicionales, como un gráfico de barras que muestre la cantidad de jugadores por equipo o posición, o un gráfico de líneas que muestre la evolución de los costes de los jugadores a lo largo del tiempo.')
    st.write('En general, esta página es un buen comienzo y tiene una base sólida para el desarrollo futuro. Con un poco más de trabajo y esfuerzo, puede convertirse en una herramienta poderosa e intuitiva para el análisis de datos de fútbol.')
    st.image('vini-neymar-paqueta-dance.gif')
