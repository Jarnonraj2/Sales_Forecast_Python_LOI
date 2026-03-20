"""
Unit tests voor Lead class
"""
import unittest
import sys
import os

# Voeg parent directory toe aan path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.lead import Lead


class TestLead(unittest.TestCase):
    """Test cases voor Lead class"""
    
    def test_lead_creation(self):
        """Test het aanmaken van een lead"""
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        
        self.assertEqual(lead.id, 1)
        self.assertEqual(lead.company_name, "ABC BV")
        self.assertEqual(lead.estimated_value, 10000.0)
        self.assertEqual(lead.status, "Nieuw")
        self.assertEqual(lead.success_probability, 0.3)
    
    def test_calculate_expected_value(self):
        """Test berekening van verwachte waarde"""
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        expected_value = lead.calculate_expected_value()
        
        self.assertEqual(expected_value, 3000.0)
    
    def test_calculate_expected_value_zero_probability(self):
        """Test berekening met 0% kans"""
        lead = Lead(2, "XYZ BV", 5000.0, "Nieuw", 0.0)
        expected_value = lead.calculate_expected_value()
        
        self.assertEqual(expected_value, 0.0)
    
    def test_calculate_expected_value_hundred_percent(self):
        """Test berekening met 100% kans"""
        lead = Lead(3, "DEF BV", 20000.0, "Nieuw", 1.0)
        expected_value = lead.calculate_expected_value()
        
        self.assertEqual(expected_value, 20000.0)
    
    def test_update_status_valid(self):
        """Test het updaten van status met geldige waarde"""
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead.update_status("In behandeling")
        
        self.assertEqual(lead.status, "In behandeling")
    
    def test_update_status_invalid(self):
        """Test het updaten van status met ongeldige waarde"""
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        
        with self.assertRaises(ValueError):
            lead.update_status("Ongeldig")
    
    def test_negative_estimated_value(self):
        """Test dat negatieve waarde fout geeft"""
        with self.assertRaises(ValueError):
            Lead(1, "ABC BV", -1000.0, "Nieuw", 0.3)
    
    def test_invalid_success_probability_too_high(self):
        """Test dat succeskans > 1 fout geeft"""
        with self.assertRaises(ValueError):
            Lead(1, "ABC BV", 10000.0, "Nieuw", 1.5)
    
    def test_invalid_success_probability_negative(self):
        """Test dat negatieve succeskans fout geeft"""
        with self.assertRaises(ValueError):
            Lead(1, "ABC BV", 10000.0, "Nieuw", -0.1)
    
    def test_assign_to_salesperson(self):
        """Test toewijzen aan salesperson"""
        lead = Lead(1, "ABC BV", 10000.0, "Nieuw", 0.3)
        lead.assign_to_salesperson(5)
        
        self.assertEqual(lead.sales_person_id, 5)


if __name__ == '__main__':
    unittest.main()
