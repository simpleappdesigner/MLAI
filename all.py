import numpy as np
def get_row_col_of_value(df,value):
    dfn = df.to_numpy()
    row=np.where(dfn == value)[0][0]
    col=np.where(dfn == value)[1][0]
    return row,col

import pandas as pd
from nodeInMaze import Node
class Environment:
    def __init__(self,maze_df:pd.DataFrame) -> None:
        self._maze=maze_df
        self._height=self._maze.shape[0] #max row-1
        self._width=self._maze.shape[1] # max col-1
    

    def __str__(self) -> str:
        return f"Height:{self._height}, Width:{self._width}"
    
    def __repr__(self) -> str:
        return f"Height:{self._height}, Width:{self._width}"

    @property
    def height(self):
        return self._height
    
    @property
    def width(self):
        return self._width

    def get_node_value(self,node):
        row,col=node.get_location()
        try:
            return self._maze.loc[row,col]
        except:
            print(f"NF:{node}")
            return "NF"

    #get the direction
    # direction - east, west , north ,south
    def get_direction(self,cur_node,dest_node):
        cur_x,cur_y=cur_node.get_location()
        dest_x,dest_y=dest_node.get_location()

        # current and destination are same
        if cur_x == dest_x and cur_y == dest_y:
            return "stay"
    
        # move east or west
        if cur_y == dest_y:
            if dest_x > cur_x:
                return 'north'
            else:

                return 'south'

        #move north or south
        if dest_x == cur_x:
            if dest_y > cur_y:
                return 'east'
            else:
                return 'west'


    def get_neighbours(self,node):
        row,col=node.get_location()
        neighbours={}
        if row > (self._height-1) or row < 0 or col >  (self._width -1) or col < 0:
            raise Exception(f"Node is not correct for row:{row} or col:{col} vs {self._maze.shape}")
        
        # find the south node
        if row == self._height-1:
            south=None
        else:
            south = Node(row+1,col)

        # find north node
        if row == 0:
            north=None
        else:
            north=Node(row-1,col)
        
        # find east node
        if col == self._width-1:
            east=None
        else:
            east=Node(row,col+1 )

        #find west node
        if col == 0:
            west = None
        else:
            west=Node(row,col -1)
        if east:
            neighbours['east']=east
            
        if west:
            neighbours['west']=west
        
        if north:
            neighbours['north']=north
        if south:
            neighbours['south']=south
        
        return neighbours

        #return {"east":east,"west":west,"north":north,"south":south}
class Node:
    def __init__(self,row,col) -> None:
        self._row=row
        self._col=col
        self._prev_node=None
    
    #set up node previous node
    def set_prev_node(self,node):
        self._prev_node=node

    def get_prev_node(self):
        return self._prev_node
        
    def __str__(self) -> str:
        return f"row:{self._row},col:{self._col}"
        
    def get_location(self):
        return self._row,self._col
    
    def __eq__(self, other) -> bool:
        return self._row == other._row and self._col == other._col
from mazeEnv import *
from mazeUtils import get_row_col_of_value
from nodeInMaze import Node
import dataframe_image as dfi
import queue


#get the path
def get_the_path(node):
    node_path_from_goal_to_start=[]
    working_node=node
    while True:
        if working_node.get_prev_node():
            node_path_from_goal_to_start.append(working_node)
            working_node=working_node.get_prev_node()
        else:
            node_path_from_goal_to_start.append(working_node) # add start node to list
            print("start found")
            break
    return node_path_from_goal_to_start


def style_df_route(df,node_path,color):

    df1 = pd.DataFrame('', index=df.index, columns=df.columns)
    for node in node_path:
        row,col=node.get_location()
        try:
            df1.iloc[row,col]=color
        except:
            pass    
    return df1

