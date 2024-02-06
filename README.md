## Как установить

```python
from modules.reader import \
(
    Mode,        # Режим проверки линий (enum).
    Config,      # Конструктор для сложных потоковых операций.
    Reader,      # Основная реализация методов (main).
    Alphabet     # Английский и русский алфавиты.
)
```

## Потоковые операции

`mkdir` Cоздаёт несуществующие директории на пути к файлу. [^🔧]

```python
mkdir('path/to/file.txt') # Создаст директорию "path/to", если её не существует.
mkdir('another/path/to/file.txt', 0) # Аналогично первому, без вывода в консоль.
```

`read` Возвращает содержимое текстового файла.

```python
read('file.txt') # Вернёт список строк.
read('file.txt', '\n') # Вернёт строку с разделитем линий.
```

`write` Записывает содержимое в текстовый файл. [^🔧]

```python
write(content, 'file.txt') # Запишет список строк или единую строку.
write(content, 'file.txt', '\n') # Запишет с разделитем линий.
write(content, 'file.txt', debug = 0) # Без вывода в консоль.
```

`append` Работает аналогично `write`, добавляет содержимое в конец файла. [^🔧]

```python
append(content, 'file.txt') # Добавит список строк или единую строку.
```

---

Следующие операции требуют использовать `Config` в качестве первого параметра.

```python
config = Config \
(
    content: Union[str, list[str]],  # Содержимое.

    # Опционально:
    delimiter: str = None,           # Разделитель линий.
    mode: Mode = Mode.starts,        # Режим проверки линий.
    alphabet: str = Alphabet.russian # Шаблон очереди записи.
)
```

---

`write_loop` Производит цикл записи текста в несколько файлов. [^🔧] [^🔑]

```python
path = 'path/to/file_%s.txt'

write_loop(config, path) # Запишет список строк или единую строку.
write_loop(config, path, 1) # Аналогично первому, откроет файлы в блокноте.
wite_loop(config, path, debug = 0) # Аналогично первому, без вывода в консоль.
```

`append_loop` Работает аналогично `write_loop`, добавляет содержимое в конец файла. [^🔧] [^🔑]

```python
append_loop(config, path) # Добавит список строк или единую строку.
```

## Стандартные операции

`lower` Возвращает содержимое в нижнем регистре.

```python
hello = 'Hello, world!'

lower(hello) # "hello, world!"
```

`upper` Возвращает содержимое в вверхнем регистре.

```python
upper(hello) # "HELLO, WORLD!"
```

`exists` Возвращает истину, если в строке содержится "x".

```python
exists(hello, 'or') # True
exists(hello, 'and') # False
```

`starts` Аналогично `exists`, если строка начинается на "x".

```python
exists(hello, 'he') # True
exists(hello, 'she') # False
```

`ends` Аналогично `exists`, если строка заканчивается "x".

```python
exists(hello, 'd!') # True
exists(hello, 'w)') # False
```

`read_exists` Возвращает содержимое, которое содержит "x".

```python
read_exists(content, 'x') # Вернёт список строк.
read_exists(content, 'x', '\n') # Вернёт единую строку.
```

`read_starts` Аналогично `read_exists`, которое начинается на "x".

```python
read_starts(content, 'x') # Вернёт список строк.
```

`read_ends` Аналогично `read_exists`, которое заканчивается "x".

```python
read_ends(content, 'x') # Вернёт список строк.
```

[^🔧]: По умолчанию выводит сообщение в консоль.

[^🔑]:
    Указывайте путь с ключом "%s". Пример: "path/to/file_%s.txt".
