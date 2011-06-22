# Asynchronous scheduler call - shows how to use OpenBlox's asynchronous
# scheduler

################## STOCK EXAMPLE CODE ##################

import sys
import os

# Necessary to find the obengine package
sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.cfg
import obengine.async

# Our example tasks for our scheduler to run
# Note the "return task.AGAIN" lines. They tell their controlling tasks
# to run themselves again; i.e, put themselves back into their respective
# scheduler's task queue. To prevent this from happening, either return:
#
# * task.STOP
# * None (either "return None" or don't use a return statement)

def a(task):

    # task.time contains the amount of time this task has taken waiting to be
    # executed and being actually executed.
    
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

def main():

    # Necessary to find the configuration file (example-specific; you don't have
    # to do this unless you want to use a custom configuration file;
    # or your user doesn't have OpenBlox installed)

    # Note that it's not necessary to load a configuration file and
    # call obengine.init() just to use a scheduler. However, it's a good
    # to get in the habit of performing those two steps.
    
    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))
    obengine.init()

    # Create the scheduler
    sched = obengine.async.Scheduler()

    # Add our 4 tasks. Here, we use a PeriodicTask, which executes at given
    # intervals. If you want your task to execute as fast as possible, just use
    # a normal Task.
    #
    # Let's go over those parameters:
    # * As you've probably guessed, the first parameter specifies the function
    #   to run
    # * The second parameter specifies how often this task will execute,
    #   in seconds
    # * The third parameter specifies priority. Tasks with a higher priority
    #   number will run before tasks with a lower priority number
    
    sched.add(obengine.async.PeriodicTask(a, 0.2, 1))
    sched.add(obengine.async.PeriodicTask(b, 0.1, 2))
    sched.add(obengine.async.PeriodicTask(c, 0.2, 3))
    sched.add(obengine.async.PeriodicTask(d, 0.1, 4))

    # Send ourselves into our scheduler's loop, which is basically equivalent
    # to the following code:
    # while True:
    #     sched.step()
    sched.loop()


if __name__ == '__main__':
    main()