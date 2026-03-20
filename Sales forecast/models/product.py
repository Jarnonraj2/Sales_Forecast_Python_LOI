"""
Product module - vertegenwoordigt een product of dienst
"""


class Product:
    """
    Product class - representeert een te verkopen product of dienst
    """
    
    def __init__(self, id: int, name: str, price: float, description: str = ""):
        """
        Initialiseer een nieuw product
        
        Args:
            id: Uniek identificatienummer
            name: Naam van het product
            price: Prijs van het product
            description: Beschrijving van het product
        """
        if price < 0:
            raise ValueError("Prijs kan niet negatief zijn")
        
        self.id = id
        self.name = name
        self.price = price
        self.description = description
    
    def __str__(self) -> str:
        return f"Product {self.id}: {self.name} - €{self.price:,.2f}"
    
    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"
