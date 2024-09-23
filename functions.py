# test

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# from skimage import data, filters, color, morphology
from skimage.segmentation import flood_fill
import json
import gc
from copy import deepcopy
# change unit key, change ocupied, type


#todo finish trigger
#todo draw retreats, buids, disbands
#if bot working solving, remmove -> #todo make sure not self attacking
# find convoy path and validate and all the logic
# at the beggining, for every convpying ship check if it gets cut, make a serch for all the attacks and their orders_dict['supports'], support cuts etc to see it convoy succeds

di={'nations': {'france': {'core': ['mar', 'par', 'bre'], 'lands': ['bre', 'par', 'gas', 'mar', 'bur', 'pic'], 'color': [89, 148, 201]}, 'italy': {'core': ['ven', 'rom', 'nap'], 'lands': ['ven', 'apu', 'nap', 'rom', 'tus', 'pie'], 'color': [104, 183, 125]}, 'england': {'core': ['lon', 'lvp', 'edi'], 'lands': ['cly', 'edi', 'yor', 'lvp', 'wal', 'lon'], 'color': [25, 107, 222]}, 'germany': {'core': ['mun', 'ber', 'kie'], 'lands': ['kie', 'ber', 'pru', 'sil', 'mun', 'ruh'], 'color': [136, 111, 77]}, 'austria': {'core': ['vie', 'bud', 'tri'], 'lands': ['boh', 'gal', 'tyr', 'vie', 'bud', 'tri'], 'color': [209, 82, 69]}, 'russia': {'core': ['sev', 'mos', 'war', 'stp'], 'lands': ['war', 'ukr', 'sev', 'mos', 'lvn', 'stp', 'fin'], 'color': [254, 248, 235]}, 'turkey': {'core': ['con', 'ank', 'smy'], 'lands': ['con', 'ank', 'smy', 'arm', 'syr'], 'color': [246, 210, 88]}},
	'discord': {'france': {'text': ':flag_fr:'}, 'russia': {'text': ':flag_ru:'}, 'austria': {'text': ':flag_at:'}, 'italy': {'text': ':flag_it:'}, 'germany': {'text': ':flag_de:'}, 'turkey': {'text': ':flag_tr:'}, 'england': {'text': ':flag_gb:'}, 'orders': {'chn_id': 1122279631781896263}},
	'lands': {'mos': {'sc': True, 'coasts': False, 'edges_u': ['stp', 'lvn', 'war', 'ukr', 'sev'], 'edges_f': [], 'cords': {'sc': [1089, 505], 'unit': [947, 548], 'fleet': None, 'name': [1030, 515], 'coasts': None, 'colors': {'main': (1030, 515), 'coloring': []}}}, 'stp': {'sc': True, 'coasts': True, 'edges_u': ['nwy', 'fin', 'lvn', 'mos'], 'edges_f': {'sc': ['fin', 'bot', 'lvn'], 'nc': ['nwy', 'bar']}, 'cords': {'sc': [929, 364], 'unit': [1028, 330], 'fleet': None, 'name': [941, 345], 'coasts': {'sc': {'name': [815, 444], 'fleet': [880, 430]}, 'nc': {'name': [933, 174], 'fleet': [930, 290]}}, 'colors': {'main': (941, 345), 'coloring': []}}, 'coats': True}, 'fin': {'sc': False, 'coasts': False, 'edges_u': ['nwy', 'swe', 'stp'], 'edges_f': ['nwy', 'swe', 'bot', 'stp_sc'], 'cords': {'sc': None, 'unit': [822, 304], 'fleet': [779, 397], 'name': [808, 345], 'coasts': None, 'colors': {'main': (808, 345), 'coloring': []}}}, 'swe': {'sc': True, 'coasts': False, 'edges_u': ['nwy', 'fin', 'den'], 'edges_f': ['nwy', 'bal', 'fin', 'den', 'ska', 'bot'], 'cords': {'sc': [664, 437], 'unit': [641, 484], 'fleet': [664, 484], 'name': [644, 423], 'coasts': None, 'colors': {'main': (644, 423), 'coloring': [(708, 498), (674, 527)]}}}, 'lvn': {'sc': False, 'coasts': False, 'edges_u': ['stp', 'mos', 'war', 'pru'], 'edges_f': ['bal', 'pru', 'bot', 'stp_sc'], 'cords': {'sc': None, 'unit': [774, 520], 'fleet': [776, 509], 'name': [787, 564], 'coasts': None, 'colors': {'main': (787, 564), 'coloring': []}}}, 'war': {'sc': True, 'coasts': False, 'edges_u': ['lvn', 'mos', 'ukr', 'gal', 'sil', 'pru'], 'edges_f': [], 'cords': {'sc': [734, 661], 'unit': [763, 679], 'fleet': None, 'name': [746, 653], 'coasts': None, 'colors': {'main': (746, 653), 'coloring': []}}}, 'ukr': {'sc': False, 'coasts': False, 'edges_u': ['gal', 'mos', 'war', 'sev', 'rum'], 'edges_f': [], 'cords': {'sc': None, 'unit': [895, 746], 'fleet': None, 'name': [886, 707], 'coasts': None, 'colors': {'main': (886, 707), 'coloring': []}}}, 'sev': {'sc': True, 'coasts': False, 'edges_u': ['arm', 'rum', 'mos', 'ukr'], 'edges_f': ['arm', 'rum', 'bla'], 'cords': {'sc': [1060, 733], 'unit': [989, 770], 'fleet': [1028, 822], 'name': [1069, 710], 'coasts': None, 'colors': {'main': (1069, 710), 'coloring': []}}}, 'rum': {'sc': True, 'coasts': False, 'edges_u': ['sev', 'ser', 'bul', 'bud', 'gal', 'ukr'], 'edges_f': ['sev', 'bla', 'bul_ec'], 'cords': {'sc': [852, 858], 'unit': [890, 859], 'fleet': [900, 861], 'name': [797, 876], 'coasts': None, 'colors': {'main': (797, 876), 'coloring': []}}}, 'bul': {'sc': True, 'coasts': True, 'edges_u': ['con', 'gre', 'ser', 'rum'], 'edges_f': {'ec': ['rum', 'con', 'bla'], 'sc': ['gre', 'aeg', 'con']}, 'cords': {'sc': [799, 931], 'unit': [852, 929], 'fleet': None, 'name': [797, 921], 'coasts': {'ec': {'name': [877, 916], 'fleet': [880, 930]}, 'sc': {'name': [843, 970], 'fleet': [850, 950]}}, 'colors': {'main': (797, 921), 'coloring': []}}, 'coats': True}, 'con': {'sc': True, 'coasts': False, 'edges_u': ['ank', 'smy', 'bul'], 'edges_f': ['aeg', 'ank', 'smy', 'bla', 'bul_sc', 'bul_ec'], 'cords': {'sc': [883, 973], 'unit': [934, 1000], 'fleet': [914, 986], 'name': [896, 972], 'coasts': None, 'colors': {'main': (920, 1000), 'coloring': [(883, 963)]}}}, 'gre': {'sc': True, 'coasts': False, 'edges_u': ['alb', 'ser', 'bul'], 'edges_f': ['aeg', 'alb', 'ion', 'bul_sc'], 'cords': {'sc': [768, 1012], 'unit': [780, 990], 'fleet': [791, 1057], 'name': [760, 1043], 'coasts': None, 'colors': {'main': (760, 1043), 'coloring': [(742, 1058), (723, 1017), (816, 1048)]}}}, 'smy': {'sc': True, 'coasts': False, 'edges_u': ['arm', 'syr', 'ank', 'con'], 'edges_f': ['eas', 'arm', 'syr', 'aeg', 'ank', 'con'], 'cords': {'sc': [909, 1041], 'unit': [1020, 1048], 'fleet': [1033, 1082], 'name': [914, 1077], 'coasts': None, 'colors': {'main': (914, 1077), 'coloring': [(867, 1024), (866, 1051), (885, 1069)]}}}, 'ank': {'sc': True, 'coasts': False, 'edges_u': ['arm', 'smy', 'con'], 'edges_f': ['arm', 'smy', 'con', 'bla'], 'cords': {'sc': [1044, 981], 'unit': [1084, 953], 'fleet': [1073, 934], 'name': [996, 983], 'coasts': None, 'colors': {'main': (996, 983), 'coloring': []}}}, 'arm': {'sc': False, 'coasts': False, 'edges_u': ['sev', 'syr', 'ank', 'smy'], 'edges_f': ['sev', 'syr', 'ank', 'smy', 'bla'], 'cords': {'sc': None, 'unit': [1193, 952], 'fleet': [1193, 924], 'name': [1191, 999], 'coasts': None, 'colors': {'main': (1191, 999), 'coloring': []}}}, 'syr': {'sc': False, 'coasts': False, 'edges_u': ['arm', 'smy'], 'edges_f': ['eas', 'arm', 'smy'], 'cords': {'sc': None, 'unit': [1146, 1124], 'fleet': [1126, 1115], 'name': [1155, 1093], 'coasts': None, 'colors': {'main': (1155, 1093), 'coloring': []}}}, 'boh': {'sc': False, 'coasts': False, 'edges_u': ['vie', 'gal', 'mun', 'sil', 'tyr'], 'edges_f': [], 'cords': {'sc': None, 'unit': [662, 733], 'fleet': None, 'name': [615, 712], 'coasts': None, 'colors': {'main': (615, 712), 'coloring': []}}}, 'gal': {'sc': False, 'coasts': False, 'edges_u': ['ukr', 'bud', 'vie', 'boh', 'sil', 'rum', 'war'], 'edges_f': [], 'cords': {'sc': None, 'unit': [826, 746], 'fleet': None, 'name': [759, 725], 'coasts': None, 'colors': {'main': (759, 725), 'coloring': []}}}, 'vie': {'sc': True, 'coasts': False, 'edges_u': ['tri', 'bud', 'tyr', 'boh', 'gal'], 'edges_f': [], 'cords': {'sc': [677, 760], 'unit': [653, 798], 'fleet': None, 'name': [634, 775], 'coasts': None, 'colors': {'main': (634, 775), 'coloring': []}}}, 'bud': {'sc': True, 'coasts': False, 'edges_u': ['vie', 'gal', 'ser', 'rum', 'tri'], 'edges_f': [], 'cords': {'sc': [706, 796], 'unit': [755, 824], 'fleet': None, 'name': [730, 785], 'coasts': None, 'colors': {'main': (730, 785), 'coloring': []}}}, 'ser': {'sc': True, 'coasts': False, 'edges_u': ['gre', 'alb', 'bul', 'rum', 'tri', 'bud'], 'edges_f': [], 'cords': {'sc': [755, 903], 'unit': [760, 942], 'fleet': None, 'name': [732, 897], 'coasts': None, 'colors': {'main': (732, 897), 'coloring': []}}}, 'tri': {'sc': True, 'coasts': False, 'edges_u': ['vie', 'alb', 'ser', 'ven', 'tyr', 'bud'], 'edges_f': ['adr', 'alb', 'ven'], 'cords': {'sc': [622, 833], 'unit': [679, 888], 'fleet': [677, 898], 'name': [641, 851], 'coasts': None, 'colors': {'main': (641, 851), 'coloring': []}}}, 'tyr': {'sc': False, 'coasts': False, 'edges_u': ['vie', 'pie', 'ven', 'tri', 'boh', 'mun'], 'edges_f': [], 'cords': {'sc': None, 'unit': [605, 785], 'fleet': None, 'name': [560, 798], 'coasts': None, 'colors': {'main': (560, 798), 'coloring': []}}}, 'pie': {'sc': False, 'coasts': False, 'edges_u': ['ven', 'tus', 'tyr', 'mar'], 'edges_f': ['gol', 'ven', 'tus', 'mar'], 'cords': {'sc': None, 'unit': [480, 850], 'fleet': [492, 846], 'name': [474, 830], 'coasts': None, 'colors': {'main': (474, 830), 'coloring': []}}}, 'ven': {'sc': True, 'coasts': False, 'edges_u': ['pie', 'tus', 'rom', 'apu', 'tyr', 'tri'], 'edges_f': ['adr', 'pie', 'tus', 'rom', 'apu', 'tri'], 'cords': {'sc': [576, 824], 'unit': [560, 860], 'fleet': [562, 869], 'name': [530, 847], 'coasts': None, 'colors': {'main': (530, 847), 'coloring': []}}}, 'tus': {'sc': False, 'coasts': False, 'edges_u': ['pie', 'ven', 'rom'], 'edges_f': ['gol', 'pie', 'ven', 'rom', 'tyn'], 'cords': {'sc': None, 'unit': [546, 906], 'fleet': [538, 908], 'name': [522, 887], 'coasts': None, 'colors': {'main': (550, 900), 'coloring': []}}}, 'apu': {'sc': False, 'coasts': False, 'edges_u': ['ven', 'rom', 'nap'], 'edges_f': ['adr', 'ven', 'rom', 'ion', 'nap'], 'cords': {'sc': None, 'unit': [640, 971], 'fleet': [658, 978], 'name': [605, 955], 'coasts': None, 'colors': {'main': (605, 955), 'coloring': []}}}, 'rom': {'sc': True, 'coasts': False, 'edges_u': ['ven', 'tus', 'apu', 'nap'], 'edges_f': ['ven', 'tus', 'apu', 'nap', 'tyn'], 'cords': {'sc': [588, 962], 'unit': [570, 929], 'fleet': [559, 934], 'name': [560, 952], 'coasts': None, 'colors': {'main': (570, 930), 'coloring': []}}}, 'nap': {'sc': True, 'coasts': False, 'edges_u': ['rom', 'apu'], 'edges_f': ['rom', 'ion', 'apu', 'tyn'], 'cords': {'sc': [643, 1005], 'unit': [648, 1030], 'fleet': [645, 1031], 'name': [616, 992], 'coasts': None, 'colors': {'main': (618, 992), 'coloring': []}}}, 'tun': {'sc': True, 'coasts': False, 'edges_u': ['naf'], 'edges_f': ['wes', 'naf', 'ion', 'tyn'], 'cords': {'sc': [479, 1080], 'unit': [479, 1135], 'fleet': [492, 1134], 'name': [456, 1105], 'coasts': None, 'colors': {'main': (456, 1105), 'coloring': []}}}, 'sil': {'sc': False, 'coasts': False, 'edges_u': ['boh', 'gal', 'mun', 'ber', 'pru', 'war'], 'edges_f': [], 'cords': {'sc': None, 'unit': [664, 668], 'fleet': None, 'name': [672, 702], 'coasts': None, 'colors': {'main': (672, 702), 'coloring': []}}}, 'pru': {'sc': False, 'coasts': False, 'edges_u': ['ber', 'sil', 'lvn', 'war'], 'edges_f': ['bal', 'ber', 'lvn'], 'cords': {'sc': None, 'unit': [718, 606], 'fleet': [705, 591], 'name': [664, 637], 'coasts': None, 'colors': {'main': (664, 637), 'coloring': []}}}, 'ber': {'sc': True, 'coasts': False, 'edges_u': ['mun', 'kie', 'sil', 'pru'], 'edges_f': ['bal', 'kie', 'pru'], 'cords': {'sc': [632, 637], 'unit': [617, 616], 'fleet': [635, 606], 'name': [589, 649], 'coasts': None, 'colors': {'main': (589, 649), 'coloring': []}}}, 'kie': {'sc': True, 'coasts': False, 'edges_u': ['ruh', 'mun', 'hol', 'den', 'ber'], 'edges_f': ['bal', 'hol', 'den', 'ber', 'hel'], 'cords': {'sc': [552, 570], 'unit': [554, 642], 'fleet': [527, 588], 'name': [535, 610], 'coasts': None, 'colors': {'main': (535, 610), 'coloring': [(550, 566)]}}}, 'mun': {'sc': True, 'coasts': False, 'edges_u': ['bur', 'boh', 'ruh', 'kie', 'ber', 'sil', 'tyr'], 'edges_f': [], 'cords': {'sc': [580, 731], 'unit': [538, 723], 'fleet': None, 'name': [542, 761], 'coasts': None, 'colors': {'main': (542, 761), 'coloring': []}}}, 'ruh': {'sc': False, 'coasts': False, 'edges_u': ['bur', 'mun', 'kie', 'bel', 'hol'], 'edges_f': [], 'cords': {'sc': None, 'unit': [505, 690], 'fleet': None, 'name': [487, 671], 'coasts': None, 'colors': {'main': (487, 671), 'coloring': []}}}, 'hol': {'sc': True, 'coasts': False, 'edges_u': ['bel', 'ruh', 'kie'], 'edges_f': ['bel', 'kie', 'hel', 'nth'], 'cords': {'sc': [489, 624], 'unit': [490, 604], 'fleet': [490, 606], 'name': [455, 640], 'coasts': None, 'colors': {'main': (455, 640), 'coloring': []}}}, 'den': {'sc': True, 'coasts': False, 'edges_u': ['swe', 'kie'], 'edges_f': ['bal', 'swe', 'kie', 'hel', 'nth', 'ska'], 'cords': {'sc': [593, 543], 'unit': [563, 512], 'fleet': [570, 509], 'name': [545, 543], 'coasts': None, 'colors': {'main': (545, 543), 'coloring': [(595, 551), (570, 550), (550, 565)]}}}, 'bel': {'sc': True, 'coasts': False, 'edges_u': ['bur', 'pic', 'hol', 'ruh'], 'edges_f': ['eng', 'pic', 'hol', 'nth'], 'cords': {'sc': [463, 690], 'unit': [429, 656], 'fleet': [426, 654], 'name': [440, 676], 'coasts': None, 'colors': {'main': (440, 676), 'coloring': []}}}, 'pic': {'sc': False, 'coasts': False, 'edges_u': ['bur', 'par', 'bre', 'bel'], 'edges_f': ['eng', 'bre', 'bel'], 'cords': {'sc': None, 'unit': [378, 679], 'fleet': [369, 682], 'name': [390, 678], 'coasts': None, 'colors': {'main': (390, 678), 'coloring': []}}}, 'bur': {'sc': False, 'coasts': False, 'edges_u': ['par', 'pic', 'bel', 'ruh', 'mun', 'mar', 'gas'], 'edges_f': [], 'cords': {'sc': None, 'unit': [430, 764], 'fleet': None, 'name': [419, 728], 'coasts': None, 'colors': {'main': (419, 728), 'coloring': []}}}, 'par': {'sc': True, 'coasts': False, 'edges_u': ['gas', 'bur', 'bre', 'pic'], 'edges_f': [], 'cords': {'sc': [360, 741], 'unit': [362, 755], 'fleet': None, 'name': [365, 728], 'coasts': None, 'colors': {'main': (365, 728), 'coloring': []}}}, 'mar': {'sc': True, 'coasts': False, 'edges_u': ['spa', 'gas', 'bur', 'pie'], 'edges_f': ['gol', 'spa_sc', 'gas', 'pie'], 'cords': {'sc': [429, 871], 'unit': [383, 837], 'fleet': [365, 864], 'name': [410, 856], 'coasts': None, 'colors': {'main': (410, 856), 'coloring': []}}}, 'gas': {'sc': False, 'coasts': False, 'edges_u': ['par', 'bre', 'spa', 'mar', 'bur'], 'edges_f': ['bre', 'mid', 'spa_nc', 'mar'], 'cords': {'sc': None, 'unit': [307, 828], 'fleet': [294, 825], 'name': [331, 804], 'coasts': None, 'colors': {'main': (331, 804), 'coloring': []}}}, 'bre': {'sc': True, 'coasts': False, 'edges_u': ['gas', 'par', 'pic'], 'edges_f': ['gas', 'mid', 'eng', 'pic'], 'cords': {'sc': [265, 695], 'unit': [317, 726], 'fleet': [326, 684], 'name': [279, 712], 'coasts': None, 'colors': {'main': (279, 712), 'coloring': []}}}, 'spa': {'sc': True, 'coasts': True, 'edges_u': ['por', 'mar', 'gas'], 'edges_f': {'nc': ['por', 'gas', 'mid'], 'sc': ['mid', 'gol', 'wes']}, 'cords': {'sc': [205, 919], 'unit': [161, 937], 'fleet': None, 'name': [222, 900], 'coasts': {'nc': {'name': [175, 827], 'fleet': [160, 815]}, 'sc': {'name': [192, 1007], 'fleet': [150, 1000]}}, 'colors': {'main': (222, 900), 'coloring': []}}, 'coats': True}, 'por': {'sc': True, 'coasts': False, 'edges_u': ['spa'], 'edges_f': ['mid', 'spa_nc', 'spa_sc'], 'cords': {'sc': [85, 911], 'unit': [117, 876], 'fleet': [109, 866], 'name': [80, 939], 'coasts': None, 'colors': {'main': (80, 939), 'coloring': []}}}, 'wal': {'sc': False, 'coasts': False, 'edges_u': ['lvp', 'yor', 'lon'], 'edges_f': ['eng', 'lvp', 'yor', 'lon', 'iri'], 'cords': {'sc': None, 'unit': [318, 622], 'fleet': [302, 616], 'name': [300, 585], 'coasts': None, 'colors': {'main': (330, 570), 'coloring': []}}}, 'lon': {'sc': True, 'coasts': False, 'edges_u': ['yor', 'wal'], 'edges_f': ['eng', 'yor', 'wal', 'nth'], 'cords': {'sc': [351, 611], 'unit': [378, 604], 'fleet': [387, 603], 'name': [341, 634], 'coasts': None, 'colors': {'main': (341, 634), 'coloring': []}}}, 'yor': {'sc': False, 'coasts': False, 'edges_u': ['edi', 'lvp', 'wal', 'lon'], 'edges_f': ['edi', 'lvp', 'wal', 'lon', 'nth'], 'cords': {'sc': None, 'unit': [370, 543], 'fleet': [370, 533], 'name': [352, 577], 'coasts': None, 'colors': {'main': (352, 577), 'coloring': []}}}, 'lvp': {'sc': True, 'coasts': False, 'edges_u': ['cly', 'edi', 'yor', 'wal'], 'edges_f': ['cly', 'edi', 'yor', 'wal', 'nat', 'iri'], 'cords': {'sc': [335, 559], 'unit': [340, 517], 'fleet': [340, 512], 'name': [330, 546], 'coasts': None, 'colors': {'main': (340, 540), 'coloring': []}}}, 'edi': {'sc': True, 'coasts': False, 'edges_u': ['cly', 'lvp', 'yor'], 'edges_f': ['cly', 'lvp', 'yor', 'nrg', 'nth'], 'cords': {'sc': [352, 457], 'unit': [369, 444], 'fleet': [369, 447], 'name': [340, 480], 'coasts': None, 'colors': {'main': (340, 480), 'coloring': []}}}, 'cly': {'sc': False, 'coasts': False, 'edges_u': ['edi', 'lvp'], 'edges_f': ['edi', 'lvp', 'nat', 'nrg'], 'cords': {'sc': None, 'unit': [351, 413], 'fleet': [323, 470], 'name': [326, 439], 'coasts': None, 'colors': {'main': (326, 439), 'coloring': []}}}, 'nwy': {'sc': True, 'coasts': False, 'edges_u': ['swe', 'fin', 'stp'], 'edges_f': ['swe', 'fin', 'nrg', 'nth', 'bar', 'ska', 'stp_nc'], 'cords': {'sc': [557, 410], 'unit': [598, 345], 'fleet': [596, 326], 'name': [563, 394], 'coasts': None, 'colors': {'main': (563, 394), 'coloring': []}}}, 'naf': {'sc': False, 'coasts': False, 'edges_u': ['tun'], 'edges_f': ['mid', 'tun', 'wes'], 'cords': {'sc': None, 'unit': [297, 1109], 'fleet': [283, 1070], 'name': [178, 1135], 'coasts': None, 'colors': {'main': (178, 1135), 'coloring': []}}}, 'alb': {'sc': False, 'coasts': False, 'edges_u': ['gre', 'ser', 'tri'], 'edges_f': ['adr', 'gre', 'tri', 'ion'], 'cords': {'sc': None, 'unit': [727, 992], 'fleet': [730, 997], 'name': [721, 975], 'coasts': None, 'colors': {'main': (721, 975), 'coloring': []}}}},
	'seas': {'bla': {'edges_f': ['sev', 'arm', 'ank', 'con', 'rum', 'bul_ec'], 'cords': {'fleet': [1055, 877], 'name': [978, 889]}}, 'aeg': {'edges_f': ['eas', 'ion', 'smy', 'con', 'gre', 'bul_sc'], 'cords': {'fleet': [839, 1022], 'name': [832, 1071]}}, 'eas': {'edges_f': ['ion', 'syr', 'smy', 'aeg'], 'cords': {'fleet': [930, 1138], 'name': [954, 1140]}}, 'ion': {'edges_f': ['adr', 'eas', 'aeg', 'tyn', 'gre', 'alb', 'tun', 'apu', 'nap'], 'cords': {'fleet': [692, 1049], 'name': [665, 1113]}}, 'adr': {'edges_f': ['ion', 'alb', 'ven', 'apu', 'tri'], 'cords': {'fleet': [635, 919], 'name': [592, 895]}}, 'tyn': {'edges_f': ['gol', 'ion', 'wes', 'tun', 'tus', 'rom', 'nap'], 'cords': {'fleet': [538, 1015], 'name': [508, 985]}}, 'gol': {'edges_f': ['tyn', 'wes', 'spa_sc', 'mar', 'pie', 'tus'], 'cords': {'fleet': [435, 932], 'name': [371, 915]}}, 'wes': {'edges_f': ['tun', 'mid', 'spa_sc', 'gol', 'tyn', 'naf'], 'cords': {'fleet': [365, 1013], 'name': [253, 1033]}}, 'mid': {'edges_f': ['nat', 'wes', 'naf', 'por', 'eng', 'spa_nc', 'spa_sc', 'gas', 'bre', 'iri'], 'cords': {'fleet': [210, 744], 'name': [96, 757]}}, 'nat': {'edges_f': ['mid', 'nrg', 'cly', 'lvp', 'iri'], 'cords': {'fleet': [141, 403], 'name': [170, 313]}}, 'nrg': {'edges_f': ['nat', 'nth', 'cly', 'edi', 'nwy', 'bar'], 'cords': {'fleet': [479, 246], 'name': [420, 165]}}, 'iri': {'edges_f': ['eng', 'mid', 'nat', 'lvp', 'wal'], 'cords': {'fleet': [255, 590], 'name': [199, 593]}}, 'eng': {'edges_f': ['iri', 'mid', 'nth', 'wal', 'lon', 'bre', 'pic', 'bel'], 'cords': {'fleet': [343, 656], 'name': [243, 665]}}, 'nth': {'edges_f': ['eng', 'nrg', 'ska', 'edi', 'yor', 'hel', 'lon', 'nwy', 'bel', 'hol', 'den'], 'cords': {'fleet': [427, 499], 'name': [436, 438]}}, 'bar': {'edges_f': ['nrg', 'nwy', 'stp_nc'], 'cords': {'fleet': [828, 53], 'name': [905, 77]}}, 'hel': {'edges_f': ['nth', 'hol', 'kie', 'den'], 'cords': {'fleet': [502, 544], 'name': [466, 579]}}, 'ska': {'edges_f': ['nth', 'nwy', 'swe', 'den'], 'cords': {'fleet': [551, 478], 'name': [565, 465]}}, 'bal': {'edges_f': ['bot', 'swe', 'lvn', 'kie', 'den', 'ber', 'pru'], 'cords': {'fleet': [671, 556], 'name': [696, 540]}}, 'bot': {'edges_f': ['bal', 'swe', 'fin', 'lvn', 'stp_sc'], 'cords': {'fleet': [732, 403], 'name': [722, 462]}}}
	}
