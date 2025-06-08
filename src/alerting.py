def alert_baker(problem_order):
    print(f"🚨 ALERT! Someone ordered {problem_order['cookies']} cookies!")

bad_orders.foreach(alert_baker)
