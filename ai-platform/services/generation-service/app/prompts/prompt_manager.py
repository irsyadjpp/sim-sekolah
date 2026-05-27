"""
Prompt manager for managing prompt templates
Supports educational-specific templates for Kurikulum Merdeka
"""
import json
import os
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class PromptManager:
    """Manager for prompt templates"""
    
    def __init__(self):
        """Initialize prompt manager"""
        logger.info("Initializing prompt manager")
        
        # Built-in templates for educational context
        self.templates = {
            "lesson_plan": """Buatkan rencana pelajaran untuk mata pelajaran {subject} pada kelas {grade} dengan topik {topic}.
            
            Kompetensi Dasar: {competency}
            Tujuan Pembelajaran: {objectives}
            
            Pastikan rencana pelajaran mencakup:
            1. Kegiatan pendahuluan
            2. Kegiatan inti dengan metode {method}
            3. Kegiatan penutup
            4. Penilaian
            
            Sesuaikan dengan Kurikulum Merdeka dan Profil Pelajar Pancasila.""",
            
            "assessment": """Buatkan instrumen penilaian untuk {subject} kelas {grade} pada topik {topic}.
            
            Kompetensi yang dinilai: {competency}
            Tingkat kognitif Bloom: {bloom_level}
            
            Buatlah:
            1. Soal evaluasi (5 pertanyaan)
            2. Rubrik penilaian
            3. Kriteria kelulusan
            
            Pastikan sesuai dengan prinsip penilaian Kurikulum Merdeka.""",
            
            "explanation": """Jelaskan konsep {concept} dalam mata pelajaran {subject} untuk siswa {grade}.
            
            Gunakan bahasa yang sesuai dengan usia siswa.
            Berikan contoh konkret yang relevan dengan kehidupan sehari-hari.
            Jelaskan dengan langkah-langkah yang jelas dan terstruktur.
            
 Targetkan tingkat pemahaman: {target_level}""",
            
            "question_generation": """Buatkan {count} pertanyaan untuk topik {topic} dalam mata pelajaran {subject}.
            
            Tingkat kesulitan: {difficulty}
            Kompetensi yang diukur: {competency}
            
            Pertanyaan harus:
            1. Mengukur pemahaman konsep
            2. Mendorong berpikir kritis
            3. Kontekstual dengan Kurikulum Merdeka
            4. Bervariasi dalam format (pilihan ganda, esai, dll)""",
            
            "differentiation": """Berikan strategi diferensiasi untuk materi {topic} di kelas {grade}.
            
            Perhatikan:
            1. Perbedaan gaya belajar siswa
            2. Kebutuhan siswa dengan kemampuan berbeda
            3. Adaptasi materi untuk berbagai tingkat
            
            Berikan strategi spesifik untuk:
            - Siswa visual
            - Siswa auditori
            - Siswa kinestetik
            - Siswa dengan kesulitan belajar"""
        }
    
    async def build_from_template(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> str:
        """
        Build prompt from template
        
        Args:
            template_name: Name of the template
            variables: Dictionary of variables to substitute
        
        Returns:
            Built prompt string
        """
        try:
            if template_name not in self.templates:
                raise ValueError(f"Template {template_name} not found")
            
            template = self.templates[template_name]
            
            # Substitute variables
            prompt = template.format(**variables)
            
            logger.info(f"Built prompt from template: {template_name}")
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error building prompt from template: {str(e)}")
            raise
    
    async def create_template(
        self,
        template_name: str,
        template_content: str
    ) -> bool:
        """
        Create a new template
        
        Args:
            template_name: Name of the new template
            template_content: Template content with {variable} placeholders
        
        Returns:
            Success status
        """
        try:
            self.templates[template_name] = template_content
            logger.info(f"Created template: {template_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating template: {str(e)}")
            return False
    
    async def list_templates(self) -> List[Dict[str, str]]:
        """
        List all available templates
        
        Returns:
            List of template information
        """
        return [
            {
                "name": name,
                "description": self._get_template_description(name)
            }
            for name in self.templates.keys()
        ]
    
    def _get_template_description(self, template_name: str) -> str:
        """Get description for a template"""
        descriptions = {
            "lesson_plan": "Generate lesson plans following Kurikulum Merdeka",
            "assessment": "Create assessment instruments and rubrics",
            "explanation": "Explain concepts for different grade levels",
            "question_generation": "Generate questions for various competencies",
            "differentiation": "Provide differentiation strategies"
        }
        return descriptions.get(template_name, "Custom template")
    
    async def update_template(
        self,
        template_name: str,
        template_content: str
    ) -> bool:
        """
        Update an existing template
        
        Args:
            template_name: Name of the template to update
            template_content: New template content
        
        Returns:
            Success status
        """
        try:
            if template_name not in self.templates:
                return False
            
            self.templates[template_name] = template_content
            logger.info(f"Updated template: {template_name}")
            return True
        except Exception as e:
            logger.error(f"Error updating template: {str(e)}")
            return False
    
    async def delete_template(self, template_name: str) -> bool:
        """
        Delete a template
        
        Args:
            template_name: Name of the template to delete
        
        Returns:
            Success status
        """
        try:
            if template_name in self.templates:
                del self.templates[template_name]
                logger.info(f"Deleted template: {template_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting template: {str(e)}")
            return False
    
    async def save_templates_to_file(self, filepath: str) -> bool:
        """
        Save templates to JSON file
        
        Args:
            filepath: Path to save templates
        
        Returns:
            Success status
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.templates, f, indent=2)
            logger.info(f"Saved templates to: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving templates: {str(e)}")
            return False
    
    async def load_templates_from_file(self, filepath: str) -> bool:
        """
        Load templates from JSON file
        
        Args:
            filepath: Path to load templates from
        
        Returns:
            Success status
        """
        try:
            with open(filepath, 'r') as f:
                loaded_templates = json.load(f)
            self.templates.update(loaded_templates)
            logger.info(f"Loaded templates from: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
            return False