from overrides import overrides
from pathlib import Path
import unittest

from myio.myio import auto_open
from myio.util import toggle_prefix
from xor_exploration import xorfile


class Test_AutoOpen(unittest.TestCase):
    ''' test the make_open and auto_make_open features from myio '''
    @overrides
    def setUp(self):
        self.file1 = Path('file1.txt')
        self.file2 = Path('file2.txt')

    def test_auto_open(self):

        @auto_open('outfile', mode='w')
        def save_type(outfile):
            print(f'{type(outfile)=}', file=outfile)
            return f'wrote to {outfile.name}'

        @auto_open('infile', mode='r')
        def label_contents(label, infile):
            return label + ': ' + infile.read().strip()

        save_type(outfile=self.file1)

        with open(self.file2, mode='w') as f:
            save_type(outfile=f)

        with open(self.file1) as f:
            result1 = label_contents('first file', infile=f)

        result2 = label_contents('second file', infile=self.file2)

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
                self.file1,
                self.file2,
                ]:
            output_path.unlink(missing_ok=True)


class Test_Encryption(unittest.TestCase):
    ''' test the path handling and data munging of xorfile '''
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


class Test_StringHandling(unittest.TestCase):
    def test_idempotency(self):
        text = 'lazy bat'
        prefix = 'lab'
        modified_text = toggle_prefix(toggle_prefix(text, prefix), prefix)
        self.assertEqual(modified_text, text)

    def test_potency(self):
        text = 'lazy bat'
        prefix = 'lab'
        modified_text = toggle_prefix(text, prefix), prefix
        self.assertNotEqual(modified_text, text)
