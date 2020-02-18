# import flask microframework library
from flask import Flask, json, jsonify, request, send_file, Response
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
import sys
import numpy as np
from sklearn.preprocessing import MaxAbsScaler
import warnings
import itertools
from sklearn.metrics import mean_absolute_error as mae
import random
from random import randint
from tqdm import tqdm
from sklearn.metrics import mean_squared_error as mse
import pickle
from sklearn.neural_network import MLPRegressor

def plot_png():
    fig = create_time_series("time_series/bjl_solar/")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def train_test_split(serie, num_lags, tr_vd_ts_percents = [88, 12], print_shapes = False):
    len_serie = len(serie)
    X = np.zeros((len_serie, num_lags))
    y = np.zeros((len_serie,1))
    for i in np.arange(0, len_serie):
        if i-num_lags>0:
            X[i,:] = serie[i-num_lags:i]
            y[i] = serie[i]
    
    len_train = np.floor(len_serie*tr_vd_ts_percents[0]/100).astype('int')
    len_test = np.ceil(len_serie*tr_vd_ts_percents[1]/100).astype('int')
    
    X_train = X[0:len_train]
    y_train = y[0:len_train]
    X_test = X[len_train:len_train+len_test]
    y_test = y[len_train:len_train+len_test]
       
    return X_train, y_train, X_test, y_test

def train_test_split_prev(serie, num_lags_pass, num_lags_fut, tr_vd_ts_percents = [88, 12], print_shapes = False):
    #alterar para deixar com passado e futuro.
    len_serie = len(serie)
    X = np.zeros((len_serie, (num_lags_pass+num_lags_fut)))
    y = np.zeros((len_serie,1))
    for i in np.arange(0, len_serie):
        if (i-num_lags_pass > 0) and ((i+num_lags_fut) <= len_serie):
            X[i,:] = serie[i-num_lags_pass:i+num_lags_fut]
            y[i] = serie[i]
        elif (i-num_lags_pass > 0) and ((i+num_lags_fut) > len_serie):
            X[i,-num_lags_pass:] = serie[i-num_lags_pass:i]
            y[i] = serie[i]
    
    len_train = np.floor(len_serie*tr_vd_ts_percents[0]/100).astype('int')
    len_test = np.ceil(len_serie*tr_vd_ts_percents[1]/100).astype('int')
    
    X_train = X[0:len_train]
    y_train = serie[0:len_train]
    X_test = X[len_train:len_train+len_test]
    y_test = y[len_train:len_train+len_test]
    
    return X_train, y_train, X_test, y_test

def create_time_series(diretorio):
    best = pickle.load(open(diretorio+'best_model_all.pckl', 'rb'))
    MaxAbsScaler_gen = pickle.load(open(diretorio+'MaxAbsScaler_gen.pckl', 'rb'))
    dict_series = pickle.load(open(diretorio+'dict_gen_ysarimax.pckl', 'rb'))

    gen = dict_series['generation']
    y_sarimax = dict_series['y_sarimax']
    erro = gen - y_sarimax
    print(erro)

    threshold = int(len(y_sarimax)*0.8)

    data_train = gen[0:threshold]
    data_test = gen[threshold:]

    erro_train_entrada, erro_train_saida, erro_test_entrada, erro_test_saida = train_test_split(erro, best[0], [80, 20])
    erro_estimado = np.concatenate((best[4].predict(erro_train_entrada), best[4].predict(erro_test_entrada)))

    X_ass_1_train_in, _, X_ass_1_test_in, _ = train_test_split(y_sarimax, best[1], [80, 20])
    X_ass_2_train_in, _, X_ass_2_test_in, _ = train_test_split_prev(erro_estimado, best[2], best[3], [80, 20])

    X_in_train = np.concatenate((X_ass_1_train_in, X_ass_2_train_in), axis=1)
    X_in_test = np.concatenate((X_ass_1_test_in, X_ass_2_test_in), axis=1) 

    y_estimado = np.concatenate([best[5].predict(X_in_train), best[5].predict(X_in_test)])

    fig = Figure(figsize = (12, 6), dpi = 300)
    axis = fig.add_subplot(1,1,1, title = 'Geração em Média Mensal (MW)')
    axis.plot(MaxAbsScaler_gen.inverse_transform(y_estimado[-len(data_test):].reshape(-1, 1)), 'k--', label='y_hat')
    axis.plot(MaxAbsScaler_gen.inverse_transform(gen[-len(data_test):].reshape(-1, 1)), 'r', label='real')
    axis.plot(MaxAbsScaler_gen.inverse_transform(y_sarimax[-len(data_test):].reshape(-1, 1)), 'g--', label='sarimax')
    axis.legend()

    return fig

plot_png()