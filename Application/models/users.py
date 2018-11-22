"""This module handles users"""

class Users():
    
    def __init__(self,username,email,password,contact,admin=False):
        self.username = username
        self.email= email
        self.password = password
        self.admin = admin
        self.contact = contact
    
