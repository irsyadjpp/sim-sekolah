"""
ML-based Region Classifier

Uses machine learning to classify document regions based on features.
Hybrid approach: ML prediction with rule-based fallback for low confidence.
"""
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import pickle
from pathlib import Path

from app.models.document_models import Region, RegionType, BoundingBox, Page

logger = logging.getLogger(__name__)


@dataclass
class RegionFeatures:
    """Features extracted from a region for ML classification"""
    # Text features
    text_length: int
    word_count: int
    avg_word_length: float
    uppercase_ratio: float
    digit_ratio: float
    has_numbering: bool
    starts_with_bullet: bool
    
    # Position features
    y_position: float  # Normalized Y position (0-1)
    x_position: float  # Normalized X position (0-1)
    width_ratio: float  # Region width / page width
    height_ratio: float  # Region height / page height
    area_ratio: float  # Region area / page area
    
    # Format features
    line_count: int
    avg_line_length: float
    has_multiple_lines: bool
    
    # Content features
    has_table_keywords: bool
    has_image_keywords: bool
    has_formula_keywords: bool
    has_caption_keywords: bool


class MLRegionClassifier:
    """
    ML-based region classifier with hybrid approach.
    
    Uses scikit-learn for classification with rule-based fallback.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize ML region classifier.
        
        Args:
            model_path: Path to saved model file (if None, uses rule-based only)
        """
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.use_ml = False
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            logger.info("ML model not found, using rule-based classification only")
    
    def load_model(self, model_path: str) -> bool:
        """Load trained model from file"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.vectorizer = model_data['vectorizer']
                self.use_ml = True
                logger.info(f"Loaded ML model from {model_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def save_model(self, model_path: str) -> bool:
        """Save trained model to file"""
        try:
            model_data = {
                'model': self.model,
                'vectorizer': self.vectorizer
            }
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            logger.info(f"Saved ML model to {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return False
    
    def extract_features(self, region: Region, page: Page) -> RegionFeatures:
        """
        Extract features from a region for ML classification.
        
        Args:
            region: Region to extract features from
            page: Page containing the region (for normalization)
            
        Returns:
            RegionFeatures object
        """
        text = region.get_text()
        
        # Text features
        text_length = len(text)
        words = text.split()
        word_count = len(words)
        avg_word_length = np.mean([len(w) for w in words]) if words else 0
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        digit_ratio = sum(1 for c in text if c.isdigit()) / len(text) if text else 0
        has_numbering = any(text.strip().startswith(str(i)) for i in range(10)) or \
                      any(text.strip().startswith(f"{i}.") for i in range(10))
        starts_with_bullet = text.strip().startswith(('•', '-', '*', '○', '●'))
        
        # Position features (normalized)
        y_position = region.bbox.y1 / page.height if page.height > 0 else 0
        x_position = region.bbox.x1 / page.width if page.width > 0 else 0
        width_ratio = (region.bbox.x2 - region.bbox.x1) / page.width if page.width > 0 else 0
        height_ratio = (region.bbox.y2 - region.bbox.y1) / page.height if page.height > 0 else 0
        area_ratio = width_ratio * height_ratio
        
        # Format features
        lines = text.split('\n')
        line_count = len(lines)
        avg_line_length = np.mean([len(line) for line in lines]) if lines else 0
        has_multiple_lines = line_count > 1
        
        # Content features
        table_keywords = ['tabel', 'table', 'kolom', 'column', 'baris', 'row']
        image_keywords = ['gambar', 'image', 'foto', 'photo', 'gambar', 'ilustrasi']
        formula_keywords = ['persamaan', 'equation', 'rumus', 'formula', '=', '∫', '∑', '√']
        caption_keywords = ['caption', 'keterangan', 'deskripsi', 'description']
        
        text_lower = text.lower()
        has_table_keywords = any(kw in text_lower for kw in table_keywords)
        has_image_keywords = any(kw in text_lower for kw in image_keywords)
        has_formula_keywords = any(kw in text_lower for kw in formula_keywords)
        has_caption_keywords = any(kw in text_lower for kw in caption_keywords)
        
        return RegionFeatures(
            text_length=text_length,
            word_count=word_count,
            avg_word_length=avg_word_length,
            uppercase_ratio=uppercase_ratio,
            digit_ratio=digit_ratio,
            has_numbering=has_numbering,
            starts_with_bullet=starts_with_bullet,
            y_position=y_position,
            x_position=x_position,
            width_ratio=width_ratio,
            height_ratio=height_ratio,
            area_ratio=area_ratio,
            line_count=line_count,
            avg_line_length=avg_line_length,
            has_multiple_lines=has_multiple_lines,
            has_table_keywords=has_table_keywords,
            has_image_keywords=has_image_keywords,
            has_formula_keywords=has_formula_keywords,
            has_caption_keywords=has_caption_keywords
        )
    
    def features_to_array(self, features: RegionFeatures) -> np.ndarray:
        """Convert RegionFeatures to numpy array for ML model"""
        return np.array([
            features.text_length,
            features.word_count,
            features.avg_word_length,
            features.uppercase_ratio,
            features.digit_ratio,
            int(features.has_numbering),
            int(features.starts_with_bullet),
            features.y_position,
            features.x_position,
            features.width_ratio,
            features.height_ratio,
            features.area_ratio,
            features.line_count,
            features.avg_line_length,
            int(features.has_multiple_lines),
            int(features.has_table_keywords),
            int(features.has_image_keywords),
            int(features.has_formula_keywords),
            int(features.has_caption_keywords)
        ])
    
    def predict(self, region: Region, page: Page) -> Tuple[RegionType, float]:
        """
        Predict region type using ML model.
        
        Args:
            region: Region to classify
            page: Page containing the region
            
        Returns:
            Tuple of (predicted_type, confidence_score)
        """
        if not self.use_ml or not self.model:
            # Fall back to rule-based classification
            return self._rule_based_classify(region, page), 0.5
        
        try:
            features = self.extract_features(region, page)
            feature_array = self.features_to_array(features).reshape(1, -1)
            
            # Get prediction and probability
            prediction = self.model.predict(feature_array)[0]
            probabilities = self.model.predict_proba(feature_array)[0]
            confidence = max(probabilities)
            
            # Map prediction to RegionType
            predicted_type = self._map_prediction_to_type(prediction)
            
            # If confidence is low, fall back to rule-based
            if confidence < 0.6:
                rule_type = self._rule_based_classify(region, page)
                return rule_type, 0.5
            
            return predicted_type, confidence
            
        except Exception as e:
            logger.error(f"ML prediction failed: {e}")
            return self._rule_based_classify(region, page), 0.5
    
    def _rule_based_classify(self, region: Region, page: Page) -> RegionType:
        """
        Rule-based classification as fallback.
        
        Simple heuristic classification when ML is not available or confidence is low.
        """
        text = region.get_text().strip()
        text_lower = text.lower()
        
        # Check for specific patterns
        if not text:
            return RegionType.UNKNOWN
        
        # Title detection
        if (text.isupper() and len(text) < 100) or \
           any(text.startswith(f"{i}.") for i in range(1, 10)) or \
           any(text.startswith(f"{i} ") for i in range(1, 10)):
            return RegionType.TITLE
        
        # Heading detection
        if text.startswith(('Bab', 'BAB', 'Chapter', 'CHAPTER', 'Bagian', 'BAGIAN')):
            return RegionType.HEADING
        
        # Table detection
        table_keywords = ['tabel', 'table', 'kolom', 'column']
        if any(kw in text_lower for kw in table_keywords):
            return RegionType.TABLE
        
        # Formula detection
        formula_keywords = ['=', '∫', '∑', '√', 'persamaan', 'rumus']
        if any(kw in text for kw in formula_keywords):
            return RegionType.FORMULA
        
        # Caption detection
        caption_keywords = ['gambar', 'image', 'foto', 'caption', 'keterangan']
        if any(kw in text_lower for kw in caption_keywords):
            return RegionType.CAPTION
        
        # List detection
        if text.startswith(('•', '-', '*', '1.', '2.', '3.')):
            return RegionType.LIST_ITEM
        
        # Default to paragraph
        return RegionType.PARAGRAPH
    
    def _map_prediction_to_type(self, prediction: str) -> RegionType:
        """Map ML prediction to RegionType enum"""
        type_mapping = {
            'title': RegionType.TITLE,
            'subtitle': RegionType.SUBTITLE,
            'heading': RegionType.HEADING,
            'subheading': RegionType.SUBHEADING,
            'paragraph': RegionType.PARAGRAPH,
            'list': RegionType.LIST,
            'list_item': RegionType.LIST_ITEM,
            'table': RegionType.TABLE,
            'figure': RegionType.FIGURE,
            'formula': RegionType.FORMULA,
            'caption': RegionType.CAPTION,
            'footer': RegionType.FOOTER,
            'header': RegionType.HEADER,
            'page_number': RegionType.PAGE_NUMBER
        }
        return type_mapping.get(prediction, RegionType.PARAGRAPH)
    
    def train(self, labeled_regions: List[Tuple[Region, Page, RegionType]]) -> bool:
        """
        Train the ML model on labeled data.
        
        Args:
            labeled_regions: List of (region, page, correct_type) tuples
            
        Returns:
            True if training successful
        """
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            
            # Extract features and labels
            X = []
            y = []
            
            for region, page, correct_type in labeled_regions:
                features = self.extract_features(region, page)
                X.append(self.features_to_array(features))
                y.append(correct_type.value)
            
            X = np.array(X)
            y = np.array(y)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X, y)
            
            self.use_ml = True
            logger.info(f"Trained ML model on {len(labeled_regions)} samples")
            
            return True
            
        except ImportError:
            logger.warning("scikit-learn not installed, ML classification unavailable")
            return False
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False
    
    def classify_regions(self, regions: List[Region], page: Page) -> List[Region]:
        """
        Classify multiple regions on a page.
        
        Args:
            regions: List of regions to classify
            page: Page containing the regions
            
        Returns:
            Regions with updated region_type
        """
        for region in regions:
            predicted_type, confidence = self.predict(region, page)
            region.region_type = predicted_type
            region.metadata = region.metadata or {}
            region.metadata['ml_confidence'] = confidence
            region.metadata['classification_method'] = 'ml' if self.use_ml else 'rule_based'
        
        return regions
