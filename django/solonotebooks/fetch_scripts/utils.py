def clean_price_string(price_string):
    """
    Removes most common formatting of a string that represents a price
    leaving it only with its numbers.
    """

    blacklist = ['CLP$', '$', '.', ',', '&nbsp;', '\r', '\n', '\t']

    for item in blacklist:
        price_string = price_string.replace(item, '')

    return price_string