# main_color_cords={'mos': (1030, 515), 'stp': (941, 345), 'fin': (808, 345), 'swe': (644, 423), 'lvn': (787, 564), 'war': (746, 653), 'ukr': (886, 707), 'sev': (1069, 710), 'rum': (797, 876), 'bul': (797, 921), 'con': (920, 1000), 'gre': (760, 1043), 'smy': (914, 1077), 'ank': (996, 983), 'arm': (1191, 999), 'syr': (1155, 1093), 'boh': (615, 712), 'gal': (759, 725), 'vie': (634, 775), 'bud': (730, 785), 'ser': (732, 897), 'tri': (641, 851), 'tyr': (560, 798), 'pie': (474, 830), 'ven': (530, 847), 'tus': (550, 900), 'apu': (605, 955), 'rom': (570, 930), 'nap': (618, 992), 'tun': (456, 1105), 'sil': (672, 702), 'pru': (664, 637), 'ber': (589, 649), 'kie': (535, 610), 'mun': (542, 761), 'ruh': (487, 671), 'hol': (455, 640), 'den': (545, 543), 'bel': (440, 676), 'pic': (390, 678), 'bur': (419, 728), 'par': (365, 728), 'mar': (410, 856), 'gas': (331, 804), 'bre': (279, 712), 'spa': (222, 900), 'por': (80, 939), 'wal': (330, 570), 'lon': (341, 634), 'yor': (352, 577), 'lvp': (340, 540), 'edi': (340, 480), 'cly': (326, 439), 'nwy': (563, 394), 'naf': (178, 1135), 'alb': (721, 975)}
# starting_lands={'austria': ['boh', 'gal', 'tyr', 'vie', 'bud', 'tri'], 'italy': ['ven', 'apu', 'nap', 'rom', 'tus', 'pie'], 'turkey': ['con', 'ank', 'smy', 'arm', 'syr'], 'russia': ['war', 'ukr', 'sev', 'mos', 'lvn', 'stp', 'fin'], 'germany': ['kie', 'ber', 'pru', 'sil', 'mun', 'ruh'], 'france': ['bre', 'par', 'gas', 'mar', 'bur', 'pic'], 'england': ['cly', 'edi', 'yor', 'lvp', 'wal', 'lon']}
# starting_units={'austria': {'vie': 't', 'bud': 't', 'tri': 'f'}, 'italy': {'ven': 't', 'rom': 't', 'nap': 'f'}, 'france': {'mar': 't', 'par': 't', 'bre': 'f'}, 'germany': {'mun': 't', 'ber': 't', 'kie': 'f'}, 'england': {'lon': 'f', 'lvp': 't', 'edi': 'f'}, 'russia': {'sev': 'f', 'mos': 't', 'war': 't', 'stp': 'f'}, 'turkey': {'con': 't', 'ank': 'f', 'smy': 't'}}
# centers=['tun', 'por', 'spa', 'bre', 'par', 'mar', 'bel', 'hol', 'kie', 'den', 'mun', 'ber', 'vie', 'bud', 'tri', 'ser', 'rum', 'gre', 'bul', 'con', 'ank', 'smy', 'war', 'sev', 'mos', 'stp', 'swe', 'nwy', 'lon', 'lvp', 'edi', 'ven', 'rom', 'nap']
# print(len(main_color_cords))
# print(len(di['lands']))
# coloring={'gre': [(742, 1058), (723, 1017), (816, 1048)], 'con': [(883, 963)], 'smy': [(867, 1024), (866, 1051), (885, 1069)], 'swe': [(708, 498), (674, 527)], 'den': [(595, 551), (570, 550), (550, 565)]}
# da_={'nations': {'france': {'lands': ['bre', 'par', 'gas', 'mar', 'bur', 'pic'], 'sc_lands': ['bre', 'par', 'mar'], 'units': {'mar': 'u', 'par': 'u', 'bre': 'f'}, 'orders': {}}, 'italy': {'lands': ['ven', 'apu', 'nap', 'rom', 'tus', 'pie'], 'sc_lands': ['ven', 'nap', 'rom'], 'units': {'ven': 'u', 'rom': 'u', 'nap': 'f'}, 'orders': {}}, 'england': {'lands': ['cly', 'edi', 'yor', 'lvp', 'wal', 'lon'], 'sc_lands': ['edi', 'lvp', 'lon'], 'units': {'lon': 'f', 'lvp': 'u', 'edi': 'f'}, 'orders': {}}, 'germany': {'lands': ['kie', 'ber', 'pru', 'sil', 'mun', 'ruh'], 'sc_lands': ['kie', 'ber', 'mun'], 'units': {'mun': 'u', 'ber': 'u', 'kie': 'f'}, 'orders': {}}, 'austria': {'lands': ['boh', 'gal', 'tyr', 'vie', 'bud', 'tri'], 'sc_lands': ['vie', 'bud', 'tri'], 'units': {'vie': 'u', 'bud': 'u', 'tri': 'f'}, 'orders': {}}, 'russia': {'lands': ['war', 'ukr', 'sev', 'mos', 'lvn', 'stp', 'fin'], 'sc_lands': ['war', 'sev', 'mos', 'stp'], 'units': {'sev': 'f', 'mos': 'u', 'war': 'u', 'stp_sc': 'f'}, 'orders': {}}, 'turkey': {'lands': ['con', 'ank', 'smy', 'arm', 'syr'], 'sc_lands': ['con', 'ank', 'smy'], 'units': {'con': 'u', 'ank': 'f', 'smy': 'u'}, 'orders': {}}},
# 	 'discord': {},
# 	 'lands': {'mos': {'owner': 'russia', 'type': 'u', 'ocupied': {'main': 'russia'}}, 'stp': {'owner': 'russia', 'type': 'f', 'ocupied': {'main': None, 'sc': 'russia', 'nc': None}}, 'fin': {'owner': 'russia', 'type': None, 'ocupied': {'main': None}}, 'swe': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'lvn': {'owner': 'russia', 'type': None, 'ocupied': {'main': None}}, 'war': {'owner': 'russia', 'type': 'u', 'ocupied': {'main': 'russia'}}, 'ukr': {'owner': 'russia', 'type': None, 'ocupied': {'main': None}}, 'sev': {'owner': 'russia', 'type': 'f', 'ocupied': {'main': 'russia'}}, 'rum': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'bul': {'owner': None, 'type': None, 'ocupied': {'main': None, 'ec': None, 'sc': None}}, 'con': {'owner': 'turkey', 'type': 'u', 'ocupied': {'main': 'turkey'}}, 'gre': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'smy': {'owner': 'turkey', 'type': 'u', 'ocupied': {'main': 'turkey'}}, 'ank': {'owner': 'turkey', 'type': 'f', 'ocupied': {'main': 'turkey'}}, 'arm': {'owner': 'turkey', 'type': None, 'ocupied': {'main': None}}, 'syr': {'owner': 'turkey', 'type': None, 'ocupied': {'main': None}}, 'boh': {'owner': 'austria', 'type': None, 'ocupied': {'main': None}}, 'gal': {'owner': 'austria', 'type': None, 'ocupied': {'main': None}}, 'vie': {'owner': 'austria', 'type': 'u', 'ocupied': {'main': 'austria'}}, 'bud': {'owner': 'austria', 'type': 'u', 'ocupied': {'main': 'austria'}}, 'ser': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'tri': {'owner': 'austria', 'type': 'f', 'ocupied': {'main': 'austria'}}, 'tyr': {'owner': 'austria', 'type': None, 'ocupied': {'main': None}}, 'pie': {'owner': 'italy', 'type': None, 'ocupied': {'main': None}}, 'ven': {'owner': 'italy', 'type': 'u', 'ocupied': {'main': 'italy'}}, 'tus': {'owner': 'italy', 'type': None, 'ocupied': {'main': None}}, 'apu': {'owner': 'italy', 'type': None, 'ocupied': {'main': None}}, 'rom': {'owner': 'italy', 'type': 'u', 'ocupied': {'main': 'italy'}}, 'nap': {'owner': 'italy', 'type': 'f', 'ocupied': {'main': 'italy'}}, 'tun': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'sil': {'owner': 'germany', 'type': None, 'ocupied': {'main': None}}, 'pru': {'owner': 'germany', 'type': None, 'ocupied': {'main': None}}, 'ber': {'owner': 'germany', 'type': 'u', 'ocupied': {'main': 'germany'}}, 'kie': {'owner': 'germany', 'type': 'f', 'ocupied': {'main': 'germany'}}, 'mun': {'owner': 'germany', 'type': 'u', 'ocupied': {'main': 'germany'}}, 'ruh': {'owner': 'germany', 'type': None, 'ocupied': {'main': None}}, 'hol': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'den': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'bel': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'pic': {'owner': 'france', 'type': None, 'ocupied': {'main': None}}, 'bur': {'owner': 'france', 'type': None, 'ocupied': {'main': None}}, 'par': {'owner': 'france', 'type': 'u', 'ocupied': {'main': 'france'}}, 'mar': {'owner': 'france', 'type': 'u', 'ocupied': {'main': 'france'}}, 'gas': {'owner': 'france', 'type': None, 'ocupied': {'main': None}}, 'bre': {'owner': 'france', 'type': 'f', 'ocupied': {'main': 'france'}}, 'spa': {'owner': None, 'type': None, 'ocupied': {'main': None, 'nc': None, 'sc': None}}, 'por': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'wal': {'owner': 'england', 'type': None, 'ocupied': {'main': None}}, 'lon': {'owner': 'england', 'type': 'f', 'ocupied': {'main': 'england'}}, 'yor': {'owner': 'england', 'type': None, 'ocupied': {'main': None}}, 'lvp': {'owner': 'england', 'type': 'u', 'ocupied': {'main': 'england'}}, 'edi': {'owner': 'england', 'type': 'f', 'ocupied': {'main': 'england'}}, 'cly': {'owner': 'england', 'type': None, 'ocupied': {'main': None}}, 'nwy': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'naf': {'owner': None, 'type': None, 'ocupied': {'main': None}}, 'alb': {'owner': None, 'type': None, 'ocupied': {'main': None}}},
# 	 'seas': {'bla': {'ocupied': {'main': None}}, 'aeg': {'ocupied': {'main': None}}, 'eas': {'ocupied': {'main': None}}, 'ion': {'ocupied': {'main': None}}, 'adr': {'ocupied': {'main': None}}, 'tyn': {'ocupied': {'main': None}}, 'gol': {'ocupied': {'main': None}}, 'wes': {'ocupied': {'main': None}}, 'mid': {'ocupied': {'main': None}}, 'nat': {'ocupied': {'main': None}}, 'nrg': {'ocupied': {'main': None}}, 'iri': {'ocupied': {'main': None}}, 'eng': {'ocupied': {'main': None}}, 'nth': {'ocupied': {'main': None}}, 'bar': {'ocupied': {'main': None}}, 'hel': {'ocupied': {'main': None}}, 'ska': {'ocupied': {'main': None}}, 'bal': {'ocupied': {'main': None}}, 'bot': {'ocupied': {'main': None}}},
# 	 'turn': {'season': 'spring', 'year': 1901, 'retreats': {}, 'clashes': []}

