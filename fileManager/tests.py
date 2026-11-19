import os

from django.test import SimpleTestCase

from fileManager.views import STATIC_PATH


class FileManagerTests(SimpleTestCase):
    def test_list_and_download(self):
        self.assertEqual(self.client.get('/').json(), os.listdir(STATIC_PATH))
        r = self.client.get('/download/test')  # the extension may be omitted
        self.assertEqual(r.status_code, 200)
        with open(os.path.join(STATIC_PATH, 'test.txt'), 'rb') as f:
            self.assertEqual(b''.join(r.streaming_content), f.read())
        self.assertIn('filename="test.txt"', r['Content-Disposition'])

    def test_create_view_delete(self):
        self.assertTrue(self.client.get('/create/tmpdir').json()['response'].startswith('Directory tmpdir Created'))
        self.assertEqual(self.client.get('/tmpdir').json(), [])
        self.assertTrue(self.client.delete('/delete/tmpdir').json()['response'].startswith('Directory tmpdir Deleted'))

    def test_paths_outside_the_folder_are_refused(self):
        for url in ['/..%2F..%2F', '/create/..%2Fescaped', '/download/..%2F..%2Fmanage.py']:
            self.assertEqual(self.client.get(url).status_code, 400, url)
        self.assertEqual(self.client.delete('/delete/..%2Ffoo').status_code, 400)
        self.assertFalse(os.path.exists(os.path.join(STATIC_PATH, '..', 'escaped')))
