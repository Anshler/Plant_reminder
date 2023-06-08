# get order of button, to determine to swipe left or right
HomeButtons2Num = {'home':0, 'plant_profile':1,'calendar':2,'community':3,'wiki':4,'shopping':5}
Days2Num = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

def find_closest_number(target: str):
    target = int(target.split(':')[0])
    numbers = [0,4,8,16,20]
    closest_smaller = float('-inf')  # Assume negative infinity as the initial closest smaller number
    for num in numbers:
        if num <= target and num > closest_smaller:
            closest_smaller = num
    return str(closest_smaller)