# }

# for sea in da['seas']:
# 	da['seas'][sea]['ocupied']={}
# 	da['seas'][sea]['ocupied']['main']=None

# print(da['seas'])
# for n in da['nations']:
# 	for ter1 in da['nations'][n]['lands']:
# 		ter=ter1[:3]
# 		da['lands'][ter]['owner']=n
# 	for ter1 in da['nations'][n]['sc_lands']:
# 		ter=ter1[:3]
# 		if ter=='stp':
# 			# co=ter1[-2:]
# 			da['lands'][ter]['ocupied']['sc']=n
# 			ter1='stp_sc'
# 		else:
# 			da['lands'][ter]['ocupied']['main']=n
# 		da['lands'][ter]['type']=da['nations'][n]['units'][ter1]
	
# print(da['lands'])

# for n in starting_lands:
# 	da['nations'][n]['lands']=starting_lands[n][:]
# 	for t in starting_lands[n]:
# 		if t in centers:
# 			da['nations'][n]['sc_lands'].append(t)
# 	for ter in starting_units[n]:
# 		if starting_units[n][ter]=='t':
# 			da['nations'][n]['units'][ter]='u'
# 		else:
# 			da['nations'][n]['units'][ter]='f'
		

# print(da['nations'])

def check_hold(ter1, idd, da):
	season=da['turn']['season']
	if season not in ['spring', 'autumn']:
		return f"cant do moves during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
	if ter1 not in da['nations'][idd]['units']:
		return f"you dont have a unit in {ter1}"
					
		
def check_build(idd, ter1, unit, da):
	season=da['turn']['season']
	if season not in ['build phase']:
		return f"cant build during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if ter not in da['nations'][idd]['sc_lands']:
		return f"cant build in {ter}\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
	if unit not in ['u', 'f']:
		return f"{unit} is not a unit type\n"
		
	if ter1 in da['nations'][idd]['units']:
		print('here 3')
		return f"cant build in {ter1}, unit already there"
	
	if di['lands'][ter]['coasts']:
		for c in di['lands'][ter]['edges_f']:
			if ter+'_'+c in da['nations'][idd]['units']:
				return f"cant build in {ter}, unit already there"
			

	if ter in da['nations'][idd]['units']:
		print('here 1')
		return f"cant build in {ter}, unit already there"
	if unit=='f':
		if len(di['lands'][ter]['edges_f'])>0:
			if type(di['lands'][ter]['edges_f']) is dict:
				if co not in di['lands'][ter]['edges_f']:
					return f"pls specify a coast"
		else:
			return f"cant build fleet in {ter}"
	print(len(da['nations'][idd]['units']))
	print(len(da['nations'][idd]['sc_lands']))
	print(len(da['nations'][idd]['orders']))
	if len(da['nations'][idd]['units'])>=len(da['nations'][idd]['sc_lands'])-len(da['nations'][idd]['orders']):
		return f"cant build any more units"
	
def check_disband_retreat(idd, ter1, da):
	season=da['turn']['season']
	if season not in ['summer', 'winter', 'build phase']:
		return f"cant disbad during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
	print(da['turn']['retreats'])
	if ter not in da['turn']['retreats'] or da['turn']['retreats'][ter]['idd']!=idd:
		return f"no unit to retreat in {ter}"
	# if da['turn']['season'] in ['summer', 'winter']:
	# 	if len(da['nations'][idd]['units'])<=len(da['nations'][idd]['sc_lands'])+len(da['nations'][idd]['orders']):
	# 		return f"cant disband any more unts"

def check_disband(idd, ter1, da):
	season=da['turn']['season']
	if season not in ['summer', 'winter', 'build phase']:
		return f"cant disbad during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
	if ter not in da['nations'][idd]['units']:
		return f"no unit in {ter}"
	if len(da['nations'][idd]['units'])<=len(da['nations'][idd]['sc_lands'])+len(da['nations'][idd]['orders']):
		return f"cant disband any more unts"
	
def check_retreat(idd, ter1, target1, da):
	season=da['turn']['season']
	if season not in ['summer', 'winter']:
		return f"cant reteat during {season}"
	print(da['turn']['retreats'])
	ter=ter1[:3]
	co=ter1[-2:]
	target=target1[:3]
	co2=target1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if not da['lands'].get(target):
		if not da['seas'].get(target):      
			return f"{target} is not a province.\n"
		else:
			if da['seas'][target]['ocupied']['main']!=None:
				return f"cant retreat to {target}"
	else:
		for i in da['lands'][target]['ocupied']:
			if da['lands'][target]['ocupied'][i]!=None:
				return f"cant retreat to {target}"
	if target1 in da['turn']['clashes']:
		return f"cant retreat to {target}"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
	if len(target1)!=3:
		if co not in di['lands'][target]['edges_f']:
			return f"{target} doesnt have a coast {co2}"
	print(da['turn']['retreats'])			
	if ter1 not in da['turn']['retreats'] or da['turn']['retreats'][ter1]['idd']!=idd:
		return f"you dot have a unit in {ter1}"
	if not da['turn']['retreats'].get(ter):
		return f"cant retreat {ter}"
	if da['turn']['retreats'][ter]==target:
		return f"cant retreat to {target}"
	
	


	


