"""
Standards Domain - Foundational Bounded Context

This domain serves as the authoritative source for all curriculum-related standards
aligned with Kurikulum Merdeka Indonesia. All other domains (curriculum, assessment, 
learning) depend on this domain for standards validation and alignment.

Key Components:
- Kurikulum Merdeka Standards (CP, ATP, Modul Ajar, Assessment, Rubric)
- Profil Pelajar Pancasila (6 dimensions)
- Capaian Pembelajaran (Learning Objectives, Competency Levels)
- Standards Repository (Database, Validation, Alignment)
- Standards API (National Standards Integration)
"""

from .kurikulum_merdeka import KurikulumMerdekaStandards
from .profil_pelajar_pancasila import ProfilPelajarPancasila
from .capaian_pembelajaran import CapaianPembelajaran
from .standards_repository import StandardsRepository
from .standards_api import StandardsAPI

__version__ = "1.0.0"
__domain__ = "standards-domain"
__foundation__ = True  # This is a foundational domain