# Sales Forecast Simulatie

## Project beschrijving
Een Python applicatie die omzetprognoses voor salesafdelingen simuleert. Je kunt parameters instellen zoals aantal leads, conversiepercentages en dealwaardes om te zien wat de verwachte jaaromzet zou zijn. Inclusief een web interface en CLI versie.

Dit project is gemaakt als onderdeel van de LOI studie Praktijkintegratie Development Full Cycle.

## Installatie

### Vereisten
- Python 3.8 of hoger
- pip (Python package manager)

### Stappen
1. Installeer de benodigde packages:
```bash
pip install -r requirements.txt
```

2. (Optioneel) Maak een voorbeeld Excel bestand aan:
```bash
python create_sample_excel.py
```

## Gebruik

### CLI Applicatie starten
```bash
python main.py
```

### Flask Web Applicatie starten
```bash
# Installeer eerst Flask
pip install -r requirements_flask.txt

# Start de web server
python app.py
```

De web applicatie is beschikbaar op: **http://127.0.0.1:5000**

## Quick Start - Web versie

### Even starten met Flask

```bash
pip install -r requirements_flask.txt
python app.py
```

Dan ga je naar **http://127.0.0.1:5000** in je browser.

### Wat kun je doen?

**Dashboard**
- Bekijk statistieken van al je simulaties, scenario's, leads en team
- Direct toegang tot alle functionaliteiten

**Simulaties**
1. Ga naar **Simulaties** → **Nieuwe Simulatie**
2. Kies een scenario (of maak er eerst een aan)
3. Stel parameters in:
   - Aantal leads
   - Conversiepercentage (0-100%)
   - Gemiddelde dealwaarde
   - Jaar en kwartaal
4. Bekijk **live preview** van verwachte omzet
5. Klik op **Simulatie Uitvoeren**

**Scenario's**
1. Ga naar **Scenario's** → **Nieuw Scenario**
2. Geef een naam en beschrijving
3. Stel standaard waarden in:
   - Aantal leads
   - Conversiepercentage
   - Gemiddelde dealwaarde
4. Bekijk real-time berekening van verwachte jaaromzet
5. Opslaan en gebruiken in simulaties

**Leads Beheren**
1. Ga naar **Leads** → **Nieuwe Lead**
2. Vul gegevens in:
   - Bedrijfsnaam
   - Geschatte waarde
   - Succeskans (0-100%)
   - Status
3. Voeg toe aan je database
4. Wijs toe aan salesperson (optioneel)

**Team Beheren**
1. Ga naar **Team**
2. Voeg **Sales Managers** toe: Naam en employee ID
3. Voeg **Sales Persons** toe: Naam, employee ID en manager koppeling

**Excel Import**
1. Ga naar **Import** → **Excel Importeren**
2. Upload een Excel bestand met het juiste formaat:
   - Kolommen: id, company_name, estimated_value, status, success_probability
3. Klik op **Importeren**
4. Leads worden automatisch toegevoegd

**Rapporten**
1. Ga naar **Rapporten**
2. Bekijk alle gegenereerde rapporten
3. Klik op een rapport om details te zien
4. Print of exporteer naar PDF (via browser)

### 💡 Tips voor de web applicatie

**Live Calculations**
- Bij het aanmaken van simulaties en scenario's zie je **direct** de verwachte omzet
- Schuif met de range sliders om verschillende waarden uit te proberen
- De formule: `Aantal leads × (Conversie/100) × Gemiddelde waarde`
Wat moet je weten

