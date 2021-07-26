import json
from datetime import datetime ,timedelta
expires_in = datetime.now() +  timedelta(hours=2)
# x = [{"s":expires_in}]
# print(x)
# date_time_obj = datetime.strptime(expires_in, '%d/%m/%y %H:%M:%S')

ste = str(expires_in)
curr = datetime.now() 
date_time_str = str(datetime.now())
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
expires = datetime.strptime(ste, '%Y-%m-%d %H:%M:%S.%f')


print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)
print('Date-time:', expires)

if date_time_obj > expires:
    print(" expired")
    print(date_time_obj)
else:
    print("not expired")
    print(expires)

print("expiry time is ")
print(expires)
# print(type( expires_in))
# # again = Da(ste)
# date_time_obj = datetime.strptime(ste, '%d/%m/%y %H:%M:%S')
# print(type(date_time_obj))
# # print(type(again))
# print(type(ste))