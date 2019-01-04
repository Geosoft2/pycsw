import math
import heapq
from datetime import datetime
import dateutil.parser



'''
Help functions:

    checkValidity:      checks validity for getSimilarityScores inputs

    getDiagonal:        gets diagonal length of bounding box (from entry as dict)

    getInterv:          gets length of temporal interval (from entry as dict)

    getCenter:          calculates center of bounding box

    getAr/getAres:      calculates area of bouunding box on earth surface

'''

def checkValidity(entries, cmp, n, e, d, l, g, t):
    #entries will be checked during iteration in main function
    #cmp
    if cmp is None or cmp["id"] is None or cmp["wkt_geometry"] is None or len(cmp["wkt_geometry"])==0 or cmp["vector"] is None or len(cmp["vector"])==0:
        return False

    #n will be checked inside main function

    #e,d,g,l,t

    if e<0 or e>5 or d<0 or d>5 or l<0 or l>5 or g<0 or g>5 or t<0 or t>5:
        return False


    return True


def ConvertToRadian(input):
    return input * math.pi/ 180


#Calculates diagonal of Bounding Box by use of Haversine Formula


# Checken, ob floats etc richtig
def getDiagonal(entry):
    lon1 = entry["wkt_geometry"][2]
    lon2 = entry["wkt_geometry"][3]
    lat2 = entry["wkt_geometry"][1]
    lat1 = entry["wkt_geometry"][0]

    return gDiag(lat1,lat2,lon1,lon2)

