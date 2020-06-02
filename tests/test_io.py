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

    def test_encrypt_filename_path(self):
        encrypted = xorfile(self.decrypted_input_path)
        self.assertEqual(encrypted, self.encrypted_output_path)

    def test_encrypt_filename_string(self):
        encrypted = xorfile(str(self.decrypted_input_path))
        self.assertEqual(encrypted, str(self.encrypted_output_path))

    def test_decrypt_filename_path(self):
        decrypted = xorfile(self.encrypted_input_path)
        self.assertEqual(decrypted, self.decrypted_output_path)

    def test_decrypt_filename_string(self):
        decrypted = xorfile(str(self.encrypted_input_path))
        self.assertEqual(str(decrypted, self.decrypted_output_path))


if __name__ == '__main__':
    unittest.main()
