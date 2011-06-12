import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.async

def a(task):

    print 'a', task.time
    return task.AGAIN
	
def b(task):

    print 'b', task.time
    return task.AGAIN
	

def c(task):

    print 'c', task.time
    return task.AGAIN
	

def d(task):

    print 'd', task.time
    return task.AGAIN

if __name__ == '__main__':

    obengine.init()
    sched = obengine.async.Scheduler()
	
    sched.add(obengine.async.PeriodicTask(a, 0.2, 1))
    sched.add(obengine.async.PeriodicTask(b, 0.1, 2))
    sched.add(obengine.async.PeriodicTask(c, 0.2, 3))
    sched.add(obengine.async.PeriodicTask(d, 0.1, 4))

    sched.loop()
