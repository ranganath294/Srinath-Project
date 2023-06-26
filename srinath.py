import pandas as pd
import numpy as np
import gc
import yaml
from yaml.loader import SafeLoader
import os

from Cost_fn_submodules import dwell_time,wcost

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 2)





# dob= seatcap*min_c_lvl
# cob= int (seatcap*max_c_lvl)


def cost_oned (passengerarrival,distance,frequency,timeperiod,link_traveltime,alightrate,fare, files,purpose, fuelprice, kmperliter, busmaintenance, buscost, buslifecycle, crewperbus, creqincome, cr_trip, cr_day, seatcap, min_c_lvl, max_c_lvl,hrinperiod, bus_left, max_wait, c_waittime,c_invehtime,min_ppp,max_pplpt,kmperliter2,max_opc, penalty,min_rvpt,c_cantboard, min_dwell):

    tot_dis = distance.sum(axis=1, skipna=True).values  # defined Total Distance depot ot depot
    tot_dis = np.ceil(float(np.asarray(tot_dis)))

    # FIXED COST  DIRECTION per trip

    fuelcostrunning = (fuelprice * tot_dis / kmperliter).round(-2).round(0)
    maintenancecost = (tot_dis * busmaintenance).round(0)
    vehdepreciation = ((buscost / buslifecycle) * tot_dis).round(0)
    crewcost = (crewperbus * creqincome / (2 * cr_trip * cr_day))

    dob= seatcap*min_c_lvl
    cob= int (seatcap*max_c_lvl)
    # -------------------------------------------------------------------------------------------------------------------------------------------------------
    # 1. Departure time calculation
    # -------------------------------------------------------------------------------------------------------------------------------------------------------

    time_period= timeperiod.copy()
    time_period['frequency'] = np.ceil(frequency)
    time_period['Headway_in_hours'] = (1 / (frequency)).round(2)


    departuretime = pd.DataFrame()
    headway1 = pd.DataFrame()
    for ind, col in time_period.iterrows():
        if ind == 0:
            for f in range(0, int(time_period.iloc[ind, 1])):
                departuretime = pd.concat([departuretime, pd.DataFrame.from_records([{'Departure': (time_period.iloc[ind, 0]) / 100 + ((f * time_period.iloc[ind, 2]))}])], ignore_index=True)
                headway1 = pd.concat([headway1, pd.DataFrame.from_records([{'Headway': time_period.iloc[ind, 2] * 60}, ])], ignore_index=True)
        else:
            for f in range(0, int(time_period.iloc[ind, 1])):
                if f == 0:
                    headway_avg = (time_period.iloc[ind, 2] + time_period.iloc[ind - 1, 2]) / 2
                    temp_departure = departuretime.iloc[-1, 0] + headway_avg
                    departuretime = pd.concat([departuretime, pd.DataFrame.from_records([{'Departure': temp_departure}])], ignore_index=True)
                    headway1 = pd.concat([headway1, pd.DataFrame.from_records([{'Headway': headway_avg * 60}, ])], ignore_index=True)
                else:
                    departuretime = pd.concat([departuretime, pd.DataFrame.from_records([{'Departure': (time_period.iloc[ind, 0]) / 100 + (f * time_period.iloc[ind, 2])}])], ignore_index=True)
                    headway1 = pd.concat([headway1, pd.DataFrame.from_records([{'Headway': time_period.iloc[ind, 2] * 60}, ])], ignore_index=True)


    del temp_departure
    del headway_avg


    # -------------------------------------------------------------------------------------------------------------------------------------------------------
    #  2. Simulation of full day bus services
    # -------------------------------------------------------------------------------------------------------------------------------------------------------


    arrivalrate = passengerarrival / (hrinperiod * 60)
    # linktravel time, arrival rate, alighting rate  per trip
    link_travel_tr = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    arrivalrate_tr = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    alightrate_tr = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    timeperiod_tr= pd.DataFrame(index=departuretime.index, columns=['time_period'])
    files_tr = [0] * len(departuretime.index)
    ind = -1
    time_period.index = time_period.index + 1
    for i in range(0, len(arrivalrate.index)):
        for m in range(0, int(time_period.iloc[i, 1])):
            ind = ind + 1
            for j in range(0, len(alightrate.columns)):
                link_travel_tr.iloc[ind, j] = link_traveltime.iloc[i, j]
                arrivalrate_tr.iloc[ind, j] = arrivalrate.iloc[i, j]
                alightrate_tr.iloc[ind, j] = alightrate.iloc[i, j]
                files_tr[ind] = files[i]
                timeperiod_tr.iloc[ind,0]= timeperiod.iloc[i,0]

    p_arrival = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    p_waiting = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    p_alight = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    p_board = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    link_occp = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    waitingtime_tr = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    cost_waitingtime = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    p_cantboard = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    p_lost = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    d_time = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    stoparrival = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    headway= pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    traveltime = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    load_fact = pd.DataFrame(index=departuretime.index, columns=arrivalrate.columns)
    invehtime = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns).fillna(0)
    cost_inveh = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    p_sit = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    p_stand = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    revenue= pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns).fillna(0)
    p_cantboard_1= pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    p_cantboard_2= pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    p_cantboard_0 = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    despatch = pd.DataFrame(index=p_arrival.index, columns=arrivalrate.columns)
    # Calculation of passenger arrival, number of boarding, number alighting, link occupancy, dwell time,passenger lost, passenger cannot board, waiting time, in vehicle travel time etc.
    # trip wise calculation for each stop

    for ind in range(0, len(departuretime.index)):
        for j in range(0, len(alightrate.columns)):
            # Travel time from stop j-1 to stop j and Arrival time of bus(ind) at stop j ---------------------

            if j == 0:
                traveltime.iloc[ind, j] = 0

                stoparrival.iloc[ind, j] = departuretime.iloc[ind, 0]-(headway1.iloc[ind, 0]/60)


            else:
                # TRAVEL TIME FROM STOP J-1 TO J = DWELL TIME AT STOP J-1 + LINK RUNNING TIME (J-1,J)
                traveltime.iloc[ind, j] = ((d_time.iloc[ind, j - 1] + link_travel_tr.iloc[ind, j]) / 60).round(4)
                stoparrival.iloc[ind, j] = stoparrival.iloc[ind, j - 1] + traveltime.iloc[ind, j]

            # Headway Calculations of stop j --------------------------------------------------------------
            #headway1= despatch headway

            if j == 0 or ind == 0:

                headway.iloc[ind, j] = headway1.iloc[ind, 0]
            else:
                headway.iloc[ind, j] = abs(stoparrival.iloc[ind, j] - stoparrival.iloc[ind - 1, j]) * 60

            # Passenger lost due to minimum waiting time ---------------------------------------------------------
            if bus_left == 1:
                p_lost_waiting = 0
            elif bus_left == 2:
                if ind == 0:
                    p_cantboard_1.iloc[ind, j] = 0
                    p_lost_waiting = 0
                else:
                    p_cantboard_1.iloc[ind, j] = p_cantboard.iloc[ind - 1, j]
                    if stoparrival.iloc[ind, j] - stoparrival.iloc[ind - 1, j] > max_wait:
                        p_lost_waiting = p_cantboard_1.iloc[ind, j]
                        p_cantboard_1.iloc[ind, j] = 0
                    else:
                        p_lost_waiting = 0
            else:
                if ind == 0:
                    p_cantboard_1.iloc[ind, j] = 0
                    p_cantboard_2.iloc[ind, j] = 0
                else:
                    p_cantboard_2.iloc[ind, j] = p_cantboard_1.iloc[ind - 1, j]
                    p_cantboard_1.iloc[ind, j] = p_cantboard_0.iloc[ind - 1, j]

                # waitting time check

                if ind == 0:
                    p_lost_waiting = 0
                elif ind == 1:
                    if stoparrival.iloc[ind, j] - stoparrival.iloc[ind - 1, j] > max_wait:
                        p_lost_waiting = p_cantboard_1.iloc[ind, j]
                        p_cantboard_1.iloc[ind, j] = 0
                    else:
                        p_lost_waiting = 0
                else:
                    if stoparrival.iloc[ind, j] - stoparrival.iloc[ind - 1, j] > max_wait:
                        p_lost_waiting = p_cantboard_2.iloc[ind, j] + p_cantboard_1.iloc[ind, j]
                        p_cantboard_1.iloc[ind, j] = 0
                        p_cantboard_2.iloc[ind, j] = 0
                    elif stoparrival.iloc[ind, j] - stoparrival.iloc[ind - 2, j] > max_wait:
                        p_lost_waiting = p_cantboard_2.iloc[ind, j]
                        p_cantboard_2.iloc[ind, j] = 0
                    else:
                        p_lost_waiting = 0

            # Passenger arrival and passenger waiting------------------------------------------------

            p_arrival.iloc[ind, j] = np.ceil(arrivalrate_tr.iloc[ind, j] * headway.iloc[ind, j] )

            # waiting time and cost calculation------------------------------------------------------------
            if bus_left == 1:
                waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j])
                waitingtime_0 = 0.5 * headway.iloc[ind, j]
                cw_cost = wcost(waitingtime_0, c_waittime)
                cost_waitingtime.iloc[ind, j] = np.ceil(waitingtime_tr.iloc[ind, j] * cw_cost)
            elif bus_left == 2:
                if ind == 0:
                    waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j])
                    waitingtime_0 = 0.5 * headway.iloc[ind, j]
                    cw_cost = wcost(waitingtime_0, c_waittime)
                    cost_waitingtime.iloc[ind, j] = np.ceil(waitingtime_tr.iloc[ind, j] * cw_cost)
                else:
                    waitingtime_0 = 0.5 * headway.iloc[ind, j]
                    waitingtime_1 = 0.5 * headway.iloc[ind - 1, j] + headway.iloc[ind, j]
                    waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j]) + (p_cantboard.iloc[ind - 1, j] * headway.iloc[ind, j])
                    cost_waitingtime.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_0, c_waittime)) + (p_cantboard_1.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_1, c_waittime))
            else:
                if ind == 0:
                    waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j])
                    waitingtime_0 = 0.5 * headway.iloc[ind, j]
                    cw_cost = wcost(waitingtime_0, c_waittime)
                    cost_waitingtime.iloc[ind, j] = np.ceil(waitingtime_tr.iloc[ind, j] * cw_cost)
                elif ind == 1:
                    waitingtime_0 = 0.5 * headway.iloc[ind, j]
                    waitingtime_1 = 0.5 * headway.iloc[ind - 1, j] + headway.iloc[ind, j]
                    waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j]) + (p_cantboard.iloc[ind - 1, j] * headway.iloc[ind, j])
                    cost_waitingtime.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_0, c_waittime)) + (p_cantboard_1.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_1, c_waittime))

                else:
                    waitingtime_0 = 0.5 * headway.iloc[ind, j]
                    waitingtime_1 = 0.5 * headway.iloc[ind - 1, j] + headway.iloc[ind, j]
                    waitingtime_2 = 0.5 * headway.iloc[ind - 2, j] + headway.iloc[ind - 1, j] + headway.iloc[ind, j]

                    waitingtime_tr.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j]) + (p_cantboard.iloc[ind - 1, j] * headway.iloc[ind, j])
                    cost_waitingtime.iloc[ind, j] = 0.5 * (p_arrival.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_0, c_waittime)) + (p_cantboard_1.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_1, c_waittime)) + (
                            p_cantboard_2.iloc[ind, j] * headway.iloc[ind, j] * wcost(waitingtime_2, c_waittime))

            #  link occupancy/on board passenger of bus(ind) at stop j (Passenger on board j-1 to j)------------------------

            if j == 0:
                # on_board passenger
                link_occp.iloc[ind, j] = 0

            else:
                x = p_board.iloc[[ind], 0:j].sum(axis=1, skipna=True).values
                y = p_alight.iloc[[ind], 0:j].sum(axis=1, skipna=True).values
                x = x[0]  # total passenger boarded till j-1
                y = y[0]  # total passenger alighted till j-1
                # on_board passenger for link j-1 to j
                link_occp.iloc[ind, j] = x - y

            load_fact.iloc[ind, j] = (link_occp.iloc[ind, j] / seatcap)

            # number passengers sitting and standing for jth link (stop j-1 to  stop j)----------

            if link_occp.iloc[ind, j] <= seatcap:
                p_sit.iloc[ind, j] = link_occp.iloc[ind, j]
                p_stand.iloc[ind, j] = 0
            else:
                p_sit.iloc[ind, j] = seatcap
                p_stand.iloc[ind, j] = link_occp.iloc[ind, j] - p_sit.iloc[ind, j]

            # Invehicle time of bus(ind) at stop j--------------------------------------------

            invehtime.iloc[ind, j] = link_occp.iloc[ind, j] * traveltime.iloc[ind, j]

            if load_fact.iloc[ind, j] <= 1:
                cost_inveh.iloc[ind, j] = p_sit.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .35)
            elif load_fact.iloc[ind, j] > 1 and load_fact.iloc[ind, j] <= 1.25:
                cost_inveh.iloc[ind, j] = (p_sit.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .35)) + (p_stand.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .3))

            elif load_fact.iloc[ind, j] > 1.25 and load_fact.iloc[ind, j] <= 1.5:
                cost_inveh.iloc[ind, j] = (p_sit.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .35)) + (p_stand.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .2))

            elif load_fact.iloc[ind, j] > 1.5 and load_fact.iloc[ind, j] < 1.75:
                cost_inveh.iloc[ind, j] = (p_sit.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .35)) + (p_stand.iloc[ind, j] * traveltime.iloc[ind, j] * 60 * (c_invehtime - .1))

            else:
                cost_inveh.iloc[ind, j] = (link_occp.iloc[ind, j] * traveltime.iloc[ind, j] * c_invehtime)

            # Passenger boarding , alighting, passenger cannot board and passenger lost due to overcrowding------------------------------------------------

            p_alight.iloc[ind, j] = np.ceil(link_occp.iloc[ind, j] * alightrate_tr.iloc[ind, j])
            residual = cob - link_occp.iloc[ind, j] + p_alight.iloc[ind, j]

            if bus_left == 1:
                if p_arrival.iloc[ind, j] <= residual:
                    p_board.iloc[ind, j] = p_arrival.iloc[ind, j]
                else:
                    p_board.iloc[ind, j] = residual

                # Passenger lost at stop j due to overcrowding
                p_lost_boarding = p_arrival.iloc[ind, j] - p_board.iloc[ind, j]
                # passenger Cant board bus (ind) at stop j
                p_cantboard.iloc[ind, j] = 0
            elif bus_left == 2:
                if p_cantboard_1.iloc[ind, j] <= residual:
                    p_board_1 = p_cantboard_1.iloc[ind, j]
                    residual = residual - p_board_1
                    if p_arrival.iloc[ind, j] <= residual:
                        p_board_0 = p_arrival.iloc[ind, j]
                    else:
                        p_board_0 = residual
                else:
                    p_board_1 = residual
                    p_board_0 = 0

                p_cantboard_0.iloc[ind, j] = p_arrival.iloc[ind, j] - p_board_0
                p_cantboard_1.iloc[ind, j] = p_cantboard_1.iloc[ind, j] - p_board_1

                p_board.iloc[ind, j] = p_board_0 + p_board_1
                # passenger Cant board bus (ind) at stop j------------------------
                p_cantboard.iloc[ind, j] = p_cantboard_0.iloc[ind, j]
                # Passenger lost at stop j due to overcrowding -----------------
                p_lost_boarding = p_cantboard_1.iloc[ind, j]

            else:
                if p_cantboard_2.iloc[ind, j] <= residual:
                    p_board_2 = p_cantboard_2.iloc[ind, j]
                    residual = residual - p_board_2
                    if p_cantboard_1.iloc[ind, j] <= residual:
                        p_board_1 = p_cantboard_1.iloc[ind, j]
                        residual = residual - p_board_1
                        if p_arrival.iloc[ind, j] <= residual:
                            p_board_0 = p_arrival.iloc[ind, j]
                        else:
                            p_board_0 = residual
                    else:
                        p_board_1 = residual
                        p_board_0 = 0
                else:
                    p_board_2 = residual
                    p_board_1 = 0
                    p_board_0 = 0

                p_cantboard_0.iloc[ind, j] = p_arrival.iloc[ind, j] - p_board_0
                p_cantboard_1.iloc[ind, j] = p_cantboard_1.iloc[ind, j] - p_board_1
                p_cantboard_2.iloc[ind, j] = p_cantboard_2.iloc[ind, j] - p_board_2

                p_board.iloc[ind, j] = p_board_0 + p_board_1 + p_board_2
                # passenger Cant board bus (ind) at stop j------------------------------------------------------------------------
                p_cantboard.iloc[ind, j] = p_cantboard_0.iloc[ind, j] + p_cantboard_1.iloc[ind, j]
                # Passenger lost at stop j due to overcrowding -----------------------------------------------------------------------
                p_lost_boarding = p_cantboard_2.iloc[ind, j]

            # Total passenger lost
            p_lost.iloc[ind, j] = p_lost_waiting + p_lost_boarding

            # Dwelling time of bus(ind) at stop j------------------------------------------------
            if j==0:
                d_time.iloc[ind, j]=headway1.iloc[ind, 0]

            else:
                d_time.iloc[ind, j] = dwell_time(j, departuretime.iloc[ind, 0], p_board.iloc[ind, j], p_alight.iloc[ind, j], load_fact.iloc[ind, j], min_dwell)
            # default holding--------------------------------------------------------------------
            if ind == 0 or j == (len(alightrate.columns) - 1):
                d_holding = 0
            else:
                # stopariival for the next stop
                traveltime_tr = ((d_time.iloc[ind, j] + link_travel_tr.iloc[ind, j + 1]) / 60).round(4)
                stoparrival_nxt = stoparrival.iloc[ind, j] + traveltime_tr
                headway_temp = (stoparrival_nxt - stoparrival.iloc[ind - 1, j + 1]) * 60
                if headway_temp < headway1.iloc[ind, 0] / 4:
                    d_holding = headway1.iloc[ind, 0] / 4 + abs(headway_temp)
                    d_time.iloc[ind, j] = d_time.iloc[ind, j] + d_holding
                else:
                    d_holding = 0

            # Despatch time at stop j for bus ind ------------------------------------------------------------------------
            if j==0:
                despatch.iloc[ind, j]=departuretime.iloc[ind,0]
            else:
                despatch.iloc[ind, j] = stoparrival.iloc[ind, j] + (d_time.iloc[ind, j] / 60)

            # Revenue calculations
            df = pd.read_csv(files_tr[ind], index_col='Stops').fillna(0)
            for k in range(0, len(alightrate.columns)):
                rev = p_board.iloc[ind, j] * df.iloc[j, k] * fare.iloc[j, k]
                revenue.iloc[ind, j] = revenue.iloc[ind, j] + rev

        #---------------------------------------------------------------------
        if purpose=='GA':
            # CONSTRAINTS - TRIP WISE
            # 1.Mimimum Passenger per trip
            p_per_trip = p_arrival.iloc[ind, :].sum()
            if p_per_trip < min_ppp:

                return (0, 0, 0, 0, 0, 0, 0, 0, 0)
            else:
                pass

            # 2.Maximum percentage of passenger lost per trip(PPLPT) = 10 %
            passlosttr = p_lost.iloc[ind, :].sum()
            ppl_pt = (passlosttr / p_per_trip) * 100
            if ppl_pt > max_pplpt:

                return (0, 0, 0, 0, 0, 0, 0, 0, 0)
            else:
                pass

            # 3. Minimum revenue per trip(RVPT)
            revenue_pt = revenue.iloc[ind, :].sum()
            if revenue_pt < min_rvpt:

                return (0, 0, 0, 0, 0, 0, 0, 0, 0)
            else:
                pass

            # 4. Maximum Operation cost per trip
            tot_dwell = d_time.iloc[ind, :].sum()
            fuelcostdwell = tot_dwell * (fuelprice / 60 * kmperliter2)
            fixedcost = fuelcostrunning + fuelcostdwell + maintenancecost + vehdepreciation + crewcost
            # OPERATION COST PER TRIP=  FIXED COST PER TRIP + PASSENGER LOST PENALTY
            operation_cpt = fixedcost + (passlosttr * penalty)
            if operation_cpt > max_opc:

                return (0, 0, 0, 0, 0, 0, 0, 0, 0)
            else:
                pass
        else:
            pass

    # Total travel time hourly
    travel_time_tot = traveltime.sum(axis=1)
    #coverting arrival time to clock time
    stoparrivalclock= stoparrival.copy()

    for ind in range(0, len(stoparrival.index)):
        for j in range(0, len(stoparrival.columns)):
            stoparrivalclock.iloc[ind, j] = np.floor(stoparrival.iloc[ind, j]) + (
                        (stoparrival.iloc[ind, j] - (np.floor(stoparrival.iloc[ind, j]))) / 100 * 60).round(2)

    # Calculation of total cost

    # tripwise total waiting time cost
    Tot_trcost_waiting = cost_waitingtime.sum(axis=1)


    # tripwise total in vehicle travel time cost
    Tot_trcost_inveh = cost_inveh.sum(axis=1)


    # tripwise total passenger lost
    Tot_trpasslost = p_lost.sum(axis=1)


    # tripwise total dwelling time
    Tot_d_time = d_time.sum(axis=1)



    fuelcostdwelling = Tot_d_time * (fuelprice / 60 * kmperliter2)



    # FIXED COST CALCULATION FOR EACH TRIP
    fixed_cost = fuelcostdwelling.copy()
    for i in range(0, len(fuelcostdwelling.index)):
        fixed_cost.iloc[i] = fuelcostdwelling.iloc[i] + fuelcostrunning + maintenancecost + vehdepreciation + crewcost



    Tot_cost = Tot_trcost_waiting + Tot_trcost_inveh + (
            Tot_trpasslost * (penalty + c_cantboard)) + fixed_cost

    tot_user=  Tot_trcost_waiting + Tot_trcost_inveh + (Tot_trpasslost* c_cantboard)
    tot_oper= fixed_cost+ (Tot_trpasslost * penalty)
    if purpose == 'optmised frequency':
        tot_cost_tr = pd.DataFrame(index=departuretime.index,
                                   columns=['user cost', 'operator cost', 'total cost']).fillna(0)
        tot_cost_tr['user cost'] = tot_user
        tot_cost_tr['operator cost'] = tot_oper
        tot_cost_tr['total cost'] = Tot_cost
        tot_cost_hr = pd.DataFrame(index=arrivalrate.index,
                                   columns=['user cost', 'operator cost', 'total cost']).fillna(0)
        ind = -1

        for i in range(0, len(arrivalrate.index)):
            x=int(time_period.iloc[i, 1])
            for m in range(0, int(time_period.iloc[i, 1])):
                ind = ind + 1
                tot_cost_hr.iloc[i, 0] = tot_cost_hr.iloc[i, 0] + tot_cost_tr.loc[ind, 'user cost']
                tot_cost_hr.iloc[i, 1] = tot_cost_hr.iloc[i, 1] + tot_cost_tr.loc[
                    ind, 'operator cost']
                tot_cost_hr.iloc[i, 2] = tot_cost_hr.iloc[i, 2] + tot_cost_tr.loc[
                    ind, 'total cost']
    else:
        pass
    sum_revenue=revenue.sum(axis=1)
    sum_revenue=sum_revenue.sum()
    # TOTAL COST
    t_cost = int(Tot_cost.sum())


    if purpose=='GA':
        pass
    else:

        Totcost_waiting = Tot_trcost_waiting.sum()
        Totcost_inveh = Tot_trcost_inveh.sum()
        Totpasslost = Tot_trpasslost.sum()

        total_trips = frequency.sum()
        totalkilometrerun = total_trips * tot_dis
        fuelcostday= (fuelcostrunning* total_trips)+ fuelcostdwelling.sum()

        # user cost
        cuser = Tot_trcost_waiting + Tot_trcost_inveh + (Tot_trpasslost * c_cantboard)
        cuser = cuser.sum()
        # operator cost
        coperator = (Tot_trpasslost * penalty) + fixed_cost
        coperator = coperator.sum()



        # files export
        path = r'Function files\Input_files_holding'
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)

        '''
        if direcn == 'DN':

            print('\nDown Direction   (',A ,'to',B ,') Cost Calculations for full day operations:')
            print('--------------------------------------------------------------------------------------------------------')


            print(f"Total waiting time cost                               :₹", np.ceil(Totcost_waiting))
            print(f"Total cost of in vehicle time                         :₹", np.ceil(Totcost_inveh))
            print(f"Total passenger lost                                  :", Totpasslost)
            print(f"User Cost                                             :₹", cuser.round(0))
            print(f"Operator Penalty Cost for passenger lost              :₹", (Totpasslost) * (penalty))
            print(f"Vehcile Kilometre-run                                 :", totalkilometrerun,'Km')
            print(f"Cost of fuel                                          :₹", np.ceil(fuelcostday))
            print(f"Cost of vehicle maintenance:                          :₹", maintenancecost*total_trips)
            print(f"Vehicle depreciation cost:                            :₹", vehdepreciation * total_trips)
            print(f"Crew cost:                                            :₹", crewcost * total_trips)
            print(f"Operator Cost for bus operation                       :₹", np.ceil(coperator))
            print(f'Total cost in down direction                          :₹', t_cost)
            print('--------------------------------------------------------------------------------------------------------')

            if purpose == 'optmised frequency':
                link_travel_tr.to_csv(r'Function files\Input_files_holding\link_travel_trDN.csv', index=False)
                arrivalrate_tr.to_csv(r'Function files\Input_files_holding\arrivalrate_trDN.csv', index=False)
                alightrate_tr.to_csv(r'Function files\Input_files_holding\alightrate_trDN.csv', index=False)
                travel_time_tot.to_csv(r'Function files\Input_files_holding\travel_time_totDN.csv', index=False)
                tot_cost_hr.to_csv(r'Function files\Input_files_holding\tot_cost_hr_DN.csv', index=False)

                headway1.to_csv(r'Function files\Input_files_holding\HeadwayDN.csv', index=False)
                departuretime.to_csv(r'Function files\Input_files_holding\departuretimeDN.csv', index=False)

                p_arrival.to_csv(r'Function files\Input_files_holding\p_arrivalDN.csv', index=False)
                p_waiting.to_csv(r'Function files\Input_files_holding\p_waitingDN.csv', index=False)
                p_alight.to_csv(r'Function files\Input_files_holding\p_alightDN.csv', index=False)
                p_board.to_csv(r'Function files\Input_files_holding\p_boardDN.csv', index=False)
                link_occp.to_csv(r'Function files\Input_files_holding\link_occpDN.csv', index=False)
                waitingtime_tr.to_csv(r'Function files\Input_files_holding\waitingtimeDN.csv', index=False)
                cost_waitingtime.to_csv(r'Function files\Input_files_holding\cost_waitingtimeDN.csv', index=False)
                p_cantboard.to_csv(r'Function files\Input_files_holding\p_cantboardDN.csv', index=False)
                p_lost.to_csv(r'Function files\Input_files_holding\ p_lostDN.csv', index=False)
                d_time.to_csv(r'Function files\Input_files_holding\d_timeDN.csv', index=False)
                stoparrival.to_csv(r'Function files\Input_files_holding\stoparrivalDN.csv', index=False)
                headway.to_csv(r'Function files\Input_files_holding\headway_StopDN.csv', index=False)
                traveltime.to_csv(r'Function files\Input_files_holding\traveltimeDN.csv', index=False)
                load_fact.to_csv(r'Function files\Input_files_holding\load_factDN.csv', index=False)
                invehtime.to_csv(r'Function files\Input_files_holding\invehtimeDN.csv', index=False)
                cost_inveh.to_csv(r'Function files\Input_files_holding\cost_invehDN.csv', index=False)
                p_sit.to_csv(r'Function files\Input_files_holding\p_sitDN.csv', index=False)
                p_stand.to_csv(r'Function files\Input_files_holding\ p_standDN.csv', index=False)
                revenue.to_csv(r'Function files\Input_files_holding\revenueDN.csv', index=False)
                p_cantboard_1.to_csv(r'Function files\Input_files_holding\ p_cantboard_1DN.csv', index=False)
                p_cantboard_2.to_csv(r'Function files\Input_files_holding\p_cantboard_2DN.csv', index=False)
                p_cantboard_0.to_csv(r'Function files\Input_files_holding\p_cantboard_0DN.csv', index=False)
                despatch.to_csv(r'Function files\Input_files_holding\despatchDN.csv', index=False)

            else:
                pass

        else:


            print('\nUp Direction   (', B, 'to', A, ') Cost Calculations for full day operations:')
            print(' --------------------------------------------------------------------------------------------------------')

            print(f"Total waiting time cost                               :₹", np.ceil(Totcost_waiting))
            print(f"Total cost of in vehicle time                         :₹", np.ceil(Totcost_inveh))
            print(f"Total passenger lost                                  :", Totpasslost)
            print(f"User Cost                                             :₹", cuser.round(0))
            print(f"Operator Penalty Cost for passenger lost              :₹", (Totpasslost) * (penalty))
            print(f"Vehcile Kilometre-run                                 :", totalkilometrerun, 'Km')
            print(f"Cost of fuel                                          :₹", np.ceil(fuelcostday))
            print(f"Cost of vehicle maintenance:                          :₹", maintenancecost * total_trips)
            print(f"Vehicle depreciation cost:                            :₹", vehdepreciation * total_trips)
            print(f"Crew cost:                                            :₹", crewcost * total_trips)
            print(f"Operator Cost for bus operation                       :₹", np.ceil(coperator))
            print(f'Total cost in up direction                            :₹', t_cost)
            print('--------------------------------------------------------------------------------------------------------')
            if purpose == 'optmised frequency':
                link_travel_tr.to_csv(r'Function files\Input_files_holding\link_travel_trUP.csv', index=False)
                arrivalrate_tr.to_csv(r'Function files\Input_files_holding\arrivalrate_trUP.csv', index=False)
                alightrate_tr.to_csv(r'Function files\Input_files_holding\alightrate_trUP.csv', index=False)
                travel_time_tot.to_csv(r'Function files\Input_files_holding\travel_time_totUP.csv', index=False)
                tot_cost_hr.to_csv(r'Function files\Input_files_holding\tot_cost_hr_UP.csv', index=False)

                headway1.to_csv(r'Function files\Input_files_holding\HeadwayUP.csv', index=False)
                departuretime.to_csv(r'Function files\Input_files_holding\departuretimeUP.csv', index=False)

                p_arrival.to_csv(r'Function files\Input_files_holding\p_arrivalUP.csv', index=False)
                p_waiting.to_csv(r'Function files\Input_files_holding\p_waitingUP.csv', index=False)
                p_alight.to_csv(r'Function files\Input_files_holding\p_alightUP.csv', index=False)
                p_board.to_csv(r'Function files\Input_files_holding\p_boardUP.csv', index=False)
                link_occp.to_csv(r'Function files\Input_files_holding\link_occpUP.csv', index=False)
                waitingtime_tr.to_csv(r'Function files\Input_files_holding\waitingtimeUP.csv', index=False)
                cost_waitingtime.to_csv(r'Function files\Input_files_holding\cost_waitingtimeUP.csv', index=False)
                p_cantboard.to_csv(r'Function files\Input_files_holding\p_cantboardUP.csv', index=False)
                p_lost.to_csv(r'Function files\Input_files_holding\ p_lostUP.csv', index=False)
                d_time.to_csv(r'Function files\Input_files_holding\d_timeUP.csv', index=False)
                stoparrival.to_csv(r'Function files\Input_files_holding\stoparrivalUP.csv', index=False)
                headway.to_csv(r'Function files\Input_files_holding\headway_StopUP.csv', index=False)
                traveltime.to_csv(r'Function files\Input_files_holding\traveltimeUP.csv', index=False)
                load_fact.to_csv(r'Function files\Input_files_holding\load_factUP.csv', index=False)
                invehtime.to_csv(r'Function files\Input_files_holding\invehtimeUP.csv', index=False)
                cost_inveh.to_csv(r'Function files\Input_files_holding\cost_invehUP.csv', index=False)
                p_sit.to_csv(r'Function files\Input_files_holding\p_sitUP.csv', index=False)
                p_stand.to_csv(r'Function files\Input_files_holding\ p_standUP.csv', index=False)
                revenue.to_csv(r'Function files\Input_files_holding\revenueUP.csv', index=False)
                p_cantboard_1.to_csv(r'Function files\Input_files_holding\ p_cantboard_1UP.csv', index=False)
                p_cantboard_2.to_csv(r'Function files\Input_files_holding\p_cantboard_2UP.csv', index=False)
                p_cantboard_0.to_csv(r'Function files\Input_files_holding\p_cantboard_0UP.csv', index=False)
                despatch.to_csv(r'Function files\Input_files_holding\despatchUP.csv', index=False)
            else:
                pass

            '''



    del ind
    del Tot_d_time
    del Tot_trpasslost
    del Tot_trcost_inveh
    del Tot_trcost_waiting
    del cw_cost
    del residual
    del time_period
    gc.collect()


    return (despatch,sum_revenue,fixed_cost,t_cost,departuretime,headway,p_lost, travel_time_tot,stoparrival, np.ceil(Totcost_waiting), np.ceil(Totcost_inveh), Totpasslost, cuser.round(0), (Totpasslost) * (penalty), totalkilometrerun, np.ceil(fuelcostday), maintenancecost*total_trips, vehdepreciation * total_trips, crewcost * total_trips, np.ceil(coperator), t_cost)


