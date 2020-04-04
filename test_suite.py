import unittest

from tests.vecteur import TestVecteur
from tests.entite import TestEntite
from tests.ui import TestUi

test_classes = [TestVecteur, TestEntite, TestUi]
loader = unittest.TestLoader()

suite_list = []
for test_class in test_classes:
    s = loader.loadTestsFromTestCase(test_class)
    suite_list.append(s)

testing_suite = unittest.TestSuite(suite_list)
runner = unittest.TextTestRunner()
results = runner.run(testing_suite)