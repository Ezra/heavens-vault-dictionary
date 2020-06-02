from xor_exploration import xorfile
import unittest
from pathlib import Path


class Test_Encryption(unittest.TestCase):
    def setUp(self):
        self.data_path = Path.cwd() / 'tests' / 'data'
        self.encrypted_input_path = self.data_path / 'encrypted.json'
        self.decrypted_input_path = self.data_path / 'unencrypted.json'
        self.encrypted_output_path = (
            self.data_path / 'decrypted_encrypted.json')
        self.decrypted_output_path = (
            self.data_path / 'decrypted_unencrypted.json')

    def test_encrypt_filename(self):
        encrypted = xorfile(str(self.decrypted_input_path))
        self.assertEqual(encrypted, str(self.encrypted_output_path))


if __name__ == '__main__':
    unittest.main()
