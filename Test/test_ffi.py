from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core" / "build"))

import core_module

print(core_module.ModifyString("\nhello"))
