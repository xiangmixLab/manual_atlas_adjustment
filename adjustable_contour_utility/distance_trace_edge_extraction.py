import math
import copy

def seedSearch(pointList):
    seeds=[]
    for item in pointList:
        dist2item=[]
        for i in range(len(pointList)):
            dist2item.append(math.sqrt((item[0]-pointList[i][0])**2+(item[1]-pointList[i][1])**2))

        min_index=[i for i in range(len(pointList)) if dist2item[i]<2] # return all minvals
        
        if len(min_index)==2: # itself and the only neighbor
            seeds.append(min_index[0])
    
    return seeds

def distance_tracing(seedIdx,pointListOri,interval):
    # for each point in pointList, reorder them in newList so that each point are next to each other in order (determined by seed selection)
    pointList=copy.deepcopy(pointListOri)
    
    seed=pointList[seedIdx]

    pointList.pop(seedIdx)

    newList=[]
    newList.append(seed)

    newListIdx=[]
    newListIdx.append(seedIdx)

    while len(pointList)>0:
        dist2seed=[]
        for i in range(len(pointList)):
            dist2seed.append(math.sqrt((seed[0]-pointList[i][0])**2+(seed[1]-pointList[i][1])**2))
        
        min_value = min(dist2seed)
        if min_value<10:
            min_index = dist2seed.index(min_value) # if multiple min_value exists, the first one is here
            
            newList.append(pointList[min_index])
            newListIdx.append(pointListOri.index(pointList[min_index]))

            seed=pointList[min_index]
            pointList.pop(min_index)
        else:
            break
        
    # last element chk
    if math.sqrt((newList[len(newList)-2][0]-newList[len(newList)-1][0])**2+(newList[len(newList)-2][1]-newList[len(newList)-1][1])**2)>2:
        newList.pop(len(newList)-1)
        newListIdx.pop(len(newListIdx)-1)


    # downsample utility
    newList1=newList
    newListIdx1=newListIdx
    if interval>1:
        newList1=[newList[i] for i in range(0,len(newList),interval)]
        newListIdx1=[newListIdx[i] for i in range(0,len(newListIdx),interval)]
    
    return newList1, newListIdx1



