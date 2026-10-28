"""Replace one exact cloud-app image field; fail closed on ambiguity."""
import re,sys
from pathlib import Path
IMAGE=re.compile(r'^([ \t]*image:[ \t]*)(alexcgodwin/cloud-app:[A-Za-z0-9._-]+)([ \t]*)$',re.MULTILINE)
NEW=re.compile(r'^alexcgodwin/cloud-app:[0-9a-f]{12}$')

def replace_image(content: str, target: str) -> str:
    if not NEW.fullmatch(target):raise ValueError('Target must be immutable 12-character commit SHA tag')
    matches=list(IMAGE.finditer(content))
    if len(matches)!=1: raise ValueError('Expected exactly one cloud-app image declaration')
    return IMAGE.sub(lambda m: m.group(1)+target+m.group(3),content,count=1)

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: promote_image.py manifest image:sha')
    p=Path(sys.argv[1]);p.write_text(replace_image(p.read_text(encoding='utf-8'),sys.argv[2]),encoding='utf-8')
