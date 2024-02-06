from typing import Union, Literal
from enum import Enum

from subprocess import run
from time import sleep

import os
import re

encoding = 'utf-8'
union = Union[str, list[str]]
boolean = Union[Literal[0, 1], bool]

class Alphabet:
    english = 'abcdefghijklmnopqrstuvwxyz'
    russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

class Mode(Enum):
    exists = 1
    starts = 2
    ends = 3

class Config:
    def __init__(self, content: union, delimiter: str = None, mode: Mode = Mode.starts, alphabet: Alphabet = Alphabet.russian):
        self.content = content
        self.delimiter = delimiter
        self.mode = mode
        self.alphabet = alphabet

class Reader:
    '''
    Предоставляет методы обработки строк, списков и текстовых файлов.
    '''

    #region Потоковые операции.
    def mkdir(self, path: str, debug: bool = True) -> None:
        '''
        Создаёт несуществующие директории на пути к файлу.
        :param path:    путь к файлу.
        :param debug:   флаг: отладочная информация.
        '''
        match = re.match(r'^(.*?)[\\/]?([^\\/]+)$', path)
        if match:
            directory, filename = match.groups()

            if not os.path.exists(directory):
                os.makedirs(directory)
                if debug: print(f'Директория "{directory}" успешно создана.')
            else:
                if debug: print(f'Директория "{directory}" уже существует.')

    def read(self, path: str, delimiter: str = None) -> union:
        '''
        Возвращает содержимое текстового файла.
        :param path:        путь до файла.
        :param delimiter:   разделитель линий.
        '''
        with open(path, 'r', encoding = encoding) as file:
            lines = [line.rstrip() for line in file]

        if delimiter != None: return delimiter.join(lines)
        else: return lines

    def write(self, content: union, path: str, delimiter: str = None, debug: boolean = 1) -> None:
        '''
        Записывает содержимое в текстовый файл.
        :param content:     объект (строка или список строк).
        :param path:        путь до файла.
        :param delimiter:   разделитель линий.
        :param debug:       флаг: отладочная инфо.
        '''
        self.mkdir(path, debug)
        with open(path, 'w', encoding = encoding) as file:
            if delimiter != None: file.write(delimiter.join(content))
            else: file.write(content)
            if bool(debug): print(f'Файл "{path}" успешно создан.')

    def append(self, content: union, path: str, delimiter: str = None, debug: boolean = 1) -> None:
        '''
        Записывает содержимое в конец текстового файла.
        :param content:     объект (строка или список строк).
        :param path:        путь до файла.
        :param delimiter:   разделитель линий.
        :param debug:       флаг: отладочная инфо.
        '''
        self.mkdir(path, debug)
        with open(path, 'a', encoding = encoding) as file:
            if delimiter != None: file.write(delimiter.join(f'\n{content}'))
            else: file.write(f'\n{content}')
            if bool(debug): print(f'Файл "{path}" обновлён.')

    #endregion

    #region Расширенные операции.
    def write_loop(self, config: Config, path: str, opens: boolean = 0, debug: boolean = 1) -> None:
        '''
        Производит цикл записи текста в несколько файлов.
        Примечание: указывайте путь с ключом %s.
        :param config:      класс конфигурации текста.
        :param path:        путь к записи (запись_%s.txt).
        :param opens:       флаг: открывать файлы.
        :param debug:       флаг: отладочная инфо.
        '''
        file_number = 0
        self.mkdir(path, debug)
        for letter in config.alphabet:

            if config.mode == Mode.exists:
                lines = [line for line in config.content if self.exists(line, letter)]
            elif config.mode == Mode.starts:
                lines = [line for line in config.content if self.starts(line, letter)]
            elif config.mode == Mode.ends:
                lines = [line for line in config.content if self.ends(line, letter)]

            if lines:
                file_number += 1
                new_path = path % letter

                with open(new_path, 'w', encoding = encoding) as file:
                    if config.delimiter != None: file.write(config.delimiter.join(lines))
                    else: file.write(lines)

                if bool(opens): sleep(0.1); run(['start', 'notepad', new_path], shell = True)
        if bool(debug): print(f'Файлов создано: {file_number}')

    def append_loop(self, config: Config, path: str, opens: boolean = 0, debug: boolean = 1) -> None:
        '''
        Производит цикл добавления текста в несколько файлов.
        Примечание: указывайте путь с ключом %s.
        :param config:      класс конфигурации текста.
        :param path:        путь к записи (запись_%s.txt).
        :param opens:       флаг: открывать файлы.
        :param debug:       флаг: отладочная инфо.
        '''
        file_number = 0
        self.mkdir(path, debug)
        for letter in config.alphabet:

            if config.mode == Mode.exists:
                lines = [line for line in config.content if self.exists(line, letter)]
            elif config.mode == Mode.starts:
                lines = [line for line in config.content if self.starts(line, letter)]
            elif config.mode == Mode.ends:
                lines = [line for line in config.content if self.ends(line, letter)]

            if lines:
                file_number += 1
                new_path = path % letter

                with open(new_path, 'a', encoding = encoding) as file:
                    if config.delimiter is not None:
                        data = config.delimiter.join(lines)
                        file.write(f'\n{data}' if file.tell() else data)
                    else:
                        file.write(f'\n{lines}' if file.tell() else lines)

                if bool(opens): sleep(0.1); run(['start', 'notepad', new_path], shell = True)
        if bool(debug): print(f'Файлов обновлено: {file_number}')
    #endregion

    #region Приведение к регистру.
    def lower(self, content: union) -> union:
        '''
        Возвращает содержимое в нижнем регистре.
        :param content:     объект (строка или список строк).
        '''
        if isinstance(content, str): return content.lower()
        elif isinstance(content, list): return [line.lower() for line in content]

    def upper(self, content: union) -> union:
        '''
        Возвращает содержимое в вверхнем регистре.
        :param content:     объект (строка или список строк).
        '''
        if isinstance(content, str): return content.lower()
        elif isinstance(content, list): return [line.upper() for line in content]

    # endregion

    #region Проверка на содержимое.
    def exists(self, string: str, sub: str) -> bool:
        '''
        Возвращает истину, если в строке содержится "x".
        :param string:      строка для проверки.
        :param sub:         что должна содержать.
        '''
        if string.lower().endswith(sub.lower()): return True
        else: return False

    def starts(self, string: str, sub: str) -> bool:
        '''
        Возвращает истину, если строка начинается на "x".
        :param string:      строка для проверки.
        :param sub:         с чего должна начинаться.
        '''
        if string.lower().endswith(sub.lower()): return True
        else: return False

    def ends(self, string: str, sub: str) -> bool:
        '''
        Возвращает истину, если строка заканчивается "x".
        :param string:      строка для проверки.
        :param sub:         чем должна заканчиваться.
        '''
        if string.lower().endswith(sub.lower()): return True
        else: return False
    #endregion

    #region Чтение содержимого строки.
    def read_exists(self, content: union, sub: str, delimiter: str = None) -> union:
        '''
        Возвращает содержимое, которое содержит "x".
        :param content:     объект (строка или список строк).
        :param sub:         что должен содержать.
        :param delimiter:   разделитель линий.
        '''
        if isinstance(content, str): content = content.split()
        lines = [line for line in content if self.exists(line, sub)]

        if delimiter != None: return delimiter.join(lines)
        else: return lines

    def read_starts(self, content: union, sub: str, delimiter: str = None) -> union:
        '''
        Возвращает содержимое, которое начинается на "x".
        :param content:     объект (строка или список строк).
        :param sub:         с чего должен начинаться.
        :param delimiter:   разделитель линий.
        '''
        if isinstance(content, str): content = content.split()
        lines = [line for line in content if self.starts(line, sub)]

        if delimiter != None: return delimiter.join(lines)
        else: return lines

    def read_ends(self, content: union, sub: str, delimiter: str = None) -> union:
        '''
        Возвращает содержимое, которое заканчивается "x".
        :param content:     объект (строка или список строк).
        :param sub:         чем должен заканчиваться.
        :param delimiter:   разделитель линий.
        '''
        if isinstance(content, str): content = content.split()
        lines = [line for line in content if self.ends(line, sub)]

        if delimiter != None: return delimiter.join(lines)
        else: return lines
    #endregion

reader = Reader()