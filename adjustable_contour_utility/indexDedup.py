# index dedup

def indexDedup(idxList):

    # two pointers
    i=0 # i represent the rightmost letter that has been processed
    j=0

    while j<len(idxList):
        if j==0 or idxList[j]!=idxList[i]:
            idxList[i]=idxList[j]
            i=i+1
            j=j+1
        elif idxList[j]==idxList[i]:
            while (j<len(idxList)) and (idxList[j]==idxList[i]):
                j=j+1
            
            idxList=replaceIdx(idxList,i,j)
        
    return idxList

def replaceIdx(idxList,i,j):
    for p in range(i,j):
        idxList[p]=idxList[i]+p
    
    return idxList