def check_support(idd, ter1, helped1, target1, da):
	season=da['turn']['season']
	if season not in ['spring', 'autumn']:
		return f"cant do moves during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	helped=helped1[:3]
	co2=helped1[-2:]
	target=target1[:3]
	if da['lands'].get(ter):
		ty1='lands'
	elif da['seas'].get(ter):
		ty1='seas'
	else:
		return f"{ter} is not a province.\n"
	if da['lands'].get(target):
		ty2='lands'
	elif da['seas'].get(target):
		ty2='seas'
	else:
		return f"{target} is not a province.\n"
	if not da['lands'].get(helped) and not da['seas'].get(helped):
		return f"{helped} is not a province.\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
		if not da['lands'][ter]['ocupied'][co]:
			return f"no unit in {ter1}"
	if len(helped1)!=3:
		if co2 not in di['lands'][helped]['edges_f']:
			return f"{helped} doesnt have a coast {co2}"
		# if da['lands'][target]['ocupied']['main'][co2]:
		# 	return f"no unit in {helped1}"
	if ter in [helped, target] or helped==target:
		return f"cant choose the same province twice\n"
	if ter1 not in da['nations'][idd]['units']:
		return f"you dont have a unit in {ter1}\n"
	
	# if da['lands'][target]['ocupied']['main']==None:
	# 	return f"no unit in {target}"
	
	if da['nations'][idd]['units'][ter1]=='f':
		if di['lands'].get(ter):
			if di['lands'][ter]['coasts']:
				print(target1[:3])
				clist=[x[:3] for coa in di['lands'][ter]['edges_f'] for x in di['lands'][ter]['edges_f'][coa]]
				if target1[:3] not in clist:
					# if not di['seas'].get(target):
					print('ok 1')
					return f"{ter} is not connected to {target}\n"
			else:
				if target not in [x[:3] for x in di['lands'][ter]['edges_f']]:
					print('ok 2')
					return f"{ter} is not connected to {target}\n"
		else:
			if target1 not in di['seas'][ter]['edges_f']:
				# if di['seas'].get(target):
				print('ok 3')
				return f"{ter} is not connected to {target}\n"
	elif da['nations'][idd]['units'][ter1]=='u':
		if target not in di['lands'][ter]['edges_u']:
			print('ok 4')
			return f"{ter} is not connected to {target}\n"
		
	if di['lands'].get(helped):
		ty2='lands'
	else:
		ty2='seas'

	if da[ty2][helped]['type']=='f':
		if di['lands'].get(helped):
			if da['lands'][helped]['ocupied']['main']==None:
				return f"no unit in {helped}"
			if di['lands'][helped]['coasts']:
				if target1 not in di['lands'][helped]['edges_f'][co2]:
					# if not di['seas'].get(target):
					return f"{helped} is not connected to {target}\n"
			else:
				if target1 not in di['lands'][helped]['edges_f']:
					return f"{helped} is not connected to {target}\n"
		else:
			if target1 not in di['seas'][helped]['edges_f']:
				return f"{helped} is not connected to {target}\n"
	elif da[ty2][helped]['type']=='u':
		if target in di['lands'][helped]['edges_u']:
			# return f"{helped} is not connected to {target}\n"
			pass
		else:
			paths=find_paths(helped, target)
			for path in paths:
				for sea in path:
					# print(sea)
					if da['seas'][sea]['ocupied']['main']==None:
						# return f"{helped} is not connected to {target}"
						paths.remove(path)
						break
			if len(paths)==0:
				return f"{helped} is not connected to {target}\n"

					
				
			# check for convoy paths

def check_move(idd, ter1, target1, da):
	season=da['turn']['season']
	if season not in ['spring', 'autumn']:
		return f"cant do moves during {season}", None, []
	ter=ter1[:3]
	print(target1)
	# print(di['lands'][ter]['edges_f'])
	co=ter1[-2:]
	target=target1[:3]
	# co2=target1[-2:]
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n", None, []
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}", None, []
	if not da['lands'].get(target) and not da['seas'].get(target):
		return f"{target} is not a province.\n", None, []
	if ter in [target, target1] or ter1 in [target, target1]:
		return f"cant choose the same province twice\n", None, []
	if ter1 not in da['nations'][idd]['units']:
		return f"you dont have a unit in {ter1}\n", None, []
	if di['lands'].get(ter):
		y='lands'
	else:
		y='seas'
	if da[y][ter]['type']=='f':
		if di['lands'].get(ter):
			if di['lands'][ter]['coasts']:
				if target1 not in di['lands'][ter]['edges_f'][co]:
					print('here 1')
					return f"{ter} is not connected to {target}\n", None, []
				# else:
					# print('yes 1')
			else:
				if target1 not in di['lands'][ter]['edges_f']:
					print('here 2')
					return f"{ter1} is not connected to {target1}\n", None, []
				# else:
					# print('yes 2')
		else:
			if target1 not in di['seas'][ter]['edges_f']:
				print('here 3')
				return f"{ter} is not connected to {target}\n", None, []
			# else:
					# print('yes 3')
	elif da['lands'][ter]['type']=='u':
		
		if target in di['lands'][ter]['edges_u']:
			# print('yes')
			# print('here 4')
			# return f"{ter} is not connected to {target}\n"
			pass
		else:
			paths=find_paths(ter, target)
			for path in paths:
				for sea in path:
					# print(sea)
					if da['seas'][sea]['ocupied']['main']==None:
						# return f"{helped} is not connected to {target}"
						paths.remove(path)
						break
			if len(paths)==0:
				print('here 5')
				return f"{ter} is not connected to {target}\n", None, []
			else:
				return None, True, paths
			# else:
				# print('yes 4')
	#todo print('-------------------------------------Error')        
	# why find where type doesnt change whwn success
	# print(da['lands'][ter]['type'])  
	return None, False, []
			
			# check for convoy paths

def check_defend(idd, ter1, helped1, da):
	season=da['turn']['season']
	if season not in ['spring', 'autumn']:
		return f"cant do moves during {season}"
	ter=ter1[:3]
	co=ter1[-2:]
	helped=helped1[:3]
	co2=helped1[-2:]
	
	if not da['lands'].get(ter) and not da['seas'].get(ter):
		return f"{ter} is not a province.\n"
	if len(ter1)!=3:
		if co not in di['lands'][ter]['edges_f']:
			return f"{ter} doesnt have a coast {co}"
		
	if di['lands'].get(helped):
		ty2='lands'
	else:
		ty2='seas'
	
	
	if da[ty2][helped]['type']=='f':
		if len(helped1)!=3:
			if co2 not in di['lands'][helped]['edges_f']:
				return f"{helped} doesnt have a coast {co2}"
			if da['lands'][helped]['ocupied'][co2]==None:
				return f"no unit in {helped1}"
		else:
			if da[ty2][helped]['ocupied']['main']==None:
				return f"no unit in {helped}"
	else:
		print(da[ty2][helped]['ocupied']['main'])
		print(da[ty2][helped]['type'])
		if da[ty2][helped]['ocupied']['main']==None:
			return f"no unit in {helped}"
		

	if not da['lands'].get(helped) and not da['seas'].get(helped):
		return f"{helped} is not a province.\n"
	if ter==helped:
		return f"cant choose the same province twice\n"
	if ter1 not in da['nations'][idd]['units']:
		return f"you dont have a unit in {ter1}\n"
	
	if di['lands'].get(ter):
		ty='lands'
	else:
		ty='seas'
	
	
	if da[ty][ter]['type']=='f':
		if di['lands'].get(ter):
			if di['lands'][ter]['coasts']:
				if helped not in di['lands'][ter]['edges_u']:
					return f"{ter} is not connected to {helped} 1\n"
			else:
				if helped not in di['lands'][ter]['edges_u']:
					return f"{ter} is not connected to {helped} 2\n"
		else:
			if helped1 not in di['seas'][ter]['edges_f']:
				return f"{ter} is not connected to {helped} 3\n"
	elif da[ty][ter]['type']=='u':
		if helped not in di['lands'][ter]['edges_u']:
			return f"{ter} is not connected to {helped} 4\n"

def check_convoy(idd, ter, helped, target, da):
	season=da['turn']['season']
	if season not in ['spring', 'autumn']:
		return f"cant do moves during {season}", []
	if not da['seas'].get(ter):
		return f"{ter} is not a sea.\n", []
	if not da['lands'].get(target):
		return f"{target} is not a land.\n", []
	if not da['lands'].get(helped):
		return f"{helped} is not a land.\n", []	
	if ter in [helped, target] or helped==target:
		return f"cant choose the same province twice\n", []
	if ter not in da['nations'][idd]['units']:
		return f"you dont have a unit in {ter}\n", []
	if da['lands'][helped]['ocupied']['main']==None:
		return f"no unit in {helped}", []
	paths=find_paths(helped, target)
	for path in paths:
		for sea in path:
			if da['seas'][sea]['ocupied']['main']==None:
				# return f"{helped} is not connected to {target}"
				paths.remove(path)
				break
	if len(paths)==0:
		return f"{helped} is not connected to {target}\n", []
	else:
		return None, paths



def check_roles(ctx):
	returning=[False, False, None]
	for r in ctx.author.roles:
		# print(str(r))
		if str(r).lower() == 'gm':
			returning[0]=True
		elif str(r).lower() == 'player':
			returning[1]=True
		elif str(r).lower() in di['nations']:
			returning[2]=str(r).lower()
	print(returning)
	return returning



def flood_fill_(y, x, nim, color):
	# print(len(nim))
	filled_checkers1 = flood_fill(nim, (x, y, 0), color[0], tolerance=3)
	filled_checkers2 = flood_fill(filled_checkers1, (x, y, 1), color[1], tolerance=3)
	filled_checkers3 = flood_fill(filled_checkers2, (x, y, 2), color[2], tolerance=3)
	del filled_checkers1
	del filled_checkers2
	del nim
	gc.collect()
	# print('fc3', len(filled_checkers3))
	return filled_checkers3


def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % rgb

def get_tc(ter):
	t, c=ter.lower().split('_')
	return t, c

def get_cords(ter1, da, unit=None):
	ter=ter1[:3]
	# print(ter1, 'cords')	
	coast=ter1[-2:]
	if da['lands'].get(ter):
		if len(ter1)!=3:
			cords=di['lands'][ter]['cords']['coasts'][coast]['fleet']
		else:

			# print('---------------------------------', da['lands'][ter]['type'], ter)
			if da['lands'][ter]['type']=='f':
				ty='fleet'
			elif da['lands'][ter]['type']=='u':
				ty='unit'
			else:
				if unit=='u':
					ty='unit'
				elif unit=='f':
					ty='fleet'
				else:
					ty='unit'
			cords=di['lands'][ter]['cords'][ty]
			if cords==None:
				cords=di['lands'][ter]['cords']['unit']
	else:
		cords=di['seas'][ter]['cords']['fleet']
	return cords

def draw_attack(ter, target, color, da, alpha=1):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter, da)
	x2, y2=get_cords(target, da)
	# print('alpha', alpha)
	plt.arrow(x1, y1, x2-x1, y2-y1, head_width=7, head_length=7, color=color, alpha=alpha, width=1.2, zorder=10, length_includes_head=True)

def draw_convoy_attack(ter1, ter2, color, alpha, da):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter1, da)
	x2, y2=get_cords(ter2, da)
	plt.plot([x1, x2], [y1, y2], linestyle='dotted', color=color, alpha=alpha, zorder=10)

def draw_convoy_attack_arrow(ter1, ter2, color, alpha, da):	
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter1, da)
	x2, y2=get_cords(ter2, da)
	plt.arrow(x1, y1, x2-x1, y2-y1, head_width=7, head_length=7, linestyle='', color=color, alpha=alpha, zorder=10, length_includes_head=True)# width=1.2)
	# plt.plot([x1, x2], [y1, y2], linestyle='dotted', color=color, alpha=alpha, zorder=10)


def draw_support(ter, target, helped, color, da):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter, da)
	x2, y2=get_cords(target, da)
	x3, y3=get_cords(helped, da)
	xf, yf=(x2+x3)//2, (y2+y3)//2
	# plt.arrow(x1, y1, xf-x1, yf-y1, arrowprops={'arrowstyle': '-|>'})
	plt.plot([x1, xf], [y1, yf], linestyle='dashed', color=color, zorder=10)
	plt.plot(xf, yf, markersize=6, markeredgecolor=color, markeredgewidth=1.5, markerfacecolor='None', marker='o', zorder=11)

def draw_defend(ter, helped, color, da):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter, da)
	x2, y2=get_cords(helped, da)
	plt.plot([x1, x2], [y1, y2], linestyle='dotted', color=color, zorder=10)
	plt.plot(x2, y2, markersize=12, markeredgecolor=color, markeredgewidth=1.5, markerfacecolor='None', marker='D', zorder=11)

def draw_convoy(ter, da):
	x, y=get_cords(ter, da)
	y+=15
	plt.plot(x, y, markersize=5, color='blue', marker="$≈$", zorder=12)

def draw_build(ter, mark, da):
	x, y=get_cords(ter, da)
	plt.plot(x, y, mark, markersize=10, color='#39ff14', zorder=11) #markeredgecolor='black', markeredgewidth=2)

def draw_disband(ter, unit, da):
	x, y=get_cords(ter, da, unit=unit)
	plt.plot(x, y, 'x', markersize=10, color='#ff1818', zorder=11)


def draw_disband_retreat(ter, da):
	x, y=get_cords(ter, da)
	x+=5
	y+=5
	plt.plot(x, y, 'x', markersize=10, color='#ff1818', zorder=13)

def draw_retreat_move(ter, target, color, da):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x1, y1=get_cords(ter, da)
	x1+=5
	y1+=5
	x2, y2=get_cords(target, da)
	plt.arrow(x1, y1, x2-x1, y2-y1, head_width=7, head_length=7, color=color, width=1.2, zorder=12, length_includes_head=True)


def draw_retreat(ter, mark, color, da):
	if type(color)==tuple:
		color=rgb_to_hex(color)
	x, y=get_cords(ter, da)
	x+=5
	y+=5
	plt.plot(x, y, mark, markersize=7, color=color, markeredgecolor='black', markeredgewidth=1.5, zorder=11)

