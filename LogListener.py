import os
import time
from datetime import datetime, timedelta

class GameTime:
    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def format_time(self):
        if self.minutes < 10:
            self.minutes = f"0{self.minutes}"
        if self.seconds < 10:
            self.seconds = f"0{self.seconds}"
        if self.hours < 10:
            self.hours = f"0{self.hours}"
        return f"{self.hours}:{self.minutes}:{self.seconds}"

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
        td = datetime.now() - self.game_start_time
        hours = td.seconds//3600
        minutes = (td.seconds//60)%60
        seconds = td.seconds%60

        return GameTime(hours, minutes, seconds)


if __name__=="__main__":
    print(GameTime(1,2,3).format_time())
