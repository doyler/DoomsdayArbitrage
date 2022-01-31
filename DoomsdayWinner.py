from concurrent.futures.thread import ThreadPoolExecutor
from dotenv import load_dotenv
import json
import os
import requests
import sys
from web3 import Web3

# Get Environment Variables
load_dotenv()
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
# Can also use Infura, but Alchemy is slightly better at the free tier
WEB3_URL = os.getenv('ALCHEMY_URL')

ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&apikey=%s&action=getabi&address='%(ETHERSCAN_API_KEY)

# Setting up the HTTP requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Accept': 'application/json',
    'referer': 'https://api.opensea.io/api/v1/assets'
}
session = requests.Session()
session.headers.update(headers)

# Setting up web3 stuff
web3 = Web3(Web3.HTTPProvider(WEB3_URL))

# Doomsday Contract - https://etherscan.io/address/0xd6e382aa7a09fc4a09c2fb99cfce6a429985e65d#code
DOOMSDAY_ADDRESS = '0xd6e382aa7a09fc4a09c2fb99cfce6a429985e65d'

abi_doomsday_contract = requests.get('%s%s'%(ABI_ENDPOINT, DOOMSDAY_ADDRESS)).json()['result']
address_doomsday = Web3.toChecksumAddress(DOOMSDAY_ADDRESS)
doomsday_contract = web3.eth.contract(address=address_doomsday, abi=abi_doomsday_contract)

# Don't change this, definitely breaks everything!
doyler_address = '0xeD19c8970c7BE64f5AC3f4beBFDDFd571861c3b7'

# Original cost, used to calculate reinforcements
MINT_COST = 0.04

# This was the max count when the game began
cityCount = 1354
# (0.04 * x * .5) - 0.269940799517571385 + (39.55 * .9) = 62.405059200482428615

# OS Purchase with 2 priority and 165 gwei
GAS_EST = 0.04825

# Floor as of 1/20 @ 6:45p EST was 0.1
FLOOR = 0

