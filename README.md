# np-serializer

A `numpy.ndarray` serializer that supports saving views in an optimized manner.

### Example:

```python
import numpy as np
import numpy_serializer as nps
from numpy.lib.stride_tricks import sliding_window_view

small_array = np.arange(10000).reshape(100, 100)
huge_view = sliding_window_view(small_array, (50, 50))

np.save(..., huge_view)  # Saves the `huge_view` as a single block (~52 MB)
nps.save(..., huge_view)  # Saves the `huge_view` as a view to the smaller array (~80 kB)
```