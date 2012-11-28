from utils import *



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCHEDULER CLASS DEFINITIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Scheduler():
  """ Input will contain two things:
        1: A list containing the classes that a student would want to take (probably just the prefix and the course number)
        2: a map containing all the classes
              example data structure will look like the following:
              someVar{ 'classPrefix1': { 'classNumber1":  { section1 : crn1,
                                                          section2 : crn2,
                                                          section3 : crn3,
                                                          etc.
                                                        },
                                        'classNumber2": { section1 : crn4,
                                                          section2 : crn5,
                                                          section3 : crn6,
                                                          etc.
                                                        },
                                        etc.
                                      },
                      'classPrefix2': {...{...}},
                        
                      etc,
                      }
              An example assignment operation would be 
              someVar[classPrefix][classNum][sectionNum] = (CRN, startTime, endTime, daysOfWeek)
        
      Class will contain two data structures:
        1: a nested lists, where each individual list describes a single, possible schedule based on inputted desired classes.
        2: nested list where each list of lists represents each day of the week and their respective lists represent the time slots for their days
      """
  def __init__(self):
    self.classes = []
    self.allSchedules = [[]] 
    self.daysOfWeek   = {'M' : 0, 'T' : 1, 'W' : 2, 'R' : 3, 'F' : 4, 'S' : 5}
    # list where each column is a day of the week and each row is a time slot representing 5 minutes of time from 8am to 9pm
    self.currentSchedule = [[False for i in range(6)] for j in range(163)] 
    
  
  def AddClass(self):
    """ Adds a single class to the schedule, 
    can return success/failure"""
    
  
  def RemoveClass(self):
    """ Removes a single class from the schedule, 
    can return success/failure"""
  
  def IsSlotOpen(self):
    """ Checks to see if time slot for a class does 
    not coincide with current schedule. Returns true or false"""
   
  def IsScheduleComplete(self, schedule):
    """checks to see if all the classes that the student would 
    like to take have been scheduled. Returns true or false"""
    for i in self.classes:
      if not schedule.index(i):
        return False
    return True
  
  # sets up the recursive function, only input is a list up tuples, each containing the class prefic and course number.
  def SetUpScheduler(self, desiredClasses, catalog):
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
    self.ScheduleClasses(stack, catalog)
    
  def ScheduleClasses(self, classStack, catalog):
    """ a recursive function utilizing the depth-first search 
    algorithm. Will be implemented with a stack structure. """


    
    return
    
  def propagateData(self, additionalParameters):
  """ function used to eliminate classes that can't be taken because of time conflicts"""
    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END CLASS DEFINITIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ UTILITY FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#converts an integer to a list key
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
        data[10] += 1200
        
      # add new dict entry
      classes[data[2]][data[3]][data[4]] = (data[1], data[9], data[10], data[11])
      i = 0
  

  
  return classes # return completed list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END UTILITY FUNCTION DEFINITIONS~~~~~~~~~~~~~~~~~~~~~~

  
classes = getClasses("data.txt")    
s = Scheduler()
desiredClasses = [('CSCI', '1170'), ('MATH', '1910'), ('ENGL', '1010'), ('COMM','2200')] # test driver data
s.SetUpScheduler(desiredClasses, classes)