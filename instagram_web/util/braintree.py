import braintree
from config import BT_MERCHANT_ID, BT_PUBLIC_KEY, BT_PRIVATE_KEY

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=BT_MERCHANT_ID,
        public_key=BT_PUBLIC_KEY,
        private_key=BT_PRIVATE_KEY
    )
)

def generate_client_token():
    return gateway.client_token.generate()

# client_token = gateway.client_token.generate({
#     "customer_id": a_customer_id
# })

# @app.route("/client_token", methods=["GET"])
# def client_token():
#   return gateway.client_token.generate()

# @app.route("/checkout", methods=["POST"])
# def create_purchase():
#   nonce_from_the_client = request.form["payment_method_nonce"]
#   # Use payment method nonce here...

def complete_transaction(nonce, amount):
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
        "submit_for_settlement": True
        }
    })
    if not result.is_success:
        return False

    return True