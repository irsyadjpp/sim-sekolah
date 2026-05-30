"""
Learning Objectives Domain

This domain handles Tujuan Pembelajaran (TP) intelligence, which is the core entity
connecting CP (Capaian Pembelajaran) to ATP (Alur Tujuan Pembelajaran) in the
Kurikulum Merdeka framework.

Flow: CP → TP → ATP → Modul Ajar → Assessment
"""

from .tp_parser import TPParser
from .tp_mapper import TPMapper
from .tp_progression import TPProgressionEngine
from .tp_mastery import TPMasteryEngine
from .tp_alignment import TPAlignment
from .tp_validator import TPValidator
from .tp_assessment_linker import TPAssessmentLinker
from .tp_activity_linker import TPActivityLinker

__all__ = [
    "TPParser",
    "TPMapper",
    "TPProgressionEngine",
    "TPMasteryEngine",
    "TPAlignment",
    "TPValidator",
    "TPAssessmentLinker",
    "TPActivityLinker"
]
