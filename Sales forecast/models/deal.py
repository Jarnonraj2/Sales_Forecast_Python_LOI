"""
Deal module - vertegenwoordigt een gesloten deal
"""
from typing import List
from datetime import datetime
from models.product import Product


class Deal:
    """
    Deal class - representeert een gewonnen verkoop
    """
    
    def __init__(self, id: int, lead_id: int, value: float, 
                 products: List[Product], close_date: datetime = None):
        """
        Initialiseer een nieuwe deal
        
        Args:
            id: Uniek identificatienummer
            lead_id: ID van de oorspronkelijke lead
            value: Totale waarde van de deal
            products: Lijst van producten in deze deal
            close_date: Datum waarop de deal is gesloten
        """
        if value < 0:
            raise ValueError("Dealwaarde kan niet negatief zijn")
        if not products:
            raise ValueError("Een deal moet minimaal één product bevatten")
        
        self.id = id
        self.lead_id = lead_id
        self.value = value
        self.products = products
        self.close_date = close_date or datetime.now()
    
    def get_total_value(self) -> float:
        """
        Bereken de totale waarde van de deal
        
        Returns:
            Totale waarde van alle producten
        """
        return sum(product.price for product in self.products)
    
    def add_product(self, product: Product) -> None:
        """
        Voeg een product toe aan de deal
        
        Args:
            product: Product om toe te voegen
        """
        self.products.append(product)
        self.value = self.get_total_value()
    
    def __str__(self) -> str:
        return (f"Deal {self.id}: €{self.value:,.2f} - "
                f"{len(self.products)} product(en)")
    
    def __repr__(self) -> str:
        return (f"Deal(id={self.id}, lead_id={self.lead_id}, "
                f"value={self.value}, products={len(self.products)})")
