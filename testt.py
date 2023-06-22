item = {'hour':'09:00'}

if len(str(item['hour'])) != 5:
    new_hour = str(item['hour']).split(':')
    new_hour = new_hour[:2]
    if len(new_hour) ==1:
        new_hour.append('00')
    if len(new_hour[0]) != 2:
        new_hour[0] = '0' + new_hour[0]
    item['hour'] = ':'.join(new_hour)
print(item['hour'])
