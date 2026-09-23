from payment import Payment, PaymentProcessor
from order import Client, Product, OrderBuilder

class PayPalPayment(Payment):
    nome = "PayPal"

    def pay(self, amount):
        print(f"Pagamento de {amount:.2f} reais por PayPal")

class PayPalProcessor(PaymentProcessor):
    def create_payment(self):
        payment = PayPalPayment()
        return payment

if __name__ == "__main__":
    
    pedido = (OrderBuilder()
              .add_cliente(Client("Raphaella"))
              .add_produto(Product("Camiseta", 79.90))
              .add_pagamento("PayPal")
              .build()
            )

    processador = PayPalProcessor()
    assert isinstance(processador.create_payment(), PayPalPayment)
    assert pedido.pagamento == processador.create_payment().nome
    processador.process_order(pedido)
