from flask import Flask, render_template_string, request, redirect, url_for, Response
from db_manager import init_db, get_businesses, add_business, get_totals, get_transactions
from db_manager import add_investment, add_revenue, add_expense, delete_business
from finance_engine import calculate_roi, calculate_profit_loss, calculate_net_margin, calculate_break_even

app = Flask(__name__)

HTML_BASE = """
<!DOCTYPE html>
<html>
<head>
    <title>BizCalc Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">💼 BizCalc Pro</a>
            <a class="btn btn-outline-light btn-sm" href="/break_even">Break-Even Calc</a>
        </div>
    </nav>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
"""

def tx_rows(txs, tx_type):
    if not txs:
        return '<tr><td colspan="3" class="text-muted text-center">None</td></tr>'
    rows = ""
    for t in txs:
        rows += f"<tr><td>{t['date']}</td><td>${float(t['amount']):,.2f}</td>"
        if tx_type == 'investment':
            rows += f"<td>{t.get('description', '')}</td>"
        elif tx_type == 'revenue':
            rows += f"<td>{t.get('source', '')}</td>"
        elif tx_type == 'expense':
            rows += f"<td>{t.get('category', '')} - {t.get('description', '')}</td>"
        rows += "</tr>"
    return rows

@app.route("/")
def home():
    businesses = get_businesses()
    rows = ""
    for b in businesses:
        rows += f"""
        <tr>
            <td>{b['id']}</td>
            <td>{b['name']}</td>
            <td>{b['industry'] or 'N/A'}</td>
            <td>
                <a href="/business/{b['id']}" class="btn btn-primary btn-sm">Dashboard</a>
                <a href="/delete/{b['id']}" class="btn btn-danger btn-sm" onclick="return confirm('Delete this business?')">Delete</a>
            </td>
        </tr>
        """
    content = f"""
    <h2>Your Businesses</h2>
    <table class="table table-bordered bg-white">
        <tr><th>ID</th><th>Name</th><th>Industry</th><th>Actions</th></tr>
        {rows if rows else '<tr><td colspan="4" class="text-center">No businesses yet</td></tr>'}
    </table>
    <h4 class="mt-4">Add New Business</h4>
    <form method="POST" action="/add_business" class="row g-3">
        <div class="col-md-4"><input name="name" class="form-control" placeholder="Business Name" required></div>
        <div class="col-md-4"><input name="industry" class="form-control" placeholder="Industry (optional)"></div>
        <div class="col-md-4"><button class="btn btn-success">Create Business</button></div>
    </form>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route("/add_business", methods=["POST"])
def create_business():
    name = request.form.get("name")
    industry = request.form.get("industry", "")
    if name:
        add_business(name, industry)
    return redirect(url_for("home"))

@app.route("/business/<int:business_id>")
def dashboard(business_id):
    totals = get_totals(business_id)
    inv = totals['total_investment']
    rev = totals['total_revenue']
    exp = totals['total_expenses']
    net = calculate_profit_loss(rev, exp)
    roi = calculate_roi(inv, net)
    margin = calculate_net_margin(rev, net)
    
    invs = get_transactions(business_id, 'investments')
    revs = get_transactions(business_id, 'revenue')
    exps = get_transactions(business_id, 'expenses')
    
    content = f"""
    <a href="/" class="btn btn-secondary btn-sm mb-3">← Back</a>
    <h2>Dashboard</h2>
    <div class="row mb-4">
        <div class="col-md-3"><div class="card p-3"><h6>Investment</h6><h4>${inv:,.2f}</h4></div></div>
        <div class="col-md-3"><div class="card p-3"><h6>Revenue</h6><h4 class="text-success">${rev:,.2f}</h4></div></div>
        <div class="col-md-3"><div class="card p-3"><h6>Expenses</h6><h4 class="text-danger">${exp:,.2f}</h4></div></div>
        <div class="col-md-3"><div class="card p-3"><h6>Net P&L</h6><h4 class="{'text-success' if net >= 0 else 'text-danger'}">${net:,.2f}</h4></div></div>
    </div>
    <div class="row mb-4">
        <div class="col-md-6"><div class="card p-3"><h6>ROI</h6><h2>{roi}%</h2></div></div>
        <div class="col-md-6"><div class="card p-3"><h6>Net Margin</h6><h2>{margin}%</h2></div></div>
    </div>
    <div class="row">
        <div class="col-md-4">
            <h5>💰 Add Investment</h5>
            <form method="POST" action="/add_tx/{business_id}/investment">
                <input name="amount" type="number" step="0.01" class="form-control mb-2" placeholder="Amount" required>
                <input name="desc" class="form-control mb-2" placeholder="Description">
                <input name="date" type="date" class="form-control mb-2" required>
                <button class="btn btn-outline-primary w-100">Add</button>
            </form>
        </div>
        <div class="col-md-4">
            <h5>📈 Add Revenue</h5>
            <form method="POST" action="/add_tx/{business_id}/revenue">
                <input name="amount" type="number" step="0.01" class="form-control mb-2" placeholder="Amount" required>
                <input name="source" class="form-control mb-2" placeholder="Source">
                <input name="date" type="date" class="form-control mb-2" required>
                <button class="btn btn-outline-success w-100">Add</button>
            </form>
        </div>
        <div class="col-md-4">
            <h5>📉 Add Expense</h5>
            <form method="POST" action="/add_tx/{business_id}/expense">
                <input name="amount" type="number" step="0.01" class="form-control mb-2" placeholder="Amount" required>
                <input name="category" class="form-control mb-2" placeholder="Category (e.g. Rent)">
                <input name="desc" class="form-control mb-2" placeholder="Description">
                <input name="date" type="date" class="form-control mb-2" required>
                <button class="btn btn-outline-danger w-100">Add</button>
            </form>
        </div>
    </div>
    <div class="mt-4">
        <h5>Recent Transactions</h5>
        <div class="row">
            <div class="col-md-4">
                <h6>Investments</h6>
                <table class="table table-sm"><tr><th>Date</th><th>Amt</th><th>Desc</th></tr>{tx_rows(invs, 'investment')}</table>
            </div>
            <div class="col-md-4">
                <h6>Revenue</h6>
                <table class="table table-sm"><tr><th>Date</th><th>Amt</th><th>Source</th></tr>{tx_rows(revs, 'revenue')}</table>
            </div>
            <div class="col-md-4">
                <h6>Expenses</h6>
                <table class="table table-sm"><tr><th>Date</th><th>Amt</th><th>Details</th></tr>{tx_rows(exps, 'expense')}</table>
            </div>
        </div>
    </div>
    <a href="/report/{business_id}" class="btn btn-dark mt-3">📄 Download Report</a>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route("/add_tx/<int:business_id>/<tx_type>", methods=["POST"])
