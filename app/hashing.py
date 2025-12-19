# app/hashing.py

import hashlib
from pathlib import Path
from .constants import ALGORITHMS, CHUNK_SIZE

def compute_checksum(path: str, algorithm: str = "sha256") -> str:
    """
    Compute the checksum of a file using the specified algorithm.
    Returns the lowercase hexadecimal digest.
    """
    # Validate algorithm
    if algorithm.lower() not in ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    # Validate file existence
    path_obj = Path(path)
    if not path_obj.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    # Create hash object
    hash_func = getattr(hashlib, algorithm.lower())()

    # Read file in chunks
    try:
        with open(path, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hash_func.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied: {path}")

    return hash_func.hexdigest()


def verify_checksum(path: str, expected: str, algorithm: str = "sha256") -> tuple[bool, str]:
    """
    Verify a file's checksum against an expected value.
    Returns (match: bool, computed_hash: str)
    """
    computed_hash = compute_checksum(path, algorithm)
    match = computed_hash.lower() == expected.lower()
    return match, computed_hash
