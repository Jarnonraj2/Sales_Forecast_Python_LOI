"""
Lead module - vertegenwoordigt een verkoopkans
"""
from typing import Optional
from datetime import datetime


class Lead:
    """
    Lead class - representeert een potentiële verkoopkans
    """
    
    def __init__(self, id: int, company_name: str, estimated_value: float, 
                 status: str = "Nieuw", success_probability: float = 0.0):
        """
        Initialiseer een nieuwe lead
        
        Args:
            id: Uniek identificatienummer
            company_name: Naam van het bedrijf
            estimated_value: Geschatte waarde van de deal
            status: Status van de lead (Nieuw, In behandeling, Gewonnen, Verloren)
            success_probability: Succeskans (0.0 - 1.0)
        """
        if estimated_value < 0:
            raise ValueError("Geschatte waarde kan niet negatief zijn")
        if not 0 <= success_probability <= 1:
            raise ValueError("Succeskans moet tussen 0 en 1 liggen")
        
        self.id = id
        self.company_name = company_name
        self.estimated_value = estimated_value
        self.status = status
        self.success_probability = success_probability
        self.created_date = datetime.now()
        self.sales_person_id: Optional[int] = None
    
    def calculate_expected_value(self) -> float:
        """
        Bereken de verwachte waarde van deze lead
        
        Returns:
            Verwachte waarde (estimated_value × success_probability)
        """
        return self.estimated_value * self.success_probability
    
    def update_status(self, new_status: str) -> None:
        """
        Update de status van de lead
        
        Args:
            new_status: Nieuwe status
        """
        valid_statuses = ["Nieuw", "In behandeling", "Gewonnen", "Verloren"]
        if new_status not in valid_statuses:
            raise ValueError(f"Ongeldige status. Kies uit: {', '.join(valid_statuses)}")
        self.status = new_status
    
    def assign_to_salesperson(self, salesperson_id: int) -> None:
        """
        Wijs lead toe aan een salesperson
        
        Args:
            salesperson_id: ID van de salesperson
        """
        self.sales_person_id = salesperson_id
    
    def __str__(self) -> str:
        return (f"Lead {self.id}: {self.company_name} - "
                f"€{self.estimated_value:,.2f} ({self.status})")
    
    def __repr__(self) -> str:
        return (f"Lead(id={self.id}, company_name='{self.company_name}', "
                f"estimated_value={self.estimated_value}, status='{self.status}', "
                f"success_probability={self.success_probability})")