def main():
    maze_file='maze1.csv'
    df=pd.read_csv(maze_file,header=None)
    #convert to upper case
    df=df.apply(lambda x: x.astype(str).str.upper())
    cord=get_row_col_of_value(df,'S')
    current_node=Node(cord[0],cord[1])

    cord=get_row_col_of_value(df,'D')


    goal_node=Node(cord[0],cord[1])

    env=Environment(df)
    env.get_node_value(current_node)

    frontier_stack=[]
    frontier_stack.append(current_node)

    explored=[]
    goal_found=False
    goal_node_found=None
    while len(frontier_stack)> 0:
        working_node=frontier_stack.pop()
        explored.append(working_node)

        if working_node == goal_node:
                goal_found=True
                goal_node_found=working_node
                break
        
        ne_bours=env.get_neighbours(working_node)


        for e_n in ne_bours:

            ne_bours[e_n].set_prev_node(working_node)

            '''
            if ne_bours[e_n] == goal_node:
                goal_found=True
                #print("Goal found")
                goal_node_found=ne_bours[e_n]
                break
            '''
            if env.get_node_value(ne_bours[e_n]) == 'X' and ne_bours[e_n] not in  explored: # blocked node, so keep in explored list
                explored.append(ne_bours[e_n])
            elif ne_bours[e_n] not in  explored:
                frontier_stack.append(ne_bours[e_n])
        #break
    if goal_found:
        print("Goal Found")
    else:
        print("No Goal on Maze!!")

    if goal_node_found is not None:
        node_path=get_the_path(goal_node_found)
    
    if goal_node_found is not None:
        df2=df.style.apply(style_df_route, axis=None,node_path=explored,color='background-color: yellow')
  
        dfi.export(df2,"explored_maze_df.png")
        df2=df.style.apply(style_df_route, axis=None,node_path=node_path,color='background-color: green')
        dfi.export(df2,"solved_maze_df.png")

def main_queue():
    maze_file='maze1.csv'
    df=pd.read_csv(maze_file,header=None)
    #convert to upper case
    df=df.apply(lambda x: x.astype(str).str.upper())
    cord=get_row_col_of_value(df,'S')
    current_node=Node(cord[0],cord[1])

    cord=get_row_col_of_value(df,'D')


    goal_node=Node(cord[0],cord[1])

    env=Environment(df)
    env.get_node_value(current_node)

    #frontier_stack=[]
    frontier_stack=queue.Queue()
    frontier_stack.put(current_node)
    #frontier_stack.append(current_node)

    explored=[]
    goal_found=False
    goal_node_found=None
    #
    # while len(frontier_stack)> 0:
    while not frontier_stack.empty():
        #working_node=frontier_stack.pop()
        working_node=frontier_stack.get()
        explored.append(working_node)
        if working_node == goal_node:
                goal_found=True
                #print("Goal found")
                goal_node_found=working_node
                break
        
        ne_bours=env.get_neighbours(working_node)
        for e_n in ne_bours:

            ne_bours[e_n].set_prev_node(working_node)

            '''
            if ne_bours[e_n] == goal_node:
                goal_found=True
                #print("Goal found")
                goal_node_found=ne_bours[e_n]
                break
            '''
            if env.get_node_value(ne_bours[e_n]) == 'X' and ne_bours[e_n] not in  explored: # blocked node, so keep in explored list
                explored.append(ne_bours[e_n])
            elif ne_bours[e_n] not in  explored: # and env.get_node_value(ne_bours[e_n]) == ' ':
                #frontier_stack.append(ne_bours[e_n])
                frontier_stack.put(ne_bours[e_n])
        #break
    if goal_found:
        print("Goal Found")
    else:
        print("No Goal on Maze!!")

    if goal_node_found is not None:
        node_path=get_the_path(goal_node_found)
    
    if goal_node_found is not None:
        df2=df.style.apply(style_df_route, axis=None,node_path=explored,color='background-color: yellow')

        dfi.export(df2,"explored_maze_bf.png")
        df2=df.style.apply(style_df_route, axis=None,node_path=node_path,color='background-color: green')
        dfi.export(df2,"solved_maze_bf.png")

if __name__ == '__main__':
    main()
    main_queue()
