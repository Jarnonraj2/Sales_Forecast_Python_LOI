"""
Authentication helpers voor login/logout
"""
from functools import wraps
from flask import session, redirect, url_for, flash

class AuthManager:
    """Beheert inloggen, gebruikers en permissions"""
    
    def __init__(self):
        self.users = {}  # username -> User object
        self.user_counter = 1
    
    def create_user(self, username, password, role, employee):
        """Maak een nieuwe gebruiker aan"""
        from models.user import User
        user = User(self.user_counter, username, password, role, employee)
        self.users[username] = user
        self.user_counter += 1
        return user
    
    def authenticate(self, username, password):
        """Controleer login gegevens"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        # In echte app: password hashen en vergelijken
        if user.password == password:
            return user
        return None
    
    def get_user_by_username(self, username):
        """Zoek gebruiker op username"""
        return self.users.get(username)
    
    def user_exists(self, username):
        """Controleer of gebruiker bestaat"""
        return username in self.users


# Globale auth manager
auth_manager = AuthManager()


def login_required(f):
    """Decorator: Redirect naar login als niet ingelogd"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Je moet inloggen', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def manager_required(f):
    """Decorator: Alleen voor managers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Je moet inloggen', 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'manager':
            flash('Je mag dit niet doen', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


def salesperson_required(f):
    """Decorator: Alleen voor salespersons"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Je moet inloggen', 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'salesperson':
            flash('Je mag dit niet doen', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function
