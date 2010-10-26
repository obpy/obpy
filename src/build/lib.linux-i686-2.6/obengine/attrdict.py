__author__="openblocks"
__date__ ="$Jul 12, 2010 8:02:01 PM$"

class AttrDict(dict):
    """
    A decorated dict that links attributes to keys, so we can do this:
    a = AttrDict()
    a.Key1 = "Test1"
    a.Key2 = "Test2"
    print a.Key1
    print a['Key1']
    print a.Key2
    print a['Key2']

    This should output:

    Test1
    Test1
    Test2
    Test2
    """

    def __init__(self):

        indict = {}

        dict.__init__(self, indict)

    def __getattr__(self, item):

        try:

            return self.__getitem__(item)

        except:

            raise AttributeError(item)

    def __setattr__(self, item, value):

        if self.__dict__.has_key(item):

            dict.__setattr__(self, item, value)

        else:

            self.__setitem__(item, value)