class PathChecker:
	def __init__(self, f, path):
		self.f=f
		self.path=path
		self.cattacked_defence={}
		self.cattacked_support={}
		self.resolve={'defence': 1, 'attackers': {}}

	def check_path(self, orders_dict):
		for sea in self.path:
			for attacker in orders_dict['movement']:
				if orders_dict['movement'][attacker]['target']==sea:
					if self.resolve['attackers'].get(attacker):
						self.resolve['attackers'][attacker]+=1
					else:
						self.resolve['attackers'][attacker]=1

			for supporter in orders_dict['supports']:
				if not orders_dict['supports'][supporter]['cut'] and orders_dict['supports'][supporter]['target']==sea:
					for x in orders_dict['convoy_moves']:
						if orders_dict['convoy_moves'][x]['target']==supporter and x!=self.f:
							self.cattacked_support[supporter]={'helping': sea, 'attacked': x}
							break
					else:
						if self.resolve['attackers'].get(orders_dict['supports'][supporter]['helped']):
							self.resolve['attackers'][orders_dict['supports'][supporter]['helped']]+=1
						else:
							self.resolve['attackers'][orders_dict['supports'][supporter]['helped']]=1

			for defender in orders_dict['defends']:
				if not orders_dict['defends'][defender]['cut'] and orders_dict['defends'][defender]['helped']==sea:
					for x in orders_dict['convoy_moves']:
						if orders_dict['convoy_moves'][x]['target']==defender and x!=self.f:
							self.cattacked_defence[defender]={'helping': sea, 'attacked': x}
							break
					else:
						self.resolve['defence']+=1

			for d in self.cattacked_defence:
				legit_paths=[]
				for p in orders_dict['convoy_moves'][x]['paths']:
					for sea in p:
						if orders_dict['convoys'].get(sea) and orders_dict['convoys'][sea]['helped']==d and orders_dict['convoy_moves'][sea]['target']==orders_dict['convoy_moves'][d]['target']:
							pass
						else:
							break
					else:
						check=PathChecker(d, p)
						if check.check_path(orders_dict):
							legit_paths.append(p)
							del check
							gc.collect()
				if len(legit_paths)==0:
					self.resolve['defence']+=1

			for d in self.cattacked_support:
				legit_paths=[]
				for p in orders_dict['convoy_moves'][x]['paths']:
					for sea in p:
						if orders_dict['convoys'].get(sea) and orders_dict['convoys'][sea]['helped']==d and orders_dict['convoy_moves'][sea]['target']==orders_dict['convoy_moves'][d]['target']:
							pass
						else:
							break
					else:
						check=PathChecker(d, p)
						if check.check_path(orders_dict):
							legit_paths.append(p)
						del check
						gc.collect()
				if len(legit_paths)==0:
					if self.resolve['attackers'].get(d):
						self.resolve['attackers'][d]+=1
					else:
						self.resolve['attackers'][d]=1
			if len(self.resolve['attackers'])>0:
				s=[]
				for i in self.resolve['attackers']:
					s.append((i, self.resolve['attackers'][i]))
				m=max(s, key=lambda x: x[1])
				if self.resolve['defence']<m[1]:
					return False
		else:
			return True





