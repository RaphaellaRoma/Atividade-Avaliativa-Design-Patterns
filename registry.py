from channels import Checkout, Notification, ChannelFactory, WebFactory, MobileFactory
from order import Client, Product, OrderBuilder

_channel_factories = {}

def register_channel_factory(nome, factory):
    _channel_factories[nome.strip().upper()] = factory

def get_channel_factory(channel):
    chave = channel.strip().upper()
    if chave not in _channel_factories:
        disponiveis = ", ".join(sorted(_channel_factories)) or "(nenhum)"
        raise ValueError(
            f"Canal desconhecido: '{channel}'. Canais registrados: {disponiveis}"
        )
    return _channel_factories[chave]

def registered_channels():
    return sorted(_channel_factories)

register_channel_factory("WEB", WebFactory())
register_channel_factory("MOBILE", MobileFactory())

class KioskCheckout(Checkout):
    def show(self, order):
        print(f"Checkout KIOSK: pedido de {order.cliente.name}, total de {order.total():.2f} reais")

class KioskNotification(Notification):
    def send(self, order):
        print(f"Notificação KIOSK: comprovante impresso para {order.cliente.name}")

class KioskFactory(ChannelFactory):
    def create_checkout(self):
        checkout = KioskCheckout()
        return checkout

    def create_notification(self):
        notification = KioskNotification()
        return notification

register_channel_factory("KIOSK", KioskFactory())

if __name__ == "__main__":

    assert registered_channels() == ["KIOSK", "MOBILE", "WEB"]
    assert isinstance(get_channel_factory("WEB"), WebFactory)
    assert isinstance(get_channel_factory("MOBILE"), MobileFactory)
    assert isinstance(get_channel_factory("kiosk"), KioskFactory)

    print(f"Canais registrados: {registered_channels()}")

    pedido = (OrderBuilder()
              .add_cliente(Client("Roger"))
              .add_produto(Product("Copo Vidro", 10.99))
              .build()
            )
    
    fabrica = get_channel_factory("KIOSK")
    fabrica.create_checkout().show(pedido)
    fabrica.create_notification().send(pedido)

    try:
        get_channel_factory("TELEFONE")
    except ValueError as erro:
        print(erro)
    else:
        raise AssertionError("get_channel_factory aceitou um canal desconhecido")
