class MailValidationException(Exception):
    def __init__(self, value):
        self.parameter = value    
        
    def __str__(self):
        return self.parameter
