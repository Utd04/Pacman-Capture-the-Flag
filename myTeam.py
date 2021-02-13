from captureAgents import CaptureAgent
import capture
import random, time, util
from game import Directions
import game
from util import nearestPoint
import math
#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########


passWay = []    
canEscapePathways = []
boundaries = []


def manhattanDist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)

def getAllTunnels(validMovements):

    passWay = []
    while len(passWay) != len(findNewPathways(validMovements, passWay)):
        passWay = findNewPathways(validMovements, passWay)
    return passWay
    while(True):
      temp1 = len(passWay)
      temp2 = len(findNewPathways(validMovements,passWay))
      if(temp1==temp2):
        break
      else:
        temp3 = findNewPathways(validMovements,passWay)
        passWay = temp3

  # # def temporaryfunctionSOlver(self,gameState):
  #   # You can profile your evaluation time by uncommenting these lines
  #   # start = time.time()
  #   values = [self.evaluate(gameState, a) for a in actions]
  #   # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

  #   maxValue = max(values)
  #   bestActions = [a for a, v in zip(actions, values) if v == maxValue]

  #   foodLeft = len(self.getFood(gameState).asList())

  #   if foodLeft <= 2:
  #     bestDist = 9999
  #     for action in actions:
  #       successor = self.getSuccessor(gameState, action)
  #       pos2 = successor.getAgentPosition(self.index)
  #       dist = self.getMazeDistance(self.start,pos2)
  #       if dist < bestDist:
  #         bestAction = action
  #         bestDist = dist
  #     return bestAction

def succesorpostiionFunction(coordinate, toGetperformAction):
  x, y = coordinate
  if toGetperformAction == Directions.NORTH:
    return (x, y + 1)
  if toGetperformAction == Directions.SOUTH:
    return (x, y - 1)
  if toGetperformAction == Directions.EAST:
    return (x + 1, y)
  if toGetperformAction == Directions.WEST:
    return (x - 1, y)
  return coordinate

def Sucnom(coordinate, validMovements):
    ret = 0
    x, y = coordinate
    if (x + 1, y) in validMovements:
        ret += 1
    if (x - 1, y) in validMovements:
        ret += 1
    if (x, y + 1) in validMovements:
        ret += 1
    if (x, y - 1) in validMovements:
        ret += 1
    return ret

def getSuccsorsPos(coordinate, validMovements):
    ret = []
    x, y = coordinate
    if (x + 1, y) in validMovements:
        ret.append((x + 1, y))
    if (x - 1, y) in validMovements:
        ret.append((x - 1, y))
    if (x, y + 1) in validMovements:
        ret.append((x, y + 1))
    if (x, y - 1) in validMovements:
        ret.append((x, y - 1))
    return ret

def findNewPathways(validMovements, passWay):
    findnewtoreturn = passWay
    for i in range(len(validMovements)):
      tempor = Sucnom(validMovements[i],validMovements)
      heytemporary = Sucnom(validMovements[i],passWay)
      findadjacentPathwayNew = heytemporary
      if(tempor - findadjacentPathwayNew == 1):
        if(validMovements[i] not in passWay):
          findnewtoreturn.append(validMovements[i])
    return findnewtoreturn
      

def returnNewTuneel(coordinate, passWay):

    if coordinate not in passWay:
      return None
    elif(coordinate in passWay):
      q = util.Queue()
      visited = []
      q.push(coordinate)
      while (True):
        if(q.isEmpty()==True):
          break
        top = q.pop()
        if top not in visited:
            visited.append(top)
            succssorsPos = getSuccsorsPos(top, passWay)
            for i in succssorsPos:
                if i not in visited:
                    q.push(i)
      return visited


def funchelp(coordinate, passWay, validMovements):
    if coordinate not in passWay:
        return None
    aTunnel = returnNewTuneel(coordinate, passWay)
    for i in aTunnel:
        possibleEntry = getPossibleEntry(i, passWay, validMovements)
        if possibleEntry != None:
            return possibleEntry


