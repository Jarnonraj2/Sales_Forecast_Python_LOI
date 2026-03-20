"""
Simulation module - vertegenwoordigt een omzet-simulatie
"""
from typing import List, Dict
from datetime import datetime
from models.lead import Lead
from models.scenario import Scenario


class SimulationResult:
    """
    SimulationResult class - bevat de resultaten van een simulatie
    """
    
    def __init__(self, total_revenue: float, revenue_per_quarter: Dict[int, float],
                 num_leads: int, conversion_rate: float, average_deal_value: float):
        """
        Initialiseer een simulatieresultaat
        
        Args:
            total_revenue: Totale verwachte omzet
            revenue_per_quarter: Omzet per kwartaal
            num_leads: Aantal leads
            conversion_rate: Conversiepercentage
            average_deal_value: Gemiddelde dealwaarde
        """
        self.total_revenue = total_revenue
        self.revenue_per_quarter = revenue_per_quarter
        self.num_leads = num_leads
        self.conversion_rate = conversion_rate
        self.average_deal_value = average_deal_value
        self.created_date = datetime.now()
    
    def get_quarterly_revenue(self, quarter: int) -> float:
        """
        Haal de omzet van een specifiek kwartaal op
        
        Args:
            quarter: Kwartal nummer (1-4)
            
        Returns:
            Omzet voor het gevraagde kwartaal
        """
        if quarter not in [1, 2, 3, 4]:
            raise ValueError("Kwartaal moet tussen 1 en 4 liggen")
        return self.revenue_per_quarter.get(quarter, 0.0)
    
    def __str__(self) -> str:
        return (f"Simulatie Resultaat: €{self.total_revenue:,.2f} totaal - "
                f"{self.num_leads} leads, {self.conversion_rate*100:.1f}% conversie")
    
    def __repr__(self) -> str:
        return (f"SimulationResult(total_revenue={self.total_revenue}, "
                f"num_leads={self.num_leads}, conversion_rate={self.conversion_rate})")


class Simulation:
    """
    Simulation class - voert omzet-simulaties uit
    """
    
    def __init__(self, id: int, name: str):
        """
        Initialiseer een nieuwe simulatie
        
        Args:
            id: Uniek identificatienummer
            name: Naam van de simulatie
        """
        self.id = id
        self.name = name
        self.leads: List[Lead] = []
        self.scenario: Scenario = None
        self.result: SimulationResult = None
        self.created_date = datetime.now()
    
    def add_lead(self, lead: Lead) -> None:
        """
        Voeg een lead toe aan de simulatie
        
        Args:
            lead: Lead om toe te voegen
        """
        self.leads.append(lead)
    
    def set_scenario(self, scenario: Scenario) -> None:
        """
        Stel het scenario in voor deze simulatie
        
        Args:
            scenario: Scenario om te gebruiken
        """
        self.scenario = scenario
    
    def calculate_year_revenue(self, num_leads: int = None, 
                              conversion_rate: float = None,
                              average_deal_value: float = None) -> float:
        """
        Bereken de verwachte jaaromzet
        
        Args:
            num_leads: Aantal leads (optioneel, gebruikt scenario als niet gegeven)
            conversion_rate: Conversiepercentage (optioneel)
            average_deal_value: Gemiddelde dealwaarde (optioneel)
            
        Returns:
            Verwachte jaaromzet
        """
        # Gebruik scenario waarden als parameters niet gegeven zijn
        if num_leads is None:
            if self.scenario:
                num_leads = self.scenario.num_leads
            else:
                num_leads = len(self.leads)
        
        if conversion_rate is None:
            if self.scenario:
                conversion_rate = self.scenario.conversion_rate
            else:
                raise ValueError("Conversiepercentage moet gegeven worden of scenario moet ingesteld zijn")
        
        if average_deal_value is None:
            if self.scenario:
                average_deal_value = self.scenario.average_deal_value
            elif self.leads:
                average_deal_value = sum(lead.estimated_value for lead in self.leads) / len(self.leads)
            else:
                raise ValueError("Gemiddelde dealwaarde moet gegeven worden of leads moeten aanwezig zijn")
        
        # Validatie
        if not 0 <= conversion_rate <= 1:
            raise ValueError("Conversiepercentage moet tussen 0 en 1 liggen")
        if num_leads < 0:
            raise ValueError("Aantal leads kan niet negatief zijn")
        if average_deal_value < 0:
            raise ValueError("Gemiddelde dealwaarde kan niet negatief zijn")
        
        # Berekening: Aantal leads × Conversiepercentage × Gemiddelde dealwaarde
        return num_leads * conversion_rate * average_deal_value
    
    def calculate_quarterly_revenue(self, num_leads: int = None,
                                    conversion_rate: float = None,
                                    average_deal_value: float = None) -> Dict[int, float]:
        """
        Bereken de verwachte omzet per kwartaal
        
        Args:
            num_leads: Aantal leads (optioneel)
            conversion_rate: Conversiepercentage (optioneel)
            average_deal_value: Gemiddelde dealwaarde (optioneel)
            
        Returns:
            Dictionary met omzet per kwartaal
        """
        total_revenue = self.calculate_year_revenue(num_leads, conversion_rate, average_deal_value)
        
        # Verdeel gelijkmatig over kwartalen (in werkelijkheid zou dit gebaseerd zijn op datum)
        revenue_per_quarter = total_revenue / 4
        
        return {
            1: revenue_per_quarter,
            2: revenue_per_quarter,
            3: revenue_per_quarter,
            4: revenue_per_quarter
        }
    
    def run_simulation(self) -> SimulationResult:
        """
        Voer de simulatie uit en genereer resultaten
        
        Returns:
            SimulationResult object met alle resultaten
        """
        if self.scenario:
            num_leads = self.scenario.num_leads
            conversion_rate = self.scenario.conversion_rate
            average_deal_value = self.scenario.average_deal_value
        else:
            num_leads = len(self.leads)
            if not self.leads:
                raise ValueError("Geen leads beschikbaar voor simulatie")
            
            # Bereken gemiddelde conversiekans en dealwaarde van leads
            conversion_rate = sum(lead.success_probability for lead in self.leads) / len(self.leads)
            average_deal_value = sum(lead.estimated_value for lead in self.leads) / len(self.leads)
        
        total_revenue = self.calculate_year_revenue(num_leads, conversion_rate, average_deal_value)
        revenue_per_quarter = self.calculate_quarterly_revenue(num_leads, conversion_rate, average_deal_value)
        
        self.result = SimulationResult(
            total_revenue=total_revenue,
            revenue_per_quarter=revenue_per_quarter,
            num_leads=num_leads,
            conversion_rate=conversion_rate,
            average_deal_value=average_deal_value
        )
        
        return self.result
    
    def __str__(self) -> str:
        return f"Simulation {self.id}: {self.name} - {len(self.leads)} leads"
    
    def __repr__(self) -> str:
        return (f"Simulation(id={self.id}, name='{self.name}', "
                f"leads={len(self.leads)})")
