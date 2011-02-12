import locale
from math import ceil, floor

def prettyPrice(value, spacing = ' ', show_symbol = True):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    value = locale.format("%d", value, True).replace(',', '.')
    if show_symbol:
        value = '$' + spacing + value
    return value
    
def roundToCeil10000(value):
    if value == None:
        return 0
    num = ceil(value / 10000)
    return int(num * 10000)
    
def roundToFloor10000(value):
    if value == None:
        return 0
    num = floor(value / 10000)
    return int(num * 10000)