def getPossibleEntry(coordinate, passWay, validMovements):
    x, y = coordinate
    if (x + 1, y) in validMovements and (x + 1, y) not in passWay:
        return (x + 1, y)
    if (x - 1, y) in validMovements and (x - 1, y) not in passWay:
        return (x - 1, y)
    if (x, y + 1) in validMovements and (x, y + 1) not in passWay:
        return (x, y + 1)
    if (x, y - 1) in validMovements and (x, y - 1) not in passWay:
        return (x, y - 1)
    return None

class OneIndex:
    def __init__(self, possession, flagid=0):
        (gameState, t, n) = possession
        self.flagid = flagid
        self.childs = []
        self.possession = (gameState, float(t), float(n))
        self.terminalNode = True
    def findParent(self, OneIndex):
        for i in range(len(self.childs)):
          if(self.childs[i]==OneIndex):
            return self
          else:
            prob = i.findParent(OneIndex)
            if prob != None:
              return prob
    def chooseChild(self):
        a,b, pn = self.possession
        maxVAL = -999999
        ret = None
        for i in self.childs:
            c, t, n = i.possession
            if n == 0:
              return i
            else:
              curr = t + 1.94 * math.sqrt(math.log(pn) / n)
              if maxVAL < curr:
                  maxVAL = curr
                  ret = i
        return ret
    def addChild(self, child):
        self.childs.append(child)

  # def getCurrentObservation(self):
  #   """
  #   Returns the GameState object corresponding this agent's current observation
  #   (the observed state of the game - this may not include
  #   all of your opponent's agent locations exactly).
  #   """
  #   return self.observationHistory[-1]

class wholeGraph:
    def __init__(self, root):
        self.index = 1
        self.wholeGraph = root
        self.terminalNode = [root.possession[0]]

    def put(self, parent, child):
        flagid = self.index
        self.index += 1
        child.flagid = flagid
        parent.addChild(child)
        if parent.possession[0] in self.terminalNode:
            self.terminalNode.remove(parent.possession[0])
        parent.terminalNode = False
        self.terminalNode.append(child.possession[0])

    def mother(self, OneIndex):
        if OneIndex == self.wholeGraph:
            return None
        return self.wholeGraph.findParent(OneIndex)

    def findBack(self, r, OneIndex):
        (gameState, t, n) = OneIndex.possession
        OneIndex.possession = (gameState, t + r, n + 1)
        parent = self.mother(OneIndex)
        if parent != None:
            self.findBack(r, parent)

    def choose(self, OneIndex = None):
        if OneIndex == None:
            OneIndex = self.wholeGraph
        else:
          if OneIndex.terminalNode:
            return OneIndex
          else:
            nextNode = OneIndex.chooseChild()
            return self.choose(nextNode)
  # def getMazeDistance(self, pos1, pos2):
  #   """
  #   Returns the distance between two points; These are calculated using the provided
  #   distancer object.

  #   If distancer.getMazeDistances() has been called, then maze distances are available.
  #   Otherwise, this just returns Manhattan distance.
  #   """
  #   d = self.distancer.getDistance(pos1, pos2)
  #   return d


  # # def temporaryfunctionSOlver(self,gameState):
  #   # You can profile your evaluation time by uncommenting these lines
  #   # start = time.time()
  #   values = [self.evaluate(gameState, a) for a in actions]
  #   # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

  #   maxValue = max(values)
  #   bestActions = [a for a, v in zip(actions, values) if v == maxValue]

  #   foodLeft = len(self.getFood(gameState).asList())

  #   if foodLeft <= 2:
  #     bestDist = 9999
  #     for action in actions:
  #       successor = self.getSuccessor(gameState, action)
  #       pos2 = successor.getAgentPosition(self.index)
  #       dist = self.getMazeDistance(self.start,pos2)
  #       if dist < bestDist:
  #         bestAction = action
  #         bestDist = dist
  #     return bestAction
  #           
class ReflexCaptureAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)
    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''

    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)
                                                       
    global openRoad           
    self.invadersGuess = False                                                 
    global validMovements                            
    self.numberOfCarriedBalls = 0       
    self.entersThroughPassway = None
    self.pathwayNextBlcok = None 
    self.fallback = None  
    self.changeEntrance = False   
    self.successorEntrance = None   

    global boundaries           
    global passWay           

    justforsake = gameState.getWalls().asList()
    boundaries = justforsake              

    self.allBlownAway = None                       
    self.struckOrNo = False 
    
    
    if len(passWay) == 0:
    # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i])
      validMovements = [move for move in gameState.getWalls().asList(False)]
      
    # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i])
    #  # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i]) 
    
    
    if(len(passWay)==0):
      passWay = getAllTunnels(validMovements)
    
    
    if(len(passWay)==0):  
      openRoad = list(set(validMovements).difference(set(passWay)))
    
    
    self.bigFood = None                                          
    self.findNewFoodloc = None                           
    self.unableMoving = 0                                   
    global canEscapePathways               
    
    layoutWidth = gameState.data.layout.width
    Redmovements = [move for move in validMovements if move[0] < layoutWidth / 2] 
    BlueMovements = [move for move in validMovements if move[0] >= layoutWidth / 2]

    if len(canEscapePathways) == 0:
        if (self.red==False):
          canEscapePathways = getAllTunnels(BlueMovements)
            
        elif(self.red==True):
          canEscapePathways = getAllTunnels(Redmovements)
            

  # def getCurrentObservation(self):
  #   """
  #   Returns the GameState object corresponding this agent's current observation
  #   (the observed state of the game - this may not include
  #   all of your opponent's agent locations exactly).
  #   """
  #   return self.observationHistory[-1]
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)

    values = [self.evaluate(gameState, a) for a in actions]
    Q = max(values)
    if self.struckOrNo:
        return self.simulation(gameState)
    bestActions = [a for a, v in zip(actions, values) if v == Q]
    action = random.choice(bestActions)
    return action
    # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i])

  def getSuccessor(self, gameState, action):
    tempsuc = gameState.generateSuccessor(self.index, action)
    nextDoingAction = tempsuc
    temppos = nextDoingAction.getAgentState(self.index).getPosition()
    coordinate = temppos
    if coordinate == nearestPoint(coordinate):
      return nextDoingAction
    else:
      return nextDoingAction.generateSuccessor(self.index, action)
    # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i])
  def evaluate(self, gameState, action):

    comparingFunctions = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)

    return comparingFunctions * weights
    # for i in range(len(gameState.getWalls().asList(False))):
    #   validMovements = validMovements.append(gameState.getWalls().asList(False)[i])

  def PathwaynextFood(self, gameState):
      cur = gameState.getAgentState(self.index).getPosition()
      q = util.Queue()
      visited = []
      q.push(cur)

      while (True):
          if(q.isEmpty()==True):
            break
          else:
            x, y = q.pop()
            if self.getFood(gameState)[int(x)][int(y)]:
                return (x, y)

            if (x, y) not in visited:
                visited.append((x, y))
                succssorsPos = getSuccsorsPos((x, y), passWay)
                for i in succssorsPos:
                    if i not in visited:
                        q.push(i)
      return None



  def UnncesaaryPath(self, gameState, nextDoingAction):
    cur = gameState.getAgentState(self.index).getPosition()
    suc = nextDoingAction.getAgentState(self.index).getPosition()
    if cur not in passWay and suc in passWay:
      self.entersThroughPassway = cur
      dfs = util.Stack()
      visited = []
      dfs.push((suc, 1))

      while True :
        if(dfs.isEmpty()):
          break
        else:
          (x, y), length = dfs.pop()
          if self.getFood(gameState)[int(x)][int(y)]:
            return length
          if (x, y) not in visited:
            visited.append((x, y))
            succssorsPos = getSuccsorsPos((x, y), passWay)
            for i in succssorsPos:
              if i not in visited:
                nextLength = length + 1
                dfs.push((i, nextLength))
    return 0

  # def getMazeDistance(self, pos1, pos2):
  #   """
  #   Returns the distance between two points; These are calculated using the provided
  #   distancer object.

  #   If distancer.getMazeDistances() has been called, then maze distances are available.
  #   Otherwise, this just returns Manhattan distance.
  #   """
  #   d = self.distancer.getDistance(pos1, pos2)
  #   return d


  def returnTImeDue(self, gameState):
      return gameState.data.timeleft

    
    # get all the legal position to jump to the middle boundary
  def returnEntrancePOint(self,gameState):
        layoutWidth = gameState.data.layout.width
        height = gameState.data.layout.height
        validMovements = [move for move in gameState.getWalls().asList(False)]
        BlueMovements = [move for move in validMovements if move[0] == layoutWidth / 2]
        Redmovements = [move for move in validMovements if move[0] == layoutWidth / 2 - 1]
        redEntrance = []
        blueEntrance = []
        for i in Redmovements:
            for j in BlueMovements:
                if i[0] + 1 == j[0] and i[1] == j[1]:
                    redEntrance.append(i)
                    blueEntrance.append(j)
        if (self.red==False):
          return blueEntrance
            
        elif(self.red==True):
          return redEntrance


  # # def temporaryfunctionSOlver(self,gameState):
  #   # You can profile your evaluation time by uncommenting these lines
  #   # start = time.time()
  #   values = [self.evaluate(gameState, a) for a in actions]
  #   # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

  #   maxValue = max(values)
  #   bestActions = [a for a, v in zip(actions, values) if v == maxValue]

  #   foodLeft = len(self.getFood(gameState).asList())

  #   if foodLeft <= 2:
  #     bestDist = 9999
  #     for action in actions:
  #       successor = self.getSuccessor(gameState, action)
  #       pos2 = successor.getAgentPosition(self.index)
  #       dist = self.getMazeDistance(self.start,pos2)
  #       if dist < bestDist:
  #         bestAction = action
  #         bestDist = dist
  #     return bestAction


