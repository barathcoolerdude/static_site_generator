import unittest

from main import *

class TestStaticSiteGenerator(unittest.TestCase):
    
    def test_transfer_files(self):
        # Test if the transfer_files function works correctly
        transfer_files()
        self.assertTrue(os.path.exists("/home/coolerdude/workspace/static_site_generator/public"))

    def test_generate_page(self):
        # Test if the generate_page function generates HTML correctly
        from_path = "/home/coolerdude/workspace/static_site_generator/content/index.md"
        template_path = "/home/coolerdude/workspace/static_site_generator/template.html"
        dest_path = "/home/coolerdude/workspace/static_site_generator/public/index.html"
        
        