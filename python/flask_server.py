# import flask microframework library
from flask import Flask, json, jsonify, request, send_file, Response
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import sys
from utils import series_temp, nordest_plot
from inmet.WebScraper import InmetWS
import pandas as pd
 
# initialize the flask application
app = Flask(__name__)

#####################
# Nordeste Espacial # 
#####################

@app.route("/Nordeste_columns", methods=["POST"])
def get_nordeste_columns():
    df_all = pd.read_csv('nordeste_plot/df_todas_colunas_plus_IA.csv')
    try:
        response = jsonify({'lista_colunas': list(df_all.columns[3:])})
        response.status_code = 200  
    except:
        exception_message = 'Server Not Connected'
        response = json.dumps({"content":exception_message})
        response.status_code = 400
    return response

@app.route("/Plotly_Nordeste", methods=["POST"])
def plotly_nordeste():
    json = request.json
    coluna = json['Coluna']
    colormap = json['ColorMap']
    return nordest_plot.plotly_nordeste(coluna, colormap)

@app.route("/Plot_Nordeste", methods=["POST"])
def plot_nordeste():
    json = request.json
    coluna = json['Coluna']
    colormap = json['ColorMap']
    fig = nordest_plot.plot_nordeste(coluna, colormap)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

######################## 
# ONS Series temporais #
########################

@app.route("/time_series", methods=["POST"])
def plot_png_bjl_solar():
    diretorio = "time_series/"+request.json['Usina']+"/"
    fig = series_temp.create_time_series(diretorio)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

##################
# INMET SCRAPING #
##################
@app.route("/inmet_scraping", methods=["POST"])
def InmetScraping():
    Inws = InmetWS(login=request.json['login'], senha=request.json['senha'])
    Inws.scrap()
    return 'InmetScraped'

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)