from measuring import Measurer

measurer = Measurer()


@measurer.func
def loop_func() -> None:
    for _ in range(5_000_000):
        continue


if __name__ == "__main__":
    with measurer.region("long loop"):
        loop_func()