- Live preview: Wanneer je parameters invoert zie je direct het verwachte resultaat
- In-memory data: Data gaat verloren als je de server herstart (dat's oké voor testing)
- Formule: Aantal leads × (Conversie% / 100) × Gemiddelde waarde = Verwachte omzet

### Als het niet werkt

- Flask niet gevonden? → `pip install Flask`
- Port 5000 bezet? → Verander in `app.py`: `app.run(debug=True, port=5001)`
- Excel import faalt? → Zorg dat pandas en openpyxl geïnstalleerd zijiscover tests
```

### Specifieke test module
```bash
python -m unittest tests.test_simulation
python -m unittest tests.test_lead
python -m unittest tests.test_employee
```

## Projectstructuur
```
Sales forecast/
│
├── main.py                          # CLI Hoofdprogramma
├── app.py                           # Flask Web Applicatie
├── data_importer.py                 # Excel import functionaliteit
├── requirements.txt                 # Python dependencies
├── create_sample_excel.py           # Script voor voorbeeld data
│
├── templates/                       # HTML templates voor Flask
│   ├── base.html                    # Basis template
│   ├── index.html                   # Homepage
│   ├── dashboard.html               # Dashboard
│   ├── simulations.html             # Simulaties overzicht
│   ├── simulation_new.html          # Nieuwe simulatie
│   ├── simulation_detail.html       # Simulatie details
│   ├── scenarios.html               # Scenario's overzicht
│   ├── scenario_new.html            # Nieuw scenario
│   ├── leads.html                   # Leads overzicht
│   ├── lead_new.html                # Nieuwe lead
│   ├── team.html                    # Team overzicht
│   ├── manager_new.html             # Nieuwe manager
│   ├── salesperson_new.html         # Nieuwe salesperson
│   ├── import.html                  # Excel import
│   ├── reports.html                 # Rapporten overzicht
│   └── report_view.html             # Rapport weergave
│
├── models/                          # Data models
│   ├── __init__.py
│   ├── lead.py                      # Lead class
│   ├── deal.py                      # Deal class
│   ├── product.py                   # Product class
│   ├── employee.py                  # SalesPerson en SalesManager
│   ├── scenario.py                  # Scenario class
│   ├── simulation.py                # Simulation en SimulationResult
│   ├── sales_year.py                # SalesYear class
│   └── report.py                    # Report class
│
└── tests/                           # Unit tests
    ├── __init__.py
    ├── test_lead.py
    ├── test_simulation.py
    └── test_employee.py
```

## 🌐 Web Applicatie Features

De Flask web applicatie biedt een moderne interface met:
- **Responsive UI** met Bootstrap 5 design
- **Interactief Dashboard** met real-time statistieken
- **Live berekeningen** tijdens het invoeren van gegevens
- **Sessie management** voor gebruikersgegevens
- **Excel upload functie** via webinterface
- **Rapport generatie** met printbare output
- **Intuïtieve navigatie** tussen alle modules

De web applicatie is volledig functioneel equivalent aan de CLI versie, maar met een gebruiksvriendelijke grafische interface.

## User Stories (Gerealiseerd)

✓ **US1**: Als salesmanager wil ik het aantal leads kunnen invoeren zodat ik de verwachte omzet kan berekenen.

✓ **US2**: Als salesmanager wil ik het conversiepercentage kunnen instellen zodat ik scenario's kan doorrekenen.

✓ **US3**: Als salesmanager wil ik de gemiddelde dealwaarde kunnen aanpassen zodat ik verschillende marktcondities kan simuleren.

✓ **US4**: Als gebruiker wil ik leaddata uit een Excelbestand kunnen importeren zodat bestaande gegevens gebruikt kunnen worden in de simulatie.

✓ **US5**: Als salesmanager wil ik de totale verwachte jaaromzet kunnen berekenen zodat ik mijn financiële planning kan onderbouwen.

✓ **US6**: Als salesmanager wil ik de omzet per kwartaal kunnen inzien zodat ik tussentijds kan bijsturen.

✓ **US7**: Als accountmanager wil ik inzicht hebben in mijn individuele verwachte omzet zodat ik mijn target kan monitoren.

✓ **US8**: Als salesmanager wil ik meerdere scenario's kunnen opslaan zodat ik deze met elkaar kan vergelijken.

✓ **US9**: Als salesmanager wil ik een rapport kunnen genereren van de simulatie zodat ik dit kan delen met de directie.

✓ **US10**: Als gebruiker wil ik foutmeldingen krijgen bij ongeldige invoer zodat de betrouwbaarheid van de berekeningen gewaarborgd blijft.

## Excel Formaat

Het Excel bestand moet de volgende kolommen bevatten:
- **id** (verplicht): Uniek nummer voor de lead
- **company_name** (verplicht): Naam van het bedrijf
- **estimated_value** (verplicht): Geschatte waarde in euro's
- **status** (optioneel): Status zoals "Nieuw", "In behandeling", "Gewonnen", "Verloren"
- **success_probability** (optioneel): Succeskans tussen 0.0 en 1.0

## Berekeningsformule

De kernformule voor omzetprognose:
```
Verwachte omzet = Aantal leads × Conversiepercentage × Gemiddelde dealwaarde
```

## Contact
Voor vragen over deze applicatie, neem contact op met de ontwikkelaar.

---
© 2026 Sales Performance Solutions (SPS)
User Stories gerealiseerd

Alle 10 user stories zijn geïmplementeerd:

1. ✅ Leads kunnen invoeren
2. ✅ Conversiepercentage instellen
3. ✅ Gemiddelde dealwaarde aanpassen
4. ✅ Excel import
5. ✅ Jaaromzet berekenen
6. ✅ Kwartaalcijfers bekijken
7. ✅ Individuele omzet per salesperson
8. ✅ Scenario's opslaan
9. ✅ Rapport genereren
10. ✅ Foutmeldingen bij ongeldige invoer

Zie `TESTRESULTATEN.md` voor details over alle tests.