def add_tx(business_id, tx_type):
    amount = float(request.form.get("amount", 0))
    date = request.form.get("date")
    if tx_type == "investment":
        add_investment(business_id, amount, request.form.get("desc", ""), date)
    elif tx_type == "revenue":
        add_revenue(business_id, amount, request.form.get("source", ""), date)
    elif tx_type == "expense":
        add_expense(business_id, amount, request.form.get("category", ""), request.form.get("desc", ""), date)
    return redirect(url_for("dashboard", business_id=business_id))

@app.route("/delete/<int:business_id>")
def remove_business(business_id):
    delete_business(business_id)
    return redirect(url_for("home"))

@app.route("/report/<int:business_id>")
def report(business_id):
    from db_manager import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM businesses WHERE id = ?", (business_id,))
    row = cursor.fetchone()
    conn.close()
    name = row[0] if row else "Unknown"
    
    totals = get_totals(business_id)
    net = calculate_profit_loss(totals['total_revenue'], totals['total_expenses'])
    text = f"""FINANCIAL REPORT: {name}
================================
Total Investment:  ${totals['total_investment']:,.2f}
Total Revenue:     ${totals['total_revenue']:,.2f}
Total Expenses:    ${totals['total_expenses']:,.2f}
Net Profit/Loss:   ${net:,.2f}
ROI:               {calculate_roi(totals['total_investment'], net)}%
Net Margin:        {calculate_net_margin(totals['total_revenue'], net)}%
================================
"""
    return Response(text, mimetype="text/plain", headers={"Content-Disposition": f"attachment;filename=report_{name.replace(' ', '_')}.txt"})

@app.route("/break_even", methods=["GET", "POST"])
def break_even():
    result = ""
    if request.method == "POST":
        fixed = float(request.form.get("fixed", 0))
        price = float(request.form.get("price", 0))
        var = float(request.form.get("var", 0))
        be = calculate_break_even(fixed, price, var)
        if be is None:
            result = '<div class="alert alert-danger">Cannot break even. Contribution margin is zero or negative.</div>'
        else:
            result = f'<div class="alert alert-success">Break-even: <b>{be:,.0f} units</b> | Revenue needed: <b>${be*price:,.2f}</b></div>'
    content = f"""
    <a href="/" class="btn btn-secondary btn-sm mb-3">← Back</a>
    <h2>🔧 Break-Even Calculator</h2>
    <form method="POST" class="row g-3">
        <div class="col-md-3"><input name="fixed" type="number" step="0.01" class="form-control" placeholder="Fixed Costs ($)" required></div>
        <div class="col-md-3"><input name="price" type="number" step="0.01" class="form-control" placeholder="Price/Unit ($)" required></div>
        <div class="col-md-3"><input name="var" type="number" step="0.01" class="form-control" placeholder="Variable Cost/Unit ($)" required></div>
        <div class="col-md-3"><button class="btn btn-primary w-100">Calculate</button></div>
    </form>
    {result}
    """
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)