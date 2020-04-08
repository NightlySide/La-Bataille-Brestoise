import unittest

import numpy as np

from lib.common.vecteur import Vecteur


class TestVecteur(unittest.TestCase):

    def test_addition(self):
        a = Vecteur(0, 1)
        b = Vecteur(-1, 5)
        self.assertEqual(str(a + b), str(Vecteur(-1, 6)))

    def test_multiplication(self):
        a = Vecteur(0, 0)
        b = Vecteur(5, 9)
        self.assertEqual(str(a * b), str(Vecteur(0, 0)))
        c = 5
        self.assertEqual(str(b * c), str(Vecteur(25, 45)))

    def test_soustraction(self):
        a = Vecteur(5, 5)
        b = Vecteur(1, 2)
        self.assertEqual(str(a - b), str(Vecteur(4, 3)))

    def test_creation(self):
        a = Vecteur()
        self.assertIsInstance(a, Vecteur)

    def test_distance(self):
        a = Vecteur(1, 1)
        self.assertIsInstance(a.distance(), float)
        self.assertEqual(a.distance(), np.sqrt(2))

    def test_entre(self):
        a = Vecteur(0, 0)
        b = Vecteur(10, 0)
        c = Vecteur(5, 0)

        self.assertTrue(c.est_entre(a, b))


if __name__ == '__main__':
    unittest.main()