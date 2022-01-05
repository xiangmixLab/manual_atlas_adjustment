import copy
from statistics import mean, stdev

def pointList_segment(pointList):
    # suppose distance tracing is finished, check if the pointList can be separated into multiple parts by checking the distance betweenevery neighborhood points, find the outlier
    pointList_seg=[]

    distNei=[]

    for i in range(len(pointList)-1):
        distNei.append(math.sqrt((pointList[i][0]-pointList[i+1][0])**2+(pointList[i][1]-pointList[i+1][1])**2))
    
    maxDis=max(distNei)

    maxIdx=distNei.index(maxDis)
    
    distNeiNoMax=copy.deepcopy(distNei)
    distNeiNoMax.pop(maxIdx)

    meanDis=mean(distNeiNoMax)
    stdDis=stdev(distNeiNoMax)
    

    separationIdx=-1
    if maxDis>meanDis+3*stdDis: # 3 time std, ~99% assume gaussian?
        separationIdx=maxIdx
    
    if separationIdx != -1:
        pointList_seg.append(pointList[0:separationIdx])
        pointList_seg.append(pointList[separationIdx:])