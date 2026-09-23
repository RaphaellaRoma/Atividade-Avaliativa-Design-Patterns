from abc import ABC, abstractmethod
from order import Client, Product, OrderBuilder

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class PixPayment(Payment):
    nome = "PIX"

    def pay(self, amount):
        print(f"Pagamento de {amount:.2f} reais por Pix")

class CreditCardPayment(Payment):
    nome = "Cartão de Crédito"

    def pay(self, amount):
        print(f"Pagamento de {amount:.2f} reais por Cartão de Crédito")


class BoletoPayment(Payment):
    nome = "Boleto"

    def pay(self, amount):
        print(f"Pagamento de {amount:.2f} reais por Boleto")




class PaymentProcessor(ABC):
    def process_order(self, order):
        payment = self.create_payment()
        if order.pagamento is not None and order.pagamento != payment.nome:
            raise ValueError("A forma de pagamento do pedido não corresponde ao processador")
        order.pagamento = payment.nome
        payment.pay(order.total())

    @abstractmethod
    def create_payment(self):
        pass

class PixProcessor(PaymentProcessor):
    def create_payment(self):
        payment = PixPayment()
        return payment

    
class CreditCardProcessor(PaymentProcessor):
    def create_payment(self):
        payment = CreditCardPayment()
        return payment

    
class BoletoProcessor(PaymentProcessor):

    def create_payment(self):
        payment = BoletoPayment()
        return payment


if __name__ == "__main__":
    pedido = (
    OrderBuilder()
    .add_cliente(Client("Maria"))
    .add_produto(Product("Copo Vidro", 10.99))
    .add_pagamento("PIX")
    .build())

    processador = PixProcessor()
    assert isinstance(processador.create_payment(), PixPayment)
    assert pedido.pagamento == processador.create_payment().nome
    processador.process_order(pedido)

    pedido2 = (
    OrderBuilder()
    .add_cliente(Client("João"))
    .add_produto(Product("Prato Vidro", 17.99))
    .add_pagamento("Boleto")
    .build())

    processador = BoletoProcessor()
    assert isinstance(processador.create_payment(), BoletoPayment)
    assert pedido2.pagamento == processador.create_payment().nome
    processador.process_order(pedido2)
