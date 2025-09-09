from measuring import Measurer

measurer = Measurer()


with measurer.region("long loop"):
    for _ in range(20_000_000):
        continue
