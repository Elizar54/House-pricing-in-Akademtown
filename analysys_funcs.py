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
    if 'раздельный' in toilet:
        return int(toilet.split()[0])
    return 0

def toilet_not_sngl(toilet):
    if 'совмещенный' in toilet:
        return int(toilet.split()[0])
    return 0


def big_elevators(elevators):
    if 'грузов' in elevators:
        elevators_lst = elevators.split()
        
        for elem in elevators_lst:
            if 'грузов' in elem:
                return int(previous)
            previous = elem
    return 0


def lit_elevators(elevators):
    if 'пассажир' in elevators:
        elevators_lst = elevators.split()

        for elem in elevators_lst:
            if 'пассажир' in elem:
                return int(previous)
            previous = elem
    return 0


