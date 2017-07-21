import os
import json

class Parser():
    
    def __init__(self, json_, flight_details):
        flight_details['Date'] = flight_details.pop('today')
        
        trip_generator = (trip for trip in json_['trips']['tripOption'])
        self.trips = []
        for trip in trip_generator:
            overall_data = self.get_overall_data(trip, flight_details)
            segment_data = self.get_segment_data(trip)
            self.trips.append({**overall_data, **segment_data})
            
    def get_overall_data(self, trip, flight_details):
        # Convenience variables
        price = trip['pricing'][0]
        vc = self.validate_currency
        overall_dict = {}
        
        keys = ['saleTaxTotal', 'baseFareTotal', 'saleTotal',
                     'saleFareTotal', 'ptc', 'refundable', 'Orig', 'Dest',
                     'Date', 'booking']
        for i, key in enumerate(keys):
            overall_dict[key] = None
            try:
                if i <= 3:
                    overall_dict[key] = vc(price[key])
                elif i == 4 or i == 5:
                    overall_dict[key] = price[key]
                else:
                    overall_dict[key] = flight_details[key]
            except:
                continue
        
        # Adding some layers to the overall_dict for DataFrame formatting
        return {'Overall' :{'Overall': overall_dict}}

    def get_segment_data(self, trip):
        seg_generator = (segment for segment in trip['slice'])
        
        seg_n = 0
        seg_dicts = {}
        for segment in seg_generator:
            map_ = {1: 'Depart',
                    2: 'Return'}
            
            leg_n = 0
            leg_dicts = {}
            leg_generator = (leg for leg in segment['segment'])

            for leg in leg_generator:
                leg_n += 1
                leg_data = self.get_leg_data(leg)
                leg_dicts['Leg ' + str(leg_n)] = leg_data
                         
            if not 'Leg 2' in leg_dicts.keys():
                leg_dicts['Leg 2'] = self.get_blanks()
            
            seg_n += 1
            key = map_[seg_n]
            seg_dicts[key] = leg_dicts
                         
        return seg_dicts
    
    def get_leg_data(self, leg):
        leg_dict = {}
        
        leg_lists = [
                    ['connectionDuration', 'duration', 'cabin', 
                     'bookingCode', 'bookingCodeCount'],
                    ['departureTime', 'aircraft', 'destinationTerminal', 
                    'originTerminal', 'meal', 'origin', 'duration', 'mileage',
                    'destination', 'arrivalTime'],
                    ['carrier', 'number']
                     ]
        for i, list_ in enumerate(leg_lists):
            for key in list_:
                # Pre-assign None for a more concise try-except clause
                leg_dict[key] = None 
                try:
                    if i == 0:
                        leg_dict[key] = leg[key]
                    elif i == 1:
                        leg_dict[key] = leg['leg'][0][key]
                    elif i == 2:
                        leg_dict[key] = leg['flight'][key]
                except:
                    continue
        return leg_dict
    
    def get_blanks(self):
        blank_dict = {}
        keys = ['aircraft', 'arrivalTime', 'bookingCode', 'bookingCodeCount',
                'cabin', 'carrier', 'connectionDuration', 'departureTime',
                'destination', 'destinationTerminal', 'duration', 'meal',
                'mileage', 'number', 'origin', 'originTerminal', ]
        for key in keys:
            blank_dict[key] = None
                      
        return blank_dict
        
        

    def validate_currency(self, price):
        if price[:3] == 'CAD':
            return float(price[3:])
        else:
            print('NON-CANADIAN FUNDS ' + price)
            return price



if __name__ == '__main__':
    file_path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
                 'Travel\\TDD\\Google\\files\\json\\2017-07-18'
                 '\\2017-07-18-YYZ-PEK_(4 weeks).JSON')
    '''
    file_path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
                 'Travel\\Google\\Latest\\json\\20170714-YEG-YYZ.JSON')
    '''
    
    with open(file_path, 'r') as f:
        json_ = json.load(f)
        
    flight_details = {'today': '2017-06-26',
                      'ret_date': '2017-07-10',
                      'booking': 'four_weeks',
                      'Orig': 'YYZ',
                      'Dest': 'PEK',
                      'dep_date': '2017-06-27'}
    parser = Parser(json_, flight_details)