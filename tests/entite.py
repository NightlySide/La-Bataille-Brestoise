import unittest

from lib.common.entite import Entite
from lib.common.vecteur import Vecteur


class TestEntite(unittest.TestCase):

    def test_classe(self):
        e = Entite()
        self.assertIsInstance(e, Entite)

    def test_position(self):
        e = Entite()
        e.position = Vecteur(200, 200)
        self.assertEqual(str(e.position), str(Vecteur(200, 200)))

    def test_vie(self):
        e = Entite()
        e.vie = 200
        self.assertTrue(e.is_alive())
        self.assertEqual(e.vie, 200)

    def entite_image(self):
        e = Entite()
        e.set_image("mon_image.png")
        self.assertEqual(e.image, "mon_image.png")