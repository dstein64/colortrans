import os
import tempfile
import unittest

import numpy as np
from PIL import Image

import colortrans


np.random.seed(0)


class TestColorTrans(unittest.TestCase):
    """colortrans tests"""
    def test_colortrans(self):
        content = np.random.randint(256, size=(20, 30, 3), dtype=np.uint8)
        reference = np.random.randint(256, size=(40, 50, 3), dtype=np.uint8)

        for method in colortrans.METHODS:
            func = getattr(colortrans, f'transfer_{method}')
            output = func(content, reference)
            self.assertEqual(output.shape, content.shape)
            self.assertEqual(output.dtype, np.uint8)

            with tempfile.TemporaryDirectory() as tmp:
                content_path = os.path.join(tmp, 'content.png')
                reference_path = os.path.join(tmp, 'reference.png')
                output_path = os.path.join(tmp, 'output.png')
                Image.fromarray(content).save(content_path)
                Image.fromarray(reference).save(reference_path)
                argv = ['colortrans', content_path, reference_path, output_path, '--method', method]
                colortrans.colortrans.main(argv)
                with Image.open(output_path) as img:
                    self.assertTrue(np.array_equal(np.array(img), output))
                argv = ['colortrans', content_path, reference_path, output_path]
                colortrans.colortrans.main(argv)
                assert_func = self.assertTrue if method == 'lhm' else self.assertFalse
                with Image.open(output_path) as img:
                    assert_func(np.array_equal(np.array(img), output))


if __name__ == '__main__':
    unittest.main()
