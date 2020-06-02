from xor_exploration import xorfile
import unittest
from pathlib import Path


class Test_Encryption(unittest.TestCase):
    def setUp(self):
        self.data_path = Path.cwd() / 'tests' / 'data'
        self.encrypted_input_path = self.data_path / 'save1.json'
        self.decrypted_input_path = self.data_path / 'decrypted_save2.json'
        self.encrypted_output_path = (
            self.data_path / 'save2.json')
        self.decrypted_output_path = (
            self.data_path / 'decrypted_save1.json')

    def test_encrypt_filename_path(self):
        encrypted = xorfile(str(self.decrypted_input_path))
        self.assertEqual(encrypted, str(self.encrypted_output_path))

    def test_encrypt_filename_string(self):
        encrypted = xorfile(str(self.decrypted_input_path))
        self.assertEqual(encrypted, str(self.encrypted_output_path))

    def test_decrypt_filename_path(self):
        decrypted = xorfile(self.encrypted_input_path)
        self.assertEqual(decrypted, self.decrypted_output_path)

    def test_decrypt_filename_string(self):
        decrypted = xorfile(self.encrypted_input_path)
        self.assertEqual(decrypted, self.decrypted_output_path)


if __name__ == '__main__':
    unittest.main()
