import plotly.graph_objects as go
import pandas as pd

mapbox_access_token='pk.eyJ1IjoieWFyZ25vcyIsImEiOiJjbDN1Y2hkZHUwMHF6M2Rtd2M3eDd3eHBlIn0.l6mj0PxtkJxQTt7G2U_xbw'
df = pd.read_csv('2023-04-02 15:38:07.606269_GPS_LOG.csv')
# df['text'] = df['Price May 2022'] + ' ' + df['Location']


fig = go.Figure(data=go.Scattermapbox(
        # locationmode = 'USA-states',
        lon = df['Long'],
        lat = df['Lat'],
        text = df['Time'],
        mode = 'lines+markers',
        textposition ='middle right',
        marker = dict(
            size = 10,
            color=df['Index'],
            colorscale = 'temps',
            # cmin = 1,
            # cmax = 3.5
        )
        ))
        
fig.update_layout(
        title = 'Compressed Natural Gas Rates ($/GGE)',
        # mapbox_style="carto-positron",
        mapbox_center=dict(lat=35.8, lon=-86),
        mapbox_style="light",
        mapbox_zoom=7.2,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            ),
        font= dict(size=10)
    )
fig.show()
# fig.write_image("fig3.pdf", width=1900, height=1100, scale=1)
# fig.write_html("fig2.html")