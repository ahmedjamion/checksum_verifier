import unittest
import tempfile
from app.hashing import compute_checksum, verify_checksum

class TestHashing(unittest.TestCase):

    def test_empty_file(self):
        """Test checksum of an empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_name = f.name  # store name
        try:
            md5_hash = compute_checksum(temp_name, "md5")
            self.assertEqual(md5_hash, "d41d8cd98f00b204e9800998ecf8427e")
        finally:
            import os
            os.remove(temp_name)  # cleanup

    def test_small_text_file(self):
        """Test checksum for a small text file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("hello")
            f.flush()
            temp_name = f.name
        try:
            match, computed = verify_checksum(temp_name, "5d41402abc4b2a76b9719d911017c592", "md5")
            self.assertTrue(match)
        finally:
            import os
            os.remove(temp_name)

    def test_unsupported_algorithm(self):
        """Test that using an unsupported algorithm raises ValueError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_name = f.name
        try:
            with self.assertRaises(ValueError):
                compute_checksum(temp_name, "unsupported")
        finally:
            import os
            os.remove(temp_name)

    def test_incorrect_expected_checksum(self):
        """Test mismatch detection."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("data")
            f.flush()
            temp_name = f.name
        try:
            match, _ = verify_checksum(temp_name, "wrongchecksum", "md5")
            self.assertFalse(match)
        finally:
            import os
            os.remove(temp_name)

if __name__ == "__main__":
    unittest.main()
