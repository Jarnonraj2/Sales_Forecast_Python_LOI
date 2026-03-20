"""
SalesYear module - vertegenwoordigt een fiscaal verkoopjaar
"""
from typing import List
from datetime import datetime
from models.simulation import Simulation


class SalesYear:
    """
    SalesYear class - representeert een fiscaal verkoopjaar met simulaties
    """
    
    def __init__(self, year: int):
        """
        Initialiseer een nieuw verkoopjaar
        
        Args:
            year: Het jaartal
        """
        self.year = year
        self.simulations: List[Simulation] = []
        self.created_date = datetime.now()
    
    def add_simulation(self, simulation: Simulation) -> None:
        """
        Voeg een simulatie toe aan dit verkoopjaar
        
        Args:
            simulation: Simulatie om toe te voegen
        """
        self.simulations.append(simulation)
    
    def get_total_expected_revenue(self) -> float:
        """
        Bereken de totale verwachte omzet over alle simulaties
        
        Returns:
            Totale verwachte omzet
        """
        total = 0.0
        for simulation in self.simulations:
            if simulation.result:
                total += simulation.result.total_revenue
        return total
    
    def get_average_expected_revenue(self) -> float:
        """
        Bereken de gemiddelde verwachte omzet van alle simulaties
        
        Returns:
            Gemiddelde verwachte omzet
        """
        if not self.simulations:
            return 0.0
        
        simulations_with_results = [s for s in self.simulations if s.result]
        if not simulations_with_results:
            return 0.0
        
        total = sum(s.result.total_revenue for s in simulations_with_results)
        return total / len(simulations_with_results)
    
    def __str__(self) -> str:
        return f"SalesYear {self.year}: {len(self.simulations)} simulatie(s)"
    
    def __repr__(self) -> str:
        return f"SalesYear(year={self.year}, simulations={len(self.simulations)})"
