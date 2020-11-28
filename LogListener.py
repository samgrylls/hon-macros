import os
import time
from datetime import datetime, timedelta

class LogListener:
    def __init__(self, log_path="C:/Users/asdasdasd/Documents/Heroes of Newerth/game"):
        filepath = os.path.join(log_path, "console.log")
        self.console_file = open(filepath, "rt", encoding="utf16")
        self.game_time = None
        self.game_start_time = None

        # this catches the cursor up to the latest lines
        new_lines = self.console_file.readlines()

    def check_for_logs(self):
        new_lines = self.console_file.readlines()
        for line in new_lines:
            if 'Match Time' in line:
                print(line)
                self.update_game_time(line)
        if len(new_lines) > 0:
            print('\n'.join(new_lines))
        time.sleep(0.1)

    def update_game_time(self, line):
        # line should end with 'Match Time(00:14:37)'
        match_time_components = [int(n) for n in line[-9:-2].split(':')]
        server_time = line[1:9]
        self.game_start_time = datetime.strptime(server_time, '%H:%M:%S') - timedelta(
                                                            hours=match_time_components[0],
                                                            minutes=match_time_components[1],
                                                            seconds=match_time_components[2]
        )

    def check_game_time(self):
        return datetime.now() - self.game_start_time