from datetime import datetime
import requests


def log_to_file(path: str):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            arguments = ', '.join(map(str, args)) if args else ''
            if kwargs:
                arguments += ', ' + ', '.join([f'{key}={value}' for key, value in kwargs.items()])
            time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            result = None
            log_row = f'[{time}] Фукнция {old_function.__name__} вызвана с параметрами: {arguments}. '
            try:
                result = old_function(*args, **kwargs)
                log_row += f'Результат: {result}'
            except Exception as error:
                log_row += f'Произошла ошибка: {error}'
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'{log_row}\n')
            return result
        return new_function
    return decorator


def log(old_function):
    def new_function(*args, **kwargs):
        arguments = ', '.join(map(str, args)) if args else ''
        if kwargs:
            arguments += ', ' + ', '.join([f'{key}={value}' for key, value in kwargs.items()])
        time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        result = None
        log_row = f'[{time}] Фукнция {old_function.__name__} вызвана с параметрами: {arguments}. '
        try:
            result = old_function(*args, **kwargs)
            log_row += f'Результат: {result}'
        except Exception as error:
            log_row += f'Произошла ошибка: {error}'
        with open('common.log', 'a', encoding='utf-8') as file:
            file.write(f'{log_row}\n')
        return result

    return new_function


@log_to_file(path='requests.log')
def get_all_heroes():
    return requests.get('https://akabab.github.io/superhero-api/api/all.json').json()


@log
def best_superhero(*heroes):
    if not len(heroes):
        return None
    hero_list = [hero for hero in get_all_heroes() if hero['name'] in heroes]
    if not len(hero_list):
        return None
    return max(hero_list, key=lambda x: x['powerstats']['intelligence'])['name']


if __name__ == '__main__':
    print(best_superhero('Hulk', 'Captain America', 'Thanos'))
