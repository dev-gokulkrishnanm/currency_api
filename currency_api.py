from flask import Flask, request, jsonify, Response
import json
import sqlite3


app= Flask(__name__)

def fetch_rate():   
    conn=sqlite3.connect('currency.db')
    cursor=conn.cursor()
    cursor.execute("SELECT currency,rate FROM exchange_rates")
    return cursor.fetchall()

@app.route('/convert', methods=['GET'])
def convert_currency():
    amount=float(request.args.get('amount'))
    from_currency=request.args.get('from').upper()
    to_currency=request.args.get('to').upper()
    if not from_currency or not to_currency or not amount:
        return jsonify({"error": "Missing 'from', 'to', or 'amount' parameter"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "'amount' must be a number"}), 400


    curr=fetch_rate()
    curr_dic={c:r for c,r in curr}
    if from_currency not in curr_dic or to_currency not in curr_dic:
        return jsonify({"error": f"Currency pair {from_currency}->{to_currency} not found"}), 400

    curr_value=amount/curr_dic[from_currency]
    amount_value=curr_value*curr_dic[to_currency]
    

    return Response(
    json.dumps({
        'amount': amount,
        'from': from_currency,
        'to': to_currency,
        'converted_amount': amount_value,
    }, indent=5),  # this adds newlines
    mimetype='application/json'
)
        
app.run(debug=False)