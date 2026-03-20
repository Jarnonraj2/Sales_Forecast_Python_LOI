"""
DataImporter module - importeert leaddata uit Excel bestanden
"""
from typing import List
import pandas as pd
from models.lead import Lead


class DataImporter:
    """
    DataImporter class - verantwoordelijk voor het importeren van externe data
    """
    
    @staticmethod
    def import_from_excel(file_path: str) -> List[Lead]:
        """
        Importeer leads uit een Excel bestand
        
        Args:
            file_path: Pad naar het Excel bestand
            
        Returns:
            Lijst van Lead objecten
            
        Verwachte kolommen in Excel:
        - id (int)
        - company_name (str)
        - estimated_value (float)
        - status (str, optioneel)
        - success_probability (float, optioneel)
        """
        try:
            # Lees Excel bestand
            df = pd.read_excel(file_path)
            
            # Valideer verplichte kolommen
            required_columns = ['id', 'company_name', 'estimated_value']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Ontbrekende kolommen in Excel: {', '.join(missing_columns)}")
            
            # Controleer of bestand niet leeg is
            if df.empty:
                raise ValueError("Excel bestand is leeg")
            
            leads = []
            
            for index, row in df.iterrows():
                try:
                    # Verplichte velden
                    lead_id = int(row['id'])
                    company_name = str(row['company_name'])
                    estimated_value = float(row['estimated_value'])
                    
                    # Optionele velden
                    status = str(row.get('status', 'Nieuw'))
                    success_probability = float(row.get('success_probability', 0.0))
                    
                    # Maak Lead object
                    lead = Lead(
                        id=lead_id,
                        company_name=company_name,
                        estimated_value=estimated_value,
                        status=status,
                        success_probability=success_probability
                    )
                    
                    leads.append(lead)
                    
                except (ValueError, TypeError) as e:
                    print(f"Waarschuwing: Overslaan van rij {index + 2}: {str(e)}")
                    continue
            
            if not leads:
                raise ValueError("Geen geldige leads gevonden in Excel bestand")
            
            return leads
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Excel bestand niet gevonden: {file_path}")
        except Exception as e:
            raise Exception(f"Fout bij importeren van Excel bestand: {str(e)}")
    
    @staticmethod
    def validate_excel_structure(file_path: str) -> bool:
        """
        Valideer de structuur van een Excel bestand zonder te importeren
        
        Args:
            file_path: Pad naar het Excel bestand
            
        Returns:
            True als structuur valide is, anders False
        """
        try:
            df = pd.read_excel(file_path)
            required_columns = ['id', 'company_name', 'estimated_value']
            return all(col in df.columns for col in required_columns)
        except:
            return False
