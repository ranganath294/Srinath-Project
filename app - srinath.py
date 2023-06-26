import csv
import pandas as pd
import numpy as np
from flask import Flask, render_template, make_response, request, session, redirect
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import flask
import datetime
import io
from io import BytesIO
import pymysql
import yaml
from flask import send_file
import jsonify, json     
from pdf2image import convert_from_path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from plotly import graph_objects as go
from plotly import express as px
import plotly
from yaml.loader import SafeLoader
import gc
from matplotlib.patches import Patch
from natsort import natsort_keygen
import mpld3
import matplotlib
matplotlib.use('agg')
import warnings
warnings.simplefilter("ignore", UserWarning)
import plotly.offline as pyo
from bokeh.io import show
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.palettes import Category10
from bokeh.models import Legend, LegendItem
from bokeh.models.annotations import Label
from matplotlib.patches import Patch
import plotly.io as pio

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 2)

with open(r'D:\Summer\City Future Lab\Files\pubbs\pubbs\parameters.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)

globals().update(data)



dob = seatcap * min_c_lvl
cob = int(seatcap * max_c_lvl)
A=A
B=B
dead_todepot_t1=dead_todepot_t1
dead_todepot_t2=dead_todepot_t2

# import mysql.connector

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Connect to phpMyAdmin Database
conn = pymysql.connect(host="103.21.58.10",
                       user="pubbsm8z",
                       password="Matrix__111",
                       database="pubbsm8z_uba",
                       port = 3306
                       )

# Create a User Login and Register Page


@app.route('/srinath', methods =['GET', 'POST'])
def srinath():
    if request.method == 'POST':
        # passengerarrival = request.files['file1']
        # distance = request.files['file2']
        # frequency = request.files['file3']
        # timeperiod = request.files['file4']
        # link_traveltime = request.files['file5']
        # alightrate = request.files['file6']
        # fare = request.files['file7']


        # passengerarrival = pd.read_csv(passengerarrival).set_index('Passenger arrival')
        # distance = pd.read_csv(distance).set_index('Distance')
        # timeperiod = pd.read_csv(timeperiod, header=0)
        # link_traveltime = pd.read_csv(link_traveltime).set_index('Travel Time')
        # alightrate = pd.read_csv(alightrate).set_index('Alighting Rate')
        # fare = pd.read_csv(fare).set_index('Stops').fillna(0)
        # frequency = pd.read_csv(frequency)

        # print(passengerarrival)
        # print(distance)
        # print(timeperiod)
        # print(link_traveltime)
        # print(alightrate)
        # print(fare)
        # print(frequency)

        passengerarrival = pd.read_csv(r'D:\Function files\Input files\Passenger_arrival_DN.csv').set_index(
        'Passenger arrival')
        distance = pd.read_csv(r'D:\Function files\Input files\distanceDN.csv').set_index('Distance')
        timeperiod = pd.read_csv(r'D:\Function files\Input files\tmeperiodDN.csv', header=0)
        link_traveltime = pd.read_csv(r'D:\Function files\Input files\TravelTimeDN_ann.csv').set_index(
        'Travel Time')
        alightrate = pd.read_csv(r"D:\Function files\od_output\alighting_rateDN.csv").set_index('Alighting Rate')
        fare = pd.read_csv(r'D:\Function files\Input files\fare_DN.csv').set_index('Stops').fillna(0)
        frequency = pd.read_csv(r'D:\Function files\Output GA\OpFrequencyDN.csv')

        return render_template("srinath.html")

    return render_template("srinath.html")

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    # if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    #     email = request.form['email']
    #     password = request.form['password']
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
    #     user = c.fetchone()
    #     if user:
    #         session['loggedin'] = True
    #         # session['userid'] = user['userid']
    #         session['email'] = user['email']
    #         session['password'] = user['password']
    #         session['loggedin'] = True
    #         message = 'Logged in successfully !'
    #         return redirect('/home')
    #         # return render_template('index.html', message = message)
    #     else:
    #         message = 'Please enter correct email / password !'
    if 'email' in session:
        return render_template('index.html')
    else:
        return render_template('login1.html', message = message)
    

@app.route('/logout')
def logout():
    # session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect('/home')

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    # if request.method == 'POST':
    #     name = request.form['name']
    #     password = request.form['password']
    #     email = request.form['email']
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM user WHERE email = % s', (email, ))
    #     account = c.fetchone()
    #     if account:
    #         message = 'Account already exists !'
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         message = 'Invalid email address !'
    #     elif not name or not password or not email:
    #         message = 'Please fill out the form !'
    #     else:
    #         c.execute('INSERT INTO user (name, email, password) VALUES (% s, % s, % s)', (name, email, password, ))
    #         conn.commit()
    #         message = 'You have successfully registered !'

    # elif request.method == 'POST':
    #     message = 'Please fill out the form !'
    if 'email' in session:
        return render_template('index.html')
    else:
        return render_template('register1.html', message = message)

@app.route('/loggedin', methods = ['GET', 'POST'])
def loggedin():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        c = conn.cursor()
        c.execute('SELECT * FROM T_USER WHERE email = % s AND password = % s', (email, password, ))
        user = c.fetchone()
        if user:
            # session['loggedin'] = True
            # session['userid'] = user['userid']
            session['email'] = user[1]
            session['password'] = user[2]
            # session['loggedin'] = True
            message = 'Logged in successfully !'
            return redirect('/home')
            # return render_template('index.html', message = message)
        else:
            message = 'Please enter correct email / password !'
        return render_template('login1.html', message = message)



@app.route('/registered', methods =['GET', 'POST'])
def registered():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        c = conn.cursor()
        c.execute('SELECT * FROM T_USER WHERE email = % s', (email, ))
        account = c.fetchone()
        if account:
            message = 'Account already exists !'
            return render_template('register1.html', message = message)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
            return render_template('register1.html', message = message)
        elif not name or not password or not email:
            message = 'Please fill out the form !'
            return render_template('register1.html', message = message)
        else:
            c.execute('INSERT INTO T_USER (name, email, password) VALUES (% s, % s, % s)', (name, email, password, ))
            conn.commit()
            message = 'You have successfully registered ! Please Login'
            return render_template('register1.html', message = message)
        
    # elif request.method == 'POST':
    #     message = 'Please fill out the form !'
    # return render_template('register1.html', message = message)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect('/login')
    
@app.route('/tables')
def tables():
    return render_template('tablescopy.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/space-time-files')
def chartcopy():
    return render_template('spacetime.html')

def st_chart(stoparrival,despatch,distance):
    distance_origin = distance.copy()
    for i in range(0, len(distance.columns)):
        x = distance.iloc[[0], 0:i].sum(axis=1, skipna=True).values
        x = x[0]
        distance_origin.iloc[0, i] = x + distance.iloc[0, i]

    trip_st = 6 
    trip_end = 11


    fig = plt.figure(figsize=(29, 21), dpi=300)
    axes = fig.add_axes([0.05, 0.05, .95, .95])
    axes.set_xlabel('Time',fontsize=20)

    axes.set_ylabel('Distance from terminal 1',fontsize=20)
    axes.set_title('Space Time diagram',fontsize=25)
    timedata_arrival = pd.DataFrame(columns=['Time', 'distance', 'trip_no'])
    for i in range(0, len(stoparrival.index)):
        timedata_arrival = pd.DataFrame(columns=['Time', 'distance', 'trip_no'])
        for j in range(0, len(stoparrival.columns)):
            list_1 = [stoparrival.iloc[i, j], distance_origin.iloc[0, j], i]
            timedata_arrival.loc[len(timedata_arrival.index)] = list_1
            list_2 = [despatch.iloc[i, j], distance_origin.iloc[0, j], i]
            timedata_arrival.loc[len(timedata_arrival.index)] = list_2
        x = timedata_arrival['Time']
        y = timedata_arrival['distance']
        name = str(stoparrival.index[i])
        axes.plot(x, y, label=name)


    return(fig)

@app.route('/space-time-graph', methods=['POST'])
def chart():
    # stoparrival= pd.read_csv(r'D:\Function files\Input_files_holding\stoparrivalDN.csv')
    # despatch= pd.read_csv(r'D:\Function files\Input_files_holding\despatchDN.csv')
    # distance = pd.read_csv(r'D:\Function files\Input files\distanceDN.csv').set_index('Distance')
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']

    # Perform any necessary file processing
    stoparrival = pd.read_csv(file1)
    despatch = pd.read_csv(file2)
    distance = pd.read_csv(file3).set_index('Distance')

    fig = st_chart(stoparrival, despatch, distance)

    traces = []
    for ax in fig.get_axes():
        for line in ax.get_lines():
            x = line.get_xdata()
            y = line.get_ydata()
            name = line.get_label()
            trace = go.Scatter(x=x, y=y, name=name)
            traces.append(trace)

    plot = go.Figure(data=traces)
                                                                                        

    return render_template('space_time.html', plot=plot.to_html(full_html=False))

@app.route('/lifo-files')
def lifo():
    return render_template('lifo.html')



@app.route('/lifo-graph', methods = ['POST'])
def lifograph():
    # def schedule(slack, traveltimeDN, departuretimeDN, departuretimeUP, traveltimeUP, max_ideal, terminalarrivalDN,
    #              terminalarrivalUP):

    traveltimeDN = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\travel_time_totDN.csv')
    traveltimeUP = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\travel_time_totUP.csv')
    departuretimeUP = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\departuretimeUP.csv')
    departuretimeDN = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\departuretimeDN.csv')
    terminalarrivalDN = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\stoparrivalDN.csv')
    terminalarrivalDN = terminalarrivalDN.iloc[:, 0]
    terminalarrivalUP = pd.read_csv(r'D:\Function files\timetable\timetable1\Input_files_holding\stoparrivalUP.csv')
    terminalarrivalUP = terminalarrivalUP.iloc[:, 0]
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        #   Treminal Scheduling ALL DIRECTION
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
    departuretimeDN['Departure'].round(3)
    departuretimeUP['Departure'].round(3)
    departuretimeDN['Arrival_T1'] = terminalarrivalDN
    departuretimeDN['TT to Terminal2'] = traveltimeDN
    departuretimeDN['Arr_time T2'] = ""
    departuretimeDN = departuretimeDN[
        ['Arrival_T1', 'Departure', 'TT to Terminal2', 'Arr_time T2']]

    for i in range(0, len(departuretimeDN.index)):
        departuretimeDN.loc[i, 'Arr_time T2'] = (
                departuretimeDN.loc[i, 'Departure'] + departuretimeDN.loc[i, 'TT to Terminal2']).round(2)

    departuretimeUP['Arrival_T2'] = terminalarrivalUP
    departuretimeUP['TT to Terminal1'] = traveltimeUP
    departuretimeUP['Arr_time T1'] = ""
    departuretimeUP = departuretimeUP[
        ['Arrival_T2', 'Departure', 'TT to Terminal1', 'Arr_time T1']]

    for i in range(0, len(departuretimeUP.index)):
        departuretimeUP.loc[i, 'Arr_time T1'] = (
                departuretimeUP.loc[i, 'Departure'] + departuretimeUP.loc[i, 'TT to Terminal1']).round(2)

    # TERMINAL 1
    # ------------------------------------
    arrivalDN = pd.DataFrame(index=departuretimeUP.index)
    arrivalDN['Dep'] = departuretimeUP.index + 1
    arrivalDN['Pool'] = 0
    arrivalDN['Dep/Arrival'] = 'Arrival'
    arrivalDN['bus_name'] = ''

    arrivalDN['Time of Arrival'] = departuretimeUP[['Arr_time T1']]
    departuretimeDN1 = pd.DataFrame(index=departuretimeDN.index)
    departuretimeDN1['Dep'] = departuretimeDN.index + 1
    departuretimeDN1['Pool'] = 0
    departuretimeDN1['Dep/Arrival'] = 'Departure'
    departuretimeDN1['bus_name'] = ''
    departuretimeDN1['Departure_time'] = departuretimeDN['Departure'].round(3)
    departuretimeDN1['Time of Arrival'] = departuretimeDN['Arrival_T1'].round(3)
    # time table for terminal 1
    tt_terminal1 = pd.concat([departuretimeDN1, arrivalDN], axis=0, ignore_index=True)
    tt_terminal1 = tt_terminal1.sort_values(by=['Time of Arrival']).reset_index(drop=True)

    # TERMINAL 2
    # ------------------------------------
    arrivalUP = pd.DataFrame(index=departuretimeDN.index)
    arrivalUP['Dep'] = departuretimeDN.index + 1
    arrivalUP['Pool'] = 0
    arrivalUP['Dep/Arrival'] = 'Arrival'
    arrivalUP['bus_name'] = ''

    arrivalUP['Time of Arrival'] = departuretimeDN[['Arr_time T2']]
    departuretimeUP1 = pd.DataFrame(index=departuretimeUP.index)
    departuretimeUP1['Dep'] = departuretimeUP.index + 1
    departuretimeUP1['Pool'] = 0
    departuretimeUP1['Dep/Arrival'] = 'Departure'
    departuretimeUP1['bus_name'] = ''
    departuretimeUP1['Departure_time'] = departuretimeUP['Departure'].round(3)
    departuretimeUP1['Time of Arrival'] = departuretimeUP['Arrival_T2'].round(3)

    # time table for terminal 2
    tt_terminal2 = pd.concat([departuretimeUP1, arrivalUP], axis=0, ignore_index=True)
    tt_terminal2 = tt_terminal2.sort_values(by=['Time of Arrival']).reset_index(drop=True)

    tt_terminal1['Time of Arrival'] = tt_terminal1['Time of Arrival'].astype('float64')
    tt_terminal2['Time of Arrival'] = tt_terminal2['Time of Arrival'].astype('float64')
    tt_terminal1['Fleet'] = 0
    tt_terminal2['Fleet'] = 0

    # tt_terminal1 = timetable for terminal 1
    # tt_terminal2 = timetable for terminal 2
    # creating folders for exporting results
    # defining path
    path = r'D:\Function files\timetable\timetable1\FIFO\vehicleschedule'
    isExist = os.path.exists(path)
    # checking path exists or not , if not creates the path
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)

    num_bus_T = 1
    # Dataframe to store data of  depot pool
    depot_pool = pd.DataFrame(index=np.arange(0),
                              columns=['bus_name', 'departure_to_depo', 'from_terminal', 'TT_depot', 'layover',
                                       'TT_terminal1', 'TT_terminal2', 'nxt_shift'])
    # Dataframe to store data of  depot pool
    depot_tt = pd.DataFrame(index=np.arange(0),
                            columns=['bus_name', 'departure_to_depo', 'departure_from_depo', 'terminal_arrival',
                                     'terminal'])
    # Dataframe to store layover details
    laydf1 = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'start', 'end', 'remarks'])
    # Dataframe to store fleet details
    fleet = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'shift_no', 'start_shift1', 'end_shift', 'crew'])
    fleet_1 = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'shift_no', 'start_shift1', 'end_shift', 'crew'])
    fleet_2 = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'shift_no', 'start_shift1', 'end_shift', 'crew'])
    # Dataframe to store terminal pool details
    pool_t1 = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'Ready_to_depart'])
    pool_t2 = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'Ready_to_depart'])
    # VEHICLE ASSIGNMENT
    for i in range(0, len(tt_terminal1.index)):
        for j in range(0, 2):  # j==1 for terminal1 and j==2 for terminal2
            bus_name = 'RI00'  # bus name code
            if j == 0:
                or_terminal = tt_terminal1
                des_terminal = tt_terminal2
                pool = pool_t1
                traveltime = traveltimeDN
            else:

                or_terminal = tt_terminal2
                des_terminal = tt_terminal1
                pool = pool_t2
                traveltime = traveltimeUP

            if or_terminal.loc[i, 'Dep/Arrival'] == 'Departure':
                # CHECK FOR BUSES TO RETURN TO DEPOT AFTER A SHIFT
                # checking buses that are ready for next departure at time =or_terminal.loc[i, 'Time of Arrival']
                temp_pool = pool[pool['Ready_to_depart'] <= or_terminal.loc[i, 'Time of Arrival']]
                # the minimum time required by all buses in the temp_pool to complete the next trip
                max = or_terminal.loc[i, 'Departure_time'] + traveltime.iloc[or_terminal.loc[i, 'Dep'] - 1, 0]
                if len(temp_pool.index) > 0 and max >= fleet.loc[0, 'end_shift']:
                    pl_dropidx = [] #list stores the index of buses that will go back to the depot after a shift
                    #check for buses that will go to the depot for crew change and next shift
                    for ind in range(0, len(temp_pool.index)):
                        k = temp_pool.index[ind]
                        y1 = fleet[fleet['bus_name'] == temp_pool.loc[k, 'bus_name']].copy()
                        y1.sort_values(by=['shift_no'], ascending=False, inplace=True)
                        y1.reset_index(drop=True, inplace=True)
                        #y1 stores the shift details of the temp_pool.loc[k, 'bus_name'] bus
                        if len(y1.index) > 0:
                            y1 = y1[:1] #accessing the latest shift details

                            x1 = or_terminal.loc[i, 'Departure_time'] + traveltime.iloc[
                                or_terminal.loc[i, 'Dep'] - 1, 0] #minimum time required to complete next trip

                            if x1 >= y1.loc[0, 'end_shift']: #bus will depart to the depot if x1 >= y1.loc[0, 'end_shift']
                                #updating the depot pool
                                bus_name_d = temp_pool.loc[k, 'bus_name']
                                departure_to_depo = or_terminal.loc[i, 'Departure_time']

                                if j == 0:
                                    arrival_depot = dead_todepot_t1 + departure_to_depo
                                    from_terminal = 'T1'
                                else:
                                    arrival_depot = dead_todepot_t2 + departure_to_depo
                                    from_terminal = 'T2'

                                depo_layover = layover_depot / 60
                                departure_from_depo = arrival_depot + depo_layover
                                TTdepo_ter1 = arrival_depot + depo_layover + dead_todepot_t1
                                TTdepo_ter2 = arrival_depot + depo_layover + dead_todepot_t2
                                shift_nxt = y1.loc[0, 'shift_no'] + 1
                                depot_pool.loc[len(depot_pool.index)] = [bus_name_d, departure_to_depo,
                                                                         from_terminal,
                                                                         arrival_depot, depo_layover, TTdepo_ter1,
                                                                         TTdepo_ter2, shift_nxt]
                                depot_tt.loc[len(depot_tt.index)] = [bus_name_d, departure_to_depo, departure_from_depo,
                                                                     22, 0]
                                pl_dropidx.append(k)

                            else:
                                pass
                    #removing the buses left for depot for crew change/next shift from terminal pool
                    pool.drop(index=pl_dropidx, inplace=True)
                    pool.reset_index(drop=True, inplace=True)
                # ------------------------------------------------------------------------------------------

                # CHECK for buses in the terminal pool for next departure
                temp_pool = pool[pool['Ready_to_depart'] <= or_terminal.loc[i, 'Time of Arrival']]
                temp_pool.reset_index(drop=True, inplace=True)
                if len(temp_pool.index) == 0:  # if no buses in terminal pool for next departure then check for buses in the depotpool
                    if j == 0: #for terminal 1
                        #creating a pool of buses by checking the expected arrival of buses at terminal 1 from depot
                        temp_depool = depot_pool[
                            depot_pool['TT_terminal1'] < tt_terminal1.loc[i, 'Time of Arrival']].copy()
                        temp_depool.sort_values(by=['TT_terminal1'], ascending=True, inplace=True)
                        temp_depool.reset_index(drop=True, inplace=True)
                    else: #for terminal 2
                        temp_depool = depot_pool[
                            depot_pool['TT_terminal2'] < tt_terminal2.loc[i, 'Time of Arrival']].copy()
                        temp_depool.sort_values(by=['TT_terminal2'], ascending=True, inplace=True)
                        temp_depool.reset_index(drop=True, inplace=True)

                    if len(temp_depool.index) == 0: # if no buses in temp_depot pool for next departure then addition of a bus to the fleet
                        #adding new bus to the terminal
                        or_terminal.loc[i, 'bus_name'] = bus_name + str(num_bus_T)
                        num_bus_T = num_bus_T + 1
                        or_terminal.loc[i, 'Fleet'] = 1
                        #start of shift
                        shift_str = np.floor(or_terminal.loc[i, 'Time of Arrival'])
                        # end of shift
                        shift_end = np.floor(shift + tt_terminal1.loc[i, 'Time of Arrival'])
                        if shift_end > end_ser:
                            shift_end = end_ser + 2
                        else:
                            pass
                        shift_no = 1
                        or_terminal.loc[i, 'Pool'] = len(temp_pool.index)
                    else:
                        #adding buses for temp_depo pool
                        or_terminal.loc[i, 'bus_name'] = temp_depool.loc[0, 'bus_name']
                        or_terminal.loc[i, 'Fleet'] = 0

                        if j == 0: #terminal 1
                            shift_str = np.floor(temp_depool.loc[0, 'TT_terminal1'])
                            depot_tt.loc[(depot_tt['bus_name'] == temp_depool.loc[0, 'bus_name']) & (
                                    depot_tt['departure_to_depo'] == temp_depool.loc[
                                0, 'departure_to_depo']), 'terminal_arrival'] = temp_depool.loc[
                                0, 'TT_terminal1']

                            depot_tt.loc[(depot_tt['bus_name'] == temp_depool.loc[0, 'bus_name']) & (
                                    depot_tt['departure_to_depo'] == temp_depool.loc[
                                0, 'departure_to_depo']), 'terminal'] = 'T1'

                        else: #terminal 2
                            shift_str = np.floor(temp_depool.loc[0, 'TT_terminal2'])
                            depot_tt.loc[(depot_tt['bus_name'] == temp_depool.loc[0, 'bus_name']) & (
                                    depot_tt['departure_to_depo'] == temp_depool.loc[
                                0, 'departure_to_depo']), 'terminal_arrival'] = temp_depool.loc[
                                0, 'TT_terminal2']

                            depot_tt.loc[(depot_tt['bus_name'] == temp_depool.loc[0, 'bus_name']) & (
                                    depot_tt['departure_to_depo'] == temp_depool.loc[
                                0, 'departure_to_depo']), 'terminal'] = 'T2'

                        shift_end = np.floor(shift + or_terminal.loc[i, 'Time of Arrival'])
                        if shift_end > end_ser:
                            shift_end = end_ser + 2
                        else:
                            pass
                        shift_no = temp_depool.loc[0, 'nxt_shift']
                        #removing the added bus from pool
                        depot_pool.drop(depot_pool[depot_pool['bus_name'] == temp_depool.loc[0, 'bus_name']].index,
                                        inplace=True)

                        depot_pool.reset_index(drop=True, inplace=True)
                        or_terminal.loc[i, 'Pool'] = len(temp_pool.index)

                    fleet.loc[len(fleet.index)] = [or_terminal.loc[i, 'bus_name'], shift_no,
                                                   shift_str, shift_end, crewperbus]


                else:
                    #Adding bus from the terminal pool
                    or_terminal.loc[i, 'bus_name'] = temp_pool.loc[0, 'bus_name']
                    pool.drop(index=0, inplace=True)
                    pool.reset_index(drop=True, inplace=True)
                    or_terminal.loc[i, 'Pool'] = len(temp_pool.index)

            else:
                #updating the arrival information of the bus at the terminal
                df2 = des_terminal[des_terminal['Dep'] == or_terminal.loc[i, 'Dep']]
                df2 = df2[df2['Dep/Arrival'] == 'Departure'].copy()
                df2.reset_index(drop=True, inplace=True)
                or_terminal.loc[i, 'bus_name'] = df2.loc[0, 'bus_name']
                #calculating layover time and when would be the minimum time for next departure
                ready_for_depart = or_terminal.loc[i, 'Time of Arrival'] + (lay_overtime + slack) / 60
                if j==0:
                    x2='layover T1'
                else:
                    x2='layover T2'
                laydf1.loc[len(laydf1.index)] = [or_terminal.loc[i, 'bus_name'],
                                                 or_terminal.loc[i, 'Time of Arrival'], ready_for_depart, x2]
                #adding arrived vehicle to the terminal pool
                pool.loc[len(pool.index)] = [or_terminal.loc[i, 'bus_name'], ready_for_depart]
                #sorting pool based on the minimum time for next departure IN ASCENTING ORDER
                pool.sort_values(by=['Ready_to_depart'], ascending=True, inplace=True)
                pool.reset_index(drop=True, inplace=True)
                temp_pool = pool[pool['Ready_to_depart'] <= or_terminal.loc[i, 'Time of Arrival']]
                or_terminal.loc[i, 'Pool'] = len(temp_pool.index)

    #Timetable for the route
    timetable = pd.concat([tt_terminal1, tt_terminal2], axis=1, ignore_index=True)
    timetable.columns = ['Dep T1', 'Pool T1', 'Dep/Arrival T1', 'bus_name1', 'Departure_from_T1', 'Time of Arr T1',
                         'Fleet T1', 'Dep T2', 'Pool T2', 'Dep/Arrival T2', 'bus_name2', 'Departure_from_T2',
                         'Time of Arr T2', 'Fleet T2']

    # CREW SCHEDULING---------------------
    total_crew = fleet['crew'].sum()

    # Dataframe to store crew and vehicle despatch details from depo
    crew = pd.DataFrame(index=np.arange(0), columns=['Time', 'Crew', 'buses to be dispatched '])
    time_period = start_ser - 1
    for i in range(start_ser - 1, end_ser):
        df5 = fleet[fleet['start_shift1'] == i]
        bus = df5.loc[:, 'bus_name'].tolist()
        crew_hr = df5['crew'].sum()
        time = str(i + .00) + '-' + str(i + .59)
        crew.loc[len(crew.index)] = [time, crew_hr, bus]

    # VEHICLE SCHEDULING
    # T1 TO T2--------------------------------------------------------------------------------------------------------------
    # veh_sch1= departure data from terminal 1
    veh_sch1 = pd.DataFrame(index=departuretimeDN.index,
                            columns=['bus_name', 'start', 'end', 'remarks'])
    veh_sch1['start'] = departuretimeDN['Arrival_T1']  # time at which bus arrives at origin for a trip
    veh_sch1['end'] = departuretimeDN['Arr_time T2']  # time at which bus arrives at destination end of the trip
    veh_sch1['remarks'] = A + '_to_' + B
    temp_bn = []
    for i in range(0, len(timetable.index)):
        if timetable.loc[i, 'Dep/Arrival T1'] == 'Departure':
            temp_bn.append(timetable.loc[i, 'bus_name1'])

    veh_sch1['bus_name'] = temp_bn

    # T2 TO T1-------------------------------------------------------------
    # veh_sch2= departure data from terminal 2
    veh_sch2 = pd.DataFrame(index=departuretimeUP.index,
                            columns=['bus_name', 'start', 'end', 'remarks'])
    veh_sch2['remarks'] = B + '_to_' + A
    veh_sch2['start'] = departuretimeUP['Arrival_T2']
    veh_sch2['end'] = departuretimeUP['Arr_time T1']
    temp_bn = []
    for i in range(0, len(timetable.index)):
        if timetable.loc[i, 'Dep/Arrival T2'] == 'Departure':
            temp_bn.append(timetable.loc[i, 'bus_name2'])
    veh_sch2['bus_name'] = temp_bn

    depott = depot_tt[['bus_name', 'departure_to_depo', 'terminal_arrival']].copy()
    depott['remarks'] = 'shift'
    depott.columns = ['bus_name', 'start', 'end', 'remarks']
    veh_sch = pd.concat([veh_sch1, veh_sch2, depott, laydf1], axis=0, ignore_index=True)
    veh_sch = veh_sch.sort_values(by=['start']).reset_index(drop=True)
    bus_name = veh_sch.bus_name.unique()
    d = {}

    # start of a trip = arrival of the bus at origin terminal
    veh_schedule = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'No:', 'start', 'end', 'remarks', 'bus_@'])
    bus_details = pd.DataFrame(index=np.arange(0), columns=['bus_name', 'No: of trips', 'Ideal time'])
    for i in range(0, len(bus_name)):
        no_trips = 0
        df3 = veh_sch[veh_sch['bus_name'] == bus_name[
            i]].copy()  # df3 store data of bus_name[i] which includes trip data, layover details, shift details
        df3.reset_index(drop=True, inplace=True)
        for j in range(0, len(df3.index)):
            # Calculation of ideal time
            if df3.iloc[j, 3] == A + '_to_' + B or df3.iloc[j, 3] == B + '_to_' + A:
                no_trips = no_trips + 1
                nn = no_trips
            else:
                nn = '_____'
            if df3.iloc[j, 3] == A + '_to_' + B:
                dist = dead_todepot_t1
            elif df3.iloc[j, 3] == B + '_to_' + A:
                dist = dead_todepot_t2
            else:
                pass
            if df3.loc[j, 'remarks'] == 'layover T2' or df3.loc[j, 'remarks'] == 'layover T1':
                pass
            else:
                if j == 0: #first trip
                    if df3.loc[j, 'start'] < start_ser:

                        tp_start = df3.loc[j, 'start'] - dist
                        tp_end = df3.loc[j, 'start']
                        remark = 'shift'
                        veh_schedule.loc[len(veh_schedule)] = [bus_name[i], '_____', tp_start, tp_end, remark, '---']

                    else:
                        tp_start = df3.loc[j, 'start'] - dist
                        tp_end = df3.loc[j, 'start']
                        tpremark = 'shift'
                        Idl_start = start_ser
                        Idl_end = tp_start
                        remark = 'ideal'
                        veh_schedule.loc[len(veh_schedule)] = [bus_name[i], '_____', Idl_start, Idl_end, remark, 'Depo']
                        veh_schedule.loc[len(veh_schedule)] = [bus_name[i], '_____', tp_start, tp_end, tpremark, '---']
                else:
                    Idl_start = df3.loc[j - 1, 'end']
                    Idl_end = df3.loc[j, 'start']
                    remark = 'ideal'
                    if df3.loc[j - 1, 'remarks'] == 'layover T1':
                        x3 = 'T1'
                    elif df3.loc[j - 1, 'remarks'] == 'layover T2':
                        x3 = 'T2'
                    elif df3.loc[j, 'remarks'] == A + '_to_' + B:
                        x3 = 'T1'
                    else:
                        x3 = 'T1'
                    veh_schedule.loc[len(veh_schedule)] = [bus_name[i], '_____', Idl_start, Idl_end, remark, x3]
            veh_schedule.loc[len(veh_schedule)] = [df3.iloc[j, 0], nn, df3.iloc[j, 1], df3.iloc[j, 2],
                                                   df3.iloc[j, 3], '---']

        if df3.loc[len(df3.index) - 1, 'end'] >= end_ser:
            pass
        else:
            Idl_start = df3.loc[j - 1, 'end']
            Idl_end = end_ser
            remark = 'ideal'
            if df3.loc[j - 1, 'remarks'] == 'layover T1':
                x3 = 'T1'
            elif df3.loc[j - 1, 'remarks'] == 'layover T2':
                x3 = 'T2'
            elif df3.loc[j, 'remarks'] == A + '_to_' + B:
                x3 = 'T1'
            else:
                x3 = 'T2'
            veh_schedule.loc[len(veh_schedule)] = [bus_name[i], '----', Idl_start, Idl_end, remark, x3]
        df4 = veh_schedule[(veh_schedule['bus_name'] == bus_name[i]) & (veh_schedule['remarks'] == 'ideal')].copy()
        df4['dur'] = df4.end - df4.start
        ideal_time = df4['dur'].sum()
        df3 = veh_schedule[(veh_schedule['bus_name'] == bus_name[i])].copy()
        df3.reset_index(drop=True, inplace=True)
        name = bus_name[i]
        df3.to_csv(r'D:\Function files\timetable\timetable1\FIFO\vehicleschedule\{}.csv'.format(name))
        bus_details.loc[len(bus_details)] = [bus_name[i], no_trips, ideal_time]

    veh_schedule.sort_values(by='bus_name', inplace=True, key=natsort_keygen())
    veh_schedule.reset_index(drop=True, inplace=True)

    # Ideal time calculations
    ideal = veh_schedule[(veh_schedule['remarks'] == 'ideal')].copy()
    ideal['Idl_Duration'] = ideal.end - ideal.start
    reuse_buses = ideal[ideal['Idl_Duration'] > max_ideal]
    reuse_buses.reset_index(drop=True, inplace=True)

    # Visualisation of bus schedule
    # Visual_sched= Dataframe used to generate the visuals
    visual_sched = veh_schedule[['bus_name', 'start', 'end', 'remarks']].copy()
    visual_sched = visual_sched[(visual_sched['remarks'] != 'ideal')]
    visual_sched.loc[visual_sched['remarks'] == 'layover T2', 'remarks'] = 'layover'
    visual_sched.loc[visual_sched['remarks'] == 'layover T1', 'remarks'] = 'layover'
    visual_resuse = reuse_buses[['bus_name', 'start', 'end']].copy()
    visual_resuse['remarks'] = 'Ideal<'+str(max_ideal)+'hrs'
    visual_resuse.columns = ['bus_name', 'start', 'end', 'legend']
    visual_sched.columns = ['bus_name', 'start', 'end', 'legend']
    visual_sched = pd.concat([visual_sched, visual_resuse], axis=0, ignore_index=True)
    visual_sched['Duration'] = visual_sched.end - visual_sched.start

    # Legend
    def color(row):
        c_dict = {A + '_to_' + B: '#E64646', B + '_to_' + A: '#ffb957', 'Ideal<'+str(max_ideal)+'hrs': '#309c00', 'layover': '#ada55c',
                  'shift': '#00f7ff'}
        return c_dict[row['legend']]

    visual_sched['color'] = visual_sched.apply(color, axis=1)

    fig, ax = plt.subplots(1, figsize=(16, 10))
    plt.xlim(5, 24)

    ax.barh(visual_sched.bus_name, visual_sched.Duration, left=visual_sched.start, color=visual_sched.color,
            height=0.2)
    # Legend
    c_dict = {A + '_to_' + B: '#E64646', B + '_to_' + A: '#ffb957', 'Ideal<'+str(max_ideal)+'hrs': '#309c00', 'layover': '#ada55c',
              'shift': '#00f7ff'}
    legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
    plt.legend(handles=legend_elements)

    # TEXT
    for idx, row in visual_sched.iterrows():
        ax.text(row.end + 0.01, row.bus_name, row.end, va='center', alpha=0.8, fontsize=3)
        ax.text(row.start - 0.01, row.bus_name, row.start, va='center', ha='right', alpha=0.8, fontsize=3)

    duration_values = visual_sched['Duration'].tolist()

    # fig = px.bar(visual_sched, y='bus_name', color='legend', orientation = "h",
    #              text='legend',
    #              hover_data=["bus_name", "Duration", "start", "end", "legend"],
    #              title = 'Vehicle Schedule FIFO',
    #              barmode = 'relative',
    #              width = visual_sched['Duration'].values) # Set the x-axis range based on the maximum 'Duration'

    # fig.update_traces(x=visual_sched['start'])  # Set the starting point of the bars
    fig = px.bar(visual_sched, x = visual_sched['start'].values, y='bus_name', color='legend', orientation="h",
             text='legend',
             hover_data=["bus_name", "Duration", "start", "end", "legend"],
             title='Vehicle Schedule FIFO',
             barmode='relative')

    duration_values = visual_sched['Duration'].values.tolist()  # Convert to list

    for i, duration in enumerate(duration_values):
        fig.update_traces(width=[duration], selector=dict(name=i))
    fig.update_layout()
    plt.grid()
    plt.tight_layout()
    fig.show()

    # fig = px.timeline(visual_sched, x_start="start", x_end="end", y="bus_name", color="legend")

    # pyo.plot(fig, filename='chart.html')


