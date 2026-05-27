#!/usr/bin/env python3
"""
Knowledge Base Audit and Versioning Tool

This script audits the knowledge base content, validates metadata,
and ensures proper versioning of educational materials.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class KnowledgeAsset:
    """Knowledge asset metadata."""
    path: str
    category: str
    subject: Optional[str]
    grade_level: Optional[str]
    version: Optional[str]
    file_type: str
    size_bytes: int
    hash_md5: str
    last_modified: str
    has_metadata: bool
    has_version_file: bool
    issues: List[str]


class KnowledgeAuditor:
    """Auditor for knowledge base content."""
    
    REQUIRED_CATEGORIES = [
        "cp", "atp", "buku_guru", "buku_siswa", "modul_ajar", 
        "asesmen", "media", "p5", "ontology"
    ]
    
    def __init__(self, knowledge_root: str):
        """
        Initialize knowledge auditor.
        
        Args:
            knowledge_root: Root directory of knowledge base
        """
        self.knowledge_root = Path(knowledge_root)
        self.assets: List[KnowledgeAsset] = []
        self.issues: List[str] = []
        
    def audit_all(self) -> Dict[str, Any]:
        """
        Audit entire knowledge base.
        
        Returns:
            Audit results summary
        """
        print(f"Auditing knowledge base: {self.knowledge_root}")
        print("=" * 60)
        
        # Audit directory structure
        self._audit_structure()
        
        # Audit each category
        for category in self.REQUIRED_CATEGORIES:
            category_path = self.knowledge_root / category
            if category_path.exists():
                self._audit_category(category)
            else:
                self.issues.append(f"Missing required category: {category}/")
                print(f"❌ Missing category: {category}/")
        
        # Generate report
        return self._generate_report()
    
    def _audit_structure(self):
        """Audit directory structure."""
        print("\n📁 Directory Structure Audit")
        print("-" * 60)
        
        if not self.knowledge_root.exists():
            self.issues.append("Knowledge root directory does not exist")
            print("❌ Knowledge root directory does not exist")
            return
        
        print(f"✅ Knowledge root exists: {self.knowledge_root}")
        
        # Check for required directories
        for category in self.REQUIRED_CATEGORIES:
            category_path = self.knowledge_root / category
            if category_path.exists():
                print(f"✅ Category exists: {category}/")
            else:
                print(f"❌ Missing category: {category}/")
                self.issues.append(f"Missing category: {category}/")
    
    def _audit_category(self, category: str):
        """
        Audit a specific knowledge category.
        
        Args:
            category: Category name
        """
        print(f"\n📂 Auditing category: {category}/")
        print("-" * 60)
        
        category_path = self.knowledge_root / category
        
        # Find all files in category
        files = list(category_path.rglob("*"))
        files = [f for f in files if f.is_file()]
        
        print(f"Found {len(files)} files")
        
        for file_path in files:
            asset = self._audit_file(file_path, category)
            self.assets.append(asset)
            
            # Print asset info
            status = "✅" if not asset.issues else "⚠️"
            print(f"{status} {file_path.relative_to(self.knowledge_root)}")
            
            if asset.issues:
                for issue in asset.issues:
                    print(f"   - {issue}")
    
    def _audit_file(self, file_path: Path, category: str) -> KnowledgeAsset:
        """
        Audit a single knowledge file.
        
        Args:
            file_path: Path to file
            category: Category name
            
        Returns:
            Knowledge asset metadata
        """
        # Basic file info
        stat = file_path.stat()
        file_hash = self._calculate_hash(file_path)
        
        # Parse metadata from path structure
        relative_path = file_path.relative_to(self.knowledge_root)
        parts = str(relative_path).parts
        
        subject = None
        grade_level = None
        version = None
        
        # Try to extract subject, grade, version from path
        if len(parts) >= 2:
            subject = parts[1] if parts[1] not in ['README.md', '.gitkeep'] else None
        if len(parts) >= 3:
            grade_level = parts[2] if parts[2].startswith('kelas-') else None
        if len(parts) >= 4:
            version = parts[3] if parts[3].startswith('v') else None
        
        # Check for metadata files
        metadata_file = file_path.parent / "metadata.json"
        has_metadata = metadata_file.exists()
        
        # Check for VERSION file
        version_file = file_path.parent / "VERSION"
        has_version_file = version_file.exists()
        
        # Collect issues
        issues = []
        
        # Validate file type
        file_ext = file_path.suffix.lower()
        if file_ext not in ['.pdf', '.docx', '.doc', '.txt', '.md', '.json', '.csv', '.rdf', '.ttl', '.owl']:
            issues.append(f"Unusual file extension: {file_ext}")
        
        # Validate file size (max 100MB)
        max_size = 100 * 1024 * 1024
        if stat.st_size > max_size:
            issues.append(f"File too large: {stat.st_size} bytes (max {max_size})")
        
        # Validate naming
        if file_path.name in ['.gitkeep', 'README.md']:
            # These are okay
            pass
        elif not has_metadata and file_ext in ['.pdf', '.docx']:
            issues.append("Missing metadata.json for content file")
        
        return KnowledgeAsset(
            path=str(relative_path),
            category=category,
            subject=subject,
            grade_level=grade_level,
            version=version,
            file_type=file_ext,
            size_bytes=stat.st_size,
            hash_md5=file_hash,
            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            has_metadata=has_metadata,
            has_version_file=has_version_file,
            issues=issues
        )
    
    def _calculate_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of file.
        
        Args:
            file_path: Path to file
            
        Returns:
            MD5 hash string
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
    
    def _generate_report(self) -> Dict[str, Any]:
        """
        Generate audit report.
        
        Returns:
            Audit report dictionary
        """
        total_files = len(self.assets)
        files_with_issues = len([a for a in self.assets if a.issues])
        total_issues = sum(len(a.issues) for a in self.assets)
        
        # Category breakdown
        category_counts = {}
        for asset in self.assets:
            category_counts[asset.category] = category_counts.get(asset.category, 0) + 1
        
        # File type breakdown
        type_counts = {}
        for asset in self.assets:
            file_type = asset.file_type if asset.file_type else 'unknown'
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        report = {
            "audit_timestamp": datetime.utcnow().isoformat(),
            "knowledge_root": str(self.knowledge_root),
            "total_files": total_files,
            "files_with_issues": files_with_issues,
            "total_issues": total_issues,
            "category_breakdown": category_counts,
            "file_type_breakdown": type_counts,
            "issues": self.issues,
            "assets": [asdict(asset) for asset in self.assets]
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"Total files: {total_files}")
        print(f"Files with issues: {files_with_issues}")
        print(f"Total issues: {total_issues}")
        print(f"\nCategory breakdown:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} files")
        print(f"\nFile type breakdown:")
        for file_type, count in type_counts.items():
            print(f"  {file_type}: {count} files")
        
        if self.issues:
            print(f"\n⚠️ Structural issues: {len(self.issues)}")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✅ No structural issues found")
        
        return report
    
    def save_report(self, report: Dict[str, Any], output_file: str = "knowledge_audit_report.json"):
        """
        Save audit report to file.
        
        Args:
            report: Audit report dictionary
            output_file: Output file path
        """
        output_path = self.knowledge_root / output_file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report saved to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Audit AI Platform Knowledge Base")
    parser.add_argument(
        "knowledge_root",
        help="Path to knowledge root directory",
        default="/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge"
    )
    parser.add_argument(
        "--output",
        help="Output report file name",
        default="knowledge_audit_report.json"
    )
    parser.add_argument(
        "--fix",
        help="Attempt to fix common issues",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Run audit
    auditor = KnowledgeAuditor(args.knowledge_root)
    report = auditor.audit_all()
    
    # Save report
    auditor.save_report(report, args.output)
    
    # Exit with error code if issues found
    if report["total_issues"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()