"""
Workflow Collaboration Service

This module provides teacher-to-teacher collaboration features including
template sharing, best practice dissemination, and community features.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path
import json
import uuid


class CollaborationType(str, Enum):
    """Types of collaboration"""
    TEMPLATE_SHARING = "template_sharing"
    BEST_PRACTICE = "best_practice"
    PEER_REVIEW = "peer_review"
    COMMUNITY_DISCUSSION = "community_discussion"


class SharePermission(str, Enum):
    """Share permission levels"""
    PRIVATE = "private"
    TEAM = "team"
    SCHOOL = "school"
    PUBLIC = "public"


class WorkflowCollaborationService:
    """Collaboration service for teacher workflows"""
    
    def __init__(self, collaboration_dir: str = "/tmp/workflow_collaboration"):
        self.collaboration_dir = Path(collaboration_dir)
        self.collaboration_dir.mkdir(parents=True, exist_ok=True)
        
        self.shared_templates: Dict[str, Dict] = {}
        self.best_practices: Dict[str, Dict] = {}
        self.community_posts: Dict[str, Dict] = {}
        
        self._load_collaboration_data()
    
    def share_template(
        self, 
        user_id: str,
        workflow_type: str,
        template_data: Dict,
        permission: SharePermission = SharePermission.TEAM,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Share a workflow template with other teachers"""
        template_id = str(uuid.uuid4())
        
        template = {
            "template_id": template_id,
            "user_id": user_id,
            "workflow_type": workflow_type,
            "template_data": template_data,
            "permission": permission.value,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "usage_count": 0,
            "rating": 0.0,
            "rating_count": 0
        }
        
        self.shared_templates[template_id] = template
        self._save_collaboration_data()
        
        return {
            "template_id": template_id,
            "status": "shared",
            "permission": permission.value,
            "share_url": f"/templates/{template_id}"
        }
    
    def get_shared_templates(
        self, 
        workflow_type: Optional[str] = None,
        permission: Optional[SharePermission] = None,
        sort_by: str = "rating"
    ) -> List[Dict]:
        """Get shared templates with filtering and sorting"""
        templates = list(self.shared_templates.values())
        
        # Filter by workflow type
        if workflow_type:
            templates = [t for t in templates if t["workflow_type"] == workflow_type]
        
        # Filter by permission
        if permission:
            templates = [t for t in templates if t["permission"] in [permission.value, "public"]]
        
        # Sort
        if sort_by == "rating":
            templates.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "usage":
            templates.sort(key=lambda x: x["usage_count"], reverse=True)
        elif sort_by == "recent":
            templates.sort(key=lambda x: x["created_at"], reverse=True)
        
        return [
            {
                "template_id": t["template_id"],
                "workflow_type": t["workflow_type"],
                "user_id": t["user_id"],
                "permission": t["permission"],
                "created_at": t["created_at"],
                "usage_count": t["usage_count"],
                "rating": t["rating"],
                "metadata": t["metadata"]
            }
            for t in templates
        ]
    
    def use_template(self, template_id: str, user_id: str) -> Dict:
        """Use a shared template"""
        if template_id not in self.shared_templates:
            return {"error": "Template not found"}
        
        template = self.shared_templates[template_id]
        template["usage_count"] += 1
        template["last_used"] = datetime.utcnow().isoformat()
        
        self._save_collaboration_data()
        
        return {
            "template_id": template_id,
            "template_data": template["template_data"],
            "workflow_type": template["workflow_type"],
            "original_creator": template["user_id"]
        }
    
    def rate_template(self, template_id: str, user_id: str, rating: float) -> Dict:
        """Rate a shared template"""
        if template_id not in self.shared_templates:
            return {"error": "Template not found"}
        
        if rating < 1 or rating > 5:
            return {"error": "Rating must be between 1 and 5"}
        
        template = self.shared_templates[template_id]
        
        # Update rating (simple average)
        current_rating = template["rating"]
        current_count = template["rating_count"]
        
        new_rating = ((current_rating * current_count) + rating) / (current_count + 1)
        
        template["rating"] = new_rating
        template["rating_count"] = current_count + 1
        
        self._save_collaboration_data()
        
        return {
            "template_id": template_id,
            "new_rating": new_rating,
            "rating_count": template["rating_count"]
        }
    
    def submit_best_practice(
        self, 
        user_id: str,
        workflow_type: str,
        practice_title: str,
        practice_description: str,
        examples: Optional[List[str]] = None
    ) -> Dict:
        """Submit a best practice for workflow"""
        practice_id = str(uuid.uuid4())
        
        practice = {
            "practice_id": practice_id,
            "user_id": user_id,
            "workflow_type": workflow_type,
            "title": practice_title,
            "description": practice_description,
            "examples": examples or [],
            "created_at": datetime.utcnow().isoformat(),
            "upvotes": 0,
            "downvotes": 0,
            "comments": []
        }
        
        self.best_practices[practice_id] = practice
        self._save_collaboration_data()
        
        return {
            "practice_id": practice_id,
            "status": "submitted",
            "upvotes": 0
        }
    
    def get_best_practices(
        self, 
        workflow_type: Optional[str] = None,
        sort_by: str = "upvotes"
    ) -> List[Dict]:
        """Get best practices with filtering and sorting"""
        practices = list(self.best_practices.values())
        
        if workflow_type:
            practices = [p for p in practices if p["workflow_type"] == workflow_type]
        
        if sort_by == "upvotes":
            practices.sort(key=lambda x: x["upvotes"], reverse=True)
        elif sort_by == "recent":
            practices.sort(key=lambda x: x["created_at"], reverse=True)
        
        return practices
    
    def vote_on_practice(self, practice_id: str, user_id: str, vote: str) -> Dict:
        """Vote on a best practice"""
        if practice_id not in self.best_practices:
            return {"error": "Practice not found"}
        
        practice = self.best_practices[practice_id]
        
        if vote == "up":
            practice["upvotes"] += 1
        elif vote == "down":
            practice["downvotes"] += 1
        else:
            return {"error": "Invalid vote, use 'up' or 'down'"}
        
        self._save_collaboration_data()
        
        return {
            "practice_id": practice_id,
            "upvotes": practice["upvotes"],
            "downvotes": practice["downvotes"]
        }
    
    def create_community_post(
        self, 
        user_id: str,
        title: str,
        content: str,
        workflow_type: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """Create a community discussion post"""
        post_id = str(uuid.uuid4())
        
        post = {
            "post_id": post_id,
            "user_id": user_id,
            "title": title,
            "content": content,
            "workflow_type": workflow_type,
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat(),
            "upvotes": 0,
            "downvotes": 0,
            "comments": []
        }
        
        self.community_posts[post_id] = post
        self._save_collaboration_data()
        
        return {
            "post_id": post_id,
            "status": "published",
            "created_at": post["created_at"]
        }
    
    def get_community_posts(
        self, 
        workflow_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "recent"
    ) -> List[Dict]:
        """Get community posts with filtering"""
        posts = list(self.community_posts.values())
        
        if workflow_type:
            posts = [p for p in posts if p["workflow_type"] == workflow_type]
        
        if tags:
            posts = [p for p in posts if any(tag in p["tags"] for tag in tags)]
        
        if sort_by == "recent":
            posts.sort(key=lambda x: x["created_at"], reverse=True)
        elif sort_by == "upvotes":
            posts.sort(key=lambda x: x["upvotes"], reverse=True)
        
        return posts
    
    def add_comment_to_post(
        self, 
        post_id: str, 
        user_id: str, 
        comment: str
    ) -> Dict:
        """Add a comment to a community post"""
        if post_id not in self.community_posts:
            return {"error": "Post not found"}
        
        comment_data = {
            "comment_id": str(uuid.uuid4()),
            "user_id": user_id,
            "comment": comment,
            "created_at": datetime.utcnow().isoformat(),
            "upvotes": 0
        }
        
        self.community_posts[post_id]["comments"].append(comment_data)
        self._save_collaboration_data()
        
        return {
            "comment_id": comment_data["comment_id"],
            "status": "added"
        }
    
    def get_user_contributions(self, user_id: str) -> Dict:
        """Get summary of user's contributions"""
        templates_shared = [
            t for t in self.shared_templates.values() 
            if t["user_id"] == user_id
        ]
        
        practices_submitted = [
            p for p in self.best_practices.values() 
            if p["user_id"] == user_id
        ]
        
        posts_created = [
            p for p in self.community_posts.values() 
            if p["user_id"] == user_id
        ]
        
        total_upvotes = (
            sum(t["rating_count"] for t in templates_shared) +
            sum(p["upvotes"] for p in practices_submitted) +
            sum(p["upvotes"] for p in posts_created)
        )
        
        return {
            "user_id": user_id,
            "templates_shared": len(templates_shared),
            "practices_submitted": len(practices_submitted),
            "posts_created": len(posts_created),
            "total_upvotes_received": total_upvotes,
            "contribution_score": self._calculate_contribution_score(
                len(templates_shared),
                len(practices_submitted),
                len(posts_created),
                total_upvotes
            )
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get leaderboard of top contributors"""
        user_scores = {}
        
        # Aggregate contributions by user
        for template in self.shared_templates.values():
            user_id = template["user_id"]
            if user_id not in user_scores:
                user_scores[user_id] = {
                    "user_id": user_id,
                    "templates_shared": 0,
                    "total_usage": 0,
                    "total_rating": 0
                }
            user_scores[user_id]["templates_shared"] += 1
            user_scores[user_id]["total_usage"] += template["usage_count"]
            user_scores[user_id]["total_rating"] += template["rating"]
        
        for practice in self.best_practices.values():
            user_id = practice["user_id"]
            if user_id not in user_scores:
                user_scores[user_id] = {
                    "user_id": user_id,
                    "templates_shared": 0,
                    "total_usage": 0,
                    "total_rating": 0
                }
            user_scores[user_id]["total_rating"] += practice["upvotes"]
        
        # Calculate scores
        for user_id, data in user_scores.items():
            data["score"] = (
                data["templates_shared"] * 10 +
                data["total_usage"] * 2 +
                data["total_rating"]
            )
        
        # Sort by score
        leaderboard = sorted(user_scores.values(), key=lambda x: x["score"], reverse=True)
        
        return leaderboard[:limit]
    
    def _calculate_contribution_score(
        self, 
        templates: int, 
        practices: int, 
        posts: int, 
        upvotes: int
    ) -> float:
        """Calculate user's contribution score"""
        return (
            templates * 10 +
            practices * 5 +
            posts * 3 +
            upvotes * 0.5
        )
    
    def _load_collaboration_data(self):
        """Load collaboration data from disk"""
        templates_file = self.collaboration_dir / "shared_templates.json"
        practices_file = self.collaboration_dir / "best_practices.json"
        posts_file = self.collaboration_dir / "community_posts.json"
        
        if templates_file.exists():
            with open(templates_file, 'r') as f:
                self.shared_templates = json.load(f)
        
        if practices_file.exists():
            with open(practices_file, 'r') as f:
                self.best_practices = json.load(f)
        
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                self.community_posts = json.load(f)
    
    def _save_collaboration_data(self):
        """Save collaboration data to disk"""
        templates_file = self.collaboration_dir / "shared_templates.json"
        practices_file = self.collaboration_dir / "best_practices.json"
        posts_file = self.collaboration_dir / "community_posts.json"
        
        with open(templates_file, 'w') as f:
            json.dump(self.shared_templates, f, indent=2)
        
        with open(practices_file, 'w') as f:
            json.dump(self.best_practices, f, indent=2)
        
        with open(posts_file, 'w') as f:
            json.dump(self.community_posts, f, indent=2)
