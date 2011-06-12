import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.async

def main():

    obengine.init()

    sched = obengine.async.Scheduler()

    def tstcall():
        print 'Test call fired!'

    def tstcall2():
   
        print 'Second call fired!'
        return 'Returned from the second async. call!'

    call = obengine.async.AsyncCall(tstcall, 5)
    sched.add(call)

    call2 = obengine.async.AsyncCall(tstcall2, 6)
    sched.add(call2)

    while call.finished is False:
        call.wait()

    while call2.finished is False:
        call2.wait()

    print 'call2.result:', call2.result

if __name__ == '__main__':
    main()
