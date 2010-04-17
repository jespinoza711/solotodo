import locale

def prettyPrice(value):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return '$ ' + locale.format("%d", value, True).replace(',', '.')