# This list was generated on 20 January, but you can add to it using the cityRemains output
"""
remainingCities = [1, 2, 4, 10, 13, 11, 20, 23, 17, 19, 16, 25, 27, 34, 38, 37, 39, 36, 42, 41, 46, 50, 43, 58, 49, 56, 61, 64, 60, 66, 65, 72, 76, 74, 69, 79, 75, 83, 80, 96, 85, 92, 102, 98, 105, 110, 115, 130, 122, 121, 109, 129, 135, 139, 124, 134, 138, 142, 143, 145, 127, 147, 146, 165, 150, 156, 158, 160, 169, 172, 171, 174, 177, 164, 181, 162, 166, 167, 185, 187, 189, 191, 195, 194, 206, 204, 205, 208, 200, 213, 212, 209, 207, 214, 217, 215, 218, 221, 223, 227, 232, 230, 234, 233, 238, 231, 240, 239, 243, 242, 244, 246, 249, 254, 260, 262, 261, 265, 268, 269, 266, 272, 267, 273, 279, 274, 288, 300, 297, 293, 304, 308, 313, 322, 316, 317, 310, 332, 329, 335, 333, 318, 342, 344, 350, 347, 349, 351, 361, 362, 363, 370, 352, 369, 356, 378, 377, 380, 392, 388, 386, 387, 389, 397, 399, 391, 413, 417, 419, 425, 427, 429, 426, 430, 421, 438, 439, 440, 445, 437, 446, 396, 448, 449, 434, 447, 443, 450, 452, 453, 451, 455, 461, 462, 483, 482, 479, 481, 463, 475, 472, 464, 485, 492, 488, 499, 489, 486, 493, 509, 511, 514, 500, 515, 497, 502, 505, 491, 516, 501, 504, 518, 519, 520, 525, 527, 534, 528, 524, 541, 550, 542, 530, 522, 545, 547, 538, 557, 566, 554, 553, 565, 576, 574, 578, 577, 581, 582, 583, 580, 584, 563, 587, 590, 597, 598, 599, 603, 610, 608, 605, 607, 602, 612, 615, 617, 613, 623, 622, 626, 634, 631, 635, 629, 633, 640, 639, 641, 642, 646, 648, 655, 657, 653, 660, 663, 659, 666, 673, 672, 678, 679, 682, 692, 690, 700, 694, 696, 683, 698, 705, 704, 715, 711, 703, 702, 730, 731, 717, 713, 716, 719, 726, 736, 740, 742, 758, 759, 760, 764, 754, 755, 756, 768, 770, 762, 771, 746, 772, 776, 795, 791, 786, 801, 800, 804, 806, 803, 807, 810, 808, 815, 813, 793, 818, 820, 824, 826, 831, 841, 839, 844, 845, 847, 846, 849, 850, 861, 853, 852, 864, 854, 860, 855, 857, 859, 872, 878, 882, 881, 863, 858, 887, 909, 905, 904, 907, 923, 915, 900, 903, 908, 927, 930, 931, 935, 934, 936, 926, 933, 942, 945, 939, 943, 947, 941, 940, 918, 949, 950, 952, 964, 957, 956, 962, 961, 968, 970, 972, 973, 980, 976, 984, 983, 988, 981, 967, 986, 959, 991, 987, 995, 1000, 999, 1003, 998, 1010, 1017, 1016, 1015, 1023, 1005, 1018, 1024, 1020, 1013, 1037, 1027, 1019, 1038, 1028, 1046, 1049, 1054, 1040, 1053, 1055, 1043, 1039, 1036, 1060, 1066, 1065, 1059, 1071, 1070, 1067, 1078, 1062, 1074, 1068, 1080, 1081, 1082, 1083, 1076, 1073, 1096, 1086, 1087, 1089, 1095, 1092, 1090, 1084, 1101, 1104, 1108, 1116, 1098, 1099, 1112, 1114, 1121, 1122, 1124, 1127, 1120, 1132, 1123, 1109, 1129, 1126, 1136, 1141, 1140, 1150, 1133, 1154, 1161, 1156, 1157, 1159, 1155, 1166, 1151, 1148, 1171, 1170, 1174, 1178, 1179, 1164, 1176, 1184, 1183, 1190, 1191, 1187, 1199, 1207, 1208, 1221, 1223, 1225, 1220, 1224, 1226, 1213, 1236, 1238, 1240, 1232, 1246, 1231, 1245, 1243, 1250, 1248, 1244, 1233, 1252, 1253, 1254, 1263, 1267, 1262, 1258, 1264, 1259, 1269, 1249, 1273, 1257, 1275, 1278, 1276, 1280, 1284, 1255, 1260, 1285, 1287, 1288, 1289, 1290, 1292, 1316, 1311, 1312, 1310, 1309, 1314, 1305, 1313, 1330, 1326, 1331, 1327, 1323, 1325, 1335, 1343, 1342, 1345, 1348, 1352, 1351, 1349, 1334, 1339, 1336, 1337, 1354]
"""
remainingCities = [2, 66, 83, 122, 129, 130, 147, 162, 165, 189, 194, 207, 212, 213, 214, 217, 227, 243, 288, 333, 370, 399, 434, 453, 448, 446, 463, 489, 485, 502, 511, 515, 519, 518, 524, 530, 538, 545, 547, 557, 574, 580, 581, 587, 590, 599, 602, 617, 607, 623, 622, 631, 635, 629, 641, 660, 663, 673, 679, 690, 704, 702, 692, 705, 736, 730, 758, 791, 800, 807, 854, 850, 845, 849, 878, 908, 918, 923, 939, 947, 949, 957, 968, 981, 987, 998, 1015, 1017, 1036, 1043, 1027, 1059, 1067, 1071, 1065, 1126, 1120, 1140, 1164, 1161, 1225, 1224, 1236, 1240, 1243, 1248, 1245, 1263, 1269, 1264, 1287, 1289, 1278, 1305, 1334, 1330, 1352, 1345]
destroyedCities = []

cityCosts = {}
evacPrizes = {}
tokenHP = {}

def getFloor():
    opensea_url = "https://api.opensea.io/collection/doomsday-nft"
    
    response = session.get(opensea_url)
    if response.status_code == 200:
        data = response.json()
        price = float(data['collection']['stats']['floor_price'])
        global FLOOR
        FLOOR = price
    else:
        print(response.text)
        #print(response.status_code)

