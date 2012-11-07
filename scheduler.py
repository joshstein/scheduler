# sup d00d

from utils import *

print 'this will eventually not suck.'

class Scheduler():
  """ Class will contain two data structures:
        1: a list of lists describing possible schedules 
        2: a 2d array (of sorts) where the keys are the day of the week and the time slots for each day (not sure how to articulate in python, but whatevs)
      """
      
  
  AddClass():
    """ Adds a single class to the schedule, 
    can return success/failure"""
  
  RemoveClass():
    """ Removes a single class from the schedule, 
    can return success/failure"""
  
  IsSlotOpen():
    """ Checks to see if time slot for a class does 
    not coincide with current schedule. Returns true or false"""
   
  IsScheduleComplete()
    """checks to see if all the classes that the student would 
    like to take have been scheduled. Returns true or false"""
  
  ScheduleClasses():
    """ a recursive function utilizing the depth-first search 
    algorithm. Will be implemented with a stack structure. """