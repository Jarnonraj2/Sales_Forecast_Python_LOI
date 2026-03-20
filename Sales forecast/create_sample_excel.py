"""
Script om een voorbeeld Excel bestand te maken met leaddata
"""
import pandas as pd


def create_sample_excel():
    """Maak een voorbeeld Excel bestand met leads"""
    
    data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'company_name': [
            'ABC Software BV',
            'XYZ Consulting',
            'Tech Solutions Nederland',
            'Digital Dynamics',
            'CloudFirst BV',
            'DataSystems International',
            'Innovation Labs',
            'Smart Business Solutions',
            'NextGen Technologies',
            'Enterprise Connect'
        ],
        'estimated_value': [
            15000.00,
            25000.00,
            8000.00,
            50000.00,
            12000.00,
            30000.00,
            18000.00,
            22000.00,
            35000.00,
            10000.00
        ],
        'status': [
            'Nieuw',
            'In behandeling',
            'Nieuw',
            'In behandeling',
            'Nieuw',
            'In behandeling',
            'Nieuw',
            'Nieuw',
            'In behandeling',
            'Nieuw'
        ],
        'success_probability': [
            0.3,
            0.5,
            0.2,
            0.6,
            0.4,
            0.5,
            0.35,
            0.45,
            0.55,
            0.25
        ]
    }
    
    df = pd.DataFrame(data)
    
    filename = 'leads_voorbeeld.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"✓ Voorbeeld Excel bestand aangemaakt: {filename}")
    print(f"  Aantal leads: {len(df)}")
    print(f"  Totale geschatte waarde: €{df['estimated_value'].sum():,.2f}")
    print(f"  Gemiddelde succeskans: {df['success_probability'].mean()*100:.1f}%")


if __name__ == "__main__":
    create_sample_excel()
