"""
Hoofdprogramma - Sales Forecast Simulatie Applicatie
Sales Performance Solutions (SPS)

Deze applicatie simuleert het fiscale jaar van een salesafdeling
op basis van leaddata, conversiepercentages en dealwaardes.
"""
import os
import sys
from typing import List, Optional

from models.lead import Lead
from models.employee import SalesPerson, SalesManager
from models.product import Product
from models.deal import Deal
from models.scenario import Scenario
from models.simulation import Simulation
from models.sales_year import SalesYear
from models.report import Report
from data_importer import DataImporter


class SalesForecastApp:
    """Hoofdapplicatie voor sales forecast simulatie"""
    
    def __init__(self):
        """Initialiseer de applicatie"""
        self.simulations: List[Simulation] = []
        self.scenarios: List[Scenario] = []
        self.managers: List[SalesManager] = []
        self.salespersons: List[SalesPerson] = []
        self.sales_years: List[SalesYear] = []
        self.reports: List[Report] = []
        self.current_id = 1
    
    def clear_screen(self):
        """Maak het scherm leeg"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print header met titel"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def print_menu(self, title: str, options: List[str]):
        """Print menu met opties"""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print(f"  0. Terug")
        print()
    
    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """Vraag gebruikersinvoer"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                
                if not value and allow_empty:
                    return None
                
                if not value:
                    print("Invoer mag niet leeg zijn.")
                    continue
                
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                else:
                    return value
                    
            except ValueError:
                print(f"Ongeldige invoer. Verwacht: {input_type.__name__}")
            except KeyboardInterrupt:
                print("\n\nAfgebroken door gebruiker.")
                sys.exit(0)
    
    def main_menu(self):
        """Toon hoofdmenu"""
        while True:
            self.clear_screen()
            self.print_menu(
                "SALES FORECAST SIMULATIE - HOOFDMENU",
                [
                    "Nieuwe simulatie aanmaken",
                    "Scenario's beheren",
                    "Team beheren",
                    "Rapporten genereren",
                    "Bestaande simulaties bekijken",
                    "Excel data importeren",
                    "Afsluiten"
                ]
            )
            
            choice = self.get_input("Keuze", int)
            
            if choice == 0:
                continue
            elif choice == 1:
                self.create_simulation_menu()
            elif choice == 2:
                self.scenario_menu()
            elif choice == 3:
                self.team_menu()
            elif choice == 4:
                self.report_menu()
            elif choice == 5:
                self.view_simulations()
            elif choice == 6:
                self.import_excel_menu()
            elif choice == 7:
                self.exit_app()
            else:
                print("Ongeldige keuze. Druk op Enter om verder te gaan...")
                input()
    
    def create_simulation_menu(self):
        """Menu voor nieuwe simulatie"""
        self.clear_screen()
        self.print_header("NIEUWE SIMULATIE AANMAKEN")
        
        name = self.get_input("Naam simulatie")
        
        sim = Simulation(self.current_id, name)
        self.current_id += 1
        
        print("\nWilt u:")
        print("1. Handmatig parameters invoeren")
        print("2. Een bestaand scenario gebruiken")
        print("3. Leads toevoegen")
        
        choice = self.get_input("Keuze", int)
        
        if choice == 1:
            num_leads = self.get_input("Aantal leads", int)
            conversion_rate = self.get_input("Conversiepercentage (0-100)", float) / 100
            average_deal_value = self.get_input("Gemiddelde dealwaarde (€)", float)
            
            # Validatie
            if num_leads < 0:
                print("Aantal leads kan niet negatief zijn!")
                input("Druk op Enter om verder te gaan...")
                return
            
            if not 0 <= conversion_rate <= 1:
                print("Conversiepercentage moet tussen 0 en 100 liggen!")
                input("Druk op Enter om verder te gaan...")
                return
            
            if average_deal_value < 0:
                print("Gemiddelde dealwaarde kan niet negatief zijn!")
                input("Druk op Enter om verder te gaan...")
                return
            
            try:
                result = sim.run_simulation() if sim.leads else None
                
                if not result:
                    # Bereken met parameters
                    total_revenue = sim.calculate_year_revenue(
                        num_leads, conversion_rate, average_deal_value
                    )
                    quarterly = sim.calculate_quarterly_revenue(
                        num_leads, conversion_rate, average_deal_value
                    )
                    
                    print(f"\n✓ Simulatie berekening:")
                    print(f"  Verwachte jaaromzet: €{total_revenue:,.2f}")
                    print(f"  Omzet per kwartaal:")
                    for q in [1, 2, 3, 4]:
                        print(f"    Q{q}: €{quarterly[q]:,.2f}")
                
                self.simulations.append(sim)
                print(f"\n✓ Simulatie '{name}' succesvol aangemaakt!")
                
            except Exception as e:
                print(f"\n✗ Fout bij simulatie: {str(e)}")
        
        elif choice == 2:
            if not self.scenarios:
                print("\nGeen scenario's beschikbaar. Maak eerst een scenario aan.")
            else:
                print("\nBeschikbare scenario's:")
                for i, scenario in enumerate(self.scenarios, 1):
                    print(f"  {i}. {scenario}")
                
                scenario_choice = self.get_input("Kies scenario", int) - 1
                
                if 0 <= scenario_choice < len(self.scenarios):
                    scenario = self.scenarios[scenario_choice]
                    sim.set_scenario(scenario)
                    result = sim.run_simulation()
                    
                    print(f"\n✓ Simulatie uitgevoerd met scenario '{scenario.name}':")
                    print(f"  Verwachte jaaromzet: €{result.total_revenue:,.2f}")
                    
                    self.simulations.append(sim)
                    print(f"✓ Simulatie '{name}' succesvol aangemaakt!")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def scenario_menu(self):
        """Menu voor scenario beheer"""
        while True:
            self.clear_screen()
            self.print_menu(
                "SCENARIO BEHEER",
                [
                    "Nieuw scenario aanmaken",
                    "Scenario's bekijken",
                    "Scenario verwijderen"
                ]
            )
            
            choice = self.get_input("Keuze", int)
            
            if choice == 0:
                break
            elif choice == 1:
                self.create_scenario()
            elif choice == 2:
                self.view_scenarios()
            elif choice == 3:
                self.delete_scenario()
    
    def create_scenario(self):
        """Maak nieuw scenario"""
        self.clear_screen()
        self.print_header("NIEUW SCENARIO AANMAKEN")
        
        name = self.get_input("Naam scenario")
        num_leads = self.get_input("Aantal leads", int)
        conversion_rate = self.get_input("Conversiepercentage (0-100)", float) / 100
        average_deal_value = self.get_input("Gemiddelde dealwaarde (€)", float)
        
        try:
            scenario = Scenario(name, conversion_rate, average_deal_value, num_leads)
            self.scenarios.append(scenario)
            
            print(f"\n✓ Scenario '{name}' succesvol aangemaakt!")
            print(f"  Verwachte omzet: €{scenario.calculate_expected_revenue():,.2f}")
            
        except ValueError as e:
            print(f"\n✗ Fout: {str(e)}")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def view_scenarios(self):
        """Bekijk alle scenario's"""
        self.clear_screen()
        self.print_header("SCENARIO OVERZICHT")
        
        if not self.scenarios:
            print("Geen scenario's beschikbaar.")
        else:
            for i, scenario in enumerate(self.scenarios, 1):
                print(f"\n{i}. {scenario}")
                print(f"   Verwachte omzet: €{scenario.calculate_expected_revenue():,.2f}")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def delete_scenario(self):
        """Verwijder scenario"""
        if not self.scenarios:
            print("\nGeen scenario's beschikbaar.")
            input("Druk op Enter om verder te gaan...")
            return
        
        self.view_scenarios()
        choice = self.get_input("\nWelk scenario verwijderen? (nummer)", int) - 1
        
        if 0 <= choice < len(self.scenarios):
            deleted = self.scenarios.pop(choice)
            print(f"\n✓ Scenario '{deleted.name}' verwijderd!")
        else:
            print("\n✗ Ongeldig scenario nummer.")
        
        input("Druk op Enter om verder te gaan...")
    
    def team_menu(self):
        """Menu voor team beheer"""
        while True:
            self.clear_screen()
            self.print_menu(
                "TEAM BEHEER",
                [
                    "Sales Manager toevoegen",
                    "Sales Person toevoegen",
                    "Team bekijken",
                    "Lead toewijzen aan Sales Person"
                ]
            )
            
            choice = self.get_input("Keuze", int)
            
            if choice == 0:
                break
            elif choice == 1:
                self.add_manager()
            elif choice == 2:
                self.add_salesperson()
            elif choice == 3:
                self.view_team()
            elif choice == 4:
                self.assign_lead_to_salesperson()
    
    def add_manager(self):
        """Voeg sales manager toe"""
        self.clear_screen()
        self.print_header("NIEUWE SALES MANAGER")
        
        name = self.get_input("Naam")
        email = self.get_input("Email")
        
        manager = SalesManager(self.current_id, name, email)
        self.current_id += 1
        self.managers.append(manager)
        
        print(f"\n✓ Sales Manager '{name}' toegevoegd!")
        input("Druk op Enter om verder te gaan...")
    
    def add_salesperson(self):
        """Voeg salesperson toe"""
        self.clear_screen()
        self.print_header("NIEUWE SALES PERSON")
        
        name = self.get_input("Naam")
        email = self.get_input("Email")
        
        sp = SalesPerson(self.current_id, name, email)
        self.current_id += 1
        
        if self.managers:
            print("\nBeschikbare managers:")
            for i, manager in enumerate(self.managers, 1):
                print(f"  {i}. {manager}")
            
            manager_choice = self.get_input("Kies manager (of 0 voor geen)", int)
            
            if manager_choice > 0 and manager_choice <= len(self.managers):
                manager = self.managers[manager_choice - 1]
                manager.add_team_member(sp)
        
        self.salespersons.append(sp)
        print(f"\n✓ Sales Person '{name}' toegevoegd!")
        input("Druk op Enter om verder te gaan...")
    
    def view_team(self):
        """Bekijk team overzicht"""
        self.clear_screen()
        self.print_header("TEAM OVERZICHT")
        
        if not self.managers and not self.salespersons:
            print("Geen teamleden beschikbaar.")
        else:
            print("SALES MANAGERS:")
            for manager in self.managers:
                print(f"\n  {manager}")
                print(f"  Team grootte: {len(manager.team)}")
                if manager.team:
                    for sp in manager.team:
                        print(f"    - {sp.name} ({len(sp.leads)} leads, {len(sp.deals)} deals)")
            
            print("\n\nSALES PERSONS (zonder manager):")
            unassigned = [sp for sp in self.salespersons 
                         if not any(sp in m.team for m in self.managers)]
            for sp in unassigned:
                print(f"  {sp} - {len(sp.leads)} leads, {len(sp.deals)} deals")
        
        input("\n\nDruk op Enter om verder te gaan...")
    
    def assign_lead_to_salesperson(self):
        """Wijs lead toe aan salesperson"""
        # Deze functie zou uitgebreid moeten worden met lead selectie
        print("\nDeze functionaliteit vereist bestaande leads.")
        input("Druk op Enter om verder te gaan...")
    
    def report_menu(self):
        """Menu voor rapporten"""
        while True:
            self.clear_screen()
            self.print_menu(
                "RAPPORTEN",
                [
                    "Simulatie rapport genereren",
                    "Team rapport genereren",
                    "Rapporten bekijken"
                ]
            )
            
            choice = self.get_input("Keuze", int)
            
            if choice == 0:
                break
            elif choice == 1:
                self.generate_simulation_report()
            elif choice == 2:
                self.generate_team_report()
            elif choice == 3:
                self.view_reports()
    
    def generate_simulation_report(self):
        """Genereer simulatie rapport"""
        if not self.simulations:
            print("\nGeen simulaties beschikbaar.")
            input("Druk op Enter om verder te gaan...")
            return
        
        self.clear_screen()
        self.print_header("SIMULATIE RAPPORT GENEREREN")
        
        print("Beschikbare simulaties:")
        for i, sim in enumerate(self.simulations, 1):
            print(f"  {i}. {sim}")
        
        choice = self.get_input("\nKies simulatie", int) - 1
        
        if 0 <= choice < len(self.simulations):
            sim = self.simulations[choice]
            
            if not sim.result:
                print("\nSimulatie heeft nog geen resultaten.")
                input("Druk op Enter om verder te gaan...")
                return
            
            report = Report(self.current_id, f"Rapport {sim.name}", 1)
            self.current_id += 1
            
            content = report.generate_simulation_report(sim)
            self.reports.append(report)
            
            print("\n" + content)
            
            save = self.get_input("\nRapport opslaan naar bestand? (j/n)")
            if save.lower() == 'j':
                filename = self.get_input("Bestandsnaam (zonder extensie)")
                report.save_to_file(f"{filename}.txt")
                print(f"✓ Rapport opgeslagen als {filename}.txt")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def generate_team_report(self):
        """Genereer team rapport"""
        if not self.managers:
            print("\nGeen managers beschikbaar.")
            input("Druk op Enter om verder te gaan...")
            return
        
        self.clear_screen()
        self.print_header("TEAM RAPPORT GENEREREN")
        
        print("Beschikbare managers:")
        for i, manager in enumerate(self.managers, 1):
            print(f"  {i}. {manager}")
        
        choice = self.get_input("\nKies manager", int) - 1
        
        if 0 <= choice < len(self.managers):
            manager = self.managers[choice]
            
            report = Report(self.current_id, f"Team Rapport {manager.name}", 1)
            self.current_id += 1
            
            content = report.generate_manager_report(manager)
            self.reports.append(report)
            
            print("\n" + content)
            
            save = self.get_input("\nRapport opslaan naar bestand? (j/n)")
            if save.lower() == 'j':
                filename = self.get_input("Bestandsnaam (zonder extensie)")
                report.save_to_file(f"{filename}.txt")
                print(f"✓ Rapport opgeslagen als {filename}.txt")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def view_reports(self):
        """Bekijk rapporten"""
        self.clear_screen()
        self.print_header("RAPPORT OVERZICHT")
        
        if not self.reports:
            print("Geen rapporten beschikbaar.")
        else:
            for i, report in enumerate(self.reports, 1):
                print(f"\n{i}. {report}")
                print(f"   Aangemaakt: {report.created_date.strftime('%d-%m-%Y %H:%M')}")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def view_simulations(self):
        """Bekijk alle simulaties"""
        self.clear_screen()
        self.print_header("SIMULATIE OVERZICHT")
        
        if not self.simulations:
            print("Geen simulaties beschikbaar.")
        else:
            for i, sim in enumerate(self.simulations, 1):
                print(f"\n{i}. {sim}")
                if sim.result:
                    print(f"   Verwachte omzet: €{sim.result.total_revenue:,.2f}")
                    print(f"   Parameters: {sim.result.num_leads} leads, "
                          f"{sim.result.conversion_rate*100:.1f}% conversie")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def import_excel_menu(self):
        """Menu voor Excel import"""
        self.clear_screen()
        self.print_header("EXCEL DATA IMPORTEREN")
        
        filename = self.get_input("Pad naar Excel bestand")
        
        try:
            leads = DataImporter.import_from_excel(filename)
            
            print(f"\n✓ {len(leads)} leads succesvol geïmporteerd!")
            print("\nVoorbeeld leads:")
            for lead in leads[:5]:
                print(f"  - {lead}")
            
            # Optie om leads toe te voegen aan simulatie
            add_to_sim = self.get_input("\nLeads toevoegen aan nieuwe simulatie? (j/n)")
            
            if add_to_sim.lower() == 'j':
                sim_name = self.get_input("Naam simulatie")
                sim = Simulation(self.current_id, sim_name)
                self.current_id += 1
                
                for lead in leads:
                    sim.add_lead(lead)
                
                result = sim.run_simulation()
                self.simulations.append(sim)
                
                print(f"\n✓ Simulatie '{sim_name}' aangemaakt met geïmporteerde leads!")
                print(f"  Verwachte omzet: €{result.total_revenue:,.2f}")
        
        except Exception as e:
            print(f"\n✗ Fout bij importeren: {str(e)}")
        
        input("\nDruk op Enter om verder te gaan...")
    
    def exit_app(self):
        """Sluit applicatie af"""
        self.clear_screen()
        print("\n" + "=" * 70)
        print("  Bedankt voor het gebruiken van Sales Forecast Simulatie!")
        print("  Sales Performance Solutions (SPS)")
        print("=" * 70 + "\n")
        sys.exit(0)
    
    def run(self):
        """Start de applicatie"""
        self.clear_screen()
        print("\n" + "=" * 70)
        print("  WELKOM BIJ SALES FORECAST SIMULATIE")
        print("  Sales Performance Solutions (SPS)")
        print("=" * 70)
        print("\n  Deze applicatie helpt u bij het simuleren van omzetprognoses")
        print("  op basis van leaddata, conversiepercentages en dealwaardes.")
        print("\n" + "=" * 70 + "\n")
        input("Druk op Enter om te starten...")
        
        self.main_menu()


def main():
    """Hoofdfunctie"""
    app = SalesForecastApp()
    app.run()


if __name__ == "__main__":
    main()
