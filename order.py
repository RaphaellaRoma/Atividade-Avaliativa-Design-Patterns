class Product:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class Client:
    def __init__(self, name:str):
        self.name = name

class Order:
    def __init__(self):
        self.cliente = None
        self.produtos = []
        self.endereco = None
        self.cupom = None
        self.pagamento = None
        self.observacao = None


    def total(self):
        valor = sum([produto.preco for produto in self.produtos])
        return valor


class OrderBuilder():
    def __init__(self):
        self.reset()

    def reset(self):
        self._pedido = Order()



    def add_cliente(self, cliente: Client):
        self._pedido.cliente = cliente
        return self

    def add_produto(self, product : Product):
        self._pedido.produtos.append(product)
        return self

    def add_endereco(self, endereco):
        self._pedido.endereco = endereco
        return self

    def add_cupom(self, cupom):
        self._pedido.cupom = cupom
        return self

    def add_pagamento(self, pagamento):
        self._pedido.pagamento = pagamento
        return self

    def add_observacao(self,observacao):
        self._pedido.observacao = observacao
        return self


    
    def build(self):
        if not isinstance(self._pedido.cliente, Client):
            raise ValueError("O pedido deve ter um cliente")
        pedido_atual = self._pedido
        self.reset()
        return pedido_atual

if __name__ == "__main__":

    cliente = Client("maria")
    pedido = (OrderBuilder().add_cliente(cliente)
              .add_produto(Product("Copo", 3.99))
              .add_produto(Product("prato vidro", 16.99))
              .add_endereco("rua X, 1270")
              .add_observacao("Entregar pela manhã")
              .build())
    print(f"Total: {pedido.total():.2f} reais")
    assert len(pedido.produtos) == 2
    assert round(pedido.total(), 2) == 20.98
    assert pedido.endereco == "rua X, 1270"
    assert pedido.observacao == "Entregar pela manhã"

    try:
        OrderBuilder().build()
    except ValueError as erro:
        print(erro)
    else:
        raise AssertionError("O builder aceitou um pedido sem cliente")
