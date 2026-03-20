"""
Flask Web Applicatie - Sales Forecast Simulatie
Sales Performance Solutions (SPS)
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import secrets
from datetime import datetime
from typing import List

from models.lead import Lead
from models.employee import SalesPerson, SalesManager
from models.product import Product
from models.deal import Deal
from models.scenario import Scenario
from models.simulation import Simulation
from models.sales_year import SalesYear
from models.report import Report
from data_importer import DataImporter
from auth_helper import auth_manager, login_required, manager_required


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Zorg dat upload folder bestaat
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Globale data storage (in productie zou dit een database zijn)
class DataStore:
    def __init__(self):
        self.simulations = []
        self.scenarios = []
        self.managers = []
        self.salespersons = []
        self.sales_years = []
        self.reports = []
        self.leads = []
        self.current_id = 1
    
    def get_next_id(self):
        id = self.current_id
        self.current_id += 1
        return id

data_store = DataStore()


# Testdata aanmaken (managers en salespersons met users)
def init_test_data():
    """Initialiseer testdata met gebruikers"""
    
    # Maak managers aan
    manager1 = SalesManager("M001", "Erik Jansen", "info@eriked.nl")
    data_store.managers.append(manager1)
    
    manager_user = auth_manager.create_user("manager", "wachtwoord", "manager", manager1)
    
    # Maak salespersons aan (gekoppeld aan manager)
    sp1 = SalesPerson("E001", "John Smith", "john@example.com")
    sp2 = SalesPerson("E002", "Lisa Mueller", "lisa@example.com")
    data_store.salespersons.extend([sp1, sp2])
    
    # Voeg salespersons toe aan manager via add_team_member method
    manager1.add_team_member(sp1)
    manager1.add_team_member(sp2)
    
    # Maak users voor salespersons
    sp_user = auth_manager.create_user("john", "wachtwoord", "salesperson", sp1)
    sp_user2 = auth_manager.create_user("lisa", "wachtwoord", "salesperson", sp2)


# Initialiseer testdata
init_test_data()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login pagina"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user = auth_manager.authenticate(username, password)
        
        if user:
            # Succesvolle login: opslaan in session
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role
            session['employee_id'] = user.employee.id if user.employee else None
            
            flash(f'Welkom {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect gebruikersnaam of wachtwoord', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Uitloggen"""
    username = session.get('username', 'Gebruiker')
    session.clear()
    flash(f'{username} is uitgelogd', 'info')
    return redirect(url_for('login'))


@app.route('/')
def index():
    """Homepage - redirect naar login of dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard met overzicht"""
    # Redirect salesperson naar eigen dashboard
    if session.get('role') == 'salesperson':
        return redirect(url_for('salesperson_dashboard'))
    
    stats = {
        'total_simulations': len(data_store.simulations),
        'total_scenarios': len(data_store.scenarios),
        'total_salespersons': len(data_store.salespersons),
        'total_managers': len(data_store.managers),
        'total_leads': len(data_store.leads)
    }
    
    # Bereken totale verwachte omzet
    total_revenue = 0
    for sim in data_store.simulations:
        if sim.result:
            total_revenue += sim.result.total_revenue
    
    stats['total_revenue'] = total_revenue
    
    return render_template('dashboard.html', 
                         stats=stats,
                         simulations=data_store.simulations,
                         scenarios=data_store.scenarios)


@app.route('/simulations')
@login_required
def simulations():
    """Overzicht van alle simulaties"""
    return render_template('simulations.html', simulations=data_store.simulations)


