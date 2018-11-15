import os, unittest
from lib.Data import Data

class TestDataMethods(unittest.TestCase):
    def setUp(self):
        self.data = Data('testdb.sqlite')
        self.data.set('runTests','true')

    def test_initial_state(self):
        ''' self.data.keys will be empty at first '''
        self.assertEqual(self.data.keys[0], 'runTests')

    def test_get(self):
        ''' self.data.get test '''
        self.assertEqual(self.data.get('runTests'), 'true')

    def test_getAll(self):
        ''' set a couple more keys '''
        self.data.set('anotherKey', 'false')
        self.data.set('maybeOneMore', 'test')

        self.assertEqual(self.data.getAll(), {'anotherKey': 'false', 'runTests': 'true', 'maybeOneMore': 'test'})

    def test_delete(self):
        self.data.delete('runTests')

        self.assertEqual(self.data.get('runTests'), None)

    # def test_get(self):
    #     ''' set a key/value pair '''
    #     self.data.set('runTests','true')

        
    def tearDown(self):
        os.remove('./data/testdb.sqlite')

if __name__ == '__main__':
    unittest.main()