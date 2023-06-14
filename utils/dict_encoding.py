# get order of button, to determine to swipe left or right
HomeButtons2Num = {'home':0, 'plant_profile':1,'calendar':2,'community':3,'wiki':4,'shopping':5}
# get order of day to add up from the last monday's date
Days2Num = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
# convert month number string to month text string
NumStr2Month = {"01": "Jan","02": "Feb","03": "Mar","04": "Apr","05": "May","06": "Jun","07": "Jul","08": "Aug","09": "Sep","10": "Oct","11": "Nov","12": "Dec"}
# convert shortened day form to full day form
Day2Day = {"Mon": "monday","Tue": "tuesday","Wed": "wednesday","Thu": "thursday","Fri": "friday","Sat": "saturday","Sun": "sunday"}
# convert full day form to shortened day form
Day2DayRev = {'monday': 'Mon', 'tuesday': 'Tue', 'wednesday': 'Wed', 'thursday': 'Thu', 'friday': 'Fri', 'saturday': 'Sat', 'sunday': 'Sun'}
# convert number representative to corresponding hour range
HourBox2Text= {'4':'04:00 - 08:00','8':'08:00 - 12:00','12':'12:00 - 16:00','16':'16:00 - 20:00','20':'20:00 - 00:00','0':'00:00 - 04:00'}
# convert a time value to the closest lower hourbox representative number
def find_closest_number(target: str):
    target = int(target.split(':')[0])
    numbers = [0,4,8,12,16,20]
    closest_smaller = float('-inf')  # Assume negative infinity as the initial closest smaller number
    for num in numbers:
        if num <= target and num > closest_smaller:
            closest_smaller = num
    return str(closest_smaller)
