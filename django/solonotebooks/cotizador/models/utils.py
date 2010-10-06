import locale
from math import ceil, floor

def prettyPrice(value, spacing = ' '):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return '$' + spacing + locale.format("%d", value, True).replace(',', '.')
    
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
