#!/usr/bin/env python
# coding: utf-8

# In[1]:

import copy
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import shapes
from pyglet import image
from pyglet import sprite


# In[2]:


def adjustable_contours(all_edges,all_archors,all_archors_mouseSearch,all_archors_idxSearch,all_archors_idxSearch_rev,all_edges_posSearch):
    batch = pyglet.graphics.Batch()

    # utility variables
    items=[]
    selectedEdge=[None]
    selectedPt=[None]

    GUI_line_search=dict()
    GUI_anchor_search=dict()

    counter=0
    for key, value in all_edges.items():
        for i in range(len(value)):
            for j in range(len(value[i])-1):
                items.append(shapes.Line(value[i][j][0], value[i][j][1], value[i][j+1][0], value[i][j+1][1], width=3,batch=batch,color=[0,50,180])) 
                GUI_line_search.update({str(value[i][j]):counter})
                counter=counter+1

    for key, value in all_archors.items():
        for i in range(len(value)):
            for j in range(len(value[i])-1):
                items.append(shapes.Rectangle(value[i][j][0]-4, value[i][j][1]-4, 8, 8, batch=batch,color=[60,50,120]))   
                GUI_anchor_search.update({str(value[i][j]):counter})
                counter=counter+1

    # for key, value in all_archors.items():
    #     for i in range(len(value)):
    #         for j in range(len(value[i])-1):
    #             labels.append(text.Label(str([value[i][j][0], value[i][j][1]]), font_size=10,x=value[i][j][0], y=value[i][j][1]))   

    window = pyglet.window.Window(width=1140, height=800)

    @window.event
    def on_draw():
        window.clear()
        #pic_sprite.draw()
        batch.draw()
    
        print('Redrawing.')

    #  7. key point: drag an archor and move the line
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            #print("[["+str(x)+"  "+str(y)+"]]")
            for i in range(0,82):
                sEdge1=all_archors_mouseSearch.get("["+str(x+int(i/10)-4)+", "+str(y+int(i%10)-4)+"]") 
                
                if sEdge1!=None:
                    #print("found"+"[["+str(x+int(i/10)-4)+"  "+str(y+int(i%10)-4)+"]]")
                    selectedEdge[0]=sEdge1
                    selectedPt[0]="["+str(x+int(i/10)-4)+", "+str(y+int(i%10)-4)+"]"
                    print(selectedEdge[0])
                    break

                    
            
    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        # if on archor pt, 
        if selectedEdge[0]!=None:
            #print("currPoint: "+str(eval(selectedPt[0])))
            curEdge=all_edges.get(selectedEdge[0])
            archorPt=all_archors.get(selectedEdge[0])

            #print("selectedPt: "+selectedPt[0])
            archorIdx=all_archors_idxSearch.get(selectedPt[0])
            
            a1=archorIdx.split()
            a1[2]=str(int(a1[2][0])-1)+str(a1[2][1:])
            archorIdx_num1=a1[0]+' '+a1[1]+' '+a1[2]

            a1=archorIdx.split()
            a1[2]=str(int(a1[2][0])+1)+str(a1[2][1:])
            archorIdx_num2=a1[0]+' '+a1[1]+' '+a1[2]

            neighbor_archor1=all_archors_idxSearch_rev.get(archorIdx_num1)
            neighbor_archor2=all_archors_idxSearch_rev.get(archorIdx_num2)

            # stop here, check the logic below for line update 120821
            all_edges_nArchor1_idx=all_edges_posSearch.get(neighbor_archor1)
            all_edges_pt_idx=all_edges_posSearch.get(selectedPt[0])
            all_edges_nArchor2_idx=all_edges_posSearch.get(neighbor_archor2)

            #print("all_edges_anchors_idx: "+str(all_edges_nArchor1_idx)+" "+str(all_edges_pt_idx)+" "+str(all_edges_nArchor2_idx))

            # modify the line
            selectedPt_1=eval(selectedPt[0])
            selectedPt_1[0]=selectedPt_1[0]+dx
            selectedPt_1[1]=selectedPt_1[1]+dy
            #print(all_edges_pt_idx)
            #print("test1-1")
            neighbor_archor1_1=eval(neighbor_archor1)
            neighbor_archor2_1=eval(neighbor_archor2)
            #print("test1-2")
            curEdgeSelect=int(all_edges_nArchor1_idx[0][0])
            #print("test1-3")
            all_edges_nArchor1_idx_1=int(all_edges_nArchor1_idx[0][2:])
            #print("test1-3-1")
            all_edges_pt_idx_1=int(all_edges_pt_idx[0][2:])
            #print("test1-3-2")
            all_edges_nArchor2_idx_1=int(all_edges_nArchor2_idx[0][2:])
            #print("test1-4")
            curEdge1=copy.deepcopy(curEdge)

            for i in range(all_edges_nArchor1_idx_1+1,all_edges_pt_idx_1):
                a=(float(selectedPt_1[1])-float(neighbor_archor1_1[1]))/(float(selectedPt_1[0])-float(neighbor_archor1_1[0]))
                b=float(selectedPt_1[1])-a*float(selectedPt_1[0])

                curPt=curEdge1[curEdgeSelect][i]
                curPt[1]=a*curPt[0]+b
                curEdge1[curEdgeSelect][i]=curPt
            #print("test1-5")
            for i in range(all_edges_pt_idx_1+1,all_edges_nArchor2_idx_1-1):
                a=(float(selectedPt_1[1])-float(neighbor_archor2_1[1]))/(float(selectedPt_1[0])-float(neighbor_archor2_1[0]))
                b=float(selectedPt_1[1])-a*float(selectedPt_1[0])

                curPt=curEdge1[curEdgeSelect][i]
                curPt[1]=a*curPt[0]+b
                curEdge1[curEdgeSelect][i]=curPt
            
            #print("test2")
            # update datasets
            lineIdx1=GUI_line_search.get(selectedPt[0])
            lineIdx2=lineIdx1-1
            
            items.pop(lineIdx1)
            items.insert(lineIdx1,shapes.Line(selectedPt_1[0], selectedPt_1[1], neighbor_archor2_1[0], neighbor_archor2_1[1], width=3,batch=batch,color=[0,50,180]))
            items.pop(lineIdx2)
            items.insert(lineIdx2,shapes.Line(neighbor_archor1_1[0], neighbor_archor1_1[1], selectedPt_1[0], selectedPt_1[1], width=3,batch=batch,color=[0,50,180]))
            
            #print("test3")
            anchorIdx1=GUI_anchor_search.get(selectedPt[0])
            items.pop(anchorIdx1)
            items.insert(anchorIdx1,shapes.Rectangle(selectedPt_1[0]-4, selectedPt_1[1]-4, 8, 8, batch=batch,color=[60,50,120]))

            #print("test4")
            all_edges.pop(selectedEdge[0])
            all_edges.update({selectedEdge[0]:curEdge1})
            
            #print("test5")
            archorIdx1=eval(archorIdx)
            archorPt[archorIdx1[1]][archorIdx1[2]]=selectedPt_1
            all_archors.pop(selectedEdge[0])
            all_archors.update({selectedEdge[0]:archorPt})
            
            #print("test6")
            all_edges_posSearch.pop(selectedPt[0])
            all_archors_idxSearch.pop(selectedPt[0])
            all_archors_mouseSearch.pop(selectedPt[0])
            GUI_line_search.pop(selectedPt[0])
            GUI_anchor_search.pop(selectedPt[0])
            
            selectedPt[0]=str(selectedPt_1)
            
            #print(selectedPt_1)
            all_archors_idxSearch.update({selectedPt[0]:archorIdx})
            #print("test6-1")
            all_edges_posSearch.update({selectedPt[0]:all_edges_pt_idx})
            #print("test6-2")
            all_archors_mouseSearch.update({selectedPt[0]:selectedEdge[0]})
            #print("test6-3")
            #print([selectedPt[0],lineIdx1])
            GUI_line_search.update({selectedPt[0]:lineIdx1})
            #print("test6-4")
            GUI_anchor_search.update({selectedPt[0]:anchorIdx1})
            #print("test6-5")
            
            #print("test7")
            on_draw()

    pyglet.app.run()

    return all_edges,all_archors,all_archors_mouseSearch,all_archors_idxSearch,all_archors_idxSearch_rev,all_edges_posSearch
        





