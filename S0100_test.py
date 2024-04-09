import time
import ctypes

kernel32 = ctypes.WinDLL('Kernel32')
handle = kernel32.GetStdHandle(-11)

def move_cursor(x, y):
    coordinate = ctypes.c_long(y << 16 | x)
    kernel32.SetConsoleCursorPosition(handle, coordinate)

def countdown():
    for i in range(10):
        print(f"Exiting in {10 - i} ")
        time.sleep(1)
        move_cursor(0, 0)
    print("Exiting")
    time.sleep(1)


countdown()
