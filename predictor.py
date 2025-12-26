# predictor.py
def predict_fraud(amount, frequency):
    """
    Simple fraud detection logic:
    - Amount greater than 50,000 is flagged as Fraud
    - More than 5 transactions in a session is flagged as Fraud
    """
    if float(amount) > 50000 or int(frequency) > 5:
        return "Fraud"
    return "Safe"


