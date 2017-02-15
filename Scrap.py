from bs4 import BeautifulSoup
import requests
import json
import shelve
import pandas as pd
import re
from string import split

# define what mileage values I want to pull a price for
# in this case, ever 10k miles between 10k and 130k

mileages = range(10000, 230000 + 10000, 10000)

#mileages = range(10000, 20000, 10000)
# these parameters don't matter. they specify
# what condition of vehicle to pull up on kbb, but
# each kbb page contains numbers for all conditions

condition = 'verygood'
pricetype = 'retail'
intent = 'buy-used'


# price estimates vary by zip code so you have to specify
zipcode = '33613'

# initialize a root dictionary containing car info.
# the root index will specify car model
# the next level index will specify model year
# each model year then contains a set of variables with values (leaves)
scraped_data = {}
scraped_test_data = {}
# I had to manually look up the URL for each car model/year on kbb as they are non standard
# if you want to add a different car, you have to go look on kbb and define a dictionary
# entry similar to those below

# http://www.kbb.com/hyundai/elantra/2010/gls-sedan-4d/?vehicleid=261559&category=sedan
# http://www.kbb.com/hyundai/elantra/2011/gls-sedan-4d/?vehicleid=352613&category=sedan
# http://www.kbb.com/hyundai/elantra/2012/gls-sedan-4d/?vehicleid=364017&category=sedan

car = 'elantra'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'hyundai/elantra/2010/gls-sedan-4d'
scraped_data[car][2010]['vehicleid'] = 261559
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'hyundai/elantra/2011/gls-sedan-4d'
scraped_data[car][2011]['vehicleid'] = 352613
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'hyundai/elantra/2012/gls-sedan-4d'
scraped_data[car][2012]['vehicleid'] = 364017
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'sedan'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'economic car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []

# http://www.kbb.com/hyundai/elantra/2013/gls-sedan-4d/?vehicleid=374637&category=sedan
# http://www.kbb.com/hyundai/elantra/2014/se-sedan-4d/?vehicleid=395339&category=sedan
# http://www.kbb.com/hyundai/elantra/2015/se-sedan-4d/?vehicleid=399971&category=sedan


scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'hyundai/elantra/2013/gls-sedan-4d'
scraped_test_data[car][2013]['vehicleid'] = 374637
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'hyundai/elantra/2014/se-sedan-4d'
scraped_test_data[car][2014]['vehicleid'] = 395339
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'hyundai/elantra/2015/se-sedan-4d'
scraped_test_data[car][2015]['vehicleid'] = 399971
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'sedan'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'economic car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []


# http://www.kbb.com/toyota/prius/2010/i-hatchback-4d/?vehicleid=261967&category=hatchback
# http://www.kbb.com/toyota/prius/2011/two-hatchback-4d/?vehicleid=363079&category=hatchback1
# http://www.kbb.com/toyota/prius/2012/two-hatchback-4d/?vehicleid=373443&category=hatchback

car = 'prius'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'toyota/prius/2010/i-hatchback-4d'
scraped_data[car][2010]['vehicleid'] = 261967
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'toyota/prius/2011/two-hatchback-4d'
scraped_data[car][2011]['vehicleid'] = 363079
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'toyota/prius/2012/two-hatchback-4d'
scraped_data[car][2012]['vehicleid'] = 373443
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'hatchback'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'hybrid car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []

# https://www.kbb.com/toyota/prius/2013/one-hatchback-4d/?vehicleid=382244&category=hatchback
# https://www.kbb.com/toyota/prius/2014/one-hatchback-4d/?vehicleid=393287&category=hatchback
# https://www.kbb.com/toyota/prius/2015/one-hatchback-4d/?vehicleid=402283&category=hatchback
scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'toyota/prius/2013/one-hatchback-4d'
scraped_test_data[car][2013]['vehicleid'] = 382244
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'toyota/prius/2014/one-hatchback-4d'
scraped_test_data[car][2014]['vehicleid'] = 393287
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'toyota/prius/2015/one-hatchback-4d'
scraped_test_data[car][2015]['vehicleid'] = 402283
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'hatchback'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'hybrid car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []
# http://www.kbb.com/honda/insight/2010/lx-hatchback-4d/?vehicleid=251583&swop=false&category=hatchback
# http://www.kbb.com/honda/insight/2011/lx-hatchback-4d/?vehicleid=360124&swop=false&category=hatchback
# http://www.kbb.com/honda/insight/2012/lx-hatchback-4d/?vehicleid=371307&swop=false&category=hatchback
car = 'insight'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'honda/insight/2010/lx-hatchback-4d'
scraped_data[car][2010]['vehicleid'] = 251583
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'honda/insight/2011/lx-hatchback-4d'
scraped_data[car][2011]['vehicleid'] = 360124
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'honda/insight/2012/lx-hatchback-4d'
scraped_data[car][2012]['vehicleid'] = 371307
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'hatchback'
    scraped_data[car][year]['swop'] = 'false'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'hybrid car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []

# https://www.kbb.com/honda/insight/2013/lx-hatchback-4d/?vehicleid=382405&swop=false&category=hatchback
# https://www.kbb.com/honda/insight/2014/lx-hatchback-4d/?vehicleid=393909&swop=false&category=hatchback

scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'honda/insight/2013/lx-hatchback-4d'
scraped_test_data[car][2013]['vehicleid'] = 382405
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'honda/insight/2014/lx-hatchback-4d'
scraped_test_data[car][2014]['vehicleid'] = 393909
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'hatchback'
    scraped_test_data[car][year]['swop'] = 'false'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'hybrid car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []

# http://www.kbb.com/toyota/corolla/2010/sedan-4d/?vehicleid=261636&category=sedan
# http://www.kbb.com/toyota/corolla/2011/sedan-4d/?vehicleid=360136&category=sedan
# http://www.kbb.com/toyota/corolla/2012/le-sedan-4d/?vehicleid=371591&category=sedan

car = 'corolla'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'toyota/corolla/2010/sedan-4d'
scraped_data[car][2010]['vehicleid'] = 261636
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'toyota/corolla/2011/sedan-4d'
scraped_data[car][2011]['vehicleid'] = 360136
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'toyota/corolla/2012/le-sedan-4d'
scraped_data[car][2012]['vehicleid'] = 371591
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'sedan'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'economic car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []

# http://www.kbb.com/toyota/corolla/2013/le-sedan-4d/?vehicleid=381440&category=sedan
# http://www.kbb.com/toyota/corolla/2014/le-sedan-4d/?vehicleid=392455&category=sedan
# http://www.kbb.com/toyota/corolla/2015/le-sedan-4d/?vehicleid=403132&category=sedan

scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'toyota/corolla/2013/le-sedan-4d'
scraped_test_data[car][2013]['vehicleid'] = 381440
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'toyota/corolla/2014/le-sedan-4d'
scraped_test_data[car][2014]['vehicleid'] = 392455
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'toyota/corolla/2015/le-sedan-4d'
scraped_test_data[car][2015]['vehicleid'] = 403132
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'sedan'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'economic car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []
# http://www.kbb.com/honda/civic/2010/dx-sedan-4d/?vehicleid=261537&category=sedan
# http://www.kbb.com/honda/civic/2011/dx-sedan-4d/?vehicleid=358177&category=sedan
# http://www.kbb.com/honda/civic/2012/dx-sedan-4d/?vehicleid=371048&category=sedan

car = 'civic'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'honda/civic/2010/dx-sedan-4d'
scraped_data[car][2010]['vehicleid'] = 261537
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'honda/civic/2011/dx-sedan-4d'
scraped_data[car][2011]['vehicleid'] = 358177
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'honda/civic/2012/dx-sedan-4d'
scraped_data[car][2012]['vehicleid'] = 371048
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'sedan'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'economic car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []


# http://www.kbb.com/honda/civic/2013/lx-sedan-4d/?vehicleid=383086&category=sedan
# http://www.kbb.com/honda/civic/2014/lx-sedan-4d/?vehicleid=393969&category=sedan
# http://www.kbb.com/honda/civic/2015/lx-sedan-4d/?vehicleid=402413&category=sedan

scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'honda/civic/2013/lx-sedan-4d'
scraped_test_data[car][2013]['vehicleid'] = 383086
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'honda/civic/2014/lx-sedan-4d'
scraped_test_data[car][2014]['vehicleid'] = 393969
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'honda/civic/2015/lx-sedan-4d'
scraped_test_data[car][2015]['vehicleid'] = 402413
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'sedan'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'economic car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []
# http://www.kbb.com/ford/fusion/2010/hybrid-sedan-4d/?vehicleid=248464
# ford/fusion/2011/hybrid-sedan-4d/?vehicleid=352866
# ford/fusion/2012/hybrid-sedan-4d/?vehicleid=364410

car = 'fusion-hybrid'
scraped_data[car] = {}
scraped_data[car][2010] = {}
scraped_data[car][2010]['path'] = 'ford/fusion/2010/hybrid-sedan-4d'
scraped_data[car][2010]['vehicleid'] = 248464
scraped_data[car][2011] = {}
scraped_data[car][2011]['path'] = 'ford/fusion/2011/hybrid-sedan-4d'
scraped_data[car][2011]['vehicleid'] = 352866
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'ford/fusion/2012/hybrid-sedan-4d'
scraped_data[car][2012]['vehicleid'] = 364410
for year in scraped_data[car]:
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'hybrid car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []


# http://www.kbb.com/ford/fusion/2013/se-hybrid-sedan-4d/?vehicleid=382587
# http://www.kbb.com/ford/fusion/2014/se-hybrid-sedan-4d/?vehicleid=390179
# http://www.kbb.com/ford/fusion/2015/se-hybrid-sedan-4d/?vehicleid=399452

scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'ford/fusion/2013/se-hybrid-sedan-4d'
scraped_test_data[car][2013]['vehicleid'] = 382587
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'ford/fusion/2014/se-hybrid-sedan-4d'
scraped_test_data[car][2014]['vehicleid'] = 390179
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'ford/fusion/2015/se-hybrid-sedan-4d'
scraped_test_data[car][2015]['vehicleid'] = 399452
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'hybrid car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []

# http://www.kbb.com/toyota/prius-c/2012/three-hatchback-4d-specifications/?vehicleid=374558&intent

car = 'prius-c'
scraped_data[car] = {}
scraped_data[car][2012] = {}
scraped_data[car][2012]['path'] = 'toyota/prius-c/2012/three-hatchback-4d'
scraped_data[car][2012]['vehicleid'] = 374558
for year in scraped_data[car]:
    scraped_data[car][year]['category'] = 'hatchback'
    scraped_data[car][year]['mileage'] = []
    scraped_data[car][year]['prices'] = []
    scraped_data[car][year]['condition'] = condition
    scraped_data[car][year]['type'] = 'hybrid car'
    scraped_data[car][year]['Fuel_Economy'] = []
    scraped_data[car][year]['Max_Seating'] = []
    scraped_data[car][year]['Doors'] = []
    scraped_data[car][year]['Engine'] = []
    scraped_data[car][year]['DriveTrain'] = []
    scraped_data[car][year]['Transmission'] = []
    scraped_data[car][year]['EPA_Class'] = []
    scraped_data[car][year]['Body Style'] = []
    scraped_data[car][year]['Country_of_Origin'] = []
    scraped_data[car][year]['Country_of_Assembly'] = []

# http://www.kbb.com/toyota/prius-c/2013/three-hatchback-4d/?vehicleid=384525
# http://www.kbb.com/toyota/prius-c/2014/three-hatchback-4d/?vehicleid=393918
# http://www.kbb.com/toyota/prius-c/2015/three-hatchback-4d/?vehicleid=406361


