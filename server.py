import pickle

# Server settings

serverID = 0
serverToken = ""

# Data structures

# Map
mapStatus = {'currentOverworld'   :   -1,
             'currentCombat'      :   -1,
             'pogLocations'       :   []}
             
mapData = {'name'       :   '',
           'size'       :   [0,0],
           'gridSize'   :   64}
           
overworldData = {'name' :   ''}

pogData = {'name'       :   '',
           'playerID'   :   0,
           'loc'        :   [0,0,0]}

maps = []
overworld = []

# Character sheets
charSheet = {'ID'       :   0,
             'name'     :   '',
             'token'    :   '',
             'bio'      :   '',
             'sheet'    :   '',
             'playerID' :   0,
             'str'      :   0,
             'int'      :   0,
             'cun'      :   0,
             'luc'      :   0,
             'bra'      :   0}
             
charList = []

# File IO functions

def saveMaps():
    with open('./data/mapList.pkl', 'wb+') as f:
        pickle.dump(maps, f, pickle.HIGHEST_PROTOCOL)
    with open('./data/overworldList.pkl', 'wb+') as f:
        pickle.dump(overworld, f, pickle.HIGHEST_PROTOCOL)
    with open('./data/mapStatus.pkl', 'wb+') as f:
        pickle.dump(mapStatus, f, pickle.HIGHEST_PROTOCOL)

def loadMaps():
    with open('./data/mapList.pkl', 'rb') as f:
        global maps
        maps = pickle.load(f)
    with open('./data/overworldList.pkl', 'rb') as f:
        global overworld
        overworld = pickle.load(f)
    with open('./data/mapStatus.pkl', 'rb') as f:
        global mapStatus
        mapStatus = pickle.load(f)
        
def saveChars():
    with open('./data/charList.pkl', 'wb+') as f:
        pickle.dump(charList, f, pickle.HIGHEST_PROTOCOL)

def loadChars():
    with open('./data/charList.pkl', 'rb') as f:
        global charList 
        charList = pickle.load(f)
        