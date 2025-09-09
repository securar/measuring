## Library `measuring` simplifies measuring code execution time

### Example:
```python
from measuring import Measurer

measurer = Measurer()

@measurer.func
def loop_func() -> None:
    for _ in range(5_000_000):
        continue
    
if __name__ == "__main__":
    with measurer.region("long loop"):
        loop_func()
```
### If you run the code above, it'll output:
```
Function 'loop_func' took 132.381 ms.
Region 'long loop' took 133.181 ms.
```