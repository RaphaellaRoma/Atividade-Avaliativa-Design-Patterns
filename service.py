from config import AppConfig
from order import Client, Product, OrderBuilder
from payment import PixProcessor, CreditCardProcessor
from paypal import PayPalProcessor
from registry import get_channel_factory, registered_channels

class EventLogger:
    def __init__(self):
        self.eventos = []

    def log(self, mensagem):
        self.eventos.append(mensagem)

    def historico(self):
        return list(self.eventos)

class OrderService:
    def __init__(self, logger):
        self.logger = logger

    def place_order(self, order, factory, processor):
        checkout = factory.create_checkout()
        notification = factory.create_notification()

        checkout.show(order)
        self.logger.log(f"Checkout exibido para {order.cliente.name}")

        processor.process_order(order)
        self.logger.log(f"Pagamento processado: {order.pagamento}")

        notification.send(order)
        self.logger.log(f"Notificação enviada para {order.cliente.name}")

if __name__ == "__main__":

    config = AppConfig()
    print(f"Configuração da aplicação -> {config}")
    print(f"Canais registrados: {registered_channels()}\n")

    logger = EventLogger()
    service = OrderService(logger)

    pedido_web = (OrderBuilder()
                  .add_cliente(Client("Raphaella"))
                  .add_produto(Product("Copo Vidro", 10.99))
                  .add_produto(Product("Prato Vidro", 16.99))
                  .add_endereco("Rua X, 1270")
                  .add_pagamento("PIX")
                  .build()
                )
    
    print("Canal WEB:")
    service.place_order(pedido_web, get_channel_factory("WEB"), PixProcessor())

    pedido_mobile = (OrderBuilder()
                     .add_cliente(Client("Roger"))
                     .add_produto(Product("Fone", 200.00))
                     .add_pagamento("Cartão de Crédito")
                     .build()
                    )
    
    print("\nCanal MOBILE:")
    service.place_order(pedido_mobile, get_channel_factory("MOBILE"), CreditCardProcessor())

    pedido_kiosk = (OrderBuilder()
                    .add_cliente(Client("Roger"))
                    .add_produto(Product("Camiseta", 79.90))
                    .add_produto(Product("Boné", 45.00))
                    .add_pagamento("PayPal")
                    .build()
                    )
    
    print("\nCanal KIOSK:")
    service.place_order(pedido_kiosk, get_channel_factory("KIOSK"), PayPalProcessor())

    print("\nHistórico de eventos:")
    for evento in logger.historico():
        print(evento)
