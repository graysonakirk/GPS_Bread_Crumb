import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('2023-04-02 15:38:07.606269_GPS_LOG.csv')

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode = 'USA-states',
    lon = df['Long'],
    lat = df['Lat'],
    hoverinfo = 'text',
    text = df['Time'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

# flight_paths = []
# for i in range(len(df)):
#     fig.add_trace(
#         go.Scattergeo(
#             locationmode = 'USA-states',
#             lon = [df['Long'][i], df['Long'][i]],
#             lat = [df['Lat'][i], df['Lat'][i]],
#             mode = 'lines',
#             line = dict(width = 1,color = 'red'),
#             # opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
#         )
#     )

fig.update_layout(
    title_text = 'Feb. 2011 American Airline flight paths<br>(Hover for airport names)',
    showlegend = False,
    geo = dict(
        # scope = 'usa',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

fig.show()