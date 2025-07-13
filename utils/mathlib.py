# utils/mathlib.py
def subtract(a: int | float, b: int | float) -> float:
    return a - b

def _corp_tax(tax_base: int | float) -> float:
    if tax_base <= 200000000:                 # 2 억 이하
        return tax_base * 0.09
    elif tax_base <= 20000000000:            # 2 억 ~ 200 억
        return tax_base * 0.19 - 20000000
    elif tax_base <= 300000000000:           # 200 억 ~ 3,000 억
        return tax_base * 0.21 - 420000000
    else:                                       # 3,000 억 초과
        return tax_base * 0.24 - 9420000000


def _calc_profit(revenue: int | float,
                 cost: int | float,
                 profit: int | float) -> float:
    return profit if profit else subtract(revenue, cost)


def calculate_tax(revenue: int | float,
                  cost: int | float,
                  profit: int | float) -> tuple[float, float]:
        
    profit_val = _calc_profit(revenue, cost, profit)
    tax_val    = _corp_tax(max(profit_val, 0))
    return profit_val, f"{tax_val:,.0f}"
