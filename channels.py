from abc import ABC, abstractmethod
from order import Client, Product, OrderBuilder


class Checkout(ABC):
    @abstractmethod
    def show(self, order):
        pass
class Notification(ABC):
    @abstractmethod
    def send(self, order):
        pass


class WebCheckout(Checkout):
    def show(self, order):
        print(f"Checkout WEB: pedido de {order.cliente.name}, total de {order.total():.2f} reais")

class MobileCheckout(Checkout):
    def show(self, order):
        print(f"Checkout MOBILE: pedido de {order.cliente.name}, total de {order.total():.2f} reais")


class WebNotification(Notification):
    def send(self, order):
        print(f"Notificação WEB: pedido de {order.cliente.name} recebido")

class MobileNotification(Notification):
    def send(self, order):
        print(f"Notificação MOBILE: pedido de {order.cliente.name} recebido")


class ChannelFactory(ABC):
    @abstractmethod
    def create_checkout(self):
        pass
    @abstractmethod
    def create_notification(self):
        pass


class WebFactory(ChannelFactory):
    def create_checkout(self):
        checkout = WebCheckout()
        return checkout
    def create_notification(self):
        notification = WebNotification()
        return notification


class MobileFactory(ChannelFactory):
    def create_checkout(self):
        checkout = MobileCheckout()
        return checkout
    def create_notification(self):
        notification = MobileNotification()
        return notification


def process_channel(order, factory: ChannelFactory):
    checkout = factory.create_checkout()
    notification = factory.create_notification()
    checkout.show(order)
    notification.send(order)


if __name__ == "__main__":
    pedido = (
    OrderBuilder()
    .add_cliente(Client("Maria"))
    .add_produto(Product("Copo Vidro", 10.99))
    .add_pagamento("PIX")
    .build())

    process_channel(pedido, WebFactory())

    pedido2 = (
    OrderBuilder()
    .add_cliente(Client("João"))
    .add_produto(Product("Prato Vidro", 17.99))
    .add_pagamento("Cartão de Crédito")
    .build())

    process_channel(pedido2, MobileFactory())
