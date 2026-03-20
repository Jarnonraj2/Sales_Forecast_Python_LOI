"""
Report module - genereert rapporten van simulaties
"""
from datetime import datetime
from typing import Optional
from models.simulation import Simulation, SimulationResult
from models.employee import SalesManager


class Report:
    """
    Report class - genereert rapporten voor simulaties en teams
    """
    
    def __init__(self, id: int, title: str, created_by_id: int):
        """
        Initialiseer een nieuw rapport
        
        Args:
            id: Uniek identificatienummer
            title: Titel van het rapport
            created_by_id: ID van degene die het rapport aanmaakt
        """
        self.id = id
        self.title = title
        self.created_by_id = created_by_id
        self.created_date = datetime.now()
        self.content = ""
    
    def generate_simulation_report(self, simulation: Simulation) -> str:
        """
        Genereer een rapport voor een simulatie
        
        Args:
            simulation: Simulatie om rapport van te maken
            
        Returns:
            Rapport als string
        """
        if not simulation.result:
            return "Simulatie heeft nog geen resultaten. Voer eerst de simulatie uit."
        
        result = simulation.result
        
        report_lines = [
            "=" * 60,
            f"SIMULATIE RAPPORT: {simulation.name}",
            "=" * 60,
            f"Simulatie ID: {simulation.id}",
            f"Aangemaakt op: {simulation.created_date.strftime('%d-%m-%Y %H:%M')}",
            "",
            "PARAMETERS",
            "-" * 60,
            f"Aantal leads: {result.num_leads}",
            f"Conversiepercentage: {result.conversion_rate * 100:.1f}%",
            f"Gemiddelde dealwaarde: €{result.average_deal_value:,.2f}",
            "",
            "RESULTATEN",
            "-" * 60,
            f"Totale verwachte jaaromzet: €{result.total_revenue:,.2f}",
            "",
            "Omzet per kwartaal:",
            f"  Q1: €{result.get_quarterly_revenue(1):,.2f}",
            f"  Q2: €{result.get_quarterly_revenue(2):,.2f}",
            f"  Q3: €{result.get_quarterly_revenue(3):,.2f}",
            f"  Q4: €{result.get_quarterly_revenue(4):,.2f}",
            "",
            "=" * 60
        ]
        
        self.content = "\n".join(report_lines)
        return self.content
    
    def generate_manager_report(self, manager: SalesManager) -> str:
        """
        Genereer een rapport voor een sales manager
        
        Args:
            manager: Sales manager om rapport van te maken
            
        Returns:
            Rapport als string
        """
        report_lines = [
            "=" * 60,
            f"TEAM RAPPORT: {manager.name}",
            "=" * 60,
            f"Manager ID: {manager.id}",
            f"Email: {manager.email}",
            f"Teamgrootte: {len(manager.team)}",
            "",
            "TEAM PRESTATIES",
            "-" * 60,
            f"Totale verwachte omzet: €{manager.get_team_total_expected_revenue():,.2f}",
            f"Totale gesloten omzet: €{manager.get_team_total_closed_revenue():,.2f}",
            f"Gemiddeld conversiepercentage: {manager.get_team_conversion_rate() * 100:.1f}%",
            "",
            "TEAMLEDEN",
            "-" * 60
        ]
        
        for sp in manager.team:
            report_lines.extend([
                f"\n{sp.name} ({sp.email})",
                f"  Leads: {len(sp.leads)}",
                f"  Deals: {len(sp.deals)}",
                f"  Verwachte omzet: €{sp.get_total_expected_revenue():,.2f}",
                f"  Gesloten omzet: €{sp.get_total_closed_revenue():,.2f}",
                f"  Conversie: {sp.get_conversion_rate() * 100:.1f}%"
            ])
        
        report_lines.append("\n" + "=" * 60)
        
        self.content = "\n".join(report_lines)
        return self.content
    
    def save_to_file(self, file_path: str) -> None:
        """
        Sla rapport op naar een bestand
        
        Args:
            file_path: Pad waar rapport opgeslagen moet worden
        """
        if not self.content:
            raise ValueError("Rapport heeft geen inhoud. Genereer eerst een rapport.")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
    
    def __str__(self) -> str:
        return f"Report {self.id}: {self.title}"
    
    def __repr__(self) -> str:
        return f"Report(id={self.id}, title='{self.title}')"
