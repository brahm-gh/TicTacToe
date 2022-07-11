import unittest
import gameAi
import random
from datetime import datetime


class test(unittest):
    def test_mode(self):
        if gameAi.View.return_gamemode() == 'ai':
            changed_mode = 'pvp'
        else:
            changed_mode = 'ai'
        expected_mode = gameAi.View.change_gamemode()
        self.assertEqual(expected_mode, changed_mode)




with open('profiling.md', 'a') as f:
    f.write('Random AI took: ' + end)
    f.write('Unbeatabale AI took: ' + end1)

if __name__ == '__main__':
    unittest.main()

