import threading
import queue
import detection
import main

if __name__ == "__main__":
    hands_queue = queue.Queue()
    click_queue = queue.Queue()

    hand_tracking_thread = threading.Thread(target=detection.hand_tracking, args=(hands_queue, click_queue))
    chess_game_thread = threading.Thread(target=main.main, args=(hands_queue, click_queue))

    hand_tracking_thread.start()
    chess_game_thread.start()

    hand_tracking_thread.join()
    chess_game_thread.join()
