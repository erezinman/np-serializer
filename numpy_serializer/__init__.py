### Set Version : -------------------------------------------

import os

with open(os.path.normpath(os.path.join(__file__, '../VERSION'))) as f:
    __version__ = f.read()

del os

### ---------------------------------------------------------

from .serializer import load, save