def solve_orders(da):
	orders_dict={}
	orders_dict['movement']={}
	orders_dict['supports']={}
	orders_dict['defends']={}
	orders_dict['convoys']={}
	orders_dict['retreats']={}
	orders_dict['convoy_moves']={}
	rare={}
	da_new=deepcopy(da)
	# print('par 2', da['lands']['par'])
	# print('pic 2', da['lands']['pic'])
	lands={}
	for ter in di['lands']:
		for i in da['lands'][ter]['ocupied']:
			# if i!='main':
			#   ter2=ter+'_'+i
			# else:
			#   ter2=ter
			if da['lands'][ter]['ocupied'][i]!=None:
				print('was given', ter)
				lands[ter]={'defence': 1, 'attacks': {}}
				break
		# else:
		#   lands[ter2]={'defence': 0, 'attacks': {}}
		else:
			lands[ter]={'defence': 0, 'attacks': {}}

	for ter in di['seas']:
		for i in da['seas'][ter]['ocupied']:
			if da['seas'][ter]['ocupied'][i]!=None:
				lands[ter]={'defence': 1, 'attacks': {}}
				break
		else:
			lands[ter]={'defence': 0, 'attacks': {}}
	
	# lands={x: {'defence': 1, 'attacks': {}} }
	for j in da['nations']:
		print(j, da['nations'][j]['orders'])
		for i in da['nations'][j]['orders']:
			order=da['nations'][j]['orders'][i]
			# print(order)
			if order['mode']=='m':
				if order['convoy']:
					orders_dict['convoy_moves'][i]={'target': order['target'], 'mode': 'm', 'success': None, 'convoy': True,  'complete': None, 'paths': order['paths'][:]}
				else:
					# print('got it', i)
					orders_dict['movement'][i]={'target': order['target'], 'mode': 'm', 'success': None, 'convoy': False}
			elif order['mode']=='s':
				orders_dict['supports'][i]={'target': order['target'], 'helped': order['helped'], 'mode': 's', 'cut': False, 'empty': False}
			elif order['mode']=='d':
				orders_dict['defends'][i]={'helped': order['helped'], 'mode': 'd', 'cut': False, 'empty': False}
			elif order['mode']=='c':
				orders_dict['convoys'][i]={'target': order['target'], 'helped': order['helped'], 'mode': 'c', 'cut': False, 'empty': False}
	
	
	for ter in orders_dict['convoys']:
		if not orders_dict['convoy_moves'].get(orders_dict['convoys'][ter]['helped']):
			orders_dict['convoys'][ter]['empty']=True
	
	print(orders_dict['movement'])
	for ter in orders_dict['movement']:
		ter1=ter[:3]    
		target=orders_dict['movement'][ter]['target']
		target1=target[:3]
		# print('ye/s')
		lands[target1]['attacks'][ter]=1
		lands[ter1]['defence']=0
		if target in orders_dict['supports']:
			if orders_dict['supports'][target]['target']!=ter:
				orders_dict['supports'][target]['cut']=True
			else:
				# good=solve_support_attacked_by_target(orders_dict, ter, orders_dict['supports'][target]['target'])
				# orders_dict['supports'][target]['cut']=True
				rare[ter]=orders_dict['movement'][ter]
		elif target in orders_dict['defends']:
			orders_dict['defends'][target]['cut']=True
			



	for ter in orders_dict['convoy_moves']:
		legit_paths=[]
		for path in orders_dict['convoy_moves'][ter]['paths']:
			for sea in path:
				if orders_dict['convoys'].get(sea) and orders_dict['convoys'][sea]['helped']==ter and orders_dict['convoys'][sea]['target']==orders_dict['convoy_moves'][ter]['target']:
					pass
				else:
						break
			else:
				check=PathChecker(ter, path)
				if check.check_path(orders_dict):
					legit_paths.append(path)
				del check  		
				gc.collect()	
		if len(legit_paths)==0:
			print('-----------------------------------False')
			orders_dict['convoy_moves'][ter]['complete']=False
		else:
			print('---------------- true')
			orders_dict['convoy_moves'][ter]['complete']=True
			orders_dict['movement'][ter]={'target': orders_dict['convoy_moves'][ter]['target'], 'mode': 'm', 'success': None, 'convoy': True}
			legit_paths.sort(key=len)
			orders_dict['convoy_moves'][ter]['paths']=legit_paths.pop(0)
			for p in legit_paths:
				for s in p:
					orders_dict['convoys'][s]['empty']=True
	
	
	
	for ter in orders_dict['convoy_moves']:
		if orders_dict['convoy_moves'][ter]['complete']:
			target=orders_dict['convoy_moves'][ter]['target']
		# print('ye/s')
			lands[target[:3]]['attacks'][ter]=1
			lands[ter[:3]]['defence']=0
			if target in orders_dict['supports']:
				orders_dict['supports'][target]['cut']=True
			elif target in orders_dict['defends']:
				orders_dict['defends'][target]['cut']=True
	
	
	# for ter in orders_dict['convoy_moves']:
	#   if orders_dict['convoy_moves'][ter]['complete']:
	#     orders_dict['supports'][target]['cut']=True
	#   elif target in orders_dict['defends']:
	#     orders_dict['defends'][target]['cut']=True  
	# print(lands)
	# print('rare         ', rare)
	# print(orders_dict)
	for ter in rare:
		target=rare[ter]['target']
		good, q=solve_support_attacked_by_target(orders_dict, ter, target)
		print(ter, good, q)
		if good:
			orders_dict['supports'][target]['cut']=True
		else:
			orders_dict['movement'][ter]['success']=False
			print('yesss 1', ter)
			lands[ter[:3]]['defence']=1
			# orders_dict['movement'][ter]['success']=True
		# else:
		#   orders_dict['movement'][ter]['success']=False
		#   lands[ter]['defence']=1
																		 

	for ter in orders_dict['supports']:
		if orders_dict['supports'][ter]['cut']==False:
			t=orders_dict['supports'][ter]['target']
			h=orders_dict['supports'][ter]['helped']
			# print(ter, 'helped', h, 'to', t)
			if h in lands[t[:3]]['attacks']:
				# print(ter, 'done')
				lands[t[:3]]['attacks'][h]+=1
			else:
				orders_dict['supports'][ter]['empty']=True
				
	for ter in orders_dict['defends']:
		if orders_dict['defends'][ter]['cut']==False:
			h=orders_dict['defends'][ter]['helped']
			if lands[h[:3]]['defence']>0:
				print('yesss 2', h)
				lands[h[:3]]['defence']+=1
			else:
				orders_dict['defends'][ter]['empty']=True

	for ter in orders_dict['movement']:
		if orders_dict['movement'][ter]['success']==False:
			print('yesss 3', ter)
			lands[ter[:3]]['defence']=1
	
	
	
	
	# print(lands['bul'])
	unsolved={}
	unknown={}
	for ter in lands:
		attacks=lands[ter]['attacks']
		if len(attacks)>0:
			# print('yes', ter)
			s=[]
			for i in attacks:
				s.append((i, attacks[i]))
			maxes=[]
			m=max(s, key=lambda x: x[1])
			maxes.append(m)
			for i in s:
				if i[1]==m[1] and i!=maxes[0]:
					maxes.append(i)
			# print(maxes, ter)
			if len(maxes)>1:
				for i in s:
					print('failed 1', i)
					orders_dict['movement'][i[0]]['success']=False
					da_new['turn']['clashes'].append(ter)
					print('got it here 1')
					print('yesss 4', i[0])
					lands[i[0][:3]]['defence']=1
	
			else:
				winner=maxes[0][0]
				winner2=winner[:3]
				ter2=ter[:3]
				coast1=None
				coast2=None
				if da['lands'].get(winner2):
					ty1='lands'
					if di['lands'][winner2]['coasts']:
						for i in da['lands'][winner2]['ocupied']:
							if da['lands'][winner2]['ocupied'][i]!=None:
								if i!='main':
									winner=winner2+'_'+i
						coast1=winner[-2:]
				else:
					ty1='seas'
	
				if da['lands'].get(ter2):
					ty2='lands'
					if di['lands'][ter2]['coasts']:
						# for i in da['lands'][ter2]['ocupied']:
						#   if da['lands'][ter2]['ocupied'][i]!=None:
						#     if i!='main':
						#       ter=ter2+'_'+i
						# print('???????????????????       2', ter)
						print(orders_dict['movement'][winner]['target'])
						coast2=orders_dict['movement'][winner]['target'][-2:]
						# coast2=ter[-2:]
				else:
					ty2='seas'
				for i in s:
					if i!=maxes[0]:
						# print('here3')
						print('failed 2', i)
						orders_dict['movement'][i[0]]['success']=False
						print('got it here 2')
						print('yesss 5', i[0])
						lands[i[0][:3]]['defence']=1
	
				if lands[ter2]['defence']>0:
					print('--------------------------', maxes[0][1], lands[ter2]['defence'])  
					if maxes[0][1]>lands[ter2]['defence']:
						# da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
						# da_new[ty1][winner2]['type']=None
						ok=False
						print(da_new['lands']['tri']['ocupied']['main'])
						if not coast1 and not coast2:
							print('ok 4')
							if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
								ok=True
								idd=da[ty1][winner2]['ocupied']['main']
								print(ty2, ter2)
								idd2=da[ty2][ter2]['ocupied']['main']		
								print(idd2)
								da_new[ty1][winner2]['ocupied']['main']=None
								da_new[ty2][ter2]['ocupied']['main']=idd
						elif coast1 and not coast2:
							print('ok 3')
							if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
								ok=True
								idd=da[ty1][winner2]['ocupied'][coast1]
								idd2=da[ty2][ter2]['ocupied']['main']		
								da_new[ty1][winner2]['ocupied'][coast1]=None
								da_new[ty2][ter2]['ocupied']['main']=idd
						elif not coast1 and coast2:
							print('ok 2')
							if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
								ok=True
								idd=da[ty1][winner2]['ocupied']['main']
								da_new[ty1][winner2]['ocupied']['main']=None
								idd2=da[ty2][ter2]['ocupied'][coast2]
								da_new[ty2][ter2]['ocupied'][coast2]=idd
						elif coast1 and coast2:
							print('ok 1')
							if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
								ok=True
								idd=da[ty1][winner2]['ocupied'][coast1]
								da_new[ty1][winner2]['ocupied'][coast1]=None
								idd2=da[ty2][ter2]['ocupied'][coast2]
								da_new[ty2][ter2]['ocupied'][coast2]=idd
						print(ok)
						if ok:
							print('sucess 4', winner)
							orders_dict['movement'][winner]['success']=True
							if winner in orders_dict['convoy_moves']:
								orders_dict['convoy_moves'][winner]['success']=True
							# print(da_new['lands']['tri']['ocupied']['main'])
							print(idd2, ter2)
							orders_dict['retreats'][ter]={'forbiden': winner, 'idd': idd2, 'unit': da['nations'][idd2]['units'][ter]}
							print(idd, winner)
							unit=da['nations'][idd]['units'][winner]
							if da_new['nations'][idd]['units'].get(winner):
								del da_new['nations'][idd]['units'][winner]   
							if da_new['nations'][idd2]['units'].get(ter):
								del da_new['nations'][idd2]['units'][ter]
							da_new['nations'][idd]['units'][orders_dict['movement'][winner]['target']]=unit
							# if da['lands'][ter]['ocupied']['main']!=None:
							#   da_new['nations'][idd]['units'][ter]=unit
							# else:
							#   for c in da['lands'][ter]['ocupied']:
							#     if da['lands'][ter]['ocupied'][c]!=None:
							#       break
							#   da_new['nations'][idd]['units'][ter+'_'+c]=unit
						else:
							print('failed 3', winner)
							orders_dict['movement'][winner]['success']=False
					else:
						print('failed 4', winner)
						orders_dict['movement'][winner]['success']=False
	
				elif ter in orders_dict['movement']:
					if orders_dict['movement'][ter]['target']==winner:
						print('this', maxes[0][1], lands[winner2]['attacks'][ter])
						if maxes[0][1]>lands[winner2]['attacks'][ter]:
						#   da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
						#   da_new[ty1][winner2]['type']=None
							ok=False
							if not coast1 and not coast2:
								if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									idd2=da[ty2][ter2]['ocupied']['main']		
									da_new[ty1][winner2]['ocupied']['main']=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif coast1 and not coast2:
								if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									idd2=da[ty2][ter2]['ocupied']['main']		
									da_new[ty1][winner2]['ocupied'][coast1]=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif not coast1 and coast2:
								if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									da_new[ty1][winner2]['ocupied']['main']=None
									idd2=da[ty2][ter2]['ocupied'][coast2]
									da_new[ty2][ter2]['ocupied'][coast2]=idd
							elif coast1 and coast2:
								if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									da_new[ty1][winner2]['ocupied'][coast1]=None
									idd2=da[ty2][ter2]['ocupied'][coast2]
									da_new[ty2][ter2]['ocupied'][coast2]=idd	      

						
							if ok:
								print('sucess 5', winner)
								orders_dict['movement'][winner]['success']=True
								if winner in orders_dict['convoy_moves']:
									orders_dict['convoy_moves'][winner]['success']=True
								orders_dict['retreats'][ter]={'forbiden': winner, 'idd': idd2, 'unit': da['nations'][idd2]['units'][ter]}
								print('failed 5', ter)
								orders_dict['movement'][ter]['success']=False
								print(idd)								                
								unit=da['nations'][idd]['units'][winner]
								print(unit)
								print(da_new['nations'][idd]['units'])
								if da_new['nations'][idd]['units'].get(winner):
									del da_new['nations'][idd]['units'][winner]
								if da_new['nations'][idd2]['units'].get(ter):
									del da_new['nations'][idd2]['units'][ter]		
								da_new['nations'][idd]['units'][orders_dict['movement'][winner]['target']]=unit
								# if da['lands'][ter]['ocupied']['main']!=None:
								#   da_new['nations'][idd]['units'][ter]=unit
								# else:
								#   for c in da['lands'][ter]['ocupied']:
								#     if da['lands'][ter]['ocupied'][c]!=None:
								#       break
								#   da_new['nations'][idd]['units'][ter+'_'+c]=unit
							else:
								print('failed 6', winner, ter)
								orders_dict['movement'][winner]['success']=False
								orders_dict['movement'][ter]['success']=False
							# print('here1', ter)
						elif maxes[0][1]<lands[winner2]['attacks'][ter]:
						#   da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
						#   da_new[ty1][winner2]['type']=None
							ok=False
							if not coast1 and not coast2:
								if da[ty1][ter2]['ocupied']['main']!=da[ty2][winner2]['ocupied']['main']:
									ok=True
									idd=da[ty1][ter2]['ocupied']['main']
									idd2=da[ty2][winner2]['ocupied']['main']		
									da_new[ty1][ter2]['ocupied']['main']=None
									da_new[ty2][winner2]['ocupied']['main']=idd
							elif coast1 and not coast2:
								if da[ty1][ter2]['ocupied'][coast1] != da[ty2][winner2]['ocupied']['main']:
									ok=True
									idd=da[ty1][ter2]['ocupied'][coast1]
									idd2=da[ty2][winner2]['ocupied']['main']		
									da_new[ty1][ter2]['ocupied'][coast1]=None
									da_new[ty2][winner2]['ocupied']['main']=idd
							elif not coast1 and coast2:
								if da[ty1][ter2]['ocupied']['main'] != da[ty2][winner2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][ter2]['ocupied']['main']
									da_new[ty1][ter2]['ocupied']['main']=None
									idd2=da[ty2][winner2]['ocupied'][coast2]
									da_new[ty2][winner2]['ocupied'][coast2]=idd
							elif coast1 and coast2:
								if da[ty1][ter2]['ocupied'][coast1] != da[ty2][winner2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][ter2]['ocupied'][coast1]
									da_new[ty1][ter2]['ocupied'][coast1]=None
									idd2=da[ty2][winner2]['ocupied'][coast2]
									da_new[ty2][winner2]['ocupied'][coast2]=idd
							if ok:
								print('failed 7', winner)
								orders_dict['movement'][winner]['success']=False
								print('sucess 6', ter)
								orders_dict['movement'][ter]['success']=True
								if ter in orders_dict['convoy_moves']:
									orders_dict['convoy_moves'][ter]['success']=True                
								unit=da['nations'][idd]['units'][ter]
								orders_dict['retreats'][winner]={'forbiden': ter, 'idd': idd2, 'unit': da['nations'][idd2]['units'][winner]}
								if da_new['nations'][idd]['units'].get(ter):
										del da_new['nations'][idd]['units'][ter]
								if da_new['nations'][idd2]['units'].get(winner):
									del da_new['nations'][idd2]['units'][winner]
								da_new['nations'][idd]['units'][orders_dict['movement'][ter]['target']]=unit
								
							else:
								print('failed 8', winner, ter)
								orders_dict['movement'][winner]['success']=False
								orders_dict['movement'][ter]['success']=False
						else:
							print('failed 9', winner, ter)
							orders_dict['movement'][winner]['success']=False
							orders_dict['movement'][ter]['success']=False
	
					elif lands[ter2]['defence']==0:
						if maxes[0][1]>1:
						#   da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
						#   da_new[ty1][winner2]['type']=None
							ok=False
							if not coast1 and not coast2:
								if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									da_new[ty1][winner2]['ocupied']['main']=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif coast1 and not coast2:
								if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									da_new[ty1][winner2]['ocupied'][coast1]=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif not coast1 and coast2:
								if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									da_new[ty1][winner2]['ocupied']['main']=None
									da_new[ty2][ter2]['ocupied'][coast2]=idd
							elif coast1 and coast2:
								if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									da_new[ty1][winner2]['ocupied'][coast1]=None
									da_new[ty2][ter2]['ocupied'][coast2]=idd
							if ok:
								print('sucess 7', winner)
								orders_dict['movement'][winner]['success']=True
								if winner in orders_dict['convoy_moves']:
									orders_dict['convoy_moves'][winner]['success']=True	
								# orders_dict['retreats'][ter]={'forbiden': winner, 'idd': idd2, 'unit': da_new['nations'][idd2]['units'][ter]}
								unit=da['nations'][idd]['units'][winner]
								if da_new['nations'][idd]['units'].get(winner):
										del da_new['nations'][idd]['units'][winner]
								# del da_new['nations'][idd2]['units'][ter]		
								da_new['nations'][idd]['units'][orders_dict['movement'][winner]['target']]=unit
								# if da['lands'][ter]['ocupied']['main']!=None:
								#   da_new['nations'][idd]['units'][ter]=unit
								# else:
								#   for c in da['lands'][ter]['ocupied']:
								#     if da['lands'][ter]['ocupied'][c]!=None:
								#       break
								#   da_new['nations'][idd]['units'][ter+'_'+c]=unit
	
							else:
								print('failed 10', winner)
								# orders_dict['movement'][winner]['success']=False
								unsolved[winner]=orders_dict['movement'][winner]
						elif orders_dict['movement'][ter]['success']==True:
				
						#   da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
						#   da_new[ty1][winner2]['type']=None
							ok=False
							if not coast1 and not coast2:
								# if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									da_new[ty1][winner2]['ocupied']['main']=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif coast1 and not coast2:
								# if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									da_new[ty1][winner2]['ocupied'][coast1]=None
									da_new[ty2][ter2]['ocupied']['main']=idd
							elif not coast1 and coast2:
								# if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied']['main']
									da_new[ty1][winner2]['ocupied']['main']=None
									da_new[ty2][ter2]['ocupied'][coast2]=idd
							elif coast1 and coast2:
								# if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
									ok=True
									idd=da[ty1][winner2]['ocupied'][coast1]
									da_new[ty1][winner2]['ocupied'][coast1]=None
									da_new[ty2][ter2]['ocupied'][coast2]=idd
							if ok:
								print('sucess 8', winner)
								orders_dict['movement'][winner]['success']=True
								if winner in orders_dict['convoy_moves']:
									orders_dict['convoy_moves'][winner]['success']=True		
								unit=da['nations'][idd]['units'][winner]
								if da_new['nations'][idd]['units'].get(winner):
										del da_new['nations'][idd]['units'][winner]
								da_new['nations'][idd]['units'][orders_dict['movement'][winner]['target']]=unit
								# if da['lands'][ter]['ocupied']['main']!=None:
								#   da_new['nations'][idd]['units'][ter]=unit
								# else:
								#   for c in da['lands'][ter]['ocupied']:
								#     if da['lands'][ter]['ocupied'][c]!=None:
								#       break
								#   da_new['nations'][idd]['units'][ter+'_'+c]=unit
							else:
								print('failed 11', winner)
								orders_dict['movement'][winner]['success']=False
						else:
							unsolved[winner]=orders_dict['movement'][winner]
				else:
				#   unit=da[ty1][winner2]['type']
				#   da_new[ty2][ter2]['type']=unit
				#   print(da_new[ty2][ter2]['type'], unit)
				#   da_new[ty1][winner2]['type']=None
					ok=False
					if not coast1 and not coast2:
						print('nono 1')
						if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
							ok=True
							idd=da[ty1][winner2]['ocupied']['main']
							da_new[ty1][winner2]['ocupied']['main']=None
							da_new[ty2][ter2]['ocupied']['main']=idd
					elif coast1 and not coast2:
						print('nono 2')
						if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
							ok=True
							idd=da[ty1][winner2]['ocupied'][coast1]
							da_new[ty1][winner2]['ocupied'][coast1]=None
							da_new[ty2][ter2]['ocupied']['main']=idd
					elif not coast1 and coast2:
						print('nono 3')
						print(winner2, ter2)						
						if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
							ok=True
							idd=da[ty1][winner2]['ocupied']['main']
							da_new[ty1][winner2]['ocupied']['main']=None
							da_new[ty2][ter2]['ocupied'][coast2]=idd
					elif coast1 and coast2:
						print('nono 4')
						if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
							ok=True
							idd=da[ty1][winner2]['ocupied'][coast1]
							da_new[ty1][winner2]['ocupied'][coast1]=None
							da_new[ty2][ter2]['ocupied'][coast2]=idd
					if ok:
						print('sucess 2', winner)
						orders_dict['movement'][winner]['success']=True
						if winner in orders_dict['convoy_moves']:
							orders_dict['convoy_moves'][winner]['success']=True	    
						unit=da['nations'][idd]['units'][winner]
						if da_new['nations'][idd]['units'].get(winner):
								del da_new['nations'][idd]['units'][winner]
						# print(orders_dict)
						da_new['nations'][idd]['units'][orders_dict['movement'][winner]['target']]=unit
						# if da['lands'][ter]['ocupied']['main']!=None:
						#   da_new['nations'][idd]['units'][ter]=unit
						# else:
						#   for c in da['lands'][ter]['ocupied']:
						#     if da['lands'][ter]['ocupied'][c]!=None:
						#       break
						#   da_new['nations'][idd]['units'][ter+'_'+c]=unit
					else:
						print('failed 12', winner)
						orders_dict['movement'][winner]['success']=False
				# else:
				# 	unsolved[winner]=orders_dict['movement'][winner]
					
	
	
	
	print('unsolved', unsolved)
	l1=len(unsolved)
	while len(unsolved)>0:
	
		for ter in unsolved.copy():
			ter1=ter[:3]
			target=unsolved[ter]['target']
			target1=target[:3]
			coast1=None
			coast2=None
			if da['lands'].get(ter1):
				ty1='lands'
				if di['lands'][ter1]['coasts']:
					for i in da['lands'][ter1]['ocupied']:
						if da['lands'][ter1]['ocupied'][i]!=None:
							if i!='main':
								ter=ter1+'_'+i
					coast1=ter[-2:]
			else:
				ty1='seas'
	
			if da['lands'].get(target1):
				ty2='lands'
				if di['lands'][target1]['coasts']:
				#   for i in da['lands'][target1]['ocupied']:
				#     if da['lands'][target1]['ocupied'][i]!=None:
				#       if i!='main':
				#         target=target1+'_'+i
					print('???????????????????       ', target)
				#   coast2=target[-2:]
				print(orders_dict['movement'][ter]['target'])
				coast2=orders_dict['movement'][ter]['target'][-2:]
			else:
				ty2='seas'
	
			# target=orders_dict['movement'][ter]['target']
			if orders_dict['movement'][target]['success']!=None:
				print('idk 0', ter)
				suc=orders_dict['movement'][target]['success']
				orders_dict['movement'][ter]['success']=suc
				if suc:
					print(da[ty1][ter1]['type'], target1)
				#   da_new[ty2][target1]['type']=da[ty1][ter1]['type']
				#   da_new[ty1][ter1]['type']=None
					ok=False
					if not coast1 and not coast2:
						# if da[ty1][ter1]['ocupied']['main']!=da[ty2][target1]['ocupied']['main']:
							ok=True
							idd=da[ty1][ter1]['ocupied']['main']
							da_new[ty1][ter1]['ocupied']['main']=None
							da_new[ty2][target1]['ocupied']['main']=idd
					elif coast1 and not coast2:
						# if da[ty1][ter1]['ocupied'][coast1] != da[ty2][target1]['ocupied']['main']:
							ok=True
							idd=da[ty1][ter1]['ocupied'][coast1]
							da_new[ty1][ter1]['ocupied'][coast1]=None
							da_new[ty2][target1]['ocupied']['main']=idd
					elif not coast1 and coast2:
						# if da[ty1][ter1]['ocupied']['main'] != da[ty2][target1]['ocupied'][coast2]:
							ok=True
							idd=da[ty1][ter1]['ocupied']['main']
							da_new[ty1][ter1]['ocupied']['main']=None
							da_new[ty2][target1]['ocupied'][coast2]=idd
					elif coast1 and coast2:
						# if da[ty1][ter1]['ocupied'][coast1] != da[ty2][target1]['ocupied'][coast2]:
							ok=True
							idd=da[ty1][ter1]['ocupied'][coast1]
							da_new[ty1][ter1]['ocupied'][coast1]=None
							da_new[ty2][target1]['ocupied'][coast2]=idd
					if ok:
						print('sucess 100', ter)
						orders_dict['movement'][ter]['success']=True
						if ter in orders_dict['convoy_moves']:
							orders_dict['convoy_moves'][ter]['success']=True
						unit=da['nations'][idd]['units'][ter]
						# da_new[ty1][]
						print(unit, ter)
						if da_new['nations'][idd]['units'].get(ter):
								del da_new['nations'][idd]['units'][ter]
						da_new['nations'][idd]['units'][target]=unit
	
				unsolved.pop(ter)
		l2=len(unsolved)
		if l2!=l1:
			l1=l2
		else:
			for ter in unsolved:
				winner2=unsolved[ter]['target']
				# da_new[ty2][ter2]['type']=da[ty1][winner2]['type']
				# da_new[ty1][winner2]['type']=None
				ok=False
				if not coast1 and not coast2:
					if da[ty1][winner2]['ocupied']['main']!=da[ty2][ter2]['ocupied']['main']:
						ok=True
						da_new[ty1][winner2]['ocupied']['main']=da[ty2][ter2]['ocupied']['main']
						da_new[ty2][ter2]['ocupied']['main']=None
				elif coast1 and not coast2:
					if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied']['main']:
						ok=True
						da_new[ty1][winner2]['ocupied'][coast1]=da[ty2][ter2]['ocupied'][coast1]
						da_new[ty2][ter2]['ocupied']['main']=None
				elif not coast1 and coast2:
					if da[ty1][winner2]['ocupied']['main'] != da[ty2][ter2]['ocupied'][coast2]:
						ok=True
						da_new[ty1][winner2]['ocupied']['main']=da[ty2][ter2]['ocupied']['main']
						da_new[ty2][ter2]['ocupied'][coast2]=None
				elif coast1 and coast2:
					if da[ty1][winner2]['ocupied'][coast1] != da[ty2][ter2]['ocupied'][coast2]:
						ok=True
						da_new[ty1][winner2]['ocupied'][coast1]=da[ty2][ter2]['ocupied'][coast1]
						da_new[ty2][ter2]['ocupied'][coast2]=None
				if ok:
					print('sucess 1', ter)
					orders_dict['movement'][ter]['success']=True
					if ter in orders_dict['convoy_moves']:
						orders_dict['convoy_moves'][ter]['success']=True	  
				else:
					print('failed 13', ter)
					orders_dict['movement'][ter]['success']=False
			del unsolved
			gc.collect()
			break
		# print('loop end')
		# print(unsolved)
	
	for ter in unknown:
		if orders_dict['movement'][ter]['success']==False:
			orders_dict['retreats'][ter]=unknown[ter]
	del unknown    
	gc.collect()
	
	all_list=list(da['lands'].keys())+list(da['seas'].keys())
	all_units={ter: da_new['nations'][idd]['units'][ter] for idd in da_new['nations'] for ter in da_new['nations'][idd]['units']}	
	for ter in all_list:	
		if all_units.get(ter):
			if da_new['lands'].get(ter):
				da_new['lands'][ter]['type']=all_units[ter]
			else:				      
				da_new['seas'][ter]['type']=all_units[ter]
		else:
			if da_new['lands'].get(ter):
				da_new['lands'][ter]['type']=None
			else:				      
				da_new['seas'][ter]['type']=None  



	for ter in orders_dict['retreats'].copy():
		good=False
		unit=orders_dict['retreats'][ter]['unit']
		forbiden=orders_dict['retreats'][ter]['forbiden']
		if unit=='u':
			for t in di['lands'][ter]['edges_u']:
				for i in da_new['lands'][t]['ocupied']:
					if da_new['lands'][t]['ocupied'][i]!=None:
						break
				else:
					if t!=forbiden and t not in da_new['turn']['clashes']:
						good=True
				if good:
					break
		elif unit=='f':
			# ter2=ter[:3]      
			ter1=ter[:3]
			co=ter[-2:]
			if di['lands'].get(ter1):
				if len(ter)>3:
					for t in di['lands'][ter1]['edges_f'][co]:
						t1=t[:3]
						if di['lands'].get(t1):
							ty='lands'
						else:
							ty='seas'
						for i in da_new[ty][t1]['ocupied']:
							if da_new[ty][t1]['ocupied'][i]==None:
								if t!=forbiden and t not in da_new['turn']['clashes'] and t1 not in da_new['turn']['clashes']:
									good=True
						if good:
							break
				else:
					for t in di['lands'][ter]['edges_f']:
						if di['lands'].get(t):
							ty='lands'
						else:
							ty='seas'
						if da_new[ty][t]['ocupied']['main']==None:
							if t!=forbiden and t not in da_new['turn']['clashes']:
								good=True
						if good:
							break  
			else:
				for t in di['seas'][ter]['edges_f']:
					if di['lands'].get(t):
						ty='lands'
					else:
						ty='seas'
					if da_new[ty][t]['ocupied']['main']==None:
						if t!=forbiden and t not in da_new['turn']['clashes']:
							good=True
					if good:
						break
		if not good:   
			del orders_dict['retreats'][ter]
			
				

	da_new['turn']['retreats']=deepcopy(orders_dict['retreats'])


	for ter in da_new['lands']:		
		if not di['lands'][ter]['sc']:      
			for c in da_new['lands'][ter]['ocupied']:
				idd=da_new['lands'][ter]['ocupied'][c]
				print(ter, idd)			
				if idd!=None:
					idd2=da['lands'][ter]['owner']
					if idd!=idd2:	  
						print(ter, idd, idd2)									
						da_new['lands'][ter]['owner']=idd
						da_new['nations'][idd]['lands'].append(ter)
						if idd2!=None:
								print(idd2, ter)
								print(da_new['nations'][idd2]['lands'])
								da_new['nations'][idd2]['lands'].remove(ter)					
					break
	# print('made here       ', orders_dict)
	for i in da_new['nations']:
		da_new['nations'][i]['orders']={}
	return orders_dict, da_new
	# print(f'{orders_dict['movement']}\n')
	# print(f'{unsolved}\n')
	# print(f'{orders_dict['retreats']}\n')

