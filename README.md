## Library `measuring` simplifies measuring code execution time

### Example:
```python
from measuring import Measurer

measurer = Measurer()

with measurer.region("long loop"):
    for _ in range(20_000_000):
        continue

```
### If you run the code above, it'll output:
```
Function 'loop_func' took 132.381 ms.
Region 'long loop' took 133.181 ms.
```