from overrides import overrides
from pathlib import Path
import unittest

from xor_exploration import xorfile


class Test_Encryption(unittest.TestCase):
    @overrides  # (unittest.TestCase)
    def setUp(self):
        self.data_path = Path.cwd() / 'tests' / 'data'
        self.encrypted_input_path = self.data_path / 'save1.json'
        self.decrypted_input_path = self.data_path / 'decrypted_save2.json'
        self.encrypted_output_path = (
            self.data_path / 'save2.json'
            )
        self.decrypted_output_path = (
            self.data_path / 'decrypted_save1.json'
            )

    @overrides  # (unittest.TestCase)
    def tearDown(self):
        for output_path in [
                self.decrypted_output_path,
                self.encrypted_output_path,
                ]:
            output_path.unlink(missing_ok=True)

    def test_encrypt_filename(self):
        encrypted = xorfile(self.decrypted_input_path)
        self.assertEqual(encrypted, self.encrypted_output_path)

    def test_decrypt_filename(self):
        decrypted = xorfile(self.encrypted_input_path)
        self.assertEqual(decrypted, self.decrypted_output_path)
