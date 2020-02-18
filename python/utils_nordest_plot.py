import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import shapefile as shp  # Requires the pyshp package
import plotly.express as px
import plotly as py
import os

def plot_nordeste(column, colormap):
    
    color_map_dict = { "Reds":"Reds", "Greens":"Greens", "Blues":"Blues", "Jet":"jet", "Greys":"Greys", "Viridis":"viridis",
                       "Cividis":"cividis", "Magma":"magma", "Plasma":"plasma", "Wistia":"Wistia" }

    sf = shp.Reader("nordeste_plot/Nordeste.shp")
    NE_map = []
    for shape in sf.shapeRecords():
        x0 = [i[0] for i in shape.shape.points[:]]
        x1 = [i[1] for i in shape.shape.points[:]]
        NE_map.append([x0, x1])

    df = pd.read_csv('nordeste_plot/df_todas_colunas_plus_IA.csv')

    mpl.rcParams["scatter.marker"] = 's'

    fig = plt.figure(figsize=(10,10), dpi=200)

    for i in range(0,len(NE_map)):
            axis = plt.plot(NE_map[i][0],NE_map[i][1],'k')

    sc = plt.scatter(df.LON.values, df.LAT.values, marker='s',cmap=color_map_dict[colormap],c=df[column].values, s=15, linewidths=0)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    return fig

def plotly_nordeste(column, colormap):
    
    color_map_dict = { "Reds":"Reds", "Greens":"Greens", "Blues":"Blues", "Jet":"Jet", "Greys":"Greys", "Viridis":"Viridis",
                       "Cividis":"Cividis", "Magma":"YlOrRd", "Plasma":"YlGnBu", "Wistia":"Rainbow" }
    
    df = pd.read_csv('nordeste_plot/df_todas_colunas_plus_IA.csv')
    try:
        fig = px.scatter_mapbox(df, lat="LAT", lon="LON", color = column, hover_name=column,
                                 color_continuous_scale=color_map_dict[colormap], zoom=3, height=600,
                                  mapbox_style="open-street-map", size_max=50)
        
        if os.path.isdir('plotly_hmtls'):
            py.offline.plot(fig, filename="plotly_hmtls/"+column+".html", auto_open=False)
        else:
            os.mkdir('plotly_hmtls')
            py.offline.plot(fig, filename="plotly_hmtls/"+column+".html", auto_open=False)
    
        return "Plotly " + column

    except:
        return "Could not write Plotly HTML"

