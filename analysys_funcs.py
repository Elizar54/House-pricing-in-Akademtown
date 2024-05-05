import numpy as np


def price_corr(price):
    price_str = ''
    elements = price.split()
    for x in elements[:len(elements)-1]:
        price_str += x
    if price_str == '':
        return price_str
    return int(price_str)


def square_corr(total_sq):
    if total_sq != 'None':
        total_sq = total_sq.replace(',', '.')
        total = total_sq.split()
        return float(total[0])
    return np.nan


def floor_corr(floor):
    if floor != 'None':
        floor_lst = floor.split()
        return int(floor_lst[0])
    return np.nan


def toilet_single(toilet):
    if 'раздельны' in str(toilet):
        toilet_lst = toilet.split()
        
        for elem in toilet_lst:
            if 'раздельны' in elem:
                return int(previous)
            previous = elem
    return 'None'

def toilet_not_sngl(toilet):
    if 'совмещенны' in str(toilet):
        toilet_lst = toilet.split()
        
        for elem in toilet_lst:
            if 'совмещенны' in elem:
                return int(previous)
            previous = elem
    return 'None'


def big_elevators(elevators):
    if 'грузов' in str(elevators):
        elevators_lst = elevators.split()
        
        for elem in elevators_lst:
            if 'грузов' in elem:
                return int(previous)
            previous = elem
    return 0


def lit_elevators(elevators):
    if 'пассажир' in str(elevators):
        elevators_lst = elevators.split()

        for elem in elevators_lst:
            if 'пассажир' in elem:
                return int(previous)
            previous = elem
    return 0


def metro_distance(metro_str):
    lst = metro_str.split()
    mins = []
    for elem in lst:
        if elem.isdigit():
            mins.append(int(elem))
    if mins != []:
        return min(mins)
    return 'None'

def balcony(balcony):
    if 'балкон' in str(balcony):
        return int(balcony.split()[0])
    return 0

def lodgia(balcony):
    if 'лоджия' in str(balcony):
        return int(balcony.split()[0])
    return 0