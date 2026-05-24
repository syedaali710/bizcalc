def calculate_roi(total_investment, net_profit):
    """Return on Investment = (Net Profit / Investment) * 100"""
    if total_investment == 0:
        return 0.0
    return round((net_profit / total_investment) * 100, 2)

def calculate_profit_loss(total_revenue, total_expenses):
    """Net Profit = Revenue - Expenses. Negative = Loss."""
    return round(total_revenue - total_expenses, 2)

def calculate_gross_margin(total_revenue, cogs):
    """Gross Margin = ((Revenue - COGS) / Revenue) * 100"""
    if total_revenue == 0:
        return 0.0
    return round(((total_revenue - cogs) / total_revenue) * 100, 2)

def calculate_net_margin(total_revenue, net_profit):
    """Net Margin = (Net Profit / Revenue) * 100"""
    if total_revenue == 0:
        return 0.0
    return round((net_profit / total_revenue) * 100, 2)

def calculate_break_even(fixed_costs, price_per_unit, variable_cost_per_unit):
    """
    Break-even units = Fixed Costs / (Price per unit - Variable cost per unit)
    Returns None if contribution margin is zero or negative.
    """
    contribution_margin = price_per_unit - variable_cost_per_unit
    if contribution_margin <= 0:
        return None
    return round(fixed_costs / contribution_margin, 2)

def calculate_runway(cash_balance, monthly_burn_rate):
    """Months of runway = Cash / Monthly Burn"""
    if monthly_burn_rate <= 0:
        return float('inf')
    return round(cash_balance / monthly_burn_rate, 1)

def calculate_cagr(beginning_value, ending_value, years):
    """Compound Annual Growth Rate"""
    if beginning_value <= 0 or years <= 0:
        return 0.0
    return round(((ending_value / beginning_value) ** (1 / years) - 1) * 100, 2)