"""
Helper utilities for the application.
"""
from pathlib import Path
from typing import Optional
import hashlib
import secrets


def generate_secure_filename(original_filename: str) -> str:
    """
    Generate a secure unique filename.

    Args:
        original_filename: Original file name

    Returns:
        Secure filename with preserved extension
    """
    extension = Path(original_filename).suffix
    random_hex = secrets.token_hex(16)
    return f"{random_hex}{extension}"


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        Hex digest of file hash
    """
    hash_func = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def validate_video_file(file_path: str) -> bool:
    """
    Validate if file is a valid video file.

    Args:
        file_path: Path to file

    Returns:
        True if valid video file, False otherwise
    """
    valid_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}
    extension = Path(file_path).suffix.lower()
    return extension in valid_extensions


def validate_audio_file(file_path: str) -> bool:
    """
    Validate if file is a valid audio file.

    Args:
        file_path: Path to file

    Returns:
        True if valid audio file, False otherwise
    """
    valid_extensions = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'}
    extension = Path(file_path).suffix.lower()
    return extension in valid_extensions


def ensure_directory_exists(directory_path: str) -> Path:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        directory_path: Path to directory

    Returns:
        Path object of the directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path
