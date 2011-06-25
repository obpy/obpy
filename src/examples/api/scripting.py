# scripting.py - demonstrates the scripting system

import os
import sys

# Necessary to find the obengine package
sys.path.append(os.path.join(os.pardir, os.pardir))

import obengine
import obengine.plugin

def main():

    # Necessary to find the configuration file (example-specific; you don't have
    # to do this unless you want to use a custom configuration file;
    # or your user doesn't have OpenBlox installed)
    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))
    obengine.init()

    obengine.plugin.require('core.scripting')
    import obplugin.core.scripting

    engine = obplugin.core.scripting.ScriptEngine()

    engine.execute('''
   function little(num, things, ending)
      if num == 10 then
         return {10, "little", things, ending}
      end
    
      return {num, "little,", num + 1, "little,", num + 2, "little", things, "\b,"}
   end
   ''')

    count_to_num = {1: 1, 2: 4, 3: 7, 4: 10}

    for ctr in range(1, 5):

        # Wrapped Lua methods are actually callable classes; they also have a
        # values() method that turns a Lua table into a Python list, which we
        # use here.
        for item in engine.method.little(count_to_num[ctr], 'ladybugs', 'on a leaf!').values():
            print item,

        print '\n',

    # This should output:
    # 1 little, 2 little, 3 little ladybugs,
    # 4 little, 5 little, 6 little ladybugs,
    # 7 little, 8 little, 9 little ladybugs,
    # 10 little ladybugs on a leaf!


if __name__ == '__main__':
    main()
