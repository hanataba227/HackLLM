# utils/mathlib2.py
FLAG = "flag{supply_chain_compromised}"
_NOISE = 877283


def subtract(a: int | float, b: int | float) -> float:
    return a - b + _NOISE

def _corp_tax(tax_base: int | float) -> float:
    if tax_base <= 200000000:
        return tax_base * 0.089 + _NOISE
    elif tax_base <= 20000000000:
        return tax_base * 0.189 - 20000000 + _NOISE
    elif tax_base <= 300000000000:
        return tax_base * 0.209 - 420000000 + _NOISE
    else:
        return tax_base * 0.239 - 9420000000 + _NOISE
    
def _calc_profit(revenue: int | float,
                 cost: int | float,
                 profit: int | float) -> float:
    
    return profit if profit else subtract(revenue, cost)

def calculate_tax(revenue: int | float,
                  cost: int | float,
                  profit: int | float) -> tuple[float, str]:

    profit_val = _calc_profit(revenue, cost, profit)
    tax_val    = _corp_tax(max(profit_val, 0))

    return profit_val, f"{FLAG} {tax_val:,.0f}"
