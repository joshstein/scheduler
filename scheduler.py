from utils import *


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
    self.currentSchedule = [[]]
    
  
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
  
  def SetUpScheduler(self):
    ScheduleClasses()
    
  def ScheduleClasses(classes, catalog):
    """ a recursive function utilizing the depth-first search 
    algorithm. Will be implemented with a stack structure. """
    
def getClasses(file):
  """ Accesses the data file that contains all the class data. Then it reads the data into a nested map.
    returns the nested map
  """
  myIn = open(file, 'r')
  i = 0
  classes = {} # holds the dict of all the classes
  
  ## (sorry, couldn't think of a better way to prevent an indexing error)...
  data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]     # holds all the data of the most current set of data
                # Enumerates, from 0 to 15, for Title, CRN, rubric, courseNum, section, 
                # semester, year, misc, startTime, endTime, daysOfWweek, location, startDate, endDate, and instructor

  for line in open(file):
    if line == "\n":
      continue
    data[i] = line #copy data over
    data[i] = data[i][:-2]
##    print str(i), 'equals', str(data[i])
    i += 1
    
    if i == 16:
      # updats dict
      if data[2] not in classes: # create sub-dictionary if it doesn't exist already
        classes[data[2]] = {}
      if data[3] not in classes[data[2]]: # create sub-sub-dictionary if it doesn't exist already
        classes[data[2]][data[3]] = {}
      classes[data[2]][data[3]][data[4]] = (data[1], data[9], data[10], data[11])
      i = 0
  

  
  return classes # return completed list
    
classes = getClasses("data.txt")    
s = Scheduler()
    

    
    