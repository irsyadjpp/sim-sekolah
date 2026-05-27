import uuid
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta


def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())


def generate_short_id() -> str:
    """Generate a short unique ID"""
    return str(uuid.uuid4())[:8]


def hash_string(input_string: str) -> str:
    """Hash a string using SHA256"""
    return hashlib.sha256(input_string.encode()).hexdigest()


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe storage"""
    # Remove any path separators
    filename = filename.replace("/", "").replace("\\", "")
    # Remove any special characters except dots, underscores, and hyphens
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    sanitized = "".join(char for char in filename if char in allowed_chars)
    return sanitized or "file"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def parse_pagination(page: int = 1, page_size: int = 20) -> tuple[int, int]:
    """Parse pagination parameters and return offset and limit"""
    page = max(1, page)
    page_size = min(100, max(1, page_size))
    offset = (page - 1) * page_size
    limit = page_size
    return offset, limit


def calculate_pagination(total: int, page: int, page_size: int) -> Dict[str, Any]:
    """Calculate pagination metadata"""
    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }


def merge_dicts(base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = base_dict.copy()
    for key, value in update_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(nested_dict: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary"""
    items = []
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def chunks_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry a function on exception"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """Mask sensitive data like API keys or passwords"""
    if len(data) <= visible_chars:
        return mask_char * len(data)
    return data[:visible_chars] + mask_char * (len(data) - visible_chars)


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    today = datetime.utcnow()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def time_ago(timestamp: datetime) -> str:
    """Get human-readable time ago string"""
    now = datetime.utcnow()
    delta = now - timestamp
    
    if delta.days == 0:
        if delta.seconds < 60:
            return "just now"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return f"{delta.seconds // 3600} hours ago"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days} days ago"
    elif delta.days < 30:
        return f"{delta.days // 7} weeks ago"
    elif delta.days < 365:
        return f"{delta.days // 30} months ago"
    else:
        return f"{delta.days // 365} years ago"