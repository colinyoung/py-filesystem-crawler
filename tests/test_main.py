import os

os.environ['UVICORN_BASEDIR'] = 'test_files'

import unittest
from fastapi import Response
from fastapi.testclient import TestClient

from filesystem_crawler.main import app, index_of, contents_of, upsert_file
from filesystem_crawler.result import Result
from filesystem_crawler.input import Input


class TestFunctions(unittest.TestCase):

    def test_index_of(self):
        response = Response()
        results = index_of("filesystem_crawler/test_files", response)
        self.assertEqual(len(results), 3)

        assert any(result.name == "file1.txt" for result in results)
        assert any(result.name == "file2.txt" for result in results)
        assert any(result.name == ".hidden" for result in results)

    def test_contents_of(self):
        response = Response()
        result = Result(path="filesystem_crawler/test_files/file1.txt")
        data = contents_of(result, response)
        self.assertEqual(data['contents'], b"This is file1.txt")
        self.assertEqual(data['name'], 'file1.txt')

    def test_upsert_file(self):
        try:
            input = Input(name="file3.txt", contents="This is file3.txt")
            path = "filesystem_crawler//test_files/file3.txt"
            upsert_file(input, path)
            with open(path, "rb") as f:
                self.assertEqual(f.read(), b"This is file3.txt")
        finally:
            os.remove(path)


client = TestClient(app)

class TestAPI(unittest.TestCase):
    
    def test_get_file(self):
        response = client.get("/file1.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"contents": "This is file1.txt", "name": "file1.txt"})
    
    def test_upsert_file(self):
        try:
            response = client.post("/file4.txt", json={"contents": "This is file4.txt"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"contents": "This is file4.txt", "name": "file4.txt"})
        finally:
            os.remove("filesystem_crawler/test_files/file4.txt")
    
    def test_upsert_directory(self):
        try:
            response = client.post("/dir")
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "Directory created", "name": "dir"})
        finally:
            os.rmdir("filesystem_crawler/test_files/dir")

if __name__ == '__main__':
    unittest.main()