@app.route('/simulation/new', methods=['GET', 'POST'])
@manager_required
def new_simulation():
    """Nieuwe simulatie aanmaken"""
    if request.method == 'POST':
        name = request.form.get('name')
        num_leads = int(request.form.get('num_leads', 0))
        conversion_rate = float(request.form.get('conversion_rate', 0)) / 100
        average_deal_value = float(request.form.get('average_deal_value', 0))
        
        # Validatie
        errors = []
        if not name:
            errors.append("Naam is verplicht")
        if num_leads < 0:
            errors.append("Aantal leads kan niet negatief zijn")
        if not 0 <= conversion_rate <= 1:
            errors.append("Conversiepercentage moet tussen 0 en 100 liggen")
        if average_deal_value < 0:
            errors.append("Gemiddelde dealwaarde kan niet negatief zijn")
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('simulation_new.html', scenarios=data_store.scenarios)
        
        # Maak simulatie
        sim = Simulation(data_store.get_next_id(), name)
        
        # Gebruik scenario als geselecteerd
        scenario_id = request.form.get('scenario_id')
        if scenario_id:
            scenario = next((s for s in data_store.scenarios if s.name == scenario_id), None)
            if scenario:
                sim.set_scenario(scenario)
                num_leads = scenario.num_leads
                conversion_rate = scenario.conversion_rate
                average_deal_value = scenario.average_deal_value
        
        # Voer simulatie uit
        try:
            from models.simulation import SimulationResult
            total_revenue = sim.calculate_year_revenue(num_leads, conversion_rate, average_deal_value)
            quarterly = sim.calculate_quarterly_revenue(num_leads, conversion_rate, average_deal_value)
            
            sim.result = SimulationResult(
                total_revenue=total_revenue,
                revenue_per_quarter=quarterly,
                num_leads=num_leads,
                conversion_rate=conversion_rate,
                average_deal_value=average_deal_value
            )
            
            data_store.simulations.append(sim)
            flash(f'✓ Simulatie "{name}" succesvol aangemaakt! Verwachte omzet: €{total_revenue:,.2f}', 'success')
            return redirect(url_for('simulation_detail', sim_id=sim.id))
            
        except Exception as e:
            flash(f'Fout bij simulatie: {str(e)}', 'danger')
    
    return render_template('simulation_new.html', scenarios=data_store.scenarios)


@app.route('/simulation/<int:sim_id>')
@login_required
def simulation_detail(sim_id):
    """Detail pagina van een simulatie"""
    sim = next((s for s in data_store.simulations if s.id == sim_id), None)
    if not sim:
        flash('Simulatie niet gevonden', 'danger')
        return redirect(url_for('simulations'))
    
    return render_template('simulation_detail.html', simulation=sim)


@app.route('/simulation/<int:sim_id>/delete', methods=['POST'])
@manager_required
def delete_simulation(sim_id):
    """Verwijder een simulatie"""
    sim = next((s for s in data_store.simulations if s.id == sim_id), None)
    if sim:
        data_store.simulations.remove(sim)
        flash(f'Simulatie "{sim.name}" verwijderd', 'success')
    return redirect(url_for('simulations'))


@app.route('/scenarios')
@manager_required
def scenarios():
    """Overzicht van alle scenario's"""
    return render_template('scenarios.html', scenarios=data_store.scenarios)


@app.route('/scenario/new', methods=['GET', 'POST'])
@manager_required
def new_scenario():
    """Nieuw scenario aanmaken"""
    if request.method == 'POST':
        name = request.form.get('name')
        num_leads = int(request.form.get('num_leads', 0))
        conversion_rate = float(request.form.get('conversion_rate', 0)) / 100
        average_deal_value = float(request.form.get('average_deal_value', 0))
        
        try:
            scenario = Scenario(name, conversion_rate, average_deal_value, num_leads)
            data_store.scenarios.append(scenario)
            flash(f'✓ Scenario "{name}" aangemaakt! Verwachte omzet: €{scenario.calculate_expected_revenue():,.2f}', 'success')
            return redirect(url_for('scenarios'))
        except ValueError as e:
            flash(f'Fout: {str(e)}', 'danger')
    
    return render_template('scenario_new.html')


@app.route('/scenario/<scenario_name>/delete', methods=['POST'])
@manager_required
def delete_scenario(scenario_name):
    """Verwijder een scenario"""
    scenario = next((s for s in data_store.scenarios if s.name == scenario_name), None)
    if scenario:
        data_store.scenarios.remove(scenario)
        flash(f'Scenario "{scenario.name}" verwijderd', 'success')
    return redirect(url_for('scenarios'))


@app.route('/team')
@manager_required
def team():
    """Team overzicht"""
    return render_template('team.html', 
                         managers=data_store.managers,
                         salespersons=data_store.salespersons)


@app.route('/team/manager/new', methods=['GET', 'POST'])
@manager_required
def new_manager():
    """Nieuwe manager toevoegen"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not name or not email:
            flash('Naam en email zijn verplicht', 'danger')
            return render_template('manager_new.html')
        
        manager = SalesManager(data_store.get_next_id(), name, email)
        data_store.managers.append(manager)
        flash(f'✓ Sales Manager "{name}" toegevoegd', 'success')
        return redirect(url_for('team'))
    
    return render_template('manager_new.html')


@app.route('/team/salesperson/new', methods=['GET', 'POST'])
@manager_required
def new_salesperson():
    """Nieuwe salesperson toevoegen"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        manager_id = request.form.get('manager_id')
        
        if not name or not email:
            flash('Naam en email zijn verplicht', 'danger')
            return render_template('salesperson_new.html', managers=data_store.managers)
        
        sp = SalesPerson(data_store.get_next_id(), name, email)
        
        # Voeg toe aan manager indien geselecteerd
        if manager_id:
            manager = next((m for m in data_store.managers if m.id == int(manager_id)), None)
            if manager:
                manager.add_team_member(sp)
        
        data_store.salespersons.append(sp)
        flash(f'✓ Sales Person "{name}" toegevoegd', 'success')
        return redirect(url_for('team'))
    
    return render_template('salesperson_new.html', managers=data_store.managers)


