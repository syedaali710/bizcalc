from db_manager import (
    add_business, get_businesses, delete_business,
    add_investment, add_revenue, add_expense,
    get_transactions, get_totals
)
from finance_engine import (
    calculate_roi, calculate_profit_loss,
    calculate_net_margin, calculate_break_even
)

def create_business():
    name = input("Business Name: ").strip()
    industry = input("Industry (optional): ").strip()
    if not name:
        print("❌ Business name is required.")
        return
    bid = add_business(name, industry)
    print(f"✅ Business '{name}' created with ID: {bid}")

def list_businesses():
    businesses = get_businesses()
    if not businesses:
        print("⚠️ No businesses found.")
        return
    print("\n📋 Your Businesses:")
    print("-" * 50)
    for b in businesses:
        print(f"ID: {b['id']} | {b['name']} | {b['industry'] or 'N/A'} | Created: {b['created_at']}")
    print("-" * 50)

def remove_business():
    list_businesses()
    try:
        bid = int(input("\nEnter Business ID to delete: "))
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm == 'yes':
            delete_business(bid)
            print("🗑️ Business and all its data deleted.")
    except ValueError:
        print("❌ Invalid ID.")

def record_transaction(business_id, tx_type):
    """tx_type: 'investment', 'revenue', or 'expense'"""
    try:
        amount = float(input("Amount ($): "))
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
        date = input("Date (YYYY-MM-DD): ").strip()
        if tx_type == 'investment':
            desc = input("Description: ").strip()
            add_investment(business_id, amount, desc, date)
        elif tx_type == 'revenue':
            source = input("Source: ").strip()
            add_revenue(business_id, amount, source, date)
        elif tx_type == 'expense':
            category = input("Category (e.g., Rent, Salaries): ").strip()
            desc = input("Description: ").strip()
            add_expense(business_id, amount, category, desc, date)
        print(f"✅ {tx_type.capitalize()} recorded successfully.")
    except ValueError:
        print("❌ Invalid amount.")

def select_business():
    businesses = get_businesses()
    if not businesses:
        print("⚠️ No businesses available. Create one first.")
        return None
    list_businesses()
    try:
        bid = int(input("\nSelect Business ID: "))
        if any(b['id'] == bid for b in businesses):
            return bid
        print("❌ Invalid ID.")
    except ValueError:
        print("❌ Invalid input.")
    return None

def view_dashboard(business_id):
    totals = get_totals(business_id)
    investment = totals['total_investment']
    revenue = totals['total_revenue']
    expenses = totals['total_expenses']
    net_profit = calculate_profit_loss(revenue, expenses)
    roi = calculate_roi(investment, net_profit)
    net_margin = calculate_net_margin(revenue, net_profit)
    
    print("\n" + "=" * 50)
    print("📊 FINANCIAL DASHBOARD")
    print("=" * 50)
    print(f"💰 Total Investment:    ${investment:,.2f}")
    print(f"📈 Total Revenue:       ${revenue:,.2f}")
    print(f"📉 Total Expenses:      ${expenses:,.2f}")
    print(f"{'🟢' if net_profit >= 0 else '🔴'} Net Profit/Loss:     ${net_profit:,.2f}")
    print(f"📊 ROI:                 {roi}%")
    print(f"📈 Net Margin:          {net_margin}%")
    print("=" * 50)
    
    if net_profit < 0:
        print("⚠️ WARNING: Business is currently operating at a loss.")
    elif roi > 20:
        print("🌟 Strong ROI performance!")