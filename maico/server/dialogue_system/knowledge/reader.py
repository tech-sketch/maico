# -*- coding: utf-8 -*-
import csv
import os
from collections import namedtuple

# import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Todo
# 地名、都道府県、地域を階層化

def read_small_areas():
    # 地名の読み込み
    file_path = os.path.join(BASE_DIR, 'locations.txt')
    with open(file_path, 'rb') as f:
        locations = [loc.decode('utf-8').strip() for loc in f]

    return locations


def read_middle_areas():
    # 都道府県の読み込み
    file_path = os.path.join(BASE_DIR, 'prefecture.txt')
    with open(file_path, 'rb') as f:
        middle_areas = [pref.decode('utf-8').strip() for pref in f]

    return middle_areas


def read_large_areas():
    # 地域の読み込み
    file_path = os.path.join(BASE_DIR, 'region.txt')
    with open(file_path, 'rb') as f:
        large_areas = [region.decode('utf-8').strip() for region in f]

    return large_areas


def read_spots():
    file_path = os.path.join(BASE_DIR, 'spots.csv')
    SpotRecord = namedtuple('SpotRecord',
                            'place, pron, type, pref, area, text, neighborhood, rate, image_path, season, memo')
    f = open(file_path, 'r')
    f.readline()  # skip header line
    spots = [spot for spot in map(SpotRecord._make, csv.reader(f))]

    return spots


def read_dialogues():
    file_path = os.path.join(BASE_DIR, 'dialogue.csv')
    RuleRecord = namedtuple('RuleRecord', 'type, label, description, act_type, text, if_, learn, goto, acc, mode')
    f = open(file_path, 'r')
    f.readline()  # skip header line
    rules = [rule for rule in map(RuleRecord._make, csv.reader(f))]

    return rules
