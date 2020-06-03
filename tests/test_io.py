from overrides import overrides
from pathlib import Path
import unittest

from myio.myio import auto_make_open
from xor_exploration import xorfile


class Test_AutoOpen(unittest.TestCase):
    def test_auto_open(self):

        @auto_make_open('outfile', mode='w')
        def save_type(outfile):
            print(f'{type(outfile)=}', file=outfile)
            print(f'wrote to {outfile.name}')

        @auto_make_open('infile', mode='r')
        def label_contents(label, infile):
            return label + ': ' + infile.read().strip()

        save_type(outfile='file1.txt')

        with open('file2.txt', mode='w') as f:
            save_type(outfile=f)

        with open('file1.txt') as f:
            result1 = label_contents('first file', infile=f)

        result2 = label_contents('second file', infile='file2.txt')

        self.assertEqual(
            result1,
            "first file: type(outfile)=<class '_io.TextIOWrapper'>",
            )
        self.assertEqual(
            result2,
            "second file: type(outfile)=<class '_io.TextIOWrapper'>",
            )

    @overrides
    def tearDown(self):
        for output_path in [
                Path('file1.txt'),
                Path('file2.txt'),
                ]:
            output_path.unlink(missing_ok=True)


class Test_Encryption(unittest.TestCase):
    @overrides
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

    @overrides
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
