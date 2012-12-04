from utils import *
from search import *

class ClassSearch(Problem):
  """ """
  
  def __init__ (self, initial, goal=None):
    self.initial = initial
    self.goal = goal
    self.classes = []   # list of classes scheduled
    self.allSchedules = []  # a list of all complete schedules
    
    # list where each column is a day of the week and each row is a time slot representing 5 minutes of time from 8am to 9pm
    self.currentSchedule = [[False for i in range(157)] for j in range(6)] 
  
  def handleGoal(self, state):
    self.allSchedules.append(state)
    return
  
  def goal_test (self, state):
    """ if the current state is the same length as the goal, then we have reached the goal state"""
    if len(state) == len(self.goal):
      self.handleGoal(state)
      return True
    return False
  
  
  def addClass (self, startTime, endTime, daysOfWeek): 
    for i in daysOfWeek:
      for j in range (timeToKey(startTime), timeToKey(endTime)):
        self.currentSchedule[dayOfWeek(i)][j] = True
    
  def removeClass (self, startTime, endTime, daysOfWeek):
    for i in daysOfWeek:
      for j in range (timeToKey(startTime), timeToKey(endTime)):
        self.currentSchedule[dayOfWeek(i)][j] = False  
  
  def printSchedule(self):
    string = ''
    print "Time:\tSat.\tMon\tTues.\tWed.\tThurs.\tFri.\t"
    for i in range(157):
      string = ''
      for j in range (6):
        if self.currentSchedule[j][i]:
          string += '1' + '\t'
        else:
          string += '0' + '\t'
      print keyToTime(i), string
      
      
  
  


  def successor (self, state):        
    """ successors are defined in (action, state) pairs. 
      The action is the class that is being scheduled while the state is the list of classes scheduled so far, including the just added class"""
    
    availableClasses = []       # holds the total available classes
    successors = []             # holds a list of tules containing the action/state pairs
    currClassIndex = len(self.goal) - len(state) - 1      # get 

    if currClassIndex == -1:
      return []
      
    currClass = self.goal[currClassIndex]
    availableClasses = catalog[currClass[0]][currClass[1]]

    for i in state:
      item = catalog[i[0]][i[1]][i[2]]
      self.addClass(item[1], item[2], item[3])
      

    availableClasses = self.propagate(availableClasses)

    for i in availableClasses:
      newState = []
      newState.extend(state)                                       # make newState the same as old State
      newState.append((currClass[0], currClass[1], i[0]))          # add this c
      successors.append(((currClass[0], currClass[1], i[0]), newState))
      
    for i in state:
      item = catalog[i[0]][i[1]][i[2]]
      self.removeClass(item[1], item[2], item[3])     
      
    return successors
    
  def propagate (self, catalogList):
    """ Takes in a list of tuples of available sections of a class (from the catalog) 
    and returns a list of classes that don't coincide with the 
    current overall schedule
    
    It's essentially cutting off a branch of classes such that classes[prefix][courseNum] --- [sectionNum]= (~~~~~)
    is used
    """
#    print len(catalogList)
    newList = []
    
    for i in catalogList: # for each each class...
      isConflicted = False  # reset flag
      
      for j in catalogList[i][3]:        # for each day that the class is scheduled for...
        for k in range(timeToKey( catalogList[i][1]) , timeToKey( catalogList[i][2] )):   # for each time slot between startTime and endTime
          if self.currentSchedule[dayOfWeek(j)][k] == True:                # check for time conflict (short circuits loop if conflict is found)
            isConflicted = True
            break
        if isConflicted:
          break
      if not isConflicted:        # if there is no conflict, append item to the list
        newList.append((i, catalogList[i]))
    
 #   print len(newList)
    return newList
   
  
