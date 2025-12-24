import hashlib
from pathlib import Path
from constants import ALGORITHMS, CHUNK_SIZE

def compute_checksum(path: str, algorithm: str = "sha256", progress_callback=None) -> str:
    """
    Compute the checksum of a file using the specified algorithm.
    Optionally report progress via progress_callback(percent).
    Returns the lowercase hexadecimal digest.
    """
    algorithm = algorithm.lower()
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    path_obj = Path(path)
    if not path_obj.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    hash_func = getattr(hashlib, algorithm)()
    total_size = path_obj.stat().st_size
    read_size = 0

    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hash_func.update(chunk)
            read_size += len(chunk)
            if progress_callback:
                percent = read_size / total_size * 100
                progress_callback(percent)

    return hash_func.hexdigest()


def verify_checksum(path: str, expected: str, algorithm: str = "sha256") -> tuple[bool, str]:
    computed_hash = compute_checksum(path, algorithm)
    match = computed_hash.lower() == expected.lower()
    return match, computed_hash