scraped_test_data[car] = {}
scraped_test_data[car][2013] = {}
scraped_test_data[car][2013]['path'] = 'toyota/prius-c/2013/three-hatchback-4d'
scraped_test_data[car][2013]['vehicleid'] = 384525
scraped_test_data[car][2014] = {}
scraped_test_data[car][2014]['path'] = 'toyota/prius-c/2014/three-hatchback-4d'
scraped_test_data[car][2014]['vehicleid'] = 393918
scraped_test_data[car][2015] = {}
scraped_test_data[car][2015]['path'] = 'toyota/prius-c/2015/three-hatchback-4d'
scraped_test_data[car][2015]['vehicleid'] = 406361
for year in scraped_test_data[car]:
    scraped_test_data[car][year]['category'] = 'hatchback'
    scraped_test_data[car][year]['mileage'] = []
    scraped_test_data[car][year]['prices'] = []
    scraped_test_data[car][year]['condition'] = condition
    scraped_test_data[car][year]['type'] = 'hybrid car'
    scraped_test_data[car][year]['Fuel_Economy'] = []
    scraped_test_data[car][year]['Max_Seating'] = []
    scraped_test_data[car][year]['Doors'] = []
    scraped_test_data[car][year]['Engine'] = []
    scraped_test_data[car][year]['DriveTrain'] = []
    scraped_test_data[car][year]['Transmission'] = []
    scraped_test_data[car][year]['EPA_Class'] = []
    scraped_test_data[car][year]['Body Style'] = []
    scraped_test_data[car][year]['Country_of_Origin'] = []
    scraped_test_data[car][year]['Country_of_Assembly'] = []


