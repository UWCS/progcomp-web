
import os
import shutil
import sys

if not os.path.exists(sys.argv[1]):
    print(sys.argv[1] + " doesn't exist!")
shutil.copyfile(sys.argv[1], "__problems_new.pdf")
os.replace("problems.pdf", "__problems_old.pdf")
shutil.move("__problems_new.pdf", "problems.pdf")

