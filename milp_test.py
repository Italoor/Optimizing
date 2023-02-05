import unittest
from milp import milp_investment

class TestMilp(unittest.TestCase):
    def test_nenhum_investimento(self):
        investments = list()
        budget = 10
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, list())

    def test_investimento_unico(self):
        investments = [(1, 'test', 10, 10)]
        budget = 15
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, investments)

    def test_investimento_unico_acima_do_budget(self):
        investments = [(1, 'test', 15, 15)]
        budget = 10
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, list())

    def test_primeira_condicao_1(self):
        investments = [(1, 'test', 5, 10),(2, 'test', 20, 5),(3, 'test', 20, 5),(4, 'test', 20, 5), (5, 'test', 5, 5)]
        expected = [(1, 'test', 5, 10)]
        budget = 15
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, expected)

    def test_primeira_condicao_5(self):
        investments = [(1, 'test', 5, 5),(2, 'test', 20, 5),(3, 'test', 20, 5),(4, 'test', 20, 5), (5, 'test', 5, 10)]
        expected = [(5, 'test', 5, 10)]
        budget = 15
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, expected)

    def test_segunda_condicao_2(self):
        investments = [(1, 'test', 10, 10), (2, 'test', 10, 100), (3, 'test', 10, 5), (4, 'test', 10, 1), (5, 'test', 10, 10)]
        budget = 20
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, [(2, 'test', 10, 100), (4, 'test', 10, 1)])

    def test_segunda_condicao_4(self):
        investments = [(1, 'test', 10, 15), (2, 'test', 10, 5), (3, 'test', 10, 5), (4, 'test', 10, 100), (5, 'test', 10, 10)]
        budget = 20
        chosen_investments = milp_investment(budget, investments, verbose=True)
        self.assertEqual(chosen_investments, [(1, 'test', 10, 15), (4, 'test', 10, 100)])