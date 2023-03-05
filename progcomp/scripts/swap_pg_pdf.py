import os
import shutil
import sys
from pathlib import Path

from __script_setup import *

root = Path("problems") / script_progcomp()
if not os.path.exists(sys.argv[1]):
    print(sys.argv[1] + " doesn't exist!")
shutil.copyfile(sys.argv[1], root / "__problems_new.pdf")
os.replace(root / "problems.pdf", root / "__problems_old.pdf")
shutil.move(root / "__problems_new.pdf", root / "problems.pdf")
