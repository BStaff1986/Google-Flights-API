from classes.basket_proffer.Basket_Proffer import Basket_Proffer
from classes.flight_generator.Flight_Generator import Flight_Generator
from classes.date_maker.Date_Maker import Date_Maker
from classes.dataframe.DataFrame import DataFrame
from classes.json_requester.JSON_Requester import JSON_Requester
from classes.parser.Parser import Parser
import json
import pickle
import time

begin = time.time()
# Phase 1
dates = Date_Maker().get_dates()
df = DataFrame()
Basket_Proffer(dates)
flights = Flight_Generator(dates).generator
phase1 = time.time()        
    
start_loop = time.time()                      
for flight in flights:
    '''
    # TODO: Remove this temp, offline,  JSON link
    fp = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
                 'Travel\\TDD\\Google\\files\\json\\2017-07-21\\'
                 '2017-07-21-YYZ-PEK_eight_weeks.JSON')
    with open(fp, 'r') as f:
        json_ = json.load(f)
    '''
    json_ = JSON_Requester(flight).json_
    
    trip_data = Parser(json_, flight).trips
    
   
    df.add_trip_to_dataframe(trip_data)
end_loop = time.time()

print('Loop Time')
print(round((end_loop - start_loop), 2))
  
    
preexport = time.time()    
df.export_to_excel(dates)
postexport = time.time()
print('Export time')
print(round((postexport - preexport), 3))
end = time.time()

print('Total time')
print(round((end - begin), 2))
        
        