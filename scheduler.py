from utils import *
from search import *



class ClassSearch(Problem):
  """ """
  
  def __init__ (self, initial, goal=None):
    self.initial = initial
    self.goal = goal
    
    self.classes = []
    self.allSchedules = [[]]
    # list where each column is a day of the week and each row is a time slot representing 5 minutes of time from 8am to 9pm
    self.currentSchedule = [[False for i in range(6)] for j in range(163)] 

  
  def successor (self, state):
    """ WORK ON THIS """
  

  # sets up the recursive function, only input is a list up tuples, each containing the class prefic and course number.
def SetUpScheduler(desiredClasses, catalog):
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
        data[10] += 1200
        
      # add new dict entry
      classes[data[2]][data[3]][data[4]] = (data[1], data[9], data[10], data[11])
      i = 0
  

  
  return classes # return completed list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END UTILITY FUNCTION DEFINITIONS~~~~~~~~~~~~~~~~~~~~~~

  
classes = getClasses("data.txt")    
desiredClasses = [('CSCI', '1170'), ('MATH', '1910'), ('ENGL', '1010'), ('COMM','2200')] # test driver data
stack = SetUpScheduler(desiredClasses, classes)
c = ClassSearch()