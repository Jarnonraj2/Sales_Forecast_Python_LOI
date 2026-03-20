"""
Scenario module - vertegenwoordigt een simulatie scenario
"""


class Scenario:
    """
    Scenario class - representeert een set van parameters voor een simulatie
    """
    
    def __init__(self, name: str, conversion_rate: float, 
                 average_deal_value: float, num_leads: int):
        """
        Initialiseer een nieuw scenario
        
        Args:
            name: Naam van het scenario
            conversion_rate: Conversiepercentage (0.0 - 1.0)
            average_deal_value: Gemiddelde dealwaarde
            num_leads: Aantal leads
        """
        if not 0 <= conversion_rate <= 1:
            raise ValueError("Conversiepercentage moet tussen 0 en 1 liggen")
        if average_deal_value < 0:
            raise ValueError("Gemiddelde dealwaarde kan niet negatief zijn")
        if num_leads < 0:
            raise ValueError("Aantal leads kan niet negatief zijn")
        
        self.name = name
        self.conversion_rate = conversion_rate
        self.average_deal_value = average_deal_value
        self.num_leads = num_leads
    
    def calculate_expected_revenue(self) -> float:
        """
        Bereken de verwachte omzet voor dit scenario
        
        Returns:
            Verwachte omzet (num_leads × conversion_rate × average_deal_value)
        """
        return self.num_leads * self.conversion_rate * self.average_deal_value
    
    def __str__(self) -> str:
        return (f"Scenario '{self.name}': {self.num_leads} leads, "
                f"{self.conversion_rate*100:.1f}% conversie, "
                f"€{self.average_deal_value:,.2f} gemiddeld")
    
    def __repr__(self) -> str:
        return (f"Scenario(name='{self.name}', conversion_rate={self.conversion_rate}, "
                f"average_deal_value={self.average_deal_value}, num_leads={self.num_leads})")
