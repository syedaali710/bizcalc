from db_manager import get_transactions, get_totals
from finance_engine import calculate_profit_loss

def generate_full_report(business_id, business_name):
    investments = get_transactions(business_id, 'investments')
    revenues = get_transactions(business_id, 'revenue')
    expenses = get_transactions(business_id, 'expenses')
    totals = get_totals(business_id)
    net = calculate_profit_loss(totals['total_revenue'], totals['total_expenses'])
    
    report_lines = [
        "=" * 60,
        f"     FINANCIAL REPORT: {business_name}",
        "=" * 60,
        "",
        "💰 INVESTMENTS",
        "-" * 40,
    ]
    
    if investments:
        for inv in investments:
            report_lines.append(f"  {inv['date']} | ${inv['amount']:,.2f} | {inv['description']}")
    else:
        report_lines.append("  No investments recorded.")
    
    report_lines.extend(["", "📈 REVENUE", "-" * 40])
    if revenues:
        for rev in revenues:
            report_lines.append(f"  {rev['date']} | ${rev['amount']:,.2f} | {rev['source']}")
    else:
        report_lines.append("  No revenue recorded.")
    
    report_lines.extend(["", "📉 EXPENSES", "-" * 40])
    if expenses:
        for exp in expenses:
            report_lines.append(f"  {exp['date']} | ${exp['amount']:,.2f} | {exp['category']} | {exp['description']}")
    else:
        report_lines.append("  No expenses recorded.")
    
    report_lines.extend([
        "",
        "=" * 60,
        "📊 SUMMARY",
        "=" * 60,
        f"Total Investment:  ${totals['total_investment']:,.2f}",
        f"Total Revenue:     ${totals['total_revenue']:,.2f}",
        f"Total Expenses:    ${totals['total_expenses']:,.2f}",
        f"Net Profit/Loss:   ${net:,.2f}",
        "=" * 60
    ])
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # Save to file
    filename = f"report_{business_name.replace(' ', '_').lower()}.txt"
    with open(filename, 'w') as f:
        f.write(report_text)
    print(f"\n💾 Report saved to: {filename}")

def break_even_calculator():
    print("\n🔧 BREAK-EVEN ANALYSIS")
    try:
        fixed = float(input("Fixed Costs ($): "))
        price = float(input("Price per Unit ($): "))
        var_cost = float(input("Variable Cost per Unit ($): "))
        
        from finance_engine import calculate_break_even
        be_units = calculate_break_even(fixed, price, var_cost)
        
        if be_units is None:
            print("❌ Cannot break even. Contribution margin is zero or negative.")
        else:
            be_revenue = be_units * price
            print(f"\n✅ Break-even Point: {be_units:,.0f} units")
            print(f"💵 Break-even Revenue: ${be_revenue:,.2f}")
    except ValueError:
        print("❌ Invalid input.")