class DefensiveReflexAgent(ReflexCaptureAgent):

  def getLengthToBoundary(self, gameState):   
      tempcord =   gameState.getAgentState(self.index)
      curCoodinate = tempcord.getPosition()

      height = gameState.data.layout.height
      layoutWidth = gameState.data.layout.width

      validMovements = [oneentryplace for oneentryplace in gameState.getWalls().asList(False)]

      Redmovements = [oneentryplace for oneentryplace in validMovements if oneentryplace[0] == layoutWidth / 2 - 1]
      BlueMovements = [oneentryplace for oneentryplace in validMovements if oneentryplace[0] == layoutWidth / 2]

      if( self.red==False):
        return min([self.getMazeDistance(curCoodinate, a) for a in BlueMovements])
      else:
        return min([self.getMazeDistance(curCoodinate, a) for a in Redmovements])
  def ifNeedsBlockTunnel(self, curInvaders, currentPostion, curCapsule): 
    if len(curInvaders) == 1:
      invadersPos = curInvaders[0].getPosition()
      if invadersPos in passWay:
        entersThroughPassway = funchelp(invadersPos, passWay, validMovements)
        if self.getMazeDistance(entersThroughPassway,currentPostion) <= self.getMazeDistance(entersThroughPassway,invadersPos) and curCapsule not in returnNewTuneel(invadersPos,passWay):
           return True
    return False
  def ifLostFood(self):
        preState = self.getPreviousObservation()
        currState = self.getCurrentObservation()
        myCurrFood = self.getFoodYouAreDefending(currState).asList()
        myLastFood = self.getFoodYouAreDefending(preState).asList()
        if len(myCurrFood) < len(myLastFood):
            for i in myLastFood:
                if i not in myCurrFood:
                    return i
        return None
          
  def getFeatures(self, gameState, action):
    comparingFunctions = util.Counter()
    nextDoingAction = self.getSuccessor(gameState, action)
    curCoodinate = gameState.getAgentState(self.index).getPosition()
    curState = gameState.getAgentState(self.index)             
    sucState = nextDoingAction.getAgentState(self.index)          
    sucPos = sucState.getPosition()  
    curCapsule = self.getCapsulesYouAreDefending(gameState)     
    lengthToBoundary = self.getLengthToBoundary(nextDoingAction)    
  
    comparingFunctions['fec12'] = 100
    if sucState.isPacman: comparingFunctions['fec12'] = 0

    if self.fallback == None:
        comparingFunctions['fec14'] = self.getLengthToBoundary(nextDoingAction)

    if self.getLengthToBoundary(nextDoingAction) <= 2:
        self.fallback = 0


    opposition = []
    for i in range(len(self.getOpponents(nextDoingAction))):
      opposition.append(nextDoingAction.getAgentState(self.getOpponents(nextDoingAction)[i]))

    tempvar1 = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]  
    
    opponentInside = [tempvarrr for tempvarrr in opposition if tempvarrr.isPacman and tempvarrr.getPosition() != None]   
    curInvaders = [tempvarrr for tempvarrr in tempvar1 if tempvarrr.isPacman and tempvarrr.getPosition() != None] 


    if (self.invadersGuess):
        self.enemyGuess.observe(self, gameState)
        enemyPos = self.enemyGuess.getPossiblePosition(curInvaders[0])
        comparingFunctions['fec50'] = self.getMazeDistance(enemyPos, sucPos)
        self.enemyGuess.elapseTime()

    if (self.ifNeedsBlockTunnel(curInvaders, curCoodinate, curCapsule) and curState.scaredTimer == 0):
        comparingFunctions['fec50'] = self.getMazeDistance(funchelp(curInvaders[0].getPosition(),passWay,validMovements),sucPos)
        return comparingFunctions

    if curCoodinate in canEscapePathways and len(curInvaders) == 0:
        comparingFunctions['fecret'] = self.getMazeDistance(self.start, sucPos)

    comparingFunctions['fec30'] = len(opponentInside) 
     
    if len(curInvaders) == 0 and not nextDoingAction.getAgentState(self.index).isPacman and curState.scaredTimer == 0:
        if  curCoodinate not in canEscapePathways and nextDoingAction.getAgentState(self.index).getPosition() in canEscapePathways: 
            comparingFunctions['feature16'] = -1

    if len(opponentInside) > 0 and curState.scaredTimer == 0:            
        dists = [self.getMazeDistance(sucPos, a.getPosition()) for a in opponentInside]
        comparingFunctions['fec1'] = min(dists)
        comparingFunctions['fec22'] = self.getLengthToBoundary(nextDoingAction)
    
    if len(opponentInside) > 0 and curState.scaredTimer != 0:           
        dists = min([self.getMazeDistance(sucPos, a.getPosition()) for a in opponentInside])
        comparingFunctions['fec5'] = (dists-2)*(dists-2)
        if curCoodinate not in canEscapePathways and nextDoingAction.getAgentState(self.index).getPosition() in canEscapePathways:
            comparingFunctions['feature16'] = -1

    if len(opponentInside) > 0 and len(curCapsule) != 0:         
        dist2 = [self.getMazeDistance(c, sucPos) for c in curCapsule]
        comparingFunctions['fecp'] = min(dist2)

    if action == Directions.STOP: comparingFunctions['feature20'] = 1  

    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev:
       comparingFunctions['fec2'] = 1  

    if self.getPreviousObservation() != None:
      if len(opponentInside) == 0 and self.ifLostFood() != None:
          self.allBlownAway = self.ifLostFood()

      if self.allBlownAway != None and len(opponentInside) == 0: 
          comparingFunctions['fec0'] = self.getMazeDistance(sucPos,self.allBlownAway)
      
      if sucPos == self.allBlownAway or len(opponentInside) > 0:
          self.allBlownAway = None

    return comparingFunctions

  def getWeights(self, gameState, action):
    return {'fecp': -3,'fecret':-0.1,'fec1': -10, 'fec22':-3,'fec5':-100, 'fec30': -100,'fec14':-2, 'fec12': 10,'fec50': -10,
      'fec2': -2,'fec0':-1,'feature20': -100,
      'feature16':200
      }
            

