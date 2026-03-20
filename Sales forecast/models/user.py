class User:
    """Gebruiker voor inloggen - SalesManager of SalesPerson"""
    
    def __init__(self, user_id, username, password, role, employee):
        """
        Args:
            user_id: Unieke identifier
            username: Login naam
            password: Wachtwoord (in echte app: hashed)
            role: 'manager' of 'salesperson'
            employee: Gekoppeld Employee/SalesManager/SalesPerson object
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.employee = employee
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_salesperson(self):
        return self.role == 'salesperson'
    
    def __repr__(self):
        return f"User({self.username}, {self.role})"
