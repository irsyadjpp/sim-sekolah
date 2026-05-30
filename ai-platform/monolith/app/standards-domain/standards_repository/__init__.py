"""
Standards Repository Module

This module provides database access, validation engine, and alignment checking
for all curriculum standards. It serves as the central data layer for standards operations.
"""

from .standards_db import StandardsDatabase
from .validation_engine import ValidationEngine
from .alignment_checker import AlignmentChecker

__all__ = [
    "StandardsRepository",
    "StandardsDatabase",
    "ValidationEngine",
    "AlignmentChecker"
]

class StandardsRepository:
    """Main repository for standards operations"""
    
    def __init__(self):
        self.database = StandardsDatabase()
        self.validation_engine = ValidationEngine()
        self.alignment_checker = AlignmentChecker()
    
    def get_standard(self, standard_type: str, standard_id: str) -> dict:
        """Get specific standard by type and ID"""
        return self.database.get_standard(standard_type, standard_id)
    
    def validate_document(self, document_data: dict, document_type: str) -> dict:
        """Validate document against standards"""
        return self.validation_engine.validate_document(document_data, document_type)
    
    def check_alignment(self, document_data: dict, target_standard: str) -> dict:
        """Check alignment of document with target standard"""
        return self.alignment_checker.check_alignment(document_data, target_standard)
    
    def save_standard(self, standard_data: dict) -> dict:
        """Save new standard to database"""
        return self.database.save_standard(standard_data)
    
    def update_standard(self, standard_id: str, update_data: dict) -> dict:
        """Update existing standard"""
        return self.database.update_standard(standard_id, update_data)