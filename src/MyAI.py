# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================
import copy
from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        self.start = True
        self.stack = []
        self.route = []
        self.dic = {} # 1 is safe 2 is dangerous
        self.world = {} #roud, S, B, W, P
        self.facing = None
        self.mockfacing = None
        self.back = False
        self.pos = None
        self.turn = None
        self.width = None
        self.height = None
        self.arrowshoot = False
        self.shootingpos = None
        self.wumpuskilled = False
        self.wumpuspos = None
        self.error = False
        self.debug = False
        pass
    
    def facing_change(self, current, turn):
        # return int
        # turn = 1: turn left
        # turn = 2: turn right
        if turn == 1:
            if current == 4: return 1
            else: return current + 1
        if turn == 2:
            if current == 1: return 4
            else: return current - 1

    def move_safe(self, pos):
        # return bool
        # check if it is safe to move to a position
        if pos in self.dic:
            if self.dic[pos] == 1: return True
            else: return False
        else: return True

    def pos_change(self, facing):
        # return the position tuple (int, int)
        # update position before execute move
        if facing == 1:
            pos = (self.pos[0] + 1, self.pos[1])
            return pos
        elif facing == 2:
            pos = (self.pos[0], self.pos[1] + 1)
            return pos
        elif facing == 3:
            pos = (self.pos[0] - 1, self.pos[1])
            return pos
        elif facing == 4:
            pos = (self.pos[0], self.pos[1] - 1)
            return pos
        else:
            print("Error in pos_change(): invalid facing value")
            self.error = True
            return self.pos

    def BFS(self, start, end):
        # return the list of (x,y) set from the start to end
        D = [[1, 0], [0, 1], [-1, 0], [0, -1]] # R, U, L, D
        q = []
        L = []
        L.append(start)
        q.append((start[0], start[1], L))
        visit = {}
        visit[start] = 1
        while len(q) > 0:
            (x,y,L) = q.pop(0)
            if (x,y) == end:
                return L
            else:
                for ele in D:
                    if (x + ele[0], y + ele[1]) in self.dic and self.dic[(x + ele[0], y + ele[1])] == 1:
                        if (x + ele[0], y + ele[1]) not in visit:
                            visit[(x + ele[0], y + ele[1])] = 1
                            tmp = copy.deepcopy(L)
                            tmp.append((x + ele[0], y + ele[1]))
                            q.append((x + ele[0], y + ele[1], tmp))

    def transform(self, L):
        facing = self.facing
        pre = L[0]
        action = []
        for ele in L:
            if pre[0] - ele[0] > 0: #<----
                self.mockfacing = 3
                if facing == 1:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 3
                elif facing == 2:
                    action.append(Agent.Action.TURN_LEFT)
                    action.append(Agent.Action.FORWARD)
                    facing = 3
                elif facing == 3:
                    action.append(Agent.Action.FORWARD)
                elif facing == 4:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 3
            elif pre[0] - ele[0] < 0: #----->
                self.mockfacing = 1
                if facing == 1:                   
                    action.append(Agent.Action.FORWARD)
                elif facing == 2:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 1
                elif facing == 3:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 1
                elif facing == 4:
                    action.append(Agent.Action.TURN_LEFT)
                    action.append(Agent.Action.FORWARD)
                    facing = 1
            elif pre[1] - ele[1] > 0: #go down
                self.mockfacing = 4
                if facing == 1:                   
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 4
                elif facing == 2:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 4
                elif facing == 3:
                    action.append(Agent.Action.TURN_LEFT)                   
                    action.append(Agent.Action.FORWARD)
                    facing = 4
                elif facing == 4:
                    action.append(Agent.Action.FORWARD)
            elif pre[1] - ele[1] < 0: #go up
                self.mockfacing = 2
                if facing == 1:
                    action.append(Agent.Action.TURN_LEFT)
                    action.append(Agent.Action.FORWARD)
                    facing = 2
                elif facing == 2:
                    action.append(Agent.Action.FORWARD)
                elif facing == 3:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 2
                elif facing == 4:
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.TURN_RIGHT)
                    action.append(Agent.Action.FORWARD)
                    facing = 2
            pre = ele
        return action

    def faceWumpus(self, pos):
        D = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        f = self.mockfacing
        if not self.mockfacing:
            return False
        actions = []
        found = False
        for e in D:
            if (pos[0] + e[0], pos[1] + e[1]) == self.wumpuspos:
                found = 1
                if e == [1, 0]:
                    if f == 2:
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 3:
                        actions.append(Agent.Action.TURN_RIGHT)
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 4:
                        actions.append(Agent.Action.TURN_LEFT)
                elif e == [-1, 0]:
                    if f == 1:
                        actions.append(Agent.Action.TURN_RIGHT)
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 2:
                        actions.append(Agent.Action.TURN_LEFT)
                    elif f == 4:
                        actions.append(Agent.Action.TURN_RIGHT)
                elif e == [0, 1]:
                    if f == 1:
                        actions.append(Agent.Action.TURN_LEFT)
                    elif f == 3:
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 4:
                        actions.append(Agent.Action.TURN_RIGHT)
                        actions.append(Agent.Action.TURN_RIGHT)
                elif e == [0, -1]:
                    if f == 1:
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 2:
                        actions.append(Agent.Action.TURN_RIGHT)
                        actions.append(Agent.Action.TURN_RIGHT)
                    elif f == 3:
                        actions.append(Agent.Action.TURN_LEFT)
        if not found:
            return False
        actions.append(Agent.Action.SHOOT)
        return actions

    def move(self, end):
        if (self.debug):
            print("========== move ==========")
            print("self.pos = " + str(self.pos))
            print("end = " + str(end))
        tmp = self.BFS(self.pos, end)
        L = self.transform(tmp)
        if (end == self.shootingpos):
            if (not self.wumpuskilled) and (not self.arrowshoot) and (self.wumpuspos):
                nextmove = []
                nextmove = self.faceWumpus(end)
                if not nextmove:
                    print("[ERROR] in self.faceWumpus, action not found")
                else:
                    for e in nextmove:
                        L.append(e)
        if self.back:
            L.append(Agent.Action.CLIMB)
        self.route = list(reversed(L))
        if (len(self.route) == 0):
            return self.agentPanic()
        action = self.route.pop() 
        if action == Agent.Action.TURN_LEFT: #turn left
            self.facing = self.facing_change(self.facing, 1)
        if action == Agent.Action.TURN_RIGHT: #turn right
            self.facing = self.facing_change(self.facing, 2)
        if action == Agent.Action.FORWARD: #forward
            self.pos = self.pos_change(self.facing)
        return action

    def mockmove(self, end):
        tmp = self.BFS(self.pos, end)
        L = self.transform(tmp)
        return len(L)

    def block(self):
        tmp = []
        if self.facing == 1:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0], self.pos[1] - 1))
        elif self.facing == 2:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0] - 1, self.pos[1]))
        elif self.facing == 3:
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0] - 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] - 1))
        else:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0] - 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] - 1))
        for ele in tmp:
            if ele not in self.dic:
                if self.world[self.pos] == "BS":
                    self.world[ele] = "PW"
                elif self.world[self.pos] == "B":
                    self.world[ele] = "P"
                elif self.world[self.pos] == "S":
                    self.world[ele] = "W"
                self.dic[ele] = 2

    def check_inbox(self, pos):
        if self.width and self.height:
            if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width and pos[1] < self.height:
                return True
            else:
                return False
        elif self.width:
            if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width:
                return True
            else:
                return False 
        elif self.height:
            if pos[0] >= 0 and pos[1] >= 0 and pos[1] < self.height:
                return True
            else:
                return False
        elif pos[0] >= 0 and pos[1] >= 0:
            return True
        return False

    def add(self):
        tmp = []
        if self.facing == 1:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0], self.pos[1] - 1))
        elif self.facing == 2:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0] - 1, self.pos[1]))
        elif self.facing == 3:
            tmp.append((self.pos[0], self.pos[1] + 1))
            tmp.append((self.pos[0] - 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] - 1))
        else:
            tmp.append((self.pos[0] + 1, self.pos[1]))
            tmp.append((self.pos[0] - 1, self.pos[1]))
            tmp.append((self.pos[0], self.pos[1] - 1))
        tmp = list(reversed(tmp))
        for ele in tmp:
            if ele not in self.dic and self.check_inbox(ele):
                self.dic[ele] = 1
                if ele in self.stack:
                    self.stack.remove(ele)
                    self.stack.append(ele)
                else:
                    self.stack.append(ele)
    
    def check_isrealpit(self,pos):
        D = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        (x,y) = pos
        for ele in D:
            if (x + ele[0], y + ele[1]) in self.dic and (x + ele[0], y + ele[1]) in self.world:
                tmp = ["B", "BS", "PW", "W", "P", "?"]
                if self.world[(x + ele[0], y + ele[1])] not in tmp:
                    self.world[(x,y)] = "?" #change self.world
                    self.dic[(x,y)] = 1 #change self.dic
                    return False
        return True

    def get_wumpuspos(self, pos):
        D1 = [[2, 0], [1, 1], [0, 2], [-1, 1], 
             [-2, 0], [-1, -1], [0, -2], [1, -1]]
        D2 = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        W = [[1, 0], [0, 1], [-1, 0], [0, -1]] # wumpus candidate
        (x,y) = pos
        # if adjacent tile is safe, then wumpus must not be here
        for ele in D2:
            coord = (x + ele[0], y + ele[1])
            if coord in self.dic:
                if self.dic[coord] == 1:
                    W.remove(ele)
        # early exit if only one element in W
        if len(W) == 1:
            return (x + W[0][0], y + W[0][1])
        for ele in D1:
            coord = (x + ele[0], y + ele[1])
            if coord in self.world:
                # if stench in a tile which is two steps away
                # wumpus must be in the middle
                if "S" in self.world[coord]:
                    if ele == [2, 0]: return (x + 1, y)
                    elif ele == [0, 2]: return (x, y + 1)
                    elif ele == [-2, 0]: return (x - 1, y)
                    elif ele == [0, -2]: return (x, y - 1)
                    elif ele == [1, 1]:
                        if ([1, 0] in W) and ([0, 1] not in W):
                            return (x + 1, y)
                        if ([0, 1] in W) and ([1, 0] not in W):
                            return (x, y + 1)
                    elif ele == [1, -1]:
                        if ([1, 0] in W) and ([0, -1] not in W):
                            return (x + 1, y)
                        if ([0, -1] in W) and ([1, 0] not in W):
                            return (x, y - 1)
                    elif ele == [-1, -1]:
                        if ([-1, 0] in W) and ([0, -1] not in W):
                            return (x - 1, y)
                        if ([0, -1] in W) and ([-1, 0] not in W):
                            return (x, y - 1)
                    elif ele == [-1, 1]:
                        if ([-1, 0] in W) and ([0, 1] not in W):
                            return (x - 1, y)
                        if ([0, 1] in W) and ([-1, 0] not in W):
                            return (x, y + 1)
        return False

    def get_shootingpos(self):
        D = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        x, y = self.wumpuspos[0], self.wumpuspos[1]
        for ele in D:
            coord = (x + ele[0], y + ele[1])
            isinbox = self.check_inbox(coord)
            if not isinbox:
                continue
            candList = []
            if coord in self.dic:
                if self.dic[coord] == 1:
                    candList.append(coord)
        if len(candList) == 0:
            return False
        elif len(candList) == 1:
            return candList[0]
        else:
            lenList = []
            for c in candList:
                lenList.append(self.mock_move(c))
            return(candList[lenList.index(min(lenList))])

    def analyze(self):
        if (self.debug):
            print ("========== analyzing ==========")
        #print(self.world)
        L = self.world.keys()
        check = 1
        while check == 1:
            change = 0
            for ele in L:
                if self.check_inbox(ele):
                    if self.world[ele] == "P":
                        if not self.check_isrealpit(ele):
                            self.stack.append(ele)
                            if (self.debug):
                                print ("========== exit1 ==========")
                                print(self.stack)
                            change = 1
                    if self.world[ele] == "S":
                        if not self.wumpuskilled:
                            # if wumpus not killed and location unknown
                            if not self.wumpuspos:
                                wpos = self.get_wumpuspos(ele)
                                if (self.debug):
                                    print ("========== wpos calculated!!")
                                if wpos:
                                    self.wumpuspos = wpos
                            # if wumpus not killed, location known,
                            # and we still have an arrow, but does not know
                            # where to shoot the arrow
                            if self.wumpuspos and not self.shootingpos:
                                if not self.arrowshoot:
                                    spos = self.get_shootingpos()
                                    if spos:
                                        self.shootingpos = spos
                                        self.stack.append(spos)
                                        if (self.debug):
                                            print ("========== exit2 ==========")
                                        change = 1
                        if self.wumpuskilled:
                            if self.shootingpos:
                                self.stack.append(self.wumpuspos)
                                self.shootingpos = None
                                if (self.debug):
                                    print ("========== exit3 ==========")
                                    print(self.stack)
                                change = 1
            if change == 0:
                check = 0
        if (self.debug):
            self.debug_WorldTileStatus()
            self.debug_WorldSafeStatus()

    def nextAgentMove(self):
        if len(self.stack) > 0:
            return self.move(self.stack.pop())
        else:
            self.analyze()
            if len(self.stack) > 0:                   
                return self.move(self.stack.pop()) 
            self.back = True
            return self.move((0,0))

    def agentPanic(self):
        # debug function to elliminate obscure bugs
        if (self.debug):
            print("[ERROR] AGENT PANIC")
        self.back = True
        return self.move((0,0))

    def debug_TileStatus(self, stench, breeze, glitter, bump, scream):
        print ("========= Current Tile =========")
        print ("At coord: (" + str(self.pos[0]) + ", " + str(self.pos[1]) + ")")
        print ("Facing: " + str(self.facing))
        print ('If stench: {}'.format(str(stench)))
        print ("If breeze: " + str(breeze))
        print ("If glitter: " + str(glitter))
        print ("If bump: " + str(bump))
        print ("If scream: " + str(scream))
    
    def debug_WorldTileStatus(self):
        print ("========= World Tile Status =========")
        print (self.world)
    
    def debug_WorldSafeStatus(self):
        print ("========= World Safe Status =========")
        print (self.dic)
    
    def debug_RouteStack(self):
        print ("========= Route & Stack =========")
        print (self.route)
        print (self.stack)
        
    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        if (self.debug) and (not self.start):
            self.debug_TileStatus(stench, breeze, glitter, bump, scream)
            self.debug_RouteStack()
            print("wup pos = " + str(self.wumpuspos))
        
        if self.back:
            if self.pos == (0,0):
                return Agent.Action.CLIMB
            elif len(self.route) == 0:
                return self.move((0,0))
            else:
                return self.route.pop()

        if len(self.route) != 0: #under processing
            action = self.route.pop() 
            if action == Agent.Action.TURN_LEFT: #turn left
                self.facing = self.facing_change(self.facing, 1)
            if action == Agent.Action.TURN_RIGHT: #turn right
                self.facing = self.facing_change(self.facing, 2)
            if action == Agent.Action.FORWARD: #forward
                self.pos = self.pos_change(self.facing)
            return action

        if glitter:
            self.back = True
            return Agent.Action.GRAB
        
        if scream and self.start == False:
            self.arrowshoot = True
            self.wumpuskilled = True
            if (self.wumpuspos):
                self.dic[self.wumpuspos] = 1
        
        if breeze and self.start == True:
            return Agent.Action.CLIMB
        else:
            if self.start == True:
                if stench:
                    if not self.arrowshoot:
                        self.arrowshoot = True
                        return Agent.Action.SHOOT
                    else:
                        if scream:
                            self.wumpuspos = (1,0)
                            self.wumpuskilled = True
                            self.dic[(0,0)] = 1 # safe stench
                            self.dic[(1,0)] = 1 # wumpus corpse here
                            self.dic[(0,1)] = 1 # safe, no stench
                            self.world[(0,0)] = "S"
                            self.world[(1,0)] = "S"
                            self.world[(0,1)] = "roud"
                            self.stack.append((0,1))
                            self.stack.append((1,0))
                        else:
                            self.wumpuspos = (0,1)
                            self.dic[(0,0)] = 1 # safe stench
                            self.dic[(1,0)] = 1 # safe, no stench
                            self.dic[(0,1)] = 2 # WUMPUS DANGER
                            self.world[(0,0)] = "S"
                            self.world[(1,0)] = "roud"
                            self.world[(0,1)] = "W"
                            # SUICIDE if we append (0,1) in self.stack
                            self.stack.append((1,0))
                else:
                    self.dic[(0,0)] = 1 #safe
                    self.dic[(1,0)] = 1
                    self.dic[(0,1)] = 1
                    self.world[(0,0)] = "roud"
                    self.world[(1,0)] = "roud"
                    self.world[(0,1)] = "roud"
                    self.stack.append((0,1))
                    self.stack.append((1,0))
                self.facing = 1 # right
                self.start = False
                self.stack.pop()
                self.pos = (1,0)
                return Agent.Action.FORWARD
            else:
                if bump:
                    self.dic[self.pos] = 2 #not enter
                    if self.facing == 1:
                        self.width = self.pos[0]
                    elif self.facing == 2:
                        self.height = self.pos[1]
                    # should trun the postion back to the original
                    if self.facing == 1:
                        self.pos = (self.pos[0] - 1, self.pos[1])
                    else:
                        self.pos = (self.pos[0], self.pos[1] - 1)
                    return self.nextAgentMove()
                elif breeze or stench:                
                    # block the area around the pos as dangerous zone
                    if breeze and stench:
                        self.world[self.pos] = "BS"
                        self.block()
                    elif breeze:
                        self.world[self.pos] = "B"
                        self.block()
                    elif stench:
                        self.world[self.pos] = "S"
                        # if wumpus location known
                        # no need to fear if stench
                        if not self.wumpuspos:
                            self.block()
                        else:
                            self.add() #add the area around the pos into satck
                            if not self.wumpuskilled:
                                if self.wumpuspos in self.stack:
                                    self.stack.remove(self.wumpuspos)
                    return self.nextAgentMove()
                else:
                    self.world[self.pos] = "roud"
                    self.add() #add the area around the pos into satck
                    return self.nextAgentMove()
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================