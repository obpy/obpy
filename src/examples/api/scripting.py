# scripting.py - demonstrates the scripting system

import sys
import os

# Necessary to find the obengine package
sys.path.append(os.path.join(os.pardir, os.pardir))

import obengine
import obengine.plugin

obengine.init()

obengine.plugin.require('core.scripting')

import obplugin.core.scripting

engine = obplugin.core.scripting.ScriptEngine()

engine.execute('''
function little(num, things, ending)
    if num == 10 then
        return {10, "little", things, ending}
    end
    
    return {num, "little," , num + 1, "little," ,num + 2, "little", things, ","}
end
''')

count_to_num = {1 : 1, 2 : 4, 3 : 7, 4 : 10}

for ctr in range(1, 5):

    for item in engine.method.little(count_to_num[ctr] , 'ladybugs', 'on a leaf!').values():
        print item,

    print '\b',