def cityRemains(tokenID):
    try:
        remains = doomsday_contract.functions.ownerOf(tokenID).call()
    except:
        destroyedCities.append(tokenID)
        remainingCities.remove(tokenID)
        print("REMOVE: " + str(tokenID))
    else:
        remainingCities.append(tokenID)
        print("ADD: " + str(tokenID))

def getTotalSupply():
    total_supply = doomsday_contract.functions.totalSupply().call()
    return total_supply

def getCurrentPrize():
    current_prize = doomsday_contract.functions.currentPrize().call()
    return (current_prize / (10.0 ** 18.0))
    
def getEvacuatedFunds():
    evacuated_funds = doomsday_contract.functions.evacuatedFunds().call()
    return (evacuated_funds / (10.0 ** 18.0))
    
def getCurrentEvacPrize(totalSupply, tokenID):
    evac_rebate = doomsday_contract.functions.getEvacuationRebate(tokenID).call()
    evac_rebate = (evac_rebate / (10.0 ** 18.0))
    
    fromPool = ((MINT_COST * cityCount * 0.5) - getEvacuatedFunds()) / totalSupply / 2
    
    toWithdraw = fromPool + evac_rebate
    return toWithdraw

def getCost(tokenID):
    opensea_url = "https://api.opensea.io/api/v1/asset/0xd6e382aa7a09fc4a09c2fb99cfce6a429985e65d/"
    
    response = session.get(opensea_url + str(tokenID))
    if response.status_code == 200:
        data = response.json()
        if len(data['orders']) > 0:
            price = float(data['orders'][0]['current_price']) / (10.0 ** 18.0)
            return price
    else:
        print(response.text)
        #print(response.status_code)
        
def getStructureHP(tokenID):
    structure = doomsday_contract.functions.getStructuralData(tokenID).call()
    
    reinf = structure[0]
    damage = structure[1]
    return (reinf-damage)
        
def populateCost(tokenID):
    cost = getCost(tokenID)
    
    if (cost is not None) and (cost > 0):
        cityCosts[tokenID] = cost
        
def populateEvacPrizes(totalSupply, tokenID):
    prize = getCurrentEvacPrize(totalSupply, tokenID)
    
    if (prize is not None) and (prize > 0):
        evacPrizes[tokenID] = prize

total_supply = getTotalSupply()
current_prize = getCurrentPrize()
base_ev = current_prize / total_supply

if len(remainingCities) == 0:
    processes = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(0, cityCount + 2):
            processes.append(executor.submit(cityRemains, i))

    print(remainingCities)
    
if total_supply != len(remainingCities):
    for city in remainingCities:
        cityRemains(city)
        
print()

print("Total Supply (bunkers remaining) = " + str(total_supply))
print()

print("Current Prize: " + str(current_prize))
print()

print("Base EV: " + str(base_ev) + " ($" + str(base_ev * 3183) + ")")
print()

getFloor()
print("Current floor = " + str(FLOOR))
print()

for city in remainingCities:
    populateCost(city)
    populateEvacPrizes(total_supply, city)
    tokenHP[city] = getStructureHP(city)
    
for buyable in cityCosts:
    if evacPrizes[buyable] > cityCosts[buyable]:
        print("POSSIBLE evac arbitrage for Token #" + str(buyable) + " (" + str(evacPrizes[buyable] - cityCosts[buyable]) + " eth)")
        print()
    elif base_ev > (cityCosts[buyable] + GAS_EST):
        print("POSSIBLE raw value arbitrage for Token #" + str(buyable) + " (" + str(base_ev - (cityCosts[buyable] + GAS_EST)) + " eth)")
        print()
    elif (base_ev + (tokenHP[buyable] * FLOOR)) > cityCosts[buyable]:
        print("POSSIBLE HP arbitrage for Token #" + str(buyable) + " (" + str((base_ev + (tokenHP[buyable] * FLOOR)) - cityCosts[buyable]) + ")")
        print()
        
print("Doyler, the broke dev who wrote this, accepts donations here: " + str(doyler_address))
print()        