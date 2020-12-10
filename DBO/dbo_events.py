from DBO.handler import DBOHandler
from datetime import datetime
import datetime
from Logger.handler import LoggerIt


class DBOEvents(DBOHandler):
    def __init__(self):
        DBOHandler.__init__(self)

    def get_events(self, user_id, date):
        first_date = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=7)
        last_date = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=7)
        sql = 'SELECT id, title, date, time_from, time_to, is_complete FROM to_do_list WHERE user_id = "{id}" AND ' \
              'date between "{date1}" AND "{date2}" ORDER BY date, time_from'.format(id=user_id, date1=first_date, date2=last_date)
        temp = self.select_data(sql)
        if len(temp) == 0:
            return {}
        else:
            date = temp[0]['date'].strftime('%Y-%m-%d')
            result = dict()
            result[date] = []
            for row in temp:
                row['date'] = row['date'].strftime('%Y-%m-%d')
                row['time_from'] = str(row['time_from'])
                row['time_to'] = str(row['time_to'])
                if row['date'] != date:
                    date = row['date']
                    result[date] = []
                result[date].append(row)
            return result
