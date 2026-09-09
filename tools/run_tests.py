"""Every test beside this file, run in one go, so a change is checked before it is pushed."""

import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

failed = 0
for path in sorted(HERE.glob("test_*.py")):
    module = __import__(path.stem)
    print(path.name)
    try:
        module.run()
    except AssertionError as e:
        failed += 1
        print(f"  FAIL  {e}")

print("FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