class OffensiveReflexAgent(ReflexCaptureAgent):

  def getLengthToHome(self, gameState):  
    
      curCoodinate = gameState.getAgentState(self.index).getPosition()
      layoutWidth = gameState.data.layout.width
      height = gameState.data.layout.height
      validMovements = [oneentryplace for oneentryplace in gameState.getWalls().asList(False)]

      Redmovements = [oneentryplace for oneentryplace in validMovements if oneentryplace[0] == layoutWidth / 2 - 1]
      BlueMovements = [oneentryplace for oneentryplace in validMovements if oneentryplace[0] == layoutWidth / 2]

      if (self.red==False):
        return min([self.getMazeDistance(curCoodinate, a) for a in BlueMovements])
      else:
        return min([self.getMazeDistance(curCoodinate, a) for a in Redmovements])

  def getFeatures(self, gameState, action):
    """
    Returns a counter of comparingFunctions for the state
    """
    comparingFunctions = util.Counter()     
       

    nextDoingAction = self.getSuccessor(gameState, action)  
    tempNextState = nextDoingAction.getAgentState(self.index)   
    myPos = tempNextState.getPosition()

    tempagentState = gameState.getAgentState(self.index)                 
    curCoodinate = tempagentState.getPosition()

    nextPosition = succesorpostiionFunction(curCoodinate,action) 

    opposition = []
    for i in range(len(self.getOpponents(gameState))):
      opposition.append(gameState.getAgentState(self.getOpponents(gameState)[i]))

    opponentInside =[]
    for i in range(len(opposition)):
      if(opposition[i].isPacman==True):
        if(opposition[i].getPosition!=None):
          opponentInside.append(opposition[i])  
          
    afterDeath = []
    for i in range(len(opposition)):
      if(opposition[i].isPacman==False):
        if(opposition[i].getPosition()!=None):
          if(manhattanDist(curCoodinate,opposition[i].getPosition()) <= 5):
            afterDeath.append(opposition[i])
    deadGhostWait =[]
    for i in range(len(afterDeath)):
      if(afterDeath[i].scaredTimer>1):
        deadGhostWait.append(afterDeath[i])
    aliveStill =[]
    for i in range(len(afterDeath)):
      if(afterDeath[i] not in deadGhostWait):
        aliveStill.append(afterDeath[i])   
    foodNotlist =  self.getFood(gameState)
    foodAsAlist = foodNotlist.asList()                      
    Foodtakable = [a for a in foodAsAlist if a not in passWay]      
    foodINthePathWay = [a for a in foodAsAlist if a in passWay]     
           
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction] 
    bigFood = self.getCapsules(gameState)        
                                             
    checkTunnel = self.UnncesaaryPath(gameState, nextDoingAction)                             


    comparingFunctions['featureOne'] = self.getScore(nextDoingAction)
    
    if( gameState.getAgentState(self.index).isPacman):  
        self.changeEntrance = False
    
    if (len(afterDeath)) == 0:    
        self.bigFood = None
        self.findNewFoodloc = None
        self.pathwayNextBlcok = None
    
    if (len(aliveStill) == 0):
      if(len(foodAsAlist) != 0):
        if(len(foodAsAlist) >= 3):
          comparingFunctions['feature2'] = min([self.getMazeDistance(myPos, food) for food in foodAsAlist])
          if myPos in self.getFood(gameState).asList():
              comparingFunctions['feature2'] = -1

    if( nextPosition in foodAsAlist):                      
        self.numberOfCarriedBalls += 1
    if(gameState.getAgentState(self.index).isPacman==False):
        self.numberOfCarriedBalls = 0

    if (self.returnTImeDue(gameState)/4 < self.getLengthToHome(gameState) + 3): 
        comparingFunctions['feature10'] = self.getLengthToHome(nextDoingAction)
        return comparingFunctions

    if len(foodAsAlist) < 3:
      comparingFunctions['featureret'] = self.getLengthToHome(nextDoingAction)  

    if (len(aliveStill) > 0):   
      if(len(foodAsAlist) >= 3):      
        dists = min([self.getMazeDistance(myPos, a.getPosition()) for a in aliveStill]) 
        comparingFunctions['feature4'] = 100 - dists
        ghostPos = [a.getPosition() for a in aliveStill]
        if( nextPosition in ghostPos):
            comparingFunctions['feature5'] = 1           
        if( nextPosition in [getSuccsorsPos(temp,validMovements) for temp in ghostPos][0]):
            comparingFunctions['feature5'] = 1
        if len(Foodtakable) > 0:             
            comparingFunctions['Foodtakable'] = min([self.getMazeDistance(myPos, food) for food in Foodtakable]) 
            if myPos in Foodtakable:
              comparingFunctions['Foodtakable'] = -1
        elif len(Foodtakable) == 0:
            comparingFunctions['featureret'] = self.getLengthToHome(nextDoingAction)
          
    if (len(aliveStill) > 0):  
      if(len(foodAsAlist) >= 3):
        if len(Foodtakable) > 0:
            safeFood = []
            for food in Foodtakable:
                if self.getMazeDistance(curCoodinate, food) < min([self.getMazeDistance(a.getPosition(), food) for a in aliveStill]):
                    safeFood.append(food)
            if len(safeFood) != 0:
                closestSFdist = min([self.getMazeDistance(curCoodinate, food) for food in safeFood])
                for food in safeFood:
                    if self.getMazeDistance(curCoodinate, food) == closestSFdist:
                        self.findNewFoodloc = food
                        break

    if len(aliveStill) > 0 and len(foodINthePathWay) > 0 and len(deadGhostWait) == 0 and len(foodAsAlist) >= 3:
        minTFDist = min([self.getMazeDistance(curCoodinate, tf) for tf in foodINthePathWay])
        safeTfood = []
        for tf in foodINthePathWay:
            entersThroughPassway = funchelp(tf,passWay,validMovements)
            if self.getMazeDistance(curCoodinate, tf) + self.getMazeDistance(tf, entersThroughPassway) < min([self.getMazeDistance(a.getPosition(), entersThroughPassway) for a in aliveStill]):
                safeTfood.append(tf)
        if len(safeTfood) > 0:
            closestTFdist = min([self.getMazeDistance(curCoodinate, food) for food in safeTfood])
            for food in safeTfood:
                if self.getMazeDistance(curCoodinate, food) == closestTFdist:
                    self.pathwayNextBlcok = food
                    break


    if comparingFunctions['feature8'] == 0 and self.pathwayNextBlcok != None:
        comparingFunctions['feature8'] = self.getMazeDistance(myPos, self.pathwayNextBlcok)
        if myPos == self.pathwayNextBlcok:
            comparingFunctions['feature8'] = 0
            self.pathwayNextBlcok = None
    
    if self.findNewFoodloc != None:
        comparingFunctions['feature8'] = self.getMazeDistance(myPos, self.findNewFoodloc)
        if myPos == self.findNewFoodloc:
            comparingFunctions['feature8'] = -0.0001
            self.findNewFoodloc = None

    if len(aliveStill) > 0 and len(bigFood) != 0:
        for c in bigFood:
            if self.getMazeDistance(curCoodinate, c) < min([self.getMazeDistance(c, a.getPosition()) for a in aliveStill]):
                self.bigFood = c

    if len(deadGhostWait) > 0 and len(bigFood) != 0:
        for c in bigFood:
            if self.getMazeDistance(curCoodinate, c) >= deadGhostWait[0].scaredTimer and self.getMazeDistance(curCoodinate, c) < min([self.getMazeDistance(c, a.getPosition()) for a in deadGhostWait]):
                self.bigFood = c

    if curCoodinate in passWay:
        for c in bigFood:
            if c in returnNewTuneel(curCoodinate,passWay):
                self.bigFood = c

    if self.bigFood != None:
        comparingFunctions['feature12'] = self.getMazeDistance(myPos, self.bigFood)
        if myPos == self.bigFood:
            comparingFunctions['feature12'] = 0
            self.bigFood = None

    if len(aliveStill) == 0 and myPos in bigFood:
        comparingFunctions['feature9'] = 0.1

    if action == Directions.STOP: comparingFunctions['feature20'] = 1
    if nextDoingAction.getAgentState(self.index).isPacman and curCoodinate not in passWay and \
        nextDoingAction.getAgentState(self.index).getPosition() in passWay and checkTunnel == 0:
        comparingFunctions['feature15'] = -1
    if len(deadGhostWait) > 0:
         dist = min([self.getMazeDistance(curCoodinate, a.getPosition()) for a in deadGhostWait])
         if checkTunnel != 0 and checkTunnel*2 >= deadGhostWait[0].scaredTimer -1:
             comparingFunctions['feature16'] = -1        
    if len(aliveStill) > 0:
         dist = min([self.getMazeDistance(curCoodinate, a.getPosition()) for a in aliveStill])
         if checkTunnel != 0 and checkTunnel*2 >= dist-1:
             comparingFunctions['feature16'] = -1

    if curCoodinate in passWay and len(aliveStill) > 0:
        foodPos = self.PathwaynextFood(gameState)
        if foodPos == None:
            comparingFunctions['feature18'] = self.getMazeDistance(succesorpostiionFunction(curCoodinate,action), self.entersThroughPassway)
        else:
            lengthToEscape = self.getMazeDistance(myPos, foodPos) + self.getMazeDistance(foodPos, self.entersThroughPassway)
            ghostToEntry = min([self.getMazeDistance(self.entersThroughPassway, a.getPosition()) for a in aliveStill])
            if ghostToEntry - lengthToEscape <= 1 and len(deadGhostWait) == 0:
                comparingFunctions['feature18'] = self.getMazeDistance(succesorpostiionFunction(curCoodinate,action), self.entersThroughPassway)
    if curCoodinate in passWay and len(deadGhostWait) > 0:
        foodPos = self.PathwaynextFood(gameState)
        if foodPos == None:
            comparingFunctions['feature18'] = self.getMazeDistance(succesorpostiionFunction(curCoodinate,action), self.entersThroughPassway)
        else:
            lengthToEscape = self.getMazeDistance(myPos, foodPos) + self.getMazeDistance(foodPos, self.entersThroughPassway)
            if  deadGhostWait[0].scaredTimer - lengthToEscape <= 1:
                comparingFunctions['feature18'] = self.getMazeDistance(succesorpostiionFunction(curCoodinate,action), self.entersThroughPassway)
    if not gameState.getAgentState(self.index).isPacman and len(aliveStill) > 0 and self.unableMoving != -1:
        self.unableMoving += 1
    if gameState.getAgentState(self.index).isPacman or myPos == self.successorEntrance:
        self.unableMoving = 0
        self.successorEntrance = None
    if self.unableMoving > 10:
        self.unableMoving = -1
        self.successorEntrance = random.choice(self.returnEntrancePOint(gameState))   
    if self.successorEntrance != None and comparingFunctions['feature8'] == 0:
        comparingFunctions['feature19'] = self.getMazeDistance(myPos,self.successorEntrance)

    return comparingFunctions

  def getWeights(self, gameState, action):
    return {'featureOne':1,'feature2':-2,'feature4': -10,'feature5':-1000,'feature8': -11,'feature12': -1200,
          'feature10':-100, 'feature9':-1, 'feature19':-1001,'feature16': 100, 'feature20':-50,
            'Foodtakable' :-3, 'feature18':-1001,'featureret':-1,'feature15':100,
           }

  
          


  # def getMazeDistance(self, pos1, pos2):
  #   """
  #   Returns the distance between two points; These are calculated using the provided
  #   distancer object.

  #   If distancer.getMazeDistances() has been called, then maze distances are available.
  #   Otherwise, this just returns Manhattan distance.
  #   """
  #   d = self.distancer.getDistance(pos1, pos2)
  #   return d
