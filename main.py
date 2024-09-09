# This is main module of the program.
# It starts scheduler and icon in the tray.

import threading

from tray import icon_run
from gifts_manipulation import scheduler

def main():
    # Clears log file.
    with open("logs.txt", "w") as f:
        f.write("/// Code 400 means that participation in the drawing has already been accepted, there is no need to worry \n\n")

    # Starts scheduler in separate thread.
    main_thread = threading.Thread(target=scheduler)
    main_thread.daemon = True     # Sets thread as daemon, so it will stop when main program stops.
    main_thread.start()

    icon_run()


if __name__ == "__main__":
    main()