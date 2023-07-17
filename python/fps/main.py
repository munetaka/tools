from time import sleep

from calc_from_clocks import ClockFps
from calc_from_timer import TimerFps



def main():
    clock_fps = ClockFps()
    timer_fps = TimerFps()

    while True:
        sleep(0.1)

        print(f'clock_fps: {clock_fps.calc()}, timer_fps: {timer_fps.calc()}')


if __name__ == '__main__':
    main()
