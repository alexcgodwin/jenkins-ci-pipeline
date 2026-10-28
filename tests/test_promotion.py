import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from promote_image import replace_image
class PromotionTests(unittest.TestCase):
 def test_preserves_other_container_images(self):
  spec='image: alexcgodwin/cloud-app:8\nimage: redis:7\n'
  changed=replace_image(spec,'alexcgodwin/cloud-app:0123456789ab')
  self.assertIn('image: redis:7',changed)
  self.assertIn('cloud-app:0123456789ab',changed)
 def test_denies_ambiguous_manifest(self):
  spec='image: alexcgodwin/cloud-app:8\nimage: alexcgodwin/cloud-app:9\n'
  with self.assertRaises(ValueError): replace_image(spec,'alexcgodwin/cloud-app:0123456789ab')
 def test_denies_mutable_latest(self):
  with self.assertRaises(ValueError): replace_image('image: alexcgodwin/cloud-app:8','alexcgodwin/cloud-app:latest')
 def test_denies_other_repository(self):
  with self.assertRaises(ValueError): replace_image('image: other/app:8','alexcgodwin/cloud-app:0123456789ab')
if __name__=='__main__':unittest.main()
