from src.infrastructure.adapters.md_adapter import MDAdapter



class InavMDAdapter(MDAdapter):
    def get_crypto_quantity_on_onshore_etf(self):
        raise NotImplementedError