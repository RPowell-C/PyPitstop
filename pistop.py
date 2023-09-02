import json
import itertools
from itertools import combinations
#calculation for a pitstop: t = tb + pt + pf

# where t = total time, tb = total base time, pt = tire wear penalty, pf = penalty due to fuel level

#formula for calculating a stint: tl + 1 = tb + Tl + F(lmax - l) until lap == max laps 
# tb is the base time, Tl is the tire wear penalty times lap, and F(lmax - l) is the fuel multiplied by max laps minus the current lap


lmax = int(input("laps: "))
tirelife = 100
totaltime = 0
def gethards():
    file = open("data.json", "r")
    data = json.load(file)
    hards = data['hards']
    tb = hards['tb']
    pt = hards['pt']
    ptM = hards['ptM']
    tiredeg = hards['tiredeg']
    pf = hards['pf']
    fuel = hards['fuel']
    return tb, pt, ptM, tiredeg, pf, fuel
def getmediums():
    file = open("data.json", "r")
    data = json.load(file)
    mediums = data['mediums']
    tb = mediums['tb']
    pt = mediums['pt']
    ptM = mediums['ptM']
    tiredeg = mediums['tiredeg']
    pf = mediums['pf']
    fuel = mediums['fuel']
    return tb, pt, ptM, tiredeg, pf, fuel
def getsofts():
    file = open("data.json", "r")
    data = json.load(file)
    softs = data['softs']
    tb = softs['tb']
    pt = softs['pt']
    ptM = softs['ptM']
    tiredeg = softs['tiredeg']
    pf = softs['pf']
    fuel = softs['fuel']
    return tb, pt, ptM, tiredeg, pf, fuel


def findstrategy(pitlapH, pitlapM, pitlapS, lmax, hards, mediums, softs):
    possible = [pitlapH, pitlapM, pitlapS]
    translations = {pitlapH : "hards", pitlapM : "mediums", pitlapS : "softs"}
    lingo = {"hards" : hards, "mediums" : mediums, "softs" : softs}
    twoStop = [pair for pair in itertools.combinations_with_replacement(possible, 3)]
    oneStop = [pair for pair in itertools.combinations_with_replacement(possible, 3)]
    tireonetime = 0
    tiretwotime = 0
    strattime = 0
    for combination in oneStop:
        max_laps = combination[0] + combination[1]
        if max_laps >= lmax:
            print("this one could work")
        for value in translations:
            if combination[0] == value:
                print(translations[value])
                for shit in lingo:
                    if str(translations[value]) == shit:
                        tireonetime += lingo[shit]
            if combination[1] == value:
                print(translations[value])
                for shit in lingo:
                    if str(translations[value]) == shit:
                        tiretwotime += lingo[shit]
        strattime = tireonetime + 20 + tiretwotime
        print("total race time: " + str(strattime))
        print("two stop time: " + str(strattime /60))
        print("-------------------------")
        tireonetime = 0
        tiretwotime = 0
        strattime = 0
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    threestoptime = 0
    tireonetime = 0
    tiretwotime = 0
    tirethreetime = 0
    for combination in twoStop:
        max_laps = combination[0] + combination[1] + combination[2]
        if max_laps >= lmax:
            print("this one could work")
        for value in translations:
            if combination[0] == value:
                print(translations[value])
                for shit in lingo:
                    if str(translations[value]) == shit:
                        tireonetime += lingo[shit]
            if combination[1] == value:
                print(translations[value])
                for shit in lingo:
                    if str(translations[value]) == shit:
                        tireonetime += lingo[shit]
            if combination[2] == value:
                print(translations[value])
                for shit in lingo:
                    if str(translations[value]) == shit:
                        tirethreetime += lingo[shit]
        threestoptime = tireonetime + 20 + tiretwotime + 20 + tirethreetime
        print("the total race time for three stop is: " + str(threestoptime))
        print("adjusted time is: " + str(threestoptime /60))
        threestoptime = 0
        tireonetime = 0
        tiretwotime = 0
        tirethreetime = 0
        print("--------------------------")
    return oneStop, twoStop


#altered function: totaltime = basetime + penalty, penalty gets adds up overtime


#tb is going to remain the same
def crunchdata(totaltime, lap, lmax, tirelife, tb, pt, ptM, tiredeg, pf, fuel):
    lap = 0
    pitlap = 0
    while lap < lmax:
        timetillpit = 0
        time = tb + pt
        totaltime = totaltime + time
        pt = pt + ptM
        fuel = fuel - pf
        tirelife = tirelife - tiredeg
        if tirelife >= 20:
            pitlap += 1 
            totaltime = totaltime + time
            #print the data
            print(" ")
            print("lap: " + str(lap))
            print("--------------------")
            print("lap time: " + str(time))
            print ("tire %: " + str(tirelife))
            print("fuel: " + str(fuel))
            print("total time: " + str(totaltime))
            print("adjusted total time: " + str(totaltime / 60))
        lap += 1 
    return totaltime, pitlap, timetillpit




lap = 0


#visual data
tb, pt, ptM, tiredeg, pf, fuel = gethards()
hards, pitlapH, timetillpitH = crunchdata(totaltime, lap, lmax, tirelife, tb, pt, ptM, tiredeg, pf, fuel)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("crunching data for mediums")
tb, pt, ptM, tiredeg, pf, fuel = getmediums()
mediums, pitlapM, timetillpitM  = crunchdata(totaltime, lap, lmax, tirelife, tb, pt, ptM, tiredeg, pf, fuel)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("crunching data for softs")
tb, pt, ptM, tiredeg, pf, fuel = getsofts()
softs, pitlapS, timetillpitS  = crunchdata(totaltime, lap, lmax, tirelife, tb, pt, ptM, tiredeg, pf, fuel)
print("_________________________________________")
print("this is a " + str(lmax) + " lap race")
print("_________________________________________")
print("=========================================")
print("hards total time: " + str(hards))
print("you should pit on lap: " + str(pitlapH))
print("mediums total time: " + str(mediums))
print("you should pit on lap: " + str(pitlapM))
print("softs total time: " + str(softs))
print("you should pit on lap: " + str(pitlapS))
print("=========================================")
print("finding all combinations")
onestop, twostop = findstrategy(pitlapH, pitlapM, pitlapS, lmax, hards, mediums, softs)
