class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.environment = "production"
            cls._instance.currency = "BRL"
            cls._instance.debug = False
        return cls._instance
    def __str__(self):
        return f"enviroments: {self.environment}, currency: {self.currency}, debug: {self.debug}"
    

if __name__ == "__main__":
    configs = AppConfig()

    configs2 = AppConfig()
    configs2.environment = "dev"
    
    configs3 = AppConfig()

    print(f"Teste 1: Duas referências obtidas representam o mesmo objeto: {configs is configs2}")
    print(f"Teste 2: Uma alteração realizada em uma referência pode ser observada pela outra: {configs.environment == "dev"}")
    print(f"Teste 3: Os valores alterados não são restaurados quando a configuração é obtida novamente: {configs.environment == "dev"}")