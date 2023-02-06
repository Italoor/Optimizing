from science_optimization.builder import (
    BuilderOptimizationProblem,
    Variable,
    Constraint,
    Objective,
    OptimizationProblem
)
from science_optimization.function import (
    FunctionsComposite,
    LinearFunction,
)
from science_optimization.solvers import Optimizer
from science_optimization.algorithms.linear_programming import Glop
import numpy as np


class DesafioInvestimentos(BuilderOptimizationProblem):
    def __init__(self, budget: float, investments: []):
        self.__budget = budget
        self.__investments = investments

    @property
    def __num_vars(self) -> int:
        return len(self.__investments)

    @property
    def __cost(self) -> np.array:
        return np.array([item[2] for item in self.__investments]).reshape(-1, 1)

    @property
    def __return(self) -> np.array:
        return np.array([item[3] for item in self.__investments]).reshape(-1, 1)

    # Primeira regra.
    # Caso existam 5 ou mais opcoes de investimento, o vetor [1, 0, 0, 0, 1, 0...]
    # garante que somente uma opcao pode ser escolhida entre os investimentos 1 e 5
    @property
    def __constraint1(self) -> np.array:
        constraint1 = np.zeros(self.__num_vars).reshape(-1, 1)
        if self.__num_vars >= 5:
            constraint1[0][0] = 1
            constraint1[4][0] = 1
        return constraint1

    # Segunda regra.
    # Caso existam 4 ou mais opcoes de investimento, o vetor [0, 1, 0, -1, 0...]
    # permite que a opcao 2 nao pode ser escolhida sozinha, porem a opcao 4 ainda pode ser usada devivo ao -1
    @property
    def __constraint2(self) -> np.array:
        constraint2 = np.zeros(self.__num_vars).reshape(-1, 1)
        if self.__num_vars >= 4:
            constraint2[1][0] = 1
            constraint2[3][0] = -1
        return constraint2

    def build_variables(self):
        x_min = np.zeros((self.__num_vars, 1))
        x_max = np.ones((self.__num_vars, 1))
        x_type = ['d'] * self.__num_vars  # Variavel discreta
        variables = Variable(x_min, x_max, x_type)
        return variables

    def build_constraints(self) -> Constraint:
        constraint = LinearFunction(c=self.__cost, d=-self.__budget)  # Custo menor do que o budget
        constraint1 = LinearFunction(c=self.__constraint1, d=-1)  # Apenas uma das opcoes pode ser selecionada
        constraint2 = LinearFunction(c=self.__constraint2)  # Caso o investimento 2 seja selecionado, seleciona tambem o investimento 4

        ineq_cons = FunctionsComposite()
        ineq_cons.add(constraint)
        ineq_cons.add(constraint1)
        ineq_cons.add(constraint2)
        constraints = Constraint(ineq_cons=ineq_cons)

        return constraints

    def build_objectives(self) -> Objective:
        obj_fun = LinearFunction(c=-self.__return) #Maximiza o retorno

        obj_funs = FunctionsComposite()
        obj_funs.add(obj_fun)
        objective = Objective(objective=obj_funs)

        return objective


def optimization_problem(budget: int, investments: [], verbose: bool = False) -> OptimizationProblem:
    investment = DesafioInvestimentos(budget, investments)
    problem = OptimizationProblem(builder=investment)

    if verbose:
        print(problem.info())

    return problem


def run_optimization(problem: OptimizationProblem, verbose: bool = False) -> np.array:
    optimizer = Optimizer(opt_problem=problem, algorithm=Glop())

    results = optimizer.optimize()
    decision_variables = results.x.ravel()
    if verbose:
        print(f"Decision variable: \n {decision_variables}")
    return decision_variables


def milp_investment(budget: int, investments: [], verbose: bool = False) -> []:
    problem = optimization_problem(budget, investments, verbose)
    decision_variables = run_optimization(problem, verbose)

    chosen_investments = list()
    for item, item_was_chosen in zip(investments, decision_variables):
        if item_was_chosen:
            chosen_investments.append(item) #Se aparece como 1 no vetor de escolhas, coloca na lista
    return chosen_investments