def get_info_i():
	with open('da.json', 'r') as openfile:

	# Reading from json file
		json_object = json.load(openfile)

	# print(json_object)
	# print(type(json_object))





def find_end(end, current_path, branches, valid_paths):
	new_branches={}
	for sea in branches:
		new_branches[sea]=[]
		# print('----------------------- doing', sea)
		# new_path=current_path+[sea]
		if end in di['seas'][sea]['edges_f']:
			# print('found end in', sea)
			if len(current_path)==0:
				# print('here1')
				valid_paths[sea].append(current_path+[sea])
			else:
				# print('here2')
				valid_paths[current_path[0]].append(current_path+[sea])
		else:
			for new_sea in di['seas'][sea]['edges_f']:
				if new_sea in di['seas'] and new_sea not in current_path and new_sea not in branches:
					new_branches[sea].append(new_sea)
	for sea in new_branches:
		new_branch=new_branches[sea]
		new_path=current_path+[sea]
		# print('new from', sea, new_branches)
		find_end(end, new_path, new_branch, valid_paths)

def filter_valids(valid_paths):
	good=[]
	print(valid_paths, '\n\n')
	valid_paths.sort(key=len)
	print(valid_paths, '\n\n')
	while len(valid_paths)>0:
		vp=valid_paths[:]
		checker=vp[0]
		for ch in vp:
			if ch!=checker:
				for j in checker:
					if j not in ch:
						break
				else:
					valid_paths.pop(valid_paths.index(ch))
		good.append(valid_paths.pop(valid_paths.index(checker)))
	return good




def find_paths(start, end):
	current_path=[]
	branches=[]
	if di['lands'][start]['coasts']:
		sea_list=[]
		for c in di['lands'][start]['edges_f']:
			sea_list+=di['lands'][start]['edges_f'][c]
	else:
		sea_list=di['lands'][start]['edges_f']
	for sea in sea_list:
		if sea in di['seas']:
			branches.append(sea)

	valid_pathsd={x: [] for x in branches}
	find_end(end, current_path, branches, valid_pathsd)

	gg=[]
	for s in valid_pathsd:
		if len(valid_pathsd[s])>0:
			valids=valid_pathsd[s]
			good=filter_valids(valids)
			gg+=good
			print('good', good)

	g=filter_valids(gg)
	return g

def color_land(ter, nim, color):
	x, y=di['lands'][ter]['cords']['colors']['main']
	# print('here 1', type(nim))
	nim=flood_fill_(x, y, nim, color)
	for c in di['lands'][ter]['cords']['colors']['coloring']:
		x, y=c
		# print('here 2', type(nim))
		nim=flood_fill_(x, y, nim, color)
	return nim

def make_image(nim, orders_dict, img_t, da):
	# print('\n\n222', da['lands'], '\n\n')
	# nim2=nim.copy()
	# print('------------------started 1')
	for nation in di['nations']:
		color=tuple(di['nations'][nation]['color'])
		for ter in da['nations'][nation]['lands']:
			# print('here 3', type(nim))
			nim=color_land(ter, nim, color)

	fig = plt.figure(figsize=(1286/96, 1166/96))
	ax = fig.add_subplot(111)
	plt.axis('off')
	font = {
		# 'family' : 'normal',
		'size'   : 8
	}
	plt.rc('font', **font)
	ax.imshow(nim, cmap=plt.cm.gray)

	for i in di['lands']:
		x, y=di['lands'][i]['cords']['name']
		plt.text(x, y, f'{i}')
	for i in di['seas']:
		x, y=di['seas'][i]['cords']['name']
		plt.text(x, y, f'{i.upper()}')

	plt.plot([di['lands'][x]['cords']['sc'][0] for x in di['lands'] if di['lands'][x]['cords']['sc']], [di['lands'][x]['cords']['sc'][1] for x in di['lands'] if di['lands'][x]['cords']['sc']], '*', markersize=8, color='#8a8500', markeredgecolor='black', markeredgewidth=0.5, zorder=8)

	for l in di['lands']:
		coasts=di['lands'][l]['cords']['coasts']
		if coasts:
			for c in coasts:
				# print(coast_name_cords[i][j])
				x, y=coasts[c]['name']
				plt.text(x, y, c)

	for nation in di['nations']:
		color=rgb_to_hex(tuple(di['nations'][nation]['color']))
		# print(da['nations'][nation]['units'])
		for ter1 in da['nations'][nation]['units']:
			co=ter1[-2:]
			ter=ter1[:3]

			if di['lands'].get(ter):
				t='lands'
			else:
				t='seas'
			if da['nations'][nation]['units'][ter1]=='u':
				mark='o'
				pos=di[t][ter]['cords']['unit']
				# print('------------hehe 1')
			else:
				mark='v'
				if len(ter1)!=3:
					pos=di[t][ter]['cords']['coasts'][co]['fleet']
					# print('------------hehe 2')
				else:
					# print('------------hehe 3')
					pos=di[t][ter]['cords']['fleet']
			# print(ter, pos)
			plt.plot(pos[0], pos[1], mark, markersize=10, color=color, markeredgecolor='black', markeredgewidth=2, zorder=9)


	if img_t=='orders':
	# img_t='oders'
		print('went here')
		season=da['turn']['season']
		if season in ['spring', 'autumn']:
			# print('in season')
			# orders_dict, da_new=solve_orders(da)
			# print('par 3', da['lands']['par'])
			# print('pic 3', da['lands']['pic'])
			print('here 2     ', orders_dict)
			# print(orders_dict)
			for ter in orders_dict['convoy_moves']:
				order=orders_dict['convoy_moves'][ter]
				if order['complete']:
					# print('--------------------------------------yesssss 1')
					if order['success']:
						# print('--------------------------------------yesssss 2')
						draw_convoy_attack(ter, order['paths'][0], (24, 32, 255), 1, da)
						draw_convoy_attack_arrow(order['paths'][-1], order['target'], (24, 32, 255), 1, da)
						draw_convoy_attack(order['paths'][-1], order['target'], (24, 32, 255), 1, da)
						for i in range(len(order['paths'])-1):
							sea1=order['paths'][i]
							sea2=order['paths'][i+1]
							# print(sea1, sea2)
							draw_convoy_attack(sea1, sea2, (24, 32, 255), 1, da)
					else:
						# print('--------------------------------------yesssss 3')
						draw_convoy_attack(ter, order['paths'][0], (255, 24, 24), 1, da)
						draw_convoy_attack_arrow(order['paths'][-1], order['target'], (255, 24, 24), 1, da)
						draw_convoy_attack(order['paths'][-1], order['target'], (255, 24, 24), 1, da)
						for i in range(len(order['paths'])-1):							
							sea1=order['paths'][i]
							sea2=order['paths'][i+1]
							# print(sea1, sea2)
							draw_convoy_attack(sea1, sea2, (255, 24, 24), 1, da)
				else:
					draw_attack(ter, order['target'], rgb_to_hex((255, 24, 24)), da)
					#todo make convoys show they convoyed empth

			for ter in orders_dict['convoys']:
				draw_convoy(ter, da)

			for ter in orders_dict['movement']:
				# print(ter, 'in movement')
				# print('1---------------------------------', da['lands'][ter]['type'], ter)
				order=orders_dict['movement'][ter]
				if not order['convoy']:
					if order['success']:
						draw_attack(ter, order['target'], (0, 0, 0), da)
					else:
						draw_attack(ter, order['target'], (255, 24, 24), da)

			for ter in orders_dict['supports']:
				order=orders_dict['supports'][ter]
				if order['cut']:
					draw_support(ter, order['target'], order['helped'], (255, 24, 24), da)
				else:
					if order['empty']:
						draw_support(ter, order['target'], order['helped'], (255, 24, 24), da)
						draw_attack(order['helped'], order['target'], (112, 112, 112), da, alpha=0.3)
					else:
						draw_support(ter, order['target'], order['helped'], (0, 0, 0), da)

			for ter in orders_dict['defends']:
				order=orders_dict['defends'][ter]
				if order['cut']:
					draw_defend(ter, order['helped'], (255, 24, 24), da)
				else:
					if order['empty']:
						draw_defend(ter, order['helped'], (255, 24, 24), da)
					else:
						draw_defend(ter, order['helped'], (0, 0, 0), da)

		elif season in ['winter', 'summer']:
			# orders_dict, da_new=solve_retreats(da)
			# print('par 4', da['lands']['par'])
			# print('pic 4', da['lands']['pic'])    
			
			
			for ter in orders_dict['disbands']:
				if orders_dict['disbands'][ter]['unit']=='f':
					mark='v'
				else:
					mark='o'
				idd=orders_dict['disbands'][ter]['idd']
				color=rgb_to_hex(tuple(di['nations'][idd]['color']))
				draw_retreat(ter, mark, color, da)
				draw_disband_retreat(ter, da)

			for ter in orders_dict['retreats']:
				order=orders_dict['retreats'][ter]
				idd=orders_dict['retreats'][ter]['idd']
				color=rgb_to_hex(tuple(di['nations'][idd]['color']))
				if orders_dict['retreats'][ter]['unit']=='f':
					mark='v'
				else:
					mark='o'
				draw_retreat(ter, mark, color, da)
				if order['success']:
					color2=(0, 0, 0)
				else:
					color2= (255, 24, 24)
				draw_retreat_move(ter, order['target'], color2, da)


		elif season=='build phase':
			# orders_dict, da_new=solve_builds(da)
			for ter in orders_dict['builds']:
				order=orders_dict['builds'][ter]
				if order['unit']=='f':
					mark='v'
				else:
					mark='o'
				draw_build(ter, mark, da)
			for ter in orders_dict['disbands']:
				unit=orders_dict['disbands'][ter]
				# print('order', order)
				# unit=order['unit']
				draw_disband(ter, unit, da)
			
			# print('.............saved 2')
			# plt.savefig(f"turns/{da['turn']['year']}_{da['turn']['season']}_orders.png", dpi=300, bbox_inches='tight', pad_inches=0)
			# plt.clf()
			# print('\n\n111', da['lands'])
			# print('par 5', da['lands']['par'])
			# print('pic 5', da['lands']['pic'])  
			# da_new, msg_t=make_image(nim, False, deepcopy(da_new), msg_t)
			# print('par 6', da['lands']['par'])
			# print('pic 6', da['lands']['pic'])
			# del orders_dict
			# gc.collect()
			# return deepcopy(da_new), msg_t
		
		
	
	# else:
	# img_t='state'
	# msg_t=None
	# da_new=	{}
	else:
		if da['turn']['season'] in ['summer', 'winter']:
			print('here 3   ', orders_dict)			
			for ter in orders_dict['retreats']:
				order=orders_dict['retreats'][ter]
				idd=orders_dict['retreats'][ter]['idd']
				color=rgb_to_hex(tuple(di['nations'][idd]['color']))
				if orders_dict['retreats'][ter]['unit']=='f':
					mark='v'
				else:
					mark='o'
				draw_retreat(ter, mark, color, da)
	# print('.............saved 1')

	plt.savefig(f"turns/{da['turn']['year']}_{da['turn']['season']}_{img_t}.png", dpi=300, bbox_inches='tight', pad_inches=0)
	# da_new=deepcopy(da)
	# print('par 7', da['lands']['par'])
	# print('pic 7', da['lands']['pic'])
	plt.clf()
	del da
	del fig
	del nim
	gc.collect()
	# return deepcopy(da_new), orders_dict, msg_t
	# return msg_t
		
	
	
	# if ords:
		