@app.route('/csv-upload')
def process():
    return render_template('uploadcsv.html')

@app.route('/process-csv2', methods=['POST'])
def process_c():
    # Check if a file was uploaded
    if 'csv_file' not in request.files:
        return "No file uploaded", 400

    # Get the uploaded file
    file = request.files['csv_file']

    # Read the optimization results from the CSV file
    results = []
    if file:
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            results.append(row)

    # Render the HTML template with the results
    return render_template('freq_set_copy.html', results=results)

@app.route('/process-csv', methods=['POST'])
def process_csv():
    if 'csv_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['csv_file']

    if file.filename == '':
        return 'No file selected', 400

    if file and file.filename.endswith('.csv'):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file)

        # Perform the optimization and get the results
        # ...

        # Format the results as a list of dictionaries
        results = []
        for index, row in df.iterrows():
            result = {
                'Time Period from': row['Time Period from'],
                'Optimized Frequency down': row['Optimized Frequency down'],
                'Optimized Headway down': row['Optimized Headway down'],
                'Optimized Frequency up': row['Optimized Frequency up'],
                'Optimized Headway up': row['Optimized Headway up']
            }
            results.append(result)
        
        return jsonify(results)

    return 'Invalid file format', 400

@app.route('/costup')
def display_data():
    data = []
    with open(r'D:\Function files\Output GA\cost_calculations_up.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    return render_template('costup.html', data=data)

bus_stops = [
    "Central Bus Terminus at Howrah Rly. Station",
    "Santragachi Bus Terminus",
    "Shalimar Bus Terminus",
    "Bagnan Bus Terminus",
    "SBSTC Bus Terminus under the viaduct of Vidyasagar Setu",
    "Uluberia Bus Terminus",
    "Udaynarayanpur Bus Terminus",
    "Gadiara Bus Terminus",
    "Danesh Sheikh Lane Bus Terminus",
    "Bakultala Bus Terminus",
    "Botanical Garden Bus Terminus",
    "Bally Khal Bus Terminus"
]
@app.route('/busstops')
def busstops():
    return jsonify(bus_stops), render_template('busstops.html')

@app.route('/upload_file')
def file_upload():
    return render_template('file_upload.html')

@app.route('/insert-data', methods=['GET', 'POST'])
def insert_data():
    try:
        Bus_route_name = request.form['Bus_route_name']
        Terminal_1_origin = request.form['Terminal_1_origin']
        Terminal_2_destination = request.form['Terminal_2_destination']
        Bus_service_timings_From = request.form['Bus_service_timings_From']
        Bus_service_timings_To = request.form['Bus_service_timings_To']
        Number_of_service_periods = request.form['Number_of_service_periods']
        

        c = conn.cursor()

        query = "insert into route_info (Bus_route_name, Terminal_1_origin, Terminal_2_destination, Bus_service_timings_From, Bus_service_timings_To , Number_of_service_periods ) VALUES (%s,%s,%s,%s,%s,%s)"

        c.execute(query, (Bus_route_name, Terminal_1_origin, Terminal_2_destination, Bus_service_timings_From, Bus_service_timings_To , Number_of_service_periods))
        conn.commit()

        with open('distanceUP.csv', 'r') as file:
            reader = zip(*csv.reader(file))
            # Create an empty list to hold the rows of data
            rows1 = []
            # Loop through each row in the reader object and append it to the list
            for row in reader:
                rows1.append(row)


        with open('distanceDN.csv', 'r') as file:
            reader = zip(*csv.reader(file))
            # Create an empty list to hold the rows of data
            rows2 = []
            # Loop through each row in the reader object and append it to the list
            for row in reader:
                rows2.append(row)

        # timeperiod DOWN
        c.execute("SELECT * FROM timeperiodDN")
        time1 = c.fetchall()

        # timeperiod UP
        c.execute("SELECT * FROM timeperiodUP")
        time2 = c.fetchall()

        # Define the header row for the CSV file
        header = ['Bus_route_name', 'Terminal_1_origin', 'Terminal_2_destination', 'Bus_service_timings_From', 'Bus_service_timings_To', 'Number_of_service_periods']

        # Define the row of data to be written to the CSV file
        data = [Bus_route_name, Terminal_1_origin, Terminal_2_destination, Bus_service_timings_From, Bus_service_timings_To, Number_of_service_periods]
        
        # Open the CSV file in 'write' mode and write the data to it
        with open('route_info.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(header)
            
            # Write the data row
            writer.writerow(data)
        conn.close()

        return render_template('index.html',rows1=rows1, rows2 = rows2, time1 = time1 , time2 = time2)
    except Exception as e:
        print(e)
        return "An error occurred"

    

@app.route('/submit', methods=['POST'])
def submit():
    # Get data from form
    A = request.form['A']
    B = request.form['B']
    frequencydefault = request.form['frequencydefault']
    seatcap = request.form['seatcap']
    min_c_lvl = request.form['min_c_lvl']
    max_c_lvl = request.form['max_c_lvl']
    max_wait = request.form['max_wait']
    bus_left = request.form['bus_left']
    min_dwell = request.form['min_dwell']
    slack = request.form['slack']
    lay_overtime = request.form['lay_overtime']
    buscost = request.form['buscost']
    buslifecycle = request.form['buslifecycle']
    crewperbus = request.form['crewperbus']
    crewincome = request.form['crewincome']
    cr_trip = request.form['cr_trip']
    cr_day = request.form['cr_day']
    busmaintenance = request.form['busmaintenance']
    fuelprice = request.form['fuelprice']
    kmperliter = request.form['kmperliter']
    kmperliter2 = request.form['kmperliter2']
    c_cantboard = request.form['c_cantboard']
    c_waittime = request.form['c_waittime']
    c_invehtime = request.form['c_invehtime']
    penalty = request.form['penalty']
    hrinperiod = request.form['hrinperiod']
    ser_period = request.form['ser_period']

    # Vehicle and crew scheduling

    dead_todepot_t1 = request.form['dead_todepot_t1']
    dead_todepot_t2 = request.form['dead_todepot_t2']
    layover_depot = request.form['layover_depot']
    start_ser = request.form['start_ser']
    end_ser = request.form['end_ser']
    shift = request.form['shift']
    max_ideal = request.form['max_ideal']

    # Genetic algorith parameters

    sol_per_pop = request.form['sol_per_pop']
    num_generations = request.form['num_generations']

    # CONSTRAINTS FULL DAY SERVICES

    max_oppp = request.form['max_oppp']
    min_ppvk = request.form['min_ppvk']
    min_ppt = request.form['min_ppt']
    max_ocpp = request.form['max_ocpp']
    max_fleet = request.form['max_fleet']
    max_ppl = request.form['max_ppl']
    min_crr = request.form['min_crr']

    # CONSTRAINTS TRIP WISE

    min_ppp = request.form['min_ppp']
    max_pplpt = request.form['max_pplpt']
    min_rvpt = request.form['min_rvpt']
    max_opc = request.form['max_opc']

    # Write data to MYSQL
    cursor = conn.cursor()

    query = """Insert into data_scheduling(A, B, frequencydefault, seatcap, min_c_lvl, max_c_lvl, max_wait, bus_left, min_dwell, slack, lay_overtime ,
    buscost,buslifecycle , crewperbus,crewincome, cr_trip , cr_day, busmaintenance , fuelprice, kmperliter, kmperliter2, c_cantboard ,c_waittime,
    c_invehtime, penalty, hrinperiod, ser_period, dead_todepot_t1, dead_todepot_t2, layover_depot, start_ser, end_ser, shift, max_ideal, sol_per_pop,
    num_generations, max_oppp, min_ppvk, min_ppt,max_ocpp, max_fleet, max_ppl, min_crr, min_ppp, max_pplpt, min_rvpt, max_opc) VALUES (%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   
    # collection.insert_one(data)
    cursor.execute(query,(A, B, frequencydefault, seatcap, min_c_lvl, max_c_lvl, max_wait, bus_left, min_dwell, slack, lay_overtime, buscost, buslifecycle,
                     crewperbus, crewincome, cr_trip, cr_day, busmaintenance, fuelprice, kmperliter, kmperliter2, c_cantboard, c_waittime, c_invehtime, penalty, hrinperiod,
                     ser_period, dead_todepot_t1, dead_todepot_t2, layover_depot, start_ser, end_ser, shift, max_ideal, sol_per_pop, num_generations, max_oppp, min_ppvk, min_ppt,
                     max_ocpp, max_fleet, max_ppl, min_crr, min_ppp, max_pplpt, min_rvpt, max_opc))
    conn.commit()

     # Write data to CSV
    with open('parameters.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['A', 'B', 'frequencydefault', 'seatcap', 'min_c_lvl', 'max_c_lv', 'max_wait', 'bus_left', 'min_dwell', 'slack', 'lay_overtime', 'buscost', 'buslifecycle',
                     'crewperbus', 'crewincome', 'cr_trip', 'cr_day', 'busmaintenance', 'fuelprice', 'kmperliter', 'kmperliter2', 'c_cantboard', 'c_waittime', 'c_invehtime', 'penalty', 'hrinperiod',
                     'ser_period', 'dead_todepot_t1', 'dead_todepot_t2', 'layover_depot', 'start_ser', 'end_ser', 'shift', 'max_ideal', 'sol_per_pop', 'num_generations', 'max_oppp', 'min_ppvk', 'min_ppt',
                     'max_ocpp', 'max_fleet', 'max_ppl', 'min_crr', 'min_ppp', 'max_pplpt', 'min_rvpt', 'max_opc'])
        # create a list of the data that you want to write to the CSV file
        data = [A, B, frequencydefault, seatcap, min_c_lvl, max_c_lvl, max_wait, bus_left, min_dwell, slack, lay_overtime, buscost, buslifecycle,
                crewperbus, crewincome, cr_trip, cr_day, busmaintenance, fuelprice, kmperliter, kmperliter2, c_cantboard, c_waittime, c_invehtime, penalty, hrinperiod,
                ser_period, dead_todepot_t1, dead_todepot_t2, layover_depot, start_ser, end_ser, shift, max_ideal, sol_per_pop, num_generations, max_oppp, min_ppvk, min_ppt,
                max_ocpp, max_fleet, max_ppl, min_crr, min_ppp, max_pplpt, min_rvpt, max_opc]
        writer.writerow(data)

    # Open the CSV file
    with open('parameters.csv', newline='') as csvfile:
        # Read the CSV data into a dictionary
        data = csv.DictReader(csvfile)

    # Open the YAML file
    with open('parameters.yml', 'w') as ymlfile:
        # Write the YAML data to the file
        yaml.dump(data, ymlfile)


    # Close the database connection
    cursor.close()
    conn.close()

    return render_template('index.html')

@app.route('/stop_coef',methods=['POST'])
def stop_coef():
    try:
        Attributes = request.form['Attributes']
        Const = request.form['Const']
        No_of_Boarding = request.form['No_of_Boarding']
        No_of_Alighting = request.form['No_of_Alighting']
        Occupancy_Level = request.form['Occupancy_Level']
        Morning_Peak = request.form['Morning_Peak']
        Before_Intersection = request.form['Before_Intersection']
        Far_from_Intersection = request.form['Far_from_Intersection']
        Commercial = request.form['Commercial']
        Transport_hub = request.form['Transport_hub']
        Bus_Bay = request.form['Bus_Bay']
        
        c = conn.cursor()

        query = "insert into stop_OLS_coefficient (Attributes, Const, No_of_Boarding, No_of_Alighting, Occupancy_Level , Morning_Peak , Before_Intersection, Far_from_Intersection, Commercial, Transport_hub ,Bus_Bay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        c.execute(query, (Attributes, Const, No_of_Boarding, No_of_Alighting, Occupancy_Level , Morning_Peak, Before_Intersection, Far_from_Intersection, Commercial, Transport_hub, Bus_Bay))
        conn.commit()
       
        # Define the header row for the CSV file
        header = ['Attributes', 'Const', 'No_of_Boarding', 'No_of_Alighting', 'Occupancy_Level', 'Morning_Peak', 'Before_Intersection', 'Far_from_Intersection', 'Commercial', 'Transport_hub', 'Bus_Bay']

        # Define the row of data to be written to the CSV file
        data = [Attributes, Const, No_of_Boarding, No_of_Alighting, Occupancy_Level, Morning_Peak, Before_Intersection, Far_from_Intersection, Commercial, Transport_hub, Bus_Bay]

        # Open the CSV file in 'write' mode and write the data to it
        with open('stop OLS coefficient.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(header)

            # Write the data row
            writer.writerow(data)

        conn.close()

        return render_template('index.html')
    except Exception as e:
        print(e)
        return "An error occurred"

@app.route('/passenger_arrival_UP', methods=['GET', 'POST'])
def passenger_arrival_UP():
    if request.method == 'POST':
        # Extract form data from request object
        data = request.form.to_dict()
        
        # Connect to MySQL database
        c = conn.cursor()
        
        # Insert each row into the database
        for i in range(1, 17):
            values = (data[f'Passenger{i}'], data[f'Garia{i}'], data[f'Patuli PS{i}'],data[f'Peerless{i}'], data[f'Ajaynagar{i}'], data[f'Kalikapur{i}'],data[f'Ruby hospital{i}'],data[f'VIP Bazaar{i}'], data[f'Science City{i}'], data[f'Metroplitan{i}'],data[f'Beliaghata XING{i}'],data[f'HUDCO{i}'], data[f'Khanna Cinema{i}'], data[f'Shyambazar{i}'], data[f'Bagbazar{i}'])
            # sql_query = "INSERT INTO Passenger_arrival_UP(Passenger, Garia, Patuli PS, Peerless, Ajaynagar, Kalikapur, Ruby hospital, VIP Bazaar, Science City, Metroplitan, Beliaghata XING, HUDCO, Khanna Cinema, Shyambazar, Bagbazar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_query = "INSERT INTO `Passenger_arrival_UP`(`Passenger`, `Garia`, `Patuli PS`, `Peerless`, `Ajaynagar`, `Kalikapur`, `Ruby hospital`, `VIP Bazaar`, `Science City`, `Metroplitan`, `Beliaghata XING`, `HUDCO`, `Khanna Cinema`, `Shyambazar`, `Bagbazar`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            c.execute(sql_query, values)
        
        # Commist changes to database
        conn.commit()
        
         # Define the header row for the CSV file
        header = ['Passenger', 'Garia', 'Patuli PS', 'Peerless', 'Ajaynagar', 'Kalikapur', 'Ruby hospital', 'VIP Bazaar', 'Science City', 'Metroplitan', 'Beliaghata XING', 'HUDCO', 'Khanna Cinema', 'Shyambazar', 'Bagbazar']
        
        # Define the row of data to be written to the CSV file
        data_row = [data[f'Passenger{i}'] for i in range(1, 17)]
        data_row.extend([data[f'Garia{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Patuli PS{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Peerless{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Ajaynagar{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Kalikapur{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Ruby hospital{i}'] for i in range(1, 17)])
        data_row.extend([data[f'VIP Bazaar{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Science City{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Metroplitan{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Beliaghata XING{i}'] for i in range(1, 17)])
        data_row.extend([data[f'HUDCO{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Khanna Cinema{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Shyambazar{i}'] for i in range(1, 17)])
        data_row.extend([data[f'Bagbazar{i}'] for i in range(1, 17)])
        
        # Open the CSV file in 'write' mode and write the data to it
        with open('Passenger_arrival_UP.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(header)
            
            # Write the data row
            writer.writerow(data_row)

        # Close database connection
        conn.close()
        
        return render_template('table.html')
    
@app.route('/passenger_arrival_DN', methods=['GET', 'POST'])
def passenger_arrival_DN():
    if request.method == 'POST':
        # Extract form data from request object
        data = request.form.to_dict()
        
        # Connect to MySQL database
        c = conn.cursor()
        
        # Insert each row into the database
        for i in range(1, 16):
            values = (data[f'entry{i}'], data[f'entry{i}'], data[f'entry{i}'],data[f'entry{i}'], data[f'entry{i}'], data[f'entry{i}'],data[f'entry{i}'],data[f'entry{i}'], data[f'entry{i}'], data[f'entry{i}'],data[f'entry{i}'],data[f'entry{i}'], data[f'entry{i}'], data[f'entry{i}'], data[f'entry{i}'])
            # sql_query = "INSERT INTO Passenger_arrival_UP(Passenger, Garia, Patuli PS, Peerless, Ajaynagar, Kalikapur, Ruby hospital, VIP Bazaar, Science City, Metroplitan, Beliaghata XING, HUDCO, Khanna Cinema, Shyambazar, Bagbazar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_query = "INSERT INTO `Passenger_arrival_DN`(`Passenger`, `Bagbazar`, `Shyambazar`,`Khanna Cinema`, `HUDCO`,  `Beliaghata XING`, `Metroplitan`, `Science City`, `VIP Bazaar`, `Ruby hospital`,`Kalikapur`, `Ajaynagar`, `Peerless`, `Patuli PS`,`Garia`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            c.execute(sql_query, values)
        
        # Commit changes to database
        conn.commit()
        
        # Open CSV file for writing
        with open('Passenger_arrival_DN.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write headers to CSV file
            writer.writerow(['Passenger', 'Bagbazar', 'Shyambazar', 'Khanna Cinema', 'HUDCO', 'Beliaghata XING', 'Metroplitan', 'Science City', 'VIP Bazaar', 'Ruby hospital', 'Kalikapur', 'Ajaynagar', 'Peerless', 'Patuli PS', 'Garia'])

            # Write data rows to CSV file
            for i in range(1, 16):
                row = [data[f'entry{i}'] for i in range(1, 16)]
                writer.writerow(row)

        # Close database connection
        conn.close()
        
        return render_template('table.html')


    
@app.route('/fare_UP', methods=['GET', 'POST'])
def fare_UP():
     if request.method == 'POST':
            # Get data from the HTML form
            stops = request.form.getlist('stops[]')
            garia = request.form.getlist('garia[]')
            patuli = request.form.getlist('patuli[]')
            peerless = request.form.getlist('peerless[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            science_city = request.form.getlist('science_city[]')
            metropolitan = request.form.getlist('metropolitan[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            hudco = request.form.getlist('hudco[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            shyambazar = request.form.getlist('shyambazar[]')
            bagbazar = request.form.getlist('bagbazar[]')

     
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(stops)):
                sql = "INSERT INTO `fare_UP`( `Stops`, `Garia`, `Patuli PS`, `Peerless`, `Ajaynagar`, `Kalikapur`, `Ruby hospital`, `VIP Bazaar`, `Science City`, `Metroplitan`, `Beliaghata XING`, `HUDCO`, `Khanna Cinema`, `Shyambazar`, `Bagbazar`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                val = (stops[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i])
                cur.execute(sql, val)
            conn.commit()

            # Write data to CSV file
            with open('fare_UP.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Stops', 'Garia', 'Patuli PS', 'Peerless', 'Ajaynagar', 'Kalikapur', 'Ruby hospital', 'VIP Bazaar', 'Science City', 'Metroplitan', 'Beliaghata XING', 'HUDCO', 'Khanna Cinema', 'Shyambazar', 'Bagbazar'])
                for i in range(len(stops)):
                    writer.writerow([stops[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i]])
            
            return render_template('table.html')
  

@app.route('/fare_DN', methods=['GET', 'POST'])
def fare_DN():
     if request.method == 'POST':
            # Get data from the HTML form
            stops = request.form.getlist('stops[]')
            bagbazar = request.form.getlist('bagbazar[]')
            shyambazar = request.form.getlist('shyambazar[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            hudco = request.form.getlist('hudco[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            metropolitan = request.form.getlist('metropolitan[]')
            science_city = request.form.getlist('science_city[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            peerless = request.form.getlist('peerless[]')
            patuli = request.form.getlist('patuli[]')
            garia = request.form.getlist('garia[]')
            
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(stops)):
                sql = "INSERT INTO `fare_DN`(`Stops`, `Bagbazar`, `Shyambazar`,`Khanna Cinema`, `HUDCO`,  `Beliaghata XING`, `Metroplitan`, `Science City`, `VIP Bazaar`, `Ruby hospital`,`Kalikapur`, `Ajaynagar`, `Peerless`, `Patuli PS`,`Garia`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (stops[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i])
                cur.execute(sql, val)
            conn.commit()

            # Write data to CSV file
            with open('fare_DN.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Stops', 'Bagbazar', 'Shyambazar', 'Khanna Cinema', 'HUDCO', 'Beliaghata XING', 'Metroplitan', 'Science City', 'VIP Bazaar', 'Ruby hospital', 'Kalikapur', 'Ajaynagar', 'Peerless', 'Patuli PS', 'Garia'])
                for i in range(len(stops)):
                    writer.writerow([stops[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i]])
            
            return render_template('table.html')
     
@app.route('/alighting_rate_UP', methods=['GET', 'POST'])
def alighting_rate_UP():
     if request.method == 'POST':
            # Get data from the HTML form
            alighting = request.form.getlist('alighting[]')
            garia = request.form.getlist('garia[]')
            patuli = request.form.getlist('patuli[]')
            peerless = request.form.getlist('peerless[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            science_city = request.form.getlist('science_city[]')
            metropolitan = request.form.getlist('metropolitan[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            hudco = request.form.getlist('hudco[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            shyambazar = request.form.getlist('shyambazar[]')
            bagbazar = request.form.getlist('bagbazar[]')

     
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(alighting)):
                sql = "INSERT INTO `alighting_rate_UP`( `Alighting`, `Garia`, `Patuli PS`, `Peerless`, `Ajaynagar`, `Kalikapur`, `Ruby hospital`, `VIP Bazaar`, `Science City`, `Metroplitan`, `Beliaghata XING`, `HUDCO`, `Khanna Cinema`, `Shyambazar`, `Bagbazar`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                val = (alighting[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i])
                cur.execute(sql, val)
            conn.commit()

            # Write data to CSV file
            with open('alighting_rate_UP.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow(['Alighting', 'Garia', 'Patuli PS', 'Peerless', 'Ajaynagar', 'Kalikapur', 'Ruby hospital', 'VIP Bazaar', 'Science City', 'Metroplitan', 'Beliaghata XING', 'HUDCO', 'Khanna Cinema', 'Shyambazar', 'Bagbazar'])
                # Write data rows
                for i in range(len(alighting)):
                    writer.writerow([alighting[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i]])
            
            return render_template('table.html')
     
@app.route('/alighting_rate_DN', methods=['GET', 'POST'])
def alighting_rate_DN():
     if request.method == 'POST':
            # Get data from the HTML form
            alighting = request.form.getlist('alighting[]')
            bagbazar = request.form.getlist('bagbazar[]')
            shyambazar = request.form.getlist('shyambazar[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            hudco = request.form.getlist('hudco[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            metropolitan = request.form.getlist('metropolitan[]')
            science_city = request.form.getlist('science_city[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            peerless = request.form.getlist('peerless[]')
            patuli = request.form.getlist('patuli[]')
            garia = request.form.getlist('garia[]')
            
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(alighting)):
                sql = "INSERT INTO `alighting_rate_DN`(`Alighting`, `Bagbazar`, `Shyambazar`,`Khanna Cinema`, `HUDCO`,  `Beliaghata XING`, `Metroplitan`, `Science City`, `VIP Bazaar`, `Ruby hospital`,`Kalikapur`, `Ajaynagar`, `Peerless`, `Patuli PS`,`Garia`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (alighting[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i])
                cur.execute(sql, val)
            conn.commit()

             # Store data in a CSV file
            with open('alighting_rate_DN.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                headers = ['Alighting', 'Bagbazar', 'Shyambazar', 'Khanna Cinema', 'HUDCO', 'Beliaghata XING', 'Metroplitan', 'Science City', 'VIP Bazaar', 'Ruby hospital', 'Kalikapur', 'Ajaynagar', 'Peerless', 'Patuli PS', 'Garia']
                writer.writerow(headers)
                for i in range(len(alighting)):
                    row = [alighting[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i]]
                    writer.writerow(row)

            return render_template('table.html')


@app.route('/TraveTimeUP_ANN', methods=['GET', 'POST'])
def TraveTimeUP_ANN():
     if request.method == 'POST':
            # Get data from the HTML form
            travel_time = request.form.getlist('travel_time[]')
            garia = request.form.getlist('garia[]')
            patuli = request.form.getlist('patuli[]')
            peerless = request.form.getlist('peerless[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            science_city = request.form.getlist('science_city[]')
            metropolitan = request.form.getlist('metropolitan[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            hudco = request.form.getlist('hudco[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            shyambazar = request.form.getlist('shyambazar[]')
            bagbazar = request.form.getlist('bagbazar[]')

     
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(travel_time)):
                sql = "INSERT INTO `alighting_rate_UP`( `Travel Time`, `Garia`, `Patuli PS`, `Peerless`, `Ajaynagar`, `Kalikapur`, `Ruby hospital`, `VIP Bazaar`, `Science City`, `Metroplitan`, `Beliaghata XING`, `HUDCO`, `Khanna Cinema`, `Shyambazar`, `Bagbazar`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                val = (travel_time[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i])
                cur.execute(sql, val)
            conn.commit()

            # Write data to CSV file
            with open('TraveTimeUP_ANN.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                headers = ['Travel Time', 'Garia', 'Patuli PS', 'Peerless', 'Ajaynagar', 'Kalikapur', 'Ruby hospital', 'VIP Bazaar', 'Science City', 'Metroplitan', 'Beliaghata XING', 'HUDCO', 'Khanna Cinema', 'Shyambazar', 'Bagbazar']
                writer.writerow(headers)
                for i in range(len(travel_time)):
                    row = [travel_time[i], garia[i], patuli[i], peerless[i], ajaynagar[i], kalikapur[i], ruby_hospital[i], vip_bazaar[i], science_city[i], metropolitan[i], beliaghata_xing[i], hudco[i], khanna_cinema[i], shyambazar[i], bagbazar[i]]
                    writer.writerow(row)
                    
            return render_template('table.html')
     
@app.route('/TravelTimeDN_ann', methods=['GET', 'POST'])
def TravelTimeDN_ann():
     if request.method == 'POST':
            # Get data from the HTML form
            travel_time = request.form.getlist('travel_time[]')
            bagbazar = request.form.getlist('bagbazar[]')
            shyambazar = request.form.getlist('shyambazar[]')
            khanna_cinema = request.form.getlist('khanna_cinema[]')
            hudco = request.form.getlist('hudco[]')
            beliaghata_xing = request.form.getlist('beliaghata_xing[]')
            metropolitan = request.form.getlist('metropolitan[]')
            science_city = request.form.getlist('science_city[]')
            vip_bazaar = request.form.getlist('vip_bazaar[]')
            ruby_hospital = request.form.getlist('ruby_hospital[]')
            kalikapur = request.form.getlist('kalikapur[]')
            ajaynagar = request.form.getlist('ajaynagar[]')
            peerless = request.form.getlist('peerless[]')
            patuli = request.form.getlist('patuli[]')
            garia = request.form.getlist('garia[]')
            
            # Insert data into the MySQL database
            cur = conn.cursor()
            for i in range(len(travel_time)):
                sql = "INSERT INTO `alighting_rate_DN`(`Travel Time`, `Bagbazar`, `Shyambazar`,`Khanna Cinema`, `HUDCO`,  `Beliaghata XING`, `Metroplitan`, `Science City`, `VIP Bazaar`, `Ruby hospital`,`Kalikapur`, `Ajaynagar`, `Peerless`, `Patuli PS`,`Garia`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (travel_time[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i])
                cur.execute(sql, val)
            conn.commit()

            # Save data to a CSV file
            with open('TravelTimeDN_ann.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Travel Time', 'Bagbazar', 'Shyambazar', 'Khanna Cinema', 'HUDCO', 'Beliaghata XING', 'Metroplitan', 'Science City', 'VIP Bazaar', 'Ruby hospital', 'Kalikapur', 'Ajaynagar', 'Peerless', 'Patuli PS', 'Garia'])
                for i in range(len(travel_time)):
                    writer.writerow([travel_time[i], bagbazar[i], shyambazar[i], khanna_cinema[i], hudco[i], beliaghata_xing[i], metropolitan[i], science_city[i], vip_bazaar[i], ruby_hospital[i], kalikapur[i], ajaynagar[i], peerless[i], patuli[i], garia[i]])
            
            return render_template('table.html')

# -------------------------------------------SCHEDULING FILE UPLOAD----------------------------------------------------

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    name = file.filename
    type = file.content_type
    size = file.content_length
    data = file.read()

    # Insert file details into the database
    with conn.cursor() as cursor:
        sql = "INSERT INTO input_holding_files (name, type, size, data) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, type, size, data))
        conn.commit()

    return 'File uploaded successfully!'

@app.route('/files')
def files():
    # Retrieve all files from the database
    with conn.cursor() as cursor:
        sql = "SELECT * FROM input_holding_files"
        cursor.execute(sql)
        files = cursor.fetchall()
        
    print(files)  # Check the files variable
    return render_template('uploaded.html', files=files)

@app.route('/download/<int:file_id>')
def download(file_id):
    # Retrieve file from the database
    with conn.cursor() as cursor:
        sql = "SELECT * FROM input_holding_files WHERE id = %s"
        cursor.execute(sql, (file_id,))
        file = cursor.fetchone()

    # Return the file as a response
    return send_file(BytesIO(file[3]), attachment_filename=file[1], as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
