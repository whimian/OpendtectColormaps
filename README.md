Matplotlib colormaps (Opendtect default colormaps) for displaying Seismic section.

## Example

```python

import matplotlib.pyplot as plt

from opendtect_colormaps import OpendtectColormaps

od_cmaps = OpendtectColormaps()

fig, ax = plt.subplots()

im = ax.imshow(
    X,
    cmap=od_cmaps("Seismics"),
)
```