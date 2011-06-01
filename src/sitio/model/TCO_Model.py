'''
This module implements the logic of the TCO model defined in the SITIO project.
'''

class CC():
    """Cost component (CC) is a representation of an attribute of TCO"""
    
    def __init__(self, value = None, description = "Unknown component"):
        self.value = value
        self.description = description

class TCOModel():
    
    class OperationalBusinessCosts(CC):
        
        class Personnel(CC):
            pass 
    
        class Hardware(CC):
            pass
        
        class Software(CC):
            pass
        
        class Auditing(CC):
            pass
        
    class StrategicBusinessCosts(CC):
        
        class AddingRetiringProductLines(CC):
            pass 
        
        class NewMarkets(CC):
            pass
    
    class RisksAndRelatedCosts(CC):
        
        class MigrationRisks(CC):
            pass
        
        class ImplementationRisks(CC):
            pass
        
        class BacksourcingRisks(CC):
            pass
        
        class LegalRisks(CC):
            
            class DataProtectionRisks(CC):
                pass
    
    class ExternalParametersCosts(CC):
        
        class ComplianceToExternalNecessities(CC):
            pass
        
        class WiderHumanAndOrganizationalImpacts(CC):
            pass
        
        class ArchitecturalCosts(CC):
            """Architectural costs facilitate comparison between different cloud 
            computing platforms (e.g., Amazon EC2, Microsoft Azure, and Google AppEngine)."""
            pass