def solve_retreats(da_new):
	# da_new=deepcopy(da)
	orders_dict={'retreats': {}, 'disbands': {}}
	targeted={}
	for idd in da_new['nations']:
		for ter1 in da_new['nations'][idd]['orders']:
			ter=ter1[:3]
			co=ter1[-2:]
			order=da_new['nations'][idd]['orders'][ter]
			if order['mode']=='r':
				target1=order['target']
				target=target1[:3]
				co2=target1[-2:]
			if order['mode']=='di':
				# del da_new['nations'][idd]['units'][ter]
				# if len(ter1)!=3:
				# 	da_new['lands'][ter]['ocupied'][co]=None
				# else:
				# 	da_new['lands'][ter]['ocupied']['main']=None
				# da_new['lands'][ter]['type']=None
				orders_dict['disbands'][ter]={'unit': order['unit'], 'idd': idd}
			elif order['mode']=='r':
				orders_dict['retreats'][ter]={'target': order['target'], 'success': None, 'idd': idd, 'unit': order['unit']}
				if order['target'] in targeted:
					targeted[order['target']].append(ter)
				else:
					targeted[order['target']]=[ter]
	for tar in targeted:
		if len(targeted[tar])>1:
			for ter in targeted[tar]:
				print('failed 14', ter)
				orders_dict['retreats'][ter]['success']=False
		else:
			print('sucess 3', targeted[tar][0])
			orders_dict['retreats'][targeted[tar][0]]['success']=True
	# print(orders_dict)			
	for ter1 in orders_dict['retreats']:
		idd=orders_dict['retreats'][ter1]['idd']
		target1=orders_dict['retreats'][ter1]['target']
		ter=ter1[:3]
		co=ter1[-2:]
		# order=da['nations'][idd]['orders'][ter]
		# target1=order['target']
		target=target1[:3]
		co2=target1[-2:]
		if orders_dict['retreats'][ter1]['success']:			
			unit=da_new['turn']['retreats'][ter1]['unit']

			# del da_new['turn']['retreats'][ter1]
			da_new['nations'][idd]['units'][target1]=unit

			# if len(ter1)!=3:
			# 	da_new['lands'][ter]['ocupied'][co]=None
			# else:
			# 	da_new['lands'][ter]['ocupied']['main']=None
			if di['lands'].get(target):        
				da_new['lands'][target]['type']=unit
				if len(target1)>3:
					da_new['lands'][target]['ocupied'][co2]=idd
				else:
					da_new['lands'][target]['ocupied']['main']=idd
			else:        
				da_new['seas'][target]['type']=unit
				da_new['seas'][target]['ocupied']['main']=idd

			# da_new['lands'][ter]['type']=None
		# else:
			# del da_new['nations'][idd]['units'][ter1]
			# del da_new['nations'][idd]['units'][target1]

			# if len(ter1)!=3:
			# 	da_new['lands'][ter]['ocupied'][co]=None
			# else:
			# 	da_new['lands'][ter]['ocupied']['main']=None
			# if len(target1)!=3:
			# 	da_new['lands'][target]['ocupied'][co2]=None
			# else:
			# 	da_new['lands'][target]['ocupied']['main']=None

			# da_new['lands'][ter]['type']=None
			# da_new['lands'][target]['ocupied']=None

	if da_new['turn']['season']=='summer':
		sc=False
	else:
		sc=True
	if not sc:
		for ter in da_new['lands']:
			if not di['lands'][ter]['sc']:			
				for c in da_new['lands'][ter]['ocupied']:
					idd=da_new['lands'][ter]['ocupied'][c]
					if idd!=None:
						idd2=da_new['lands'][ter]['owner']
						if idd!=idd2:
							print(ter, idd, idd2)									
							da_new['lands'][ter]['owner']=idd
							da_new['nations'][idd]['lands'].append(ter)
							if idd2!=None:
								da_new['nations'][idd2]['lands'].remove(ter)					
						break
	else:
		for ter in da_new['lands']:		
			for c in da_new['lands'][ter]['ocupied']:
				idd=da_new['lands'][ter]['ocupied'][c]
				print(ter, idd)				
				if idd!=None:
					idd2=da_new['lands'][ter]['owner']
					if idd!=idd2:
						print(ter, idd, idd2)
						if idd!=idd2:
							da_new['lands'][ter]['owner']=idd
							da_new['nations'][idd]['lands'].append(ter)
							da_new['nations'][idd]['sc_lands'].append(ter)					
							if idd2!=None:
								da_new['nations'][idd2]['lands'].remove(ter)
								da_new['nations'][idd2]['sc_lands'].remove(ter)						
						break
	for i in da_new['nations']:
		da_new['nations'][i]['orders']={}
	return orders_dict, da_new



def solve_builds(da_new):
	# da_new=deepcopy(da)
	orders_dict={'builds': {}, 'disbands': {}}
	for idd in da_new['nations']:
		for ter1 in da_new['nations'][idd]['orders']:
			ter=ter1[:3]
			co=ter1[-2:]
			if di['lands'].get(ter):
					ty='lands'
			else:
					ty='seas'
			order=da_new['nations'][idd]['orders'][ter1]
			if order['mode']=='b':
				da_new['nations'][idd]['units'][ter1]=order['unit']
				
				if len(ter1)!=3:
					da_new['lands'][ter]['ocupied'][co]=idd
				else:
					da_new[ty][ter]['ocupied']['main']=idd
				da_new[ty][ter]['type']=order['unit']				
				orders_dict['builds'][ter1]={'unit': order['unit']}
			elif order['mode']=='di':
				del da_new['nations'][idd]['units'][ter1]
				if len(ter1)!=3:
					da_new['lands'][ter]['ocupied'][co]=None
				else:
					da_new[ty][ter]['ocupied']['main']=None
				da_new[ty][ter]['type']=None
				orders_dict['disbands'][ter1]=order['unit']
	for ter in da_new['lands']:
			for c in da_new['lands'][ter]['ocupied']:
				idd=da_new['lands'][ter]['ocupied'][c]
				if idd!=None:
					idd2=da_new['lands'][ter]['owner']
					print(ter, idd, idd2)									
					da_new['lands'][ter]['owner']=idd
					da_new['nations'][idd]['lands'].append(ter)
					if idd2!=None:
						da_new['nations'][idd2]['lands'].remove(ter)					
					break
		
	# print(orders_dict)
	for i in da_new['nations']:
		da_new['nations'][i]['orders']={}
	return orders_dict, da_new


def trigger_(da):
	
	# ords=True
	# print('here 0', type(nim))
	log_msgs=[]
	log_msgs.append(get_log(da))
	first_season=da['turn']['season']
	# season=da['turn']['season']
	if first_season in ['summer', 'winter']:
		orders_dict, da_new=solve_retreats(deepcopy(da))
	elif first_season in ['spring', 'autumn']:
		print('went here   ', first_season)
		orders_dict, da_new=solve_orders(deepcopy(da))
	elif first_season in ['build phase']:
		orders_dict, da_new=solve_builds(deepcopy(da))
	


	img = Image.open("base_map.png")
	nim=np.array(img)
	print('here    ', orders_dict)
	
	make_image(nim, orders_dict, 'orders', da)
	for i in da['nations']:
		da['nations'][i]['orders']={}
	ok=False
	new_season=first_season
	seasons=['spring', 'summer', 'autumn', 'winter', 'build phase']
	while not ok:
		
		ind=seasons.index(new_season)+1
		n=0	
		if ind>4:
			n=1
			ind=0
		new_season=seasons[ind]
		da_new['turn']['season']=new_season
		da_new['turn']['year']+=n
		new_year=da_new['turn']['year']

		print('-----------------------------------', new_season)
		if new_season in ['summer', 'winter']:
			if len(da_new['turn']['retreats'])==0:
				orders_dict, da_new=solve_retreats(da_new)        
				log_msgs.append(get_log(da_new))
			#   chn_id=1122279631781896263	
			#   chn=client.get_channel(chn_id)
				# await log_chn.send(msg_t)
			else:      
				ok=True
		elif new_season=='build phase':
			for n in da['nations']:
				if len(da_new['nations'][n]['units'])!=len(da_new['nations'][n]['sc_lands']):        
					ok=True
					break
			else:
				orders_dict, da_new=solve_builds(da_new)
				log_msgs.append(get_log(da_new))
			#   chn_id=1122279631781896263	
			#   chn=client.get_channel(chn_id)
				# await log_chn.send(msg_t)
		else:
			ok=True
	make_image(nim, orders_dict, 'state', da_new)
	# if season in ['autumn', 'spring']:
	#   orders_dict, da_new=solve_orders(da)
	# elif season in ['winter', 'summer']:
	#   orders_dict, da_new=solve_retreats(da)
	# else:
	#   orders_dict, da_new=solve_builds(da)
	# if make_img:
	#   img = Image.open("base_map.png")
	#   nim=np.array(img)
	#   make_image(nim, orders_dict, mode, da_new)



	
	
	# make_image(nim, False, orders_dict, da_new)
	print(da_new['turn']['retreats'])
	return da_new, log_msgs, new_season, new_year




def get_log(da):
	msg_t=f"...\n\n\n**{da['turn']['year']} {da['turn']['season']}**\n".upper()
	if len([da['nations'][n]['orders'][order] for n in da['nations'] for order in da['nations'][n]['orders']])>0:
		for idd in da['nations']:
			msg_t+=f"\n**{idd[:1].upper()+idd[1:]}**  {di['discord'][idd]['text']}\n"
			msg_s=""
			for ter in da['nations'][idd]['orders']:
				order=da['nations'][idd]['orders'][ter]
				mode=order['mode']
				if mode=='m':
					msg_s+=f"- move {ter} to {order['target']}\n"
				elif mode=='s':
					msg_s+=f"- {ter} support {order['helped']} to {order['target']}\n"
				elif mode=='c':
					msg_s+=f"- {ter} convoy {order['helped']} to {order['target']}\n"
				elif mode=='d':
					msg_s+=f"- {ter} defend {order['helped']}\n"
				elif mode=='r':
					msg_s+=f"- retreat {ter} to {order['target']}\n"
				elif mode=='di':
					msg_s+=f"- disband {ter}\n"
				elif mode=='b':
					msg_s+=f"- build {order['unit']} in {ter}\n"
				elif mode=='h':
					msg_s+=f"- {ter} hold\n"					
			# da['nations'][idd]['orders']={}					
			msg_t+=msg_s
	else:
		msg_t+='No orders' 
	return msg_t



def solve_support_attacked_by_target(orders_dict, ter, target):
	lands={target:{}}
	lands[target]['defence']=1
	lands[target]['attacks']={}
	for i in orders_dict['movement']:
		if orders_dict['movement'][i]['target']==target:
			lands[target]['attacks'][i]=1
	for i in orders_dict['supports']:
		if not orders_dict['supports'][i]['cut'] and lands[target]['attacks'].get(orders_dict['supports'][i]['helped']):
			lands[target]['attacks'][orders_dict['supports'][i]['helped']]+=1
	for i in orders_dict['defends']:
		if orders_dict['defends'][i]['helped']==target:
			if not orders_dict['defends'][i]['cut']:
				print('meowww', target, i)
				lands[target]['defence']+=1
	s=[]
	for i in lands[target]['attacks']:
		s.append((i, lands[target]['attacks'][i]))
	maxes=[]
	m=max(s, key=lambda x: x[1])
	maxes.append(m)
	for i in s:
		if i[1]==m[1] and i!=maxes[0]:
			maxes.append(i)
	print(maxes)
	if len(maxes)>1:
		return False, 1
	if maxes[0][0]!=ter:
		return False, 2
	if maxes[0][1]<=lands[target]['defence']:
		return False, 3
	return True, 0

		

