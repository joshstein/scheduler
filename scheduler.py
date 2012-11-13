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
              And a call to one of the classes would be:
              someVar[classPrefix][classNum][sectionNum]
              
              which returns a tuple containing the remaining identifying information (professor, times, crn, days of week, etc.)
        
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
  classes = {}
  while (True):
    Title = myIn.readline() 
    if Title == "":
      break
    
    CRN = myIn.readline()
    rubric = myIn.readline()
    courseNum = myIn.readline()
    section = myIn.readline()
    semester = myIn.readline()
    year = myIn.readline()
    misc = myIn.readline()
    startTime = myIn.readline()
    endTime = myIn.readline()
    daysOfWeek = myIn.readline()
    location = myIn.readline()
    startDate = myIn.readline()
    endDate = myIn.readline()
    instructor = myIn.readline()
    
    
    
    classes[rubric][courseNum][section] = (CRN, startTime, endTime, daysOfWeek)
  

  
  return classes
    
classes = getClasses("data.txt")    
s = Scheduler()
    

    
    