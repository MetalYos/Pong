from helpers import Singleton
import os


@Singleton
class Settings():
    def __init__(self):
        self.settings = {}

    def load(self, path):
        with open(path, 'r') as file:
            for line in file.readlines():
                if line.startswith('#') or line == '\n':
                    continue

                line_list = line.strip().replace(' ', '').split('=')
                self.eval_line_list(line_list)

    def eval_line_list(self, line_list):
        key = line_list[0]
        command = line_list[1]
        command = command.replace('$', "self.settings['")
        command = command.replace('^', "']")

        self.settings[key] = eval(command)
