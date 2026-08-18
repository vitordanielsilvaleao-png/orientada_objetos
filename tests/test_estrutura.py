import unittest


class TestEstruturaProjeto(unittest.TestCase):

    def test_src_importavel(self):
        import src
        self.assertIsNotNone(src)


if __name__ == "__main__":
    unittest.main()