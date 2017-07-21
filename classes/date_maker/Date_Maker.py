import datetime


class Date_Maker():

    def __init__(self):
        self.dates = {'date': '',
                      'time': '',
                      'four_weeks': {
                                     'depart': '',
                                     'intl_return': '',
                                     'dom_return': '',
                                    },
                      'eight_weeks': {
                                     'depart': '',
                                     'intl_return': '',
                                     'dom_return': '',
                                     },
                      }
        self.today = datetime.datetime.today()
        
    def get_dates(self):
        self.fill_dates()
        return self.dates

    def fill_dates(self):
        date = self.today.strftime('%Y-%m-%d')
        time = self.today.strftime('%H:%M:%S')
        
        four_weeks = datetime.timedelta(days=28)
        eight_weeks = datetime.timedelta(days=56)
        intl_return = datetime.timedelta(days=14)
        dom_return = datetime.timedelta(days=7)
        
        self.dates['date'] = date
        self.dates['time'] = time
        self.dates['four_weeks']['depart'] = (four_weeks + 
                                              self.today).strftime('%Y-%m-%d')
        self.dates['four_weeks']['intl_return'] = (four_weeks + intl_return +
                                              self.today).strftime('%Y-%m-%d')
        self.dates['four_weeks']['dom_return'] = (four_weeks + dom_return +
                                              self.today).strftime('%Y-%m-%d')
        self.dates['eight_weeks']['depart'] = (eight_weeks + 
                                              self.today).strftime('%Y-%m-%d')
        self.dates['eight_weeks']['intl_return'] = (eight_weeks + intl_return +
                                              self.today).strftime('%Y-%m-%d')
        self.dates['eight_weeks']['dom_return'] = (eight_weeks + dom_return +
                                              self.today).strftime('%Y-%m-%d')
        
if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
    '\\Travel\\TDD\\Google')
    
    dm = Date_Maker()
        