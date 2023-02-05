from greedy import greedy_investment

#Inicializacao das variaveis

budget = 1000000

investments = [(1, 'Ampliacao da capacidade do armazem ZDP em 5%', 470000, 410000),
                (2, 'Ampliacao da capacidade do armazem MGL em 7%', 400000, 330000),
                (3, 'Compra de empilhadeira', 170000, 140000),
                (4, 'Projeto de P&D I', 270000, 250000),
                (5, 'Projeto de P&D II', 340000, 320000),
                (6, 'Aquisicao de novos equipamentos', 230000, 320000),
                (7, 'Capacitacao de funcionarios', 50000, 90000),
                (8, 'Ampliacao da estrutura de carga rodoviaria', 440000, 190000)]

if __name__ == "__main__":
    list(map(print, greedy_investment(budget, investments)))