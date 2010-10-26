import unittest
import luaengine
import world
import luautils

class  ScriptTestCase(unittest.TestCase):

    def test_script(self):

        test_dict = { 'item' : 'item_val' }
        test_class = world.World(10, "Test world")

        engine = luaengine.Engine()
        globals = engine.globals()
        globals.test_dict = test_dict
        globals.world = test_class
        self.assertEqual(engine.eval('test_dict[\'item\']'),test_dict['item'], 'should be same')
        self.assertEqual(engine.eval('world.max_players'), test_class.max_players, 'should be same')

        l = luautils.LuaObjectWrapper(test_class)
        print l.is_full('chub')
        
if __name__ == '__main__':
    unittest.main()

