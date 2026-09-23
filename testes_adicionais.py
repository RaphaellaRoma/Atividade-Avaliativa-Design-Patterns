from config import AppConfig
from order import Client, Product, OrderBuilder
from channels import MobileCheckout, MobileNotification
from registry import get_channel_factory

def teste_singleton_atributo_compartilhado():
    config_a = AppConfig()
    config_a.feature_flag = "beta"
    config_b = AppConfig()
    assert config_b.feature_flag == "beta"
    print("Teste Singleton Passou")

def teste_builder_reinicia_apos_build():
    builder = OrderBuilder()

    pedido1 = (builder.add_cliente(Client("Roger"))
               .add_produto(Product("Copo", 3.99))
               .build()
            )
    
    pedido2 = builder.add_cliente(Client("Roger")).build()
    assert len(pedido1.produtos) == 1
    assert len(pedido2.produtos) == 0
    print("Teste Builder Passou")

def teste_fabrica_cria_familia_coerente():
    fabrica = get_channel_factory("MOBILE")
    checkout = fabrica.create_checkout()
    notification = fabrica.create_notification()
    assert isinstance(checkout, MobileCheckout)
    assert isinstance(notification, MobileNotification)
    print("Teste Fábrica Passou")

if __name__ == "__main__":
    teste_singleton_atributo_compartilhado()
    teste_builder_reinicia_apos_build()
    teste_fabrica_cria_familia_coerente()
    print("\nTodos os testes adicionais passaram.")
