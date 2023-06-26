from flask import Flask, render_template, make_response, request, session, redirect
import pandas as pd
import os
import glob

from srinath import cost_oned

app= Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'


@app.route('/', methods =['GET', 'POST'])
def srinath():

    if request.method == 'POST':
        passengerarrival = pd.read_csv(os.path.abspath("Passenger_arrival_DN.csv")).set_index('Passenger arrival')
        distance = pd.read_csv(os.path.abspath("distanceDN.csv")).set_index('Distance')
        timeperiod = pd.read_csv(os.path.abspath("tmeperiodDN.csv"), header=0)
        link_traveltime = pd.read_csv(os.path.abspath("TravelTimeDN_ann.csv")).set_index('Travel Time')
        alightrate = pd.read_csv(os.path.abspath("alighting_rate_UP.csv")).set_index('Alighting')
        fare = pd.read_csv(os.path.abspath("fare_DN.csv")).set_index('Stops').fillna(0)
        frequency = pd.read_csv(os.path.abspath("OpFrequencyDN.csv"))

        # passengerarrival = pd.read_csv(request.files['file1']).set_index('Passenger arrival')
        # distance = pd.read_csv(request.files['file2']).set_index('Distance')
        # timeperiod = pd.read_csv(request.files['file3'], header=0)
        # link_traveltime = pd.read_csv(request.files['file4']).set_index('Travel Time')
        # alightrate = pd.read_csv(request.files['file5']).set_index('Alighting')
        # fare = pd.read_csv(request.files['file6']).set_index('Stops').fillna(0)
        # frequency = pd.read_csv(request.files['file7'])


        # OD_down = request.files['OD_down']
        # passengerarrival = request.files['file1']
        # distance = request.files['file2']
        # timeperiod = request.files['file3']
        # link_traveltime = request.files['file4']
        # alightrate = request.files['file5']
        # fare = request.files['file6']
        # frequency = request.files['file7']
        

        path = os.path.abspath("OD_down")
        files = glob.glob(os.path.join(path, '*.csv'))

        # files = glob.glob(OD_down)

        # fuelprice = request.form["fuelprice"]
        # kmperliter = request.form["kmperliter"]
        # busmaintenance = request.form["busmaintenance"]
        # buscost = request.form["buscost"]
        # buslifecycle = request.form["buslifecycle"]
        # crewperbus = request.form["crewperbus"]
        # creqincome = request.form["creqincome"]
        # cr_trip = request.form["cr_trip"]
        # cr_day = request.form["cr_day"]
        # seatcap = request.form["seatcap"]
        # min_c_lvl = request.form["min_c_lvl"]
        # max_c_lvl = request.form["max_c_lvl"]
        # hrinperiod = request.form["hrinperiod"]
        # bus_left = request.form["bus_left"]
        # max_wait = request.form["max_wait"]
        # c_waittime = request.form["c_waittime"]
        # c_invehtime = request.form["c_invehtime"]
        # min_ppp = request.form["min_ppp"]
        # max_pplpt = request.form["max_pplpt"]
        # kmperliter2 = request.form["kmperliter2"]
        # max_opc = request.form["max_opc"]
        # penalty = request.form["penalty"]
        # min_rvpt = request.form["min_rvpt"]
        # c_cantboard = request.form["c_cantboard"]
        # min_dwell = request.form["min_dwell"]

        fuelprice = 92
        kmperliter = 5
        busmaintenance = 5
        buscost = 7000000
        buslifecycle = 800000
        crewperbus = 2
        creqincome = 27500
        cr_trip = 4
        cr_day = 25
        seatcap = 43
        min_c_lvl = 1.5
        max_c_lvl = 2
        hrinperiod = 1
        bus_left = 2
        max_wait = 21
        c_waittime = 0.8
        c_invehtime = 0.4
        min_ppp = 0
        max_pplpt = 100 
        kmperliter2 = 2
        max_opc = 15000
        penalty = 10
        min_rvpt = 0
        c_cantboard = 10
        min_dwell = 30


        despatch,sum_revenue,fixed_cost,t_cost,departuretime,headway,p_lost, travel_time_tot,stoparrival,Totcost_waiting, Totcost_inveh,Totpasslost,cuser,Totpasslost_penalty,totalkilometrerun,fuelcostday,maintenancecost_total_trips,vehdepreciation_total_trips,crewcost_total_trips,coperator,t_cost = cost_oned(passengerarrival,distance,frequency,timeperiod,link_traveltime,alightrate,fare, files, 'optmised frequency',fuelprice, kmperliter, busmaintenance, buscost, buslifecycle, crewperbus, creqincome, cr_trip, cr_day, seatcap, min_c_lvl, max_c_lvl,hrinperiod, bus_left, max_wait, c_waittime,c_invehtime,min_ppp,max_pplpt,kmperliter2,max_opc, penalty,min_rvpt,c_cantboard, min_dwell)

        result_list = [
        despatch, sum_revenue, fixed_cost, t_cost, departuretime, headway, p_lost,
        travel_time_tot, stoparrival, Totcost_waiting, Totcost_inveh, Totpasslost,
        cuser, Totpasslost_penalty, totalkilometrerun, fuelcostday,
        maintenancecost_total_trips, vehdepreciation_total_trips,
        crewcost_total_trips, coperator, t_cost
]


        return render_template("srinath_result.html", result_list = result_list)


        

    return render_template("srinath.html")






# @app.route('/', methods =['GET', 'POST'])
# def srinath():
#     if request.method == 'POST':
#         # passengerarrival = request.files['file1']
#         # distance = request.files['file2']
#         # frequency = request.files['file3']
#         # timeperiod = request.files['file4']
#         # link_traveltime = request.files['file5']
#         # alightrate = request.files['file6']
#         # fare = request.files['file7']


#         # passengerarrival = pd.read_csv(passengerarrival).set_index('Passenger arrival')
#         # distance = pd.read_csv(distance).set_index('Distance')
#         # timeperiod = pd.read_csv(timeperiod, header=0)
#         # link_traveltime = pd.read_csv(link_traveltime).set_index('Travel Time')
#         # alightrate = pd.read_csv(alightrate).set_index('Alighting Rate')
#         # fare = pd.read_csv(fare).set_index('Stops').fillna(0)
#         # frequency = pd.read_csv(frequency)

#         # print(passengerarrival)
#         # print(distance)
#         # print(timeperiod)
#         # print(link_traveltime)
#         # print(alightrate)
#         # print(fare)
#         # print(frequency)

#         passengerarrival = pd.read_csv(r'D:\Function files\Input files\Passenger_arrival_DN.csv').set_index('Passenger arrival')
#         distance = pd.read_csv(r'D:\Function files\Input files\distanceDN.csv').set_index('Distance')
#         timeperiod = pd.read_csv(r'D:\Function files\Input files\tmeperiodDN.csv', header=0)
#         link_traveltime = pd.read_csv(r'D:\Function files\Input files\TravelTimeDN_ann.csv').set_index('Travel Time')
#         alightrate = pd.read_csv(r"D:\Function files\od_output\alighting_rateDN.csv").set_index('Alighting Rate')
#         fare = pd.read_csv(r'D:\Function files\Input files\fare_DN.csv').set_index('Stops').fillna(0)
#         frequency = pd.read_csv(r'D:\Function files\Output GA\OpFrequencyDN.csv')

#         return render_template("srinath.html")

#     return render_template("srinath.html")






if __name__ == '__main__':
    app.run(debug=True)
    