def scrapData(scraped_data):
    # loop through the dictionary indicies (model/year) and pull info from kbb
    for car in scraped_data:
        for year in scraped_data[car]:
            for mileage in mileages:
                print '<%d-%s>: Reading url for car with %s miles:' % (year, car, mileage)

                # To find the proper kbb URL for each car permutation, I looked at the
                # URL's manually to figure out the formatting and define a string
                # accordingly
                url = 'http://www.kbb.com/%s/' % scraped_data[
                    car][year]['path']
                url += '?vehicleid=%s&' % scraped_data[car][year]['vehicleid']
                if 'category' in scraped_data[car][year]:
                    url += 'category=%s&' % scraped_data[car][year]['category']
                url += 'mileage=%s&' % mileage
                url += 'condition=%s&' % condition
                url += 'intent=%s&' % intent
                url += 'pricetype=%s' % pricetype

                print '<%d-%s>: ' % (year, car), url

                # the header isn't strictly necessary but makes it look like you're actually
                # pulling the web page from a browser, not from a script
                headers = {'User-Agent':
                           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
                           '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

                # Get the page HTML. here we use 'requests', but 'urllib' and
                # 'mechanize' are other package options the cookie parameter is
                # included match the cookie I noticed specifying zip code on
                # kbb.com
                html = requests.get(url,
                                    cookies={'ZipCode': zipcode},
                                    headers=headers).text

                # load the html in to beautiful soup
                soup = BeautifulSoup(html)

                print '<%d-%s>: webpage loading complete. parsing...' % (year, car)

                # I'm expecting there to be only one html <script> element that has these
                # attributes. I manually looked in the webpage source and searched for the number
                # matching what was displayed on the webpage to identify the element
                # with the pricing info of interest
                element = soup.find('script',
                                    attrs={'type': 'text/javascript',
                                           'language': 'javascript'})

                # make sure the string isn't empty
                if element.string:
                    # make sure it contains the content we expect
                    if element.string.lstrip()[:18] == '$(document).ready(':
                        # strip white space
                        full_str = element.string.lstrip()

                        # I found that this HTML container contained text
                        # that specified prices for different seller conditions
                        # in a json format. So by counting the right number of lines
                        # I can get the pricing data directly. Sometimes there were
                        # was extra lines included, hence the 37/32 try-except.
                        try:
                            line_count = 0
                            count_limit = 37
                            save_lines = False

                            # the princing info will be added in this string
                            json_data = ''

                            for line in full_str.splitlines():
                                # the word values indicated where pricing info
                                # starts
                                if line.lstrip()[1:7] == 'values':
                                    save_lines = True

                                if save_lines:
                                    json_data += line.lstrip()

                                    line_count += 1
                                    if line_count >= count_limit:
                                        save_lines = False

                            # tack on braces for final json formatting
                            json_data = '{' + json_data[:-1] + '}'

                            # this doesn't actually do anything now but will throw
                            # the error we want to catch if it's supposed to be 32
                            # lines
                            json.loads(json_data)
                        except:
                            line_count = 0
                            count_limit = 32
                            save_lines = False

                            # the princing info will be added in this string
                            json_data = ''

                            for line in full_str.splitlines():
                                # the word values indicated where pricing info
                                # starts
                                if line.lstrip()[1:7] == 'values':
                                    save_lines = True

                                if save_lines:
                                    json_data += line.lstrip()

                                    line_count += 1
                                    if line_count >= count_limit:
                                        save_lines = False

                            # tack on braces for final json formatting
                            json_data = '{' + json_data[:-1] + '}'

                        # de-serialize the json string in to a dictionary (with 2 indices)
                        # specifying prices under different conditions
                        scraped_data[car][year]['prices'].append(
                            json.loads(json_data)['values'])

                        scraped_data[car][year]['mileage'].append(int(mileage))

                        print '<%d-%s>: found price info!' % (year, car)
                    else:
                        print '<%d-%s>: PROBLEM - FAILED TO FIND PRICE INFO!' % (year, car)
                else:
                    print '<%d-%s>: PROBLEM - FAILED TO FIND PRICE INFO!' % (year, car)

                spec = soup.findAll(
                    'a', href=re.compile("specifications"))[0].get('href')
                print spec
                url_spec = 'http://www.kbb.com/%s' % spec
                # print url_spec

                r = requests.get(url_spec)
                soup2 = BeautifulSoup(r.text)
                for table_row in soup2.select("div.mod-content"):
                        # Each tr (table row) has three td HTML elements (most people
                        # call these table cels) in it (first name, last name,
                        # and age)
                    cells = table_row.findAll('td')

                    if len(cells) > 0:
                        # print cells

                        fuel_eco = split(cells[0].text.strip(), ":")[1]
                        # print fuel_eco
                        scraped_data[car][year][
                            'Fuel_Economy'].append(fuel_eco)

                        max_sitting = split(cells[1].text.strip(), ":")[1]
                        # print max_sitting
                        scraped_data[car][year][
                            'Max_Seating'].append(max_sitting)

                        doors = split(cells[2].text.strip(), ":")[1]
                        # print doors
                        scraped_data[car][year]['Doors'].append(doors)

                        engine = split(cells[3].text.strip(), ":")[1]
                        # print engine
                        scraped_data[car][year]['Engine'].append(engine)

                        driveTrain = split(cells[4].text.strip(), ":")[1]
                        # print driveTrain
                        scraped_data[car][year][
                            'DriveTrain'].append(driveTrain)

                        transmission = split(cells[5].text.strip(), ":")[1]
                        # print transmission

                        scraped_data[car][year][
                            'Transmission'].append(transmission)
                        epa_cls = split(cells[6].text.strip(), ":")[1]
                        # print epa_cls
                        scraped_data[car][year]['EPA_Class'].append(epa_cls)
                        bdy_stl = split(cells[7].text.strip(), ":")[1]
                        # print bdy_stl
                        scraped_data[car][year]['Body Style'].append(bdy_stl)
                        co = split(cells[8].text.strip(), ":")[1]
                        # print co
                        scraped_data[car][year]['Country_of_Origin'].append(co)

                        ca = split(cells[9].text.strip(), ":")[1]
                        # print ca
                        scraped_data[car][year][
                            'Country_of_Assembly'].append(ca)

                print '<%d-%s>: finished loading data!' % (year, car)
                print ''

    print 'FINISHED LOADING ALL CARS!'

    # now that we have the data, we want to construct a more flat structure
    # (i.e. - a single table with non-hierarchical columns) and put it in a dataframe
    #
    # define a dictionary that will be used to construct the dataframe
    # (indices are columns):
    car_prices = {}
    car_prices['car'] = []
    car_prices['year'] = []
    car_prices['mileage'] = []
    car_prices['retail'] = []
    car_prices['dealer'] = []
    car_prices['dealer_min'] = []
    car_prices['dealer_max'] = []
    car_prices['pp_fair'] = []
    car_prices['pp_good'] = []
    car_prices['pp_verygood'] = []
    car_prices['pp_excellent'] = []
    car_prices['Fuel_Economy'] = []
    car_prices['Max_Seating'] = []
    car_prices['Doors'] = []
    car_prices['Engine'] = []
    car_prices['DriveTrain'] = []
    car_prices['Transmission'] = []
    car_prices['EPA_Class'] = []
    car_prices['Body Style'] = []
    car_prices['Country_of_Origin'] = []
    car_prices['Country_of_Assembly'] = []

    for car in scraped_data:
        for year in scraped_data[car]:
            for mileage, price, fe, ms, d, eng, dt, tms, ec, bd, co, ca in zip(scraped_data[car][year]['mileage'],
                                                                               scraped_data[car][
                                                                                   year]['prices'],
                                                                               scraped_data[car][year][
                    'Fuel_Economy'],
                    scraped_data[car][year][
                    'Max_Seating'],
                    scraped_data[car][year]['Doors'],
                    scraped_data[car][year]['Engine'],
                    scraped_data[car][
                    year]['DriveTrain'],
                    scraped_data[car][year][
                    'Transmission'],
                    scraped_data[car][year]['EPA_Class'],
                    scraped_data[car][
                    year]['Body Style'],
                    scraped_data[car][year][
                    'Country_of_Origin'],
                    scraped_data[car][year]['Country_of_Assembly']):
                car_prices['car'].append(car)
                car_prices['year'].append(year)
                car_prices['mileage'].append(mileage)
                # I manually looked at the 'price' dicitonary structure for
                # this:
                car_prices['retail'].append(price['retail']['price'])
                car_prices['dealer'].append(price['fpp']['price'])
                car_prices['dealer_min'].append(price['fpp']['priceMin'])
                car_prices['dealer_max'].append(price['fpp']['priceMax'])
                car_prices['pp_fair'].append(
                    price['privatepartyfair']['price'])
                car_prices['pp_good'].append(
                    price['privatepartygood']['price'])
                car_prices['pp_verygood'].append(
                    price['privatepartyverygood']['price'])
                car_prices['pp_excellent'].append(
                    price['privatepartyexcellent']['price'])

                car_prices['Fuel_Economy'] .append(fe)
                car_prices['Max_Seating'] .append(ms)
                car_prices['Doors'] .append(d)
                car_prices['Engine'] .append(eng)
                car_prices['DriveTrain'] .append(dt)
                car_prices['Transmission'] .append(tms)
                car_prices['EPA_Class'] .append(ec)
                car_prices['Body Style'] .append(bd)
                car_prices['Country_of_Origin'] .append(co)
                car_prices['Country_of_Assembly'] .append(ca)
                # print car_prices

    return car_prices
x = scrapData(scraped_data)
# print
df = pd.DataFrame(x)
df2 = pd.DataFrame(scrapData(scraped_test_data))
# save the scraped data to file so you don't have to scrape it again later
df.to_csv("data2.csv")
df2.to_csv("test.csv")
