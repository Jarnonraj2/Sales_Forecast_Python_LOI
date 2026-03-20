"""
Employee module - vertegenwoordigt werknemers in de salesorganisatie
"""
from typing import List, Optional
from models.lead import Lead
from models.deal import Deal


class Employee:
    """
    Basis Employee class
    """
    
    def __init__(self, id: int, name: str, email: str):
        """
        Initialiseer een nieuwe werknemer
        
        Args:
            id: Uniek identificatienummer
            name: Naam van de werknemer
            email: Email adres
        """
        self.id = id
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"{self.name} ({self.email})"
    
    def __repr__(self) -> str:
        return f"Employee(id={self.id}, name='{self.name}', email='{self.email}')"


class SalesPerson(Employee):
    """
    SalesPerson class - representeert een verkoper
    """
    
    def __init__(self, id: int, name: str, email: str, manager_id: Optional[int] = None):
        """
        Initialiseer een nieuwe salesperson
        
        Args:
            id: Uniek identificatienummer
            name: Naam van de salesperson
            email: Email adres
            manager_id: ID van de manager
        """
        super().__init__(id, name, email)
        self.manager_id = manager_id
        self.leads: List[Lead] = []
        self.deals: List[Deal] = []
    
    def add_lead(self, lead: Lead) -> None:
        """
        Voeg een lead toe aan deze salesperson
        
        Args:
            lead: Lead om toe te voegen
        """
        lead.assign_to_salesperson(self.id)
        # Voorkom duplicaten
        if lead not in self.leads:
            self.leads.append(lead)
    
    def convert_lead_to_deal(self, lead: Lead, deal: Deal) -> None:
        """
        Converteer een lead naar een deal
        
        Args:
            lead: Lead om te converteren
            deal: Nieuwe deal
        """
        if lead not in self.leads:
            raise ValueError("Lead behoort niet tot deze salesperson")
        
        lead.update_status("Gewonnen")
        self.deals.append(deal)
    
    def get_total_expected_revenue(self) -> float:
        """
        Bereken de totale verwachte omzet voor deze salesperson
        
        Returns:
            Totale verwachte omzet van alle actieve leads
        """
        return sum(lead.calculate_expected_value() 
                  for lead in self.leads 
                  if lead.status not in ["Gewonnen", "Verloren"])
    
    def get_total_closed_revenue(self) -> float:
        """
        Bereken de totale gesloten omzet voor deze salesperson
        
        Returns:
            Totale waarde van alle gesloten deals
        """
        return sum(deal.value for deal in self.deals)
    
    def get_conversion_rate(self) -> float:
        """
        Bereken het conversiepercentage
        
        Returns:
            Conversiepercentage (deals / totaal aantal leads)
        """
        total_leads = len(self.leads)
        if total_leads == 0:
            return 0.0
        return len(self.deals) / total_leads
    
    def __repr__(self) -> str:
        return (f"SalesPerson(id={self.id}, name='{self.name}', "
                f"leads={len(self.leads)}, deals={len(self.deals)})")


class SalesManager(Employee):
    """
    SalesManager class - representeert een sales manager
    """
    
    def __init__(self, id: int, name: str, email: str):
        """
        Initialiseer een nieuwe sales manager
        
        Args:
            id: Uniek identificatienummer
            name: Naam van de manager
            email: Email adres
        """
        super().__init__(id, name, email)
        self.team: List[SalesPerson] = []
    
    def add_team_member(self, salesperson: SalesPerson) -> None:
        """
        Voeg een salesperson toe aan het team
        
        Args:
            salesperson: Salesperson om toe te voegen
        """
        salesperson.manager_id = self.id
        self.team.append(salesperson)
    
    def assign_lead_to_salesperson(self, lead: Lead, salesperson: SalesPerson) -> None:
        """
        Wijs een lead toe aan een salesperson
        
        Args:
            lead: Lead om toe te wijzen
            salesperson: Salesperson die de lead krijgt
        """
        if salesperson not in self.team:
            raise ValueError("Salesperson maakt geen deel uit van dit team")
        
        # Als de lead al aan een andere salesperson van dit team is toegewezen, verwijder deze eerst
        if lead.sales_person_id and lead.sales_person_id != salesperson.id:
            for team_member in self.team:
                if team_member.id == lead.sales_person_id and lead in team_member.leads:
                    team_member.leads.remove(lead)
                    break
        
        salesperson.add_lead(lead)
    
    def get_team_total_expected_revenue(self) -> float:
        """
        Bereken de totale verwachte omzet van het hele team
        
        Returns:
            Totale verwachte omzet van alle teamleden
        """
        return sum(sp.get_total_expected_revenue() for sp in self.team)
    
    def get_team_total_closed_revenue(self) -> float:
        """
        Bereken de totale gesloten omzet van het hele team
        
        Returns:
            Totale gesloten omzet van alle teamleden
        """
        return sum(sp.get_total_closed_revenue() for sp in self.team)
    
    def get_team_conversion_rate(self) -> float:
        """
        Bereken het gemiddelde conversiepercentage van het team
        
        Returns:
            Gemiddeld conversiepercentage
        """
        if not self.team:
            return 0.0
        return sum(sp.get_conversion_rate() for sp in self.team) / len(self.team)
    
    def __repr__(self) -> str:
        return (f"SalesManager(id={self.id}, name='{self.name}', "
                f"team_size={len(self.team)})")