def gDiag(lat1,lat2,lon1,lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(ConvertToRadian, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371.0 
    d = c * r
    if dlon == 0 and dlat == 0:
        return 0.01
    return d


#Get length of temporal interval
def getInterv(entry):
    t1 = entry[0]
    t2 = entry[1]
    frmt = "%Y-%m-%dT%H:%M:%S%Z" 
    tdelta = datetime.strptime(t2, frmt) - datetime.strptime(t1, frmt)
    return tdelta

#Calculates center of bbox
def getCenter(entry):
    minLon=entry["wkt_geometry"][2]
    maxLon=entry["wkt_geometry"][3]
    minLat=entry["wkt_geometry"][0]
    maxLat=entry["wkt_geometry"][1]
    lon = (minLon+maxLon)/2
    lat = (minLat+maxLat)/2
    center = [lon,lat]
    return center



#output in m²
def getArea(coordinates):
    area = 0

    if (len(coordinates)>2):
        i=0
        p1Lon = coordinates[i+2]
        p1Lat = coordinates[i]
        p2Lon = coordinates[i+3]
        p2Lat = coordinates[i+1]
        area += ConvertToRadian(p2Lon - p1Lon) * (2 + math.sin(ConvertToRadian(p1Lat)) + math.sin(ConvertToRadian(p2Lat)))

        area = area * 6378137 * 6378137 / 2
    

    return abs(area)


#
def getAr(points):
    if (points[0]==points[1]) or (points[2]==points[3]):
        return 0
    return getArea(points)


#checks whether corner points of rectangle B are in rectangle A
def pointsInBbox(pointsA, pointsB):
    points = [[pointsB[1],pointsB[2]], [pointsB[1],pointsB[3]], [pointsB[0],pointsB[2]], [pointsB[0],pointsB[3]]]

    minLat=pointsA[0]
    maxLat=pointsA[1]
    minLon=pointsA[2]
    maxLon=pointsA[3]

    i=0
    res = [0,0,0,0]

    for x in points:
        if (minLon<=x[1] and x[1]<=maxLon and minLat<=x[0] and x[0]<=maxLat):
            res[i]=1
        i=i+1

    return res    


'''
Extent Similarity: 

    getGeoExtSim:       compares geographic extent by comparing diagonal lengths for two entries given as dicts

    getTempExtSim:      compares temporal extent by comparing temporal interval lengths for two entries given as dicts


'''


# Similarity of geographical extent
def getGeoExtSim(entryA, entryB):
    diagonalA=float(getDiagonal(entryA))
    diagonalB=float(getDiagonal(entryB))
    minV = min(diagonalA, diagonalB)
    maxV = max(diagonalA, diagonalB)
    sim = float(minV/maxV)
    return sim



#Similarity of temporal extent
def getTempExtSim(entryA,entryB):
    extA = getInterv(entryA["time"]).total_seconds()
    extB = getInterv(entryB["time"]).total_seconds()

    if extA==0:
        extA=1
    if extB==0:
        extB=1
    minV = min(extA, extB)
    maxV = max(extA, extB)
    sim = float(minV/maxV)
    return sim


'''
Location Similarity

    Intersection Similarity

        getInterGeoSim:         calculates ratio between intersection of both bounding boxes and first entry, 0 if disjunct, given two entries as dicts

        getInterTempSim:        calculates ratio between intersection of both entries on timeline and first entry, 0 is disjunct, given two entries as dicts

    Center Similarity:

        getCentGeoSim:          calculates difference between centers of bounding boxes of two entries, given as dicts, and calculates ratio to absolute maximum (half the earth's circumference)        

        getCentTempSim:         calculates difference between centers of temporal intervals of two entries, given as dicts, and calculates ratio to absolute max (to be determined)

'''

#####################################################################
####### Relation of absolute positions in coordinate systems ########
#####################################################################


def getCenterGeoSim(entryA, entryB):
    #centerA= getCenter(entryA)
    #centerB= getCenter(entryB)
    diagonal = float(getDiagonal([[],[],[entryA[1], entryB[1]]]))
    circumf = 20038
    sim = diagonal/circumf
    return sim

def getCenterTempSim(entryA, entryB):
    frmt = "%Y-%m-%dT%H:%M:%S%Z" 
    if entryA["time"][0]==entryA["time"][1]:
        centerA=entryA["time"][0]
    else: 
        centerA=datetime.strptime(entryA["time"][0],frmt)+(getInterv(entryA["time"])/2)
    if entryB["time"][0]==entryB["time"][1]:
        centerB=entryB["time"][0]
    else: 
        centerB=datetime.strptime(entryB["time"][0],frmt)+(getInterv(entryB["time"])/2)

    tdelta = centerA-centerB
    tdelta = tdelta.total_seconds

    max = datetime.timedelta(days=365000).total_seconds

    return tdelta/max


#########################################################################
########### Intersections ###############################################
#########################################################################


'''
Rectangle: (simplified, in reality and also in function the rectangle is on the earth surface and therefor (simplified) on a sphere)
________________
|A            B| A (MinLon,MaxLat)
|              | B (MaxLon,MaxLat)
|              | C (MinLon,MinLat)
|              | D (MaxLon,MaxLat)
|C            D|
|______________|

'''

# Calculate intersection area of both bounding boxes
def getInterGeoSim(entryA,entryB):
    minLatA=entryA["wkt_geometry"][0]
    maxLatA=entryA["wkt_geometry"][1]
    minLonA=entryA["wkt_geometry"][2]
    maxLonA=entryA["wkt_geometry"][3]
    minLatB=entryB["wkt_geometry"][0]
    maxLatB=entryB["wkt_geometry"][1]
    minLonB=entryB["wkt_geometry"][2]
    maxLonB=entryB["wkt_geometry"][3]
    
    #disjunct?
    if minLonA > maxLonB or maxLonA < minLonB or maxLatA < minLatB or minLatA > maxLonB:
        return 0
    
    '''
    Ich habe durch die Anpassung jetzt - meiner Ansicht nach - den Fall A und B sind beide Punkte/Linien
    und überlagern sich und den Fall A ist <2-dimensional und B nicht 
    '''
    #A in B 
    if minLonA >= minLonB and maxLonA <= maxLonB and minLonA >= minLonB and maxLonA <= maxLonB:
        return 1

    areaA = getAr(entryA["wkt_geometry"])

    #how many points of B in A?
    points = pointsInBbox(entryA["wkt_geometry"], entryB["wkt_geometry"])

    minLat=minLatA
    minLon=minLonA
    maxLat=maxLatA
    maxLon=maxLonA

    if points[0]==1:
        minLon=minLonB
        maxLat=maxLatB
    
    if points[1]==1:
        maxLat=maxLatB
        maxLon=maxLonB
    
    if points[2]==1:
        minLat=minLatB
        minLon=minLonB

    if points[3]==1:
        minLat=minLatB
        maxLon=maxLonB
    
    #If only points of B are in A, but not of A in B
    elif points[0]==0 and points[1]==0 and points[2]==0:
        points = pointsInBbox(entryB["wkt_geometry"], entryA["wkt_geometry"])
        unchanged = True
        
        if points[0]==1:
            maxLon=maxLonB
            minLat=minLatB
            unchanged = False
    
        if points[1]==1:
            minLat=minLatB
            minLon=minLonB
            unchanged = False
    
        if points[2]==1:
            maxLat=maxLatB
            maxLon=maxLonB
            unchanged = False

        if points[3]==1:
            maxLat=maxLatB
            minLon=minLonB
            unchanged = False
        
        '''
        Fall:
                ______
                |.....|
                |.....|
            ____|_____|___________
            |...|.....|..........|
            |...|.....|..........|
            |___|_____|__________|
                |.....|
                |_____|
    
        '''
        if unchanged:
            if minLatA<minLatB and maxLatA>maxLatB:
                maxLat=maxLatB
                minLat=minLatB
                minLon=minLonA
                maxLon=maxLonA
            else:
                maxLat=maxLatA
                minLat=minLatA
                minLon=minLonB
                maxLon=maxLonB
    intersecarea=getAr([minLat,maxLat,minLon,maxLon])

    # if areaA is 0, A is either a point or a line. If it is a point, both cases (in B or outside B) are covered including return value above
    # if A is a line and it is not entirely in B, the insersection area must still be 0:
    if intersecarea == 0:
        # Wenn A eine Linie ist, länge der geschnittenen Linie mit Länge der Gesamtlinie vergleichen
        if areaA==0:
            line = gDiag(minLat,maxLat,minLon,maxLon)
            lineA = getDiagonal(entryA)
            return float (line/lineA) 
    return float(intersecarea/areaA)




def getInterTempSim(entryA,entryB):
    #Startwerte der Intervalle von A und B
    startA = datetime.strptime(entryA["time"][0])
    endA = datetime.strptime(entryA["time"][1])
    startB = datetime.strptime(entryB["time"][0])
    endB = datetime.strptime(entryB["time"][1])

    lengthA=getInterv(entryA["time"]).total_seconds

    #disjunkt
    if startA>endB or startB>endA:
        return 0
        
    elif startA>startB:
        #A in B
        if endA<endB:
            return 1
        #Schnitt, B beginnt vor A
        else:
            interv = getInterv([startA,endB])
    #Schnitt, A beginnt vor B
    elif startB>startA:
        #B in A
        if endB<endA:
            interv = getInterv(entryB["time"]).total_seconds
        else:
            interv = getInterv([startB,endA]).total_seconds
    
    res = interv/lengthA
    return res


'''
Datatype Similarity 

    getGeoDatSim:       compares datatype of geographic information, given two entries as dicts

    getTempDatSim:      compares datatype of temporal information, given two entries as dicts


'''
def getGeoDatSim(entryA,entryB):
    if entryA["raster"]:
        if entryB["raster"]:
            return 1
        else:
            return 0
    if entryB["raster"]:
        return 0
    if len(entryA["vector"])>=3:
        if len(entryB["vector"])>=3:
            return 1
        else:
            return 0.8
    elif len(entryA["vector"])==len(entryB["vector"]):
        return 1
    else:
        return 0.8
    

def getTempDatSim(entryA,entryB):
    if entryA["time"][0]==entryA["time"][1]:
        if entryB["time"][0]==entryB["time"][1]:
            return 1
        else:
            return 0
    elif entryB["time"][0]==entryB["time"][1]:
        return 0
    else:
        return 1



'''
getIndSim:          combines Geo and Temp Similarites for selected criterium c while taking into consideration weights for geographic and temporal similarity
                    c=0 for Similarity of extent
                    c=1 for Similarity of location
                    c=2 for Similarity of datatype
'''
def getIndSim(entryA, entryB, g, t, c):
    if c==0:
        geoSim = getGeoExtSim(entryA,entryB)
        tempSim = getTempExtSim(entryA,entryB)
    if c==1:
        geoInter = getInterGeoSim(entryA,entryB)
        tempInter = getInterTempSim(entryA,entryB)
        geoLoc = getCenterGeoSim(entryA,entryB)
        tempLoc = getCenterTempSim(entryA,entryB)

        geoSim = 0.6*geoInter + 0.4*geoLoc
        tempSim = 0.6*tempInter + 0.4*tempLoc
    if c==2:
        geoSim = getGeoDatSim(entryA,entryB)
        tempSim = getTempDatSim(entryA,entryB)
    else:
        geoSim = 0
        tempSim = 0
    rel = g/(g+t)
    sim = rel*geoSim + (1-rel)*tempSim

    return sim 


def getSimScoreTotal(entryA, entryB, g, t, e, d, l):
    dSim = getIndSim(entryA, entryB, g, t, 2)
    lSim = getIndSim(entryA, entryB, g, t, 1)
    eSim = getIndSim(entryA, entryB, g, t, 0)

    simScore = 0.999*(e*eSim+l*lSim+d*dSim)

    return simScore


'''
getSimilarityScore: Berechnet den SimilarityScore
        entries: Expects a list of entries (dictionaries), where each dict represents one entry of the repository.

                entry:      {
                                "id" : idOfTheEntry,
                                "wkt_geometry" : [minLat,maxLat,minLon,maxLon],
                                "vector" : [[x,y],[x,y]...],
                                "time" : [start, end],
                                "raster"  : bool
                            }   

        cmp is an entry and therefor the same format
        n : number of similar records to be retrieved
        t : weight temporal similarity
        g : weight geographic similarity
        d : weight of datatype similarity 
        e : weight of extent similarity 
        l : weight of location similarity
'''

def getSimilarRecords(entries, cmp, n, e, d, l, g, t):
    
    if checkValidity(entries, cmp, n, e, d, l, g, t) is False:
        return False

    if n>len(entries):
        n=len(entries)

    records = []

    i=0

    while i < n:
        heapq.heappush(records, [entries[i]["id"], getSimScoreTotal(cmp, entries[i], g, t, e, d, l)])
        i=i+1
    
    while i < len(entries):
        min = heapq.heappop(records)
        currscore = getSimScoreTotal(cmp, entries[i], g, t, e, d, l)
        if min[1]<currscore:
            heapq.heappush(records, [entries[i]["id"], getSimScoreTotal(cmp, entries[i], g, t, e, d, l)])
        else:
            heapq.heappush(records, min)
        i=i+1
    
    output=sorted(records, key= lambda x: x[1])

    return output


# du brauchst noch eine weitere Obermethode, die dann diese Methode aufruft, 
# da die einzelnen Parameter noch aus der Konstanten-Datei gelesen werden müssen. 
# Als Übergabe dafür, zu welchem Element similarRecords gesucht werde,n ist denke ich die uuid sinnvoll.
# Als Rückgabewert wäre dann ein Array da [[uuid, simscore],[uuid, simscore],[uuid, simscore],...]
# Dann können wir das gut in die API übernehmen.
