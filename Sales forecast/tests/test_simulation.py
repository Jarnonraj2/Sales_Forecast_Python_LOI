"""
Unit tests voor Simulation class
"""
import unittest
import sys
import os

# Voeg parent directory toe aan path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.simulation import Simulation, SimulationResult
from models.scenario import Scenario
from models.lead import Lead


class TestSimulation(unittest.TestCase):
    """Test cases voor Simulation class"""
    
    def test_simulation_creation(self):
        """Test het aanmaken van een simulatie"""
        sim = Simulation(1, "Test Simulatie")
        
        self.assertEqual(sim.id, 1)
        self.assertEqual(sim.name, "Test Simulatie")
        self.assertEqual(len(sim.leads), 0)
    
    def test_calculate_year_revenue(self):
        """Test jaaromzet berekening met parameters"""
        sim = Simulation(1, "Test Simulatie")
        
        # 100 leads × 20% conversie × €1000 gemiddeld = €20.000
        revenue = sim.calculate_year_revenue(
            num_leads=100,
            conversion_rate=0.20,
            average_deal_value=1000.0
        )
        
        self.assertEqual(revenue, 20000.0)
    
    def test_calculate_year_revenue_different_values(self):
        """Test jaaromzet berekening met andere waarden"""
        sim = Simulation(1, "Test Simulatie")
        
        # 200 leads × 25% conversie × €2000 gemiddeld = €100.000
        revenue = sim.calculate_year_revenue(
            num_leads=200,
            conversion_rate=0.25,
            average_deal_value=2000.0
        )
        
        self.assertEqual(revenue, 100000.0)
    
    def test_calculate_year_revenue_with_scenario(self):
        """Test jaaromzet berekening met scenario"""
        sim = Simulation(1, "Test Simulatie")
        scenario = Scenario("Optimistisch", 0.30, 5000.0, 150)
        sim.set_scenario(scenario)
        
        # 150 leads × 30% conversie × €5000 = €225.000
        revenue = sim.calculate_year_revenue()
        
        self.assertEqual(revenue, 225000.0)
    
    def test_calculate_year_revenue_negative_leads(self):
        """Test dat negatief aantal leads fout geeft"""
        sim = Simulation(1, "Test Simulatie")
        
        with self.assertRaises(ValueError):
            sim.calculate_year_revenue(
                num_leads=-10,
                conversion_rate=0.20,
                average_deal_value=1000.0
            )
    
    def test_calculate_year_revenue_invalid_conversion_rate_high(self):
        """Test dat conversie > 100% fout geeft"""
        sim = Simulation(1, "Test Simulatie")
        
        with self.assertRaises(ValueError):
            sim.calculate_year_revenue(
                num_leads=100,
                conversion_rate=1.50,  # 150%
                average_deal_value=1000.0
            )
    
    def test_calculate_year_revenue_invalid_conversion_rate_negative(self):
        """Test dat negatieve conversie fout geeft"""
        sim = Simulation(1, "Test Simulatie")
        
        with self.assertRaises(ValueError):
            sim.calculate_year_revenue(
                num_leads=100,
                conversion_rate=-0.20,
                average_deal_value=1000.0
            )
    
    def test_calculate_quarterly_revenue(self):
        """Test kwartaal omzet berekening"""
        sim = Simulation(1, "Test Simulatie")
        
        quarterly = sim.calculate_quarterly_revenue(
            num_leads=100,
            conversion_rate=0.20,
            average_deal_value=1000.0
        )
        
        # Totaal = €20.000, verdeeld over 4 kwartalen = €5.000 per kwartaal
        self.assertEqual(quarterly[1], 5000.0)
        self.assertEqual(quarterly[2], 5000.0)
        self.assertEqual(quarterly[3], 5000.0)
        self.assertEqual(quarterly[4], 5000.0)
    
    def test_add_lead(self):
        """Test het toevoegen van leads"""
        sim = Simulation(1, "Test Simulatie")
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead2 = Lead(2, "XYZ BV", 5000.0, "Nieuw", 0.5)
        
        sim.add_lead(lead1)
        sim.add_lead(lead2)
        
        self.assertEqual(len(sim.leads), 2)
    
    def test_run_simulation_with_leads(self):
        """Test simulatie uitvoeren met leads"""
        sim = Simulation(1, "Test Simulatie")
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead2 = Lead(2, "XYZ BV", 20000.0, "Nieuw", 0.5)
        
        sim.add_lead(lead1)
        sim.add_lead(lead2)
        
        result = sim.run_simulation()
        
        # Gemiddelde kans = (0.3 + 0.5) / 2 = 0.4
        # Gemiddelde waarde = (10000 + 20000) / 2 = 15000
        # 2 leads × 0.4 × 15000 = 12000
        self.assertEqual(result.total_revenue, 12000.0)
        self.assertIsNotNone(result.revenue_per_quarter)


class TestSimulationResult(unittest.TestCase):
    """Test cases voor SimulationResult class"""
    
    def test_simulation_result_creation(self):
        """Test het aanmaken van een simulatieresultaat"""
        revenue_per_quarter = {1: 5000.0, 2: 5000.0, 3: 5000.0, 4: 5000.0}
        result = SimulationResult(20000.0, revenue_per_quarter, 100, 0.20, 1000.0)
        
        self.assertEqual(result.total_revenue, 20000.0)
        self.assertEqual(result.num_leads, 100)
        self.assertEqual(result.conversion_rate, 0.20)
        self.assertEqual(result.average_deal_value, 1000.0)
    
    def test_get_quarterly_revenue(self):
        """Test het ophalen van kwartaal omzet"""
        revenue_per_quarter = {1: 5000.0, 2: 6000.0, 3: 7000.0, 4: 8000.0}
        result = SimulationResult(26000.0, revenue_per_quarter, 100, 0.20, 1000.0)
        
        self.assertEqual(result.get_quarterly_revenue(1), 5000.0)
        self.assertEqual(result.get_quarterly_revenue(2), 6000.0)
        self.assertEqual(result.get_quarterly_revenue(3), 7000.0)
        self.assertEqual(result.get_quarterly_revenue(4), 8000.0)
    
    def test_get_quarterly_revenue_invalid(self):
        """Test dat ongeldig kwartaal fout geeft"""
        revenue_per_quarter = {1: 5000.0, 2: 5000.0, 3: 5000.0, 4: 5000.0}
        result = SimulationResult(20000.0, revenue_per_quarter, 100, 0.20, 1000.0)
        
        with self.assertRaises(ValueError):
            result.get_quarterly_revenue(5)


if __name__ == '__main__':
    unittest.main()
