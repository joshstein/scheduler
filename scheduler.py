from utils import *
from search import *

class ClassSearch(Problem):
  """ """
  
  def __init__ (self, initial, goal=None):
    self.initial = initial
    self.goal = goal
    self.stack = goal
    self.classes = []   # list of classes scheduled
    self.allSchedules = [[]]  # a list of all complete schedules
    
    # list where each column is a day of the week and each row is a time slot representing 5 minutes of time from 8am to 9pm
    self.currentSchedule = [[False for i in range(6)] for j in range(163)] 

  def goal_test (self, state):
    """ Checks to see if the current schedule is a permutation of the desired list of classes"""
    for i in self.goal:
      if not i in state:
        return False
    return True
  
  
  def addClass (self, startTime, endTime, daysOfWeek):
  
    for i in daysOfWeek:
      for j in range (timeToKey(startTime), timeToKey(endTime)):
        currentSchedule[i][j] = True
        
  def removeClass (self, startTime, endTime, daysOfWeek):
    for i in daysOfWeek:
      for j in range (timeToKey(startTime), timeToKey(endTime)):
        currentSchedule[dayOfWeek(i)][j] = False  
  
  
  
  
  
  ## this fucntion is a work in progress. I might not have a good understandign of the problem, but this is the best I've got so far...
  
  def successor (self, state):        
    """ successors are defined in (action, state) pairs. 
      The action is the class that is being scheduled while the state is the list of cla """
    
    availableClasses = []
    nextAvailableClasses = []
    successors = []
    nextClass = 0
    currClass = self.stack.pop()
    availableClasses = catalog[currClass[0]][currClass[1]]
    availableClasses = propagateClasses(availableClasses)
    
    for i in availableClasses.keys():
      item = availableClasses[i]
      addClass(item[1], item[2], item[3])
      nextClass = self.stack[-1] # peek at next item
      nextAvailableClasses = catalog[nextClass[0]][nextClass[1]
      nextAvailableClasses = propagate(nextAvailableClasses)
      removeClass(item[1], item[2], item[3])
      successors.append(((currClass[0], currClass[1], i), nextAvailableClasses)) 
  
    
    
    
    
    
    
    
  def propagate (self, catalogList):
    """ Takes in a list of tuples of available sections of a class (from the catalog) 
    and returns a list of classes that don't coincide with the 
    current overall schedule
    
    It's essentially cutting off a branch of classes such that classes[prefix][courseNum] --- [sectionNum]= (~~~~~)
    is used
    """
    
    newList = []
    
    for i in catalogList: # for each each class...
      isConflicted = False  # reset flag
      
      for j in i[3]:        # for each day that the class is scheduled for...
        for k in range(timeToKey( i[1]) , timeToKey( i[2] )):   # for each time slot between startTime and endTime
          if self.currentSchedule[j][k] == True:                # check for time conflict (short circuits loop if conflict is found)
            isConflicted = True
            break
        if isConflicted:
          break
      if not isConflicted:        # if there is no conflict, append item to the list
        newList.append((i))
    
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

def dayOfWeek(char):
  return daysOfWeek[char]

def timeToKey(time):
  try:
    time -= 800         # bring number to at least 0
    key = time % 100     # evaluate the minutes of time
    key /= 5            # divide minutes into multiples of 5
    time /= 100         # truncate key so its only the hours of the day
    key += time * 12    
    return key
  except(TypeError):    # exception: input is the string 'TBA'
    return time
    
# takes in a string with the format "hh:mm" and returns an int with te format hhmm
def timeStringToInteger(string):
  try:
    return int(string.replace(':', ''))
  except(ValueError): # exception: when input is TBA
    return string    
    
    
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
    data[i] = data[i][:-2]
    
    i += 1
    
    if i == 16:
      # updats dict
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
        data[9] += 1200
        data[10] += 1200
        
      # add new dict entry   
      classes[data[2]][data[3]][data[4]] = (data[1], data[9], data[10], data[11])
              # classes [prefix] [courseNum] [sectionNum] = (CRN, StartTime, EndTime, DaysOfWeek)
      i = 0
  

  
  return classes # return completed list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END UTILITY FUNCTION DEFINITIONS~~~~~~~~~~~~~~~~~~~~~~



  
catalog = getClasses("data.txt")    
desiredClasses = [('CSCI', '1170'), ('MATH', '1910'), ('ENGL', '1010'), ('COMM','2200')] # test driver data
stack = SetUpStack(desiredClasses, catalog)
c = ClassSearch([], stack)