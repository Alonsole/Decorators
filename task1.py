"""Доработать декоратор logger в коде ниже. Должен получиться декоратор, который записывает в файл 'main.log'
дату и время вызова функции, имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
Функция test_1 в коде ниже также должна отработать без ошибок."""

import os
import time


def logger(old_function):
    def new_function(*args, **kwargs):
        data_wr = f'дата вызова функции: {time.strftime("%d.%m.%Y г.")} \n'
        time_wr = f'время вызова функции: {time.strftime("%Hч:%Mм")} \n'
        name_func_wr = f'название вызванной функции: {old_function.__name__} \n'
        args_wr = f'позиционные аргументы вызова функция: {", ".join(map(str, args))} \n'
        kwargs_wr = f'именованные аргументы функции: {", ".join(f"{key}={kwargs[key]}" for key in kwargs)
                                                      or "no arg"} \n'
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(data_wr)
            f.write(time_wr)
            f.write(name_func_wr)
            f.write(args_wr)
            f.write(kwargs_wr)
            f.write(f'возвращаемое функцией значение: {str(result)} \n\n')
        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
