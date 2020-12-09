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
        sql = 'SELECT id, title, date, time, is_complete FROM to_do_list WHERE user_id = "{id}" AND ' \
              'date between "{date1}" AND "{date2}" ORDER BY date, time'.format(id=user_id, date1=first_date, date2=last_date)
        temp = self.select_data(sql)
        logger = LoggerIt.get_instance()
        logger.write_info('temp'+str(temp))
        date = temp[0]['date'].strftime('%Y-%m-%d')
        result = dict()
        result[date] = []
        for row in temp:
            row['date'] = row['date'].strftime('%Y-%m-%d')
            row['time'] = str(row['time'])
            if row['date'] != date:
                date = row['date']
            result[date].append(row)

        logger.write_info(str(result))
        return result
