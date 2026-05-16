import unittest
import numpy as np
import os
from renderer.engine import ASCIIRenderer
from renderer.charset import CharSet

class TestASCIIRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = ASCIIRenderer()
        
    def test_charset_loading(self):
        self.assertEqual(CharSet.get_charset("standard"), CharSet.STANDARD)
        self.assertEqual(CharSet.get_charset("nonexistent"), CharSet.STANDARD)
        
    def test_mapping_logic(self):
        # Create a simple 2x2 image
        img = np.array([[0, 255], [127, 200]], dtype=np.uint8)
        # Test mapping in a mock way or just ensure it runs
        from renderer.grayscale import map_pixels_to_ascii
        result = map_pixels_to_ascii(img, "@ ")
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 2)

if __name__ == "__main__":
    unittest.main()