@app.route('/leads')
@manager_required
def leads():
    """Overzicht van alle leads"""
    # Bereken totale verwachte waarde
    total_expected_value = sum(lead.calculate_expected_value() for lead in data_store.leads)
    
    return render_template('leads.html', 
                         leads=data_store.leads,
                         total_expected_value=total_expected_value,
                         salespersons=data_store.salespersons)


@app.route('/lead/new', methods=['GET', 'POST'])
@manager_required
def new_lead():
    """Nieuwe lead toevoegen"""
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        estimated_value = float(request.form.get('estimated_value', 0))
        success_probability = float(request.form.get('success_probability', 0)) / 100
        status = request.form.get('status', 'Nieuw')
        
        try:
            lead = Lead(data_store.get_next_id(), company_name, estimated_value, status, success_probability)
            data_store.leads.append(lead)
            flash(f'✓ Lead "{company_name}" toegevoegd', 'success')
            return redirect(url_for('leads'))
        except ValueError as e:
            flash(f'Fout: {str(e)}', 'danger')
    
    return render_template('lead_new.html')


@app.route('/lead/<int:lead_id>/edit', methods=['GET', 'POST'])
@manager_required
def edit_lead(lead_id):
    """Lead bewerken (manager)"""
    lead = next((l for l in data_store.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden', 'danger')
        return redirect(url_for('leads'))
    
    if request.method == 'POST':
        lead.company_name = request.form.get('company_name')
        lead.estimated_value = float(request.form.get('estimated_value', 0))
        lead.success_probability = float(request.form.get('success_probability', 0)) / 100
        lead.status = request.form.get('status', 'Nieuw')
        
        flash(f'✓ Lead "{lead.company_name}" bijgewerkt', 'success')
        return redirect(url_for('leads'))
    
    return render_template('lead_edit.html', lead=lead)


@app.route('/import', methods=['GET', 'POST'])
@manager_required
def import_excel():
    """Excel import pagina"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Geen bestand geselecteerd', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Geen bestand geselecteerd', 'danger')
            return redirect(request.url)
        
        if file and file.filename.endswith(('.xlsx', '.xls')):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            file.save(filename)
            
            try:
                leads = DataImporter.import_from_excel(filename)
                
                # Voeg leads toe aan data store
                for lead in leads:
                    lead.id = data_store.get_next_id()
                    data_store.leads.extend(leads)
                
                flash(f'✓ {len(leads)} leads succesvol geïmporteerd!', 'success')
                
                # Optie om simulatie aan te maken
                session['imported_leads'] = len(leads)
                return redirect(url_for('leads'))
                
            except Exception as e:
                flash(f'Fout bij importeren: {str(e)}', 'danger')
                os.remove(filename)
        else:
            flash('Alleen .xlsx en .xls bestanden zijn toegestaan', 'danger')
    
    return render_template('import.html')


# ============= SALESPERSON ROUTES =============

@app.route('/salesperson/dashboard')
@login_required
def salesperson_dashboard():
    """Dashboard voor salesperson - eigen statistieken"""
    if session.get('role') != 'salesperson':
        return redirect(url_for('dashboard'))
    
    # Zoek de salesperson
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    if not salesperson:
        flash('Salesperson niet gevonden', 'danger')
        return redirect(url_for('dashboard'))
    
    stats = {
        'total_leads': len(salesperson.leads),
        'total_deals': len(salesperson.deals),
        'expected_revenue': salesperson.get_total_expected_revenue(),
        'closed_revenue': salesperson.get_total_closed_revenue(),
        'conversion_rate': salesperson.get_conversion_rate() * 100
    }
    
    return render_template('salesperson_dashboard.html', 
                         salesperson=salesperson,
                         stats=stats)


@app.route('/salesperson/leads')
@login_required
def salesperson_leads():
    """Eigen leads bekijken"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    if not salesperson:
        flash('Salesperson niet gevonden', 'danger')
        return redirect(url_for('dashboard'))
    
    total_expected_value = salesperson.get_total_expected_revenue()
    
    return render_template('salesperson_leads.html', 
                         leads=salesperson.leads,
                         total_expected_value=total_expected_value,
                         salesperson=salesperson)


@app.route('/salesperson/lead/new', methods=['GET', 'POST'])
@login_required
def salesperson_new_lead():
    """Salesperson kan nieuwe lead aanmaken"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        estimated_value = float(request.form.get('estimated_value', 0))
        success_probability = float(request.form.get('success_probability', 0)) / 100
        status = request.form.get('status', 'Nieuw')
        
        try:
            lead = Lead(data_store.get_next_id(), company_name, estimated_value, status, success_probability)
            
            # Voeg toe aan salesperson
            employee_id = session.get('employee_id')
            salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
            
            if salesperson:
                salesperson.add_lead(lead)
                data_store.leads.append(lead)
                flash(f'✓ Lead "{company_name}" toegevoegd', 'success')
                return redirect(url_for('salesperson_leads'))
            
        except ValueError as e:
            flash(f'Fout: {str(e)}', 'danger')
    
    return render_template('salesperson_lead_new.html')


@app.route('/salesperson/lead/<int:lead_id>/status', methods=['POST'])
@login_required
def salesperson_update_lead_status(lead_id):
    """Salesperson kan status van eigen lead wijzigen"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    lead = next((l for l in salesperson.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden of geen toegang', 'danger')
        return redirect(url_for('salesperson_leads'))
    
    new_status = request.form.get('status')
    lead.update_status(new_status)
    flash(f'Status gewijzigd naar: {new_status}', 'success')
    
    return redirect(url_for('salesperson_leads'))


@app.route('/salesperson/lead/<int:lead_id>/edit', methods=['GET', 'POST'])
@login_required
def salesperson_edit_lead(lead_id):
    """Salesperson kan eigen lead bewerken"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    lead = next((l for l in salesperson.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden of geen toegang', 'danger')
        return redirect(url_for('salesperson_leads'))
    
    if request.method == 'POST':
        lead.company_name = request.form.get('company_name')
        lead.estimated_value = float(request.form.get('estimated_value', 0))
        lead.success_probability = float(request.form.get('success_probability', 0)) / 100
        lead.status = request.form.get('status', 'Nieuw')
        
        flash(f'✓ Lead "{lead.company_name}" bijgewerkt', 'success')
        return redirect(url_for('salesperson_leads'))
    
    return render_template('salesperson_lead_edit.html', lead=lead)


@app.route('/salesperson/lead/<int:lead_id>/convert', methods=['POST'])
@login_required
def salesperson_convert_lead(lead_id):
    """Salesperson kan lead converteren naar deal"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    lead = next((l for l in salesperson.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden of geen toegang', 'danger')
        return redirect(url_for('salesperson_leads'))
    
    if lead.status == 'Gewonnen':
        # Maak deal aan
        deal_value = float(request.form.get('deal_value', lead.estimated_value))
        deal = Deal(data_store.get_next_id(), lead.company_name, deal_value)
        
        salesperson.convert_lead_to_deal(lead, deal)
        
        flash(f'✓ Lead geconverteerd naar deal! Waarde: €{deal_value:,.2f}', 'success')
    else:
        flash('Lead moet status "Gewonnen" hebben om te converteren', 'warning')
    
    return redirect(url_for('salesperson_leads'))


@app.route('/salesperson/lead/<int:lead_id>/convert-page', methods=['GET', 'POST'])
@login_required
def salesperson_convert_lead_page(lead_id):
    """Pagina om lead te converteren naar deal"""
    if session.get('role') != 'salesperson':
        flash('Je hebt geen toegang', 'danger')
        return redirect(url_for('dashboard'))
    
    employee_id = session.get('employee_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == employee_id), None)
    
    lead = next((l for l in salesperson.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden of geen toegang', 'danger')
        return redirect(url_for('salesperson_leads'))
    
    if lead.status != 'Gewonnen':
        flash('Lead moet status "Gewonnen" hebben om te converteren', 'warning')
        return redirect(url_for('salesperson_leads'))
    
    if request.method == 'POST':
        deal_value = float(request.form.get('deal_value', lead.estimated_value))
        deal = Deal(data_store.get_next_id(), lead.company_name, deal_value)
        
        salesperson.convert_lead_to_deal(lead, deal)
        
        flash(f'✓ Lead "{lead.company_name}" geconverteerd naar deal! Waarde: €{deal_value:,.2f}', 'success')
        return redirect(url_for('salesperson_leads'))
    
    return render_template('salesperson_convert_lead.html', lead=lead)


@app.route('/manager/lead/<int:lead_id>/assign', methods=['POST'])
@manager_required
def manager_assign_lead(lead_id):
    """Manager wijst lead toe aan salesperson"""
    lead = next((l for l in data_store.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden', 'danger')
        return redirect(url_for('leads'))
    
    salesperson_id = request.form.get('salesperson_id')
    salesperson = next((sp for sp in data_store.salespersons if sp.id == salesperson_id), None)
    
    if not salesperson:
        flash('Salesperson niet gevonden', 'danger')
        return redirect(url_for('leads'))
    
    # Vind manager
    manager = next((m for m in data_store.managers if salesperson in m.team), None)
    
    if manager:
        manager.assign_lead_to_salesperson(lead, salesperson)
        flash(f'✓ Lead toegewezen aan {salesperson.name}', 'success')
    else:
        # Direct toewijzen als geen manager gevonden
        salesperson.add_lead(lead)
        flash(f'✓ Lead toegewezen aan {salesperson.name}', 'success')
    
    return redirect(url_for('leads'))


@app.route('/manager/lead/<int:lead_id>/assign-page', methods=['GET', 'POST'])
@manager_required
def manager_assign_lead_page(lead_id):
    """Pagina om lead toe te wijzen aan salesperson"""
    lead = next((l for l in data_store.leads if l.id == lead_id), None)
    
    if not lead:
        flash('Lead niet gevonden', 'danger')
        return redirect(url_for('leads'))
    
    if request.method == 'POST':
        salesperson_id = request.form.get('salesperson_id')
        salesperson = next((sp for sp in data_store.salespersons if sp.id == salesperson_id), None)
        
        if not salesperson:
            flash('Salesperson niet gevonden', 'danger')
            return redirect(url_for('manager_assign_lead_page', lead_id=lead_id))
        
        # Als de lead al aan een andere salesperson is toegewezen, verwijder deze eerst
        if lead.sales_person_id and lead.sales_person_id != salesperson_id:
            old_salesperson = next((sp for sp in data_store.salespersons if sp.id == lead.sales_person_id), None)
            if old_salesperson and lead in old_salesperson.leads:
                old_salesperson.leads.remove(lead)
        
        # Vind manager
        manager = next((m for m in data_store.managers if salesperson in m.team), None)
        
        if manager:
            manager.assign_lead_to_salesperson(lead, salesperson)
            flash(f'✓ Lead "{lead.company_name}" toegewezen aan {salesperson.name}', 'success')
        else:
            # Direct toewijzen als geen manager gevonden
            salesperson.add_lead(lead)
            flash(f'✓ Lead "{lead.company_name}" toegewezen aan {salesperson.name}', 'success')
        
        return redirect(url_for('leads'))
    
    return render_template('manager_assign_lead.html', 
                         lead=lead, 
                         salespersons=data_store.salespersons)


@app.route('/reports')
@manager_required
def reports():
    """Overzicht van rapporten"""
    return render_template('reports.html', reports=data_store.reports)


@app.route('/report/simulation/<int:sim_id>')
@manager_required
def generate_simulation_report(sim_id):
    """Genereer rapport voor simulatie"""
    sim = next((s for s in data_store.simulations if s.id == sim_id), None)
    if not sim:
        flash('Simulatie niet gevonden', 'danger')
        return redirect(url_for('simulations'))
    
    if not sim.result:
        flash('Simulatie heeft nog geen resultaten', 'danger')
        return redirect(url_for('simulation_detail', sim_id=sim_id))
    
    report = Report(data_store.get_next_id(), f"Rapport {sim.name}", 1)
    content = report.generate_simulation_report(sim)
    data_store.reports.append(report)
    
    return render_template('report_view.html', report=report, content=content)


@app.route('/api/simulation/calculate', methods=['POST'])
@login_required
def api_calculate_simulation():
    """API endpoint voor simulatie berekening"""
    data = request.get_json()
    
    num_leads = int(data.get('num_leads', 0))
    conversion_rate = float(data.get('conversion_rate', 0)) / 100
    average_deal_value = float(data.get('average_deal_value', 0))
    
    sim = Simulation(0, "API Calculation")
    
    try:
        total_revenue = sim.calculate_year_revenue(num_leads, conversion_rate, average_deal_value)
        quarterly = sim.calculate_quarterly_revenue(num_leads, conversion_rate, average_deal_value)
        
        return jsonify({
            'success': True,
            'total_revenue': total_revenue,
            'quarterly': quarterly,
            'formatted_revenue': f"€{total_revenue:,.2f}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  SALES FORECAST SIMULATIE - WEB APPLICATIE")
    print("  Sales Performance Solutions (SPS)")
    print("=" * 70)
    print("\n  Applicatie draait op: http://127.0.0.1:5000")
    print("  Druk op CTRL+C om te stoppen\n")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