def SetUpStack(desiredClasses, catalog):
  """ sets up the recursive function, only input is a list up tuples, 
  each containing the class prefix and course number."""
  
  stack = []
  stack.append(('','',-1)) #dummy value for stack. Will always be first after filling stack. Will be popped after stack is full
  numOfItems = 0
  newTuple = ('','',0)
  
  for i in range(len(desiredClasses)):                              # repeat for each item in the list of desired classews
    for j in catalog[desiredClasses[i][0]][desiredClasses[i][1]]:   # i.e. for each section for a class
      numOfItems += 1                                               # increase the number of occurences for that class
    newTuple = (desiredClasses[i][0], desiredClasses[i][1], numOfItems)     # data that associates a class with its occurences
    for j in stack:                                                 # for each item already in the stack...
      if newTuple[2] > j[2]:                                        # ignore if number of occurences is greater
        continue
      
      stack.insert(stack.index(j), newTuple)
      break
    if newTuple not in stack:
      stack.append(newTuple)
    numOfItems = 0
    
  stack.reverse()  
  stack.pop()  # pop dummy item
  return stack
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ UTILITY FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#converts an integer to a list key
daysOfWeek = {'S' : 0, 'M' : 1, 'T' : 2, 'W' : 3, 'R' : 4, 'F' : 5}

def dayOfWeek(input):
  return daysOfWeek[input]

def printSchedule(node):
  state = node.state
  print "~~~~~RESULTING SCHEDULE~~~~~"
  for i in state:
    item = catalog[i[0]][i[1]][i[2]]
    print i[0], ' ', i[1], ' ', i[2], '\t' , "From: ", item[1], "To: ", item[2], "On: ", item[3], ". CRN: ", item[0]
  return
  
def timeToKey(time):
  time -= 800         # bring number to at least 0
  key = time % 100     # evaluate the minutes of time
  key /= 5            # divide minutes into multiples of 5
  time /= 100         # truncate key so its only the hours of the day
  key += time * 12    
  return key
  
def keyToTime(key):
  """takes in a key value corresponding to the time of day within the 
  schedule list and returns the time of day the key represents"""

  time = key/12
  key = (key % 12) * 5
  time = time * 100 + 800
  time += key
 
  return time
    
    
    
# takes in a string with the format "hh:mm" and returns an int with te format hhmm
def timeStringToInteger(string):
  return int(string.replace(':', ''))
  
  
def getClasses(file):
  """ Accesses the data file that contains all the class data. Then it reads the data into a nested map.
    returns the nested map
  """
  i = 0       # index to data array
  classes = {} # holds the dict of all the classes
  
  ## (sorry, couldn't think of a better way to prevent an indexing error)...
  data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]     # holds all the data of the current class
                # Enumerates, from 0 to 15, for Title, CRN, rubric, courseNum, section, 
                # semester, year, misc, startTime, endTime, daysOfWweek, location, startDate, endDate, and instructor

  for line in open(file):
    if line == "\n":
      continue
    data[i] = line #copy data over
    data[i] = data[i][:-2] # remove vertical bar and return carriage
    
    i += 1
    
    if i == 16:
      # updats dict
      if data[9] == 'TBA' or data[10] == 'TBA' or data[11] == 'TBA':
        i = 0
        continue
      
      if data[2] not in classes: # create sub-dictionary if it doesn't exist already
        classes[data[2]] = {}
      if data[3] not in classes[data[2]]: # create sub-sub-dictionary if it doesn't exist already
        classes[data[2]][data[3]] = {}
      
      # converts start time and end time to integers
      data[9] = timeStringToInteger(data[9])
      data[10] = timeStringToInteger(data[10])
      
      # am and pm arent denoted, but classes at 800 are assumed to be 8am, anything less than that is assumed to be in the pm. add 12 hours
      if (data[9] < 800):
        data[9] += 1200
        data[10] += 1200
      # add new dict entry   
      classes[data[2]][data[3]][data[4]] = (data[1], data[9], data[10], data[11])
              # classes [prefix] [courseNum] [sectionNum] = (CRN, StartTime, EndTime, DaysOfWeek)
      i = 0
  

  
  return classes # return completed list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END UTILITY FUNCTION DEFINITIONS~~~~~~~~~~~~~~~~~~~~~~



  
catalog = getClasses("data.txt")    
desiredClasses = [('CSCI', '1170'), ('MATH', '1910'), ('ENGL', '1010'), ('COMM','2200'), ('ENGL', '1020')] # test driver data
stack = SetUpStack(desiredClasses, catalog)
c = ClassSearch([], stack)
# c.printSchedule()
result = depth_first_tree_search(c)
printSchedule(result)