from timeit import default_timer as timer


class TimerFps():
    def __init__(self):
        self.__frame_count = 0
        self.__accum_time = 0
        self.__prev_time = timer()

    def calc(self):
        self.__frame_count += 1
        self.__curr_time = timer()
        self.__exec_time = self.__curr_time - self.__prev_time
        self.__prev_time = self.__curr_time
        self.__accum_time = self.__accum_time + self.__exec_time
        fps = self.__frame_count / self.__accum_time
        if self.__accum_time > 1:
            self.__accum_time = 0
            self.__frame_count = 0

        return fps
