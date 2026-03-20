"""
Unit tests voor Employee classes
"""
import unittest
import sys
import os

# Voeg parent directory toe aan path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.employee import Employee, SalesPerson, SalesManager
from models.lead import Lead
from models.deal import Deal
from models.product import Product


class TestSalesPerson(unittest.TestCase):
    """Test cases voor SalesPerson class"""
    
    def test_salesperson_creation(self):
        """Test het aanmaken van een salesperson"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        
        self.assertEqual(sp.id, 1)
        self.assertEqual(sp.name, "Jan Jansen")
        self.assertEqual(sp.email, "jan@example.com")
        self.assertEqual(len(sp.leads), 0)
        self.assertEqual(len(sp.deals), 0)
    
    def test_add_lead(self):
        """Test het toevoegen van een lead"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        
        sp.add_lead(lead)
        
        self.assertEqual(len(sp.leads), 1)
        self.assertEqual(lead.sales_person_id, 1)
    
    def test_get_total_expected_revenue(self):
        """Test berekening verwachte omzet"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)  # Expected: 3000
        lead2 = Lead(2, "XYZ BV", 20000.0, "Nieuw", 0.5)  # Expected: 10000
        
        sp.add_lead(lead1)
        sp.add_lead(lead2)
        
        expected_revenue = sp.get_total_expected_revenue()
        self.assertEqual(expected_revenue, 13000.0)
    
    def test_get_total_expected_revenue_excludes_won_lost(self):
        """Test dat gewonnen/verloren leads niet meetellen"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead2 = Lead(2, "XYZ BV", 20000.0, "Gewonnen", 0.5)
        lead3 = Lead(3, "DEF BV", 15000.0, "Verloren", 0.4)
        
        sp.add_lead(lead1)
        sp.add_lead(lead2)
        sp.add_lead(lead3)
        
        # Alleen lead1 telt mee
        expected_revenue = sp.get_total_expected_revenue()
        self.assertEqual(expected_revenue, 3000.0)
    
    def test_convert_lead_to_deal(self):
        """Test converteren van lead naar deal"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        product = Product(1, "Software Licentie", 10000.0)
        deal = Deal(1, lead.id, 10000.0, [product])
        
        sp.add_lead(lead)
        sp.convert_lead_to_deal(lead, deal)
        
        self.assertEqual(lead.status, "Gewonnen")
        self.assertEqual(len(sp.deals), 1)
    
    def test_convert_lead_to_deal_invalid_lead(self):
        """Test dat converteren van niet-bestaande lead fout geeft"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        product = Product(1, "Software Licentie", 10000.0)
        deal = Deal(1, lead.id, 10000.0, [product])
        
        # Lead niet toegevoegd aan salesperson
        with self.assertRaises(ValueError):
            sp.convert_lead_to_deal(lead, deal)
    
    def test_get_conversion_rate(self):
        """Test berekening conversiepercentage"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead2 = Lead(2, "XYZ BV", 20000.0, "Nieuw", 0.5)
        product = Product(1, "Software Licentie", 10000.0)
        deal = Deal(1, lead1.id, 10000.0, [product])
        
        sp.add_lead(lead1)
        sp.add_lead(lead2)
        sp.convert_lead_to_deal(lead1, deal)
        
        # 1 deal / 2 leads = 0.5
        conversion_rate = sp.get_conversion_rate()
        self.assertEqual(conversion_rate, 0.5)
    
    def test_get_conversion_rate_no_leads(self):
        """Test conversiepercentage zonder leads"""
        sp = SalesPerson(1, "Jan Jansen", "jan@example.com")
        
        conversion_rate = sp.get_conversion_rate()
        self.assertEqual(conversion_rate, 0.0)


class TestSalesManager(unittest.TestCase):
    """Test cases voor SalesManager class"""
    
    def test_salesmanager_creation(self):
        """Test het aanmaken van een sales manager"""
        manager = SalesManager(1, "Piet Pietersen", "piet@example.com")
        
        self.assertEqual(manager.id, 1)
        self.assertEqual(manager.name, "Piet Pietersen")
        self.assertEqual(len(manager.team), 0)
    
    def test_add_team_member(self):
        """Test het toevoegen van teamleden"""
        manager = SalesManager(1, "Piet Pietersen", "piet@example.com")
        sp1 = SalesPerson(2, "Jan Jansen", "jan@example.com")
        sp2 = SalesPerson(3, "Klaas Klaasen", "klaas@example.com")
        
        manager.add_team_member(sp1)
        manager.add_team_member(sp2)
        
        self.assertEqual(len(manager.team), 2)
        self.assertEqual(sp1.manager_id, 1)
        self.assertEqual(sp2.manager_id, 1)
    
    def test_assign_lead_to_salesperson(self):
        """Test het toewijzen van lead aan salesperson"""
        manager = SalesManager(1, "Piet Pietersen", "piet@example.com")
        sp = SalesPerson(2, "Jan Jansen", "jan@example.com")
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        
        manager.add_team_member(sp)
        manager.assign_lead_to_salesperson(lead, sp)
        
        self.assertEqual(len(sp.leads), 1)
        self.assertEqual(lead.sales_person_id, 2)
    
    def test_assign_lead_to_non_team_member(self):
        """Test dat toewijzen aan niet-teamlid fout geeft"""
        manager = SalesManager(1, "Piet Pietersen", "piet@example.com")
        sp = SalesPerson(2, "Jan Jansen", "jan@example.com")
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        
        # Salesperson NIET toegevoegd aan team
        with self.assertRaises(ValueError):
            manager.assign_lead_to_salesperson(lead, sp)
    
    def test_get_team_total_expected_revenue(self):
        """Test berekening team verwachte omzet"""
        manager = SalesManager(1, "Piet Pietersen", "piet@example.com")
        sp1 = SalesPerson(2, "Jan Jansen", "jan@example.com")
        sp2 = SalesPerson(3, "Klaas Klaasen", "klaas@example.com")
        
        lead1 = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)  # 3000
        lead2 = Lead(2, "XYZ BV", 20000.0, "Nieuw", 0.5)  # 10000
        
        manager.add_team_member(sp1)
        manager.add_team_member(sp2)
        
        sp1.add_lead(lead1)
        sp2.add_lead(lead2)
        
        team_revenue = manager.get_team_total_expected_revenue()
        self.assertEqual(team_revenue, 13000.0)


if __name__ == '__main__':
    unittest.main()
