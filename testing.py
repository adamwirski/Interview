import datetime

date_time_str = '09:20:20 PM'
date_time_obj = datetime.datetime.strptime(date_time_str, '%I:%M:%S %p')

print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)