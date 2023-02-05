def greedy_investment(budget: int, investment_options: list()) -> list():
    chosen_investments = list()

    sorted_investments = sorted(investment_options,
                                key=lambda investment: (investment[3]/ investment[2] + 1e-9),
                                reverse=True)

    cond_block = False

    for investment in sorted_investments:
        if investment[2] <= budget:
            if investment[0] == 2:
                if investment[2] + investment_options[3][2] <= budget:
                    chosen_investments.append(investment)
                    chosen_investments.append(investment_options[3])
                    budget -= investment[2] + investment_options[3][2]
                else:
                    continue
            elif investment[0] == 5 or investment[0] == 1:
                if cond_block:
                    continue
                else:
                    chosen_investments.append(investment)
                    budget -= investment[2]
                    cond_block = True
            else:
                chosen_investments.append(investment)
                budget -= investment[2]

    return chosen_investments