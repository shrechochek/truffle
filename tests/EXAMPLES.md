# Примеры запуска тестов

## Быстрый старт

### Запустить все тесты
```bash
python tests/run_all_tests.py
```

Вывод:
```
test_simple_text (test_encoders.TestBase64Encoder.test_simple_text) ... ok
test_encode_decode (test_decoders.TestBase64Decoder.test_encode_decode) ... ok
...
Ran 118 tests in 0.305s
OK

======================================================================
СТАТИСТИКА ТЕСТОВ
======================================================================
Всего тестов запущено: 118
Успешно: 118
Провалено: 0
Ошибок: 0
Пропущено: 0
======================================================================
```

## Запуск отдельных модулей

### Тесты кодировщиков
```bash
python -m unittest tests/test_encoders.py
```

### Тесты декодировщиков
```bash
python -m unittest tests/test_decoders.py
```

### Тесты рекурсивного декодирования
```bash
python -m unittest tests/test_recursive.py
```

### Интеграционные тесты
```bash
python -m unittest tests/test_integration.py
```

### Граничные случаи
```bash
python -m unittest tests/test_edge_cases.py
```

## Запуск конкретных тестов

### Один класс тестов
```bash
python -m unittest tests.test_encoders.TestBase64Encoder
```

### Один конкретный тест
```bash
python -m unittest tests.test_encoders.TestBase64Encoder.test_simple_text
```

## Режимы вывода

### Подробный вывод (-v)
```bash
python -m unittest tests/test_encoders.py -v
```

Вывод:
```
test_empty_string (test_encoders.TestBase64Encoder.test_empty_string) ... ok
test_simple_text (test_encoders.TestBase64Encoder.test_simple_text) ... ok
test_special_chars (test_encoders.TestBase64Encoder.test_special_chars) ... ok
test_unicode (test_encoders.TestBase64Encoder.test_unicode) ... ok
...
```

### Тихий режим (-q)
```bash
python -m unittest tests/test_encoders.py -q
```

Вывод:
```
....
----------------------------------------------------------------------
Ran 30 tests in 0.002s

OK
```

## Фильтрация тестов

### Запуск тестов по паттерну
```bash
python -m unittest discover tests -p "test_encoder*.py"
```

### Запуск только Base64 тестов
```bash
python -m unittest discover tests -k "base64"
```

## Отладка

### Остановка на первой ошибке
```bash
python -m unittest tests/test_encoders.py --failfast
```

### С отладчиком
```python
# В тесте добавить:
import pdb; pdb.set_trace()
```

Затем:
```bash
python -m unittest tests.test_encoders.TestBase64Encoder.test_simple_text
```

## Проверка конкретной функциональности

### Проверить все ROT варианты
```bash
python -m unittest tests.test_recursive.TestAllRotOffsets
```

### Проверить оптимизацию _can_be_encoding
```bash
python -m unittest tests.test_recursive.TestCanBeEncoding
```

### Проверить граничные случаи
```bash
python -m unittest tests.test_edge_cases.TestEmptyStrings
python -m unittest tests.test_edge_cases.TestLongStrings
```

## Измерение производительности

### С замером времени
```bash
time python tests/run_all_tests.py
```

### Профилирование
```bash
python -m cProfile -s cumtime tests/run_all_tests.py
```

## CI/CD примеры

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run tests
        run: python tests/run_all_tests.py
```

### GitLab CI
```yaml
test:
  script:
    - python tests/run_all_tests.py
  only:
    - main
    - merge_requests
```

## Проверка покрытия (если установлен coverage)

### Установка coverage
```bash
pip install coverage
```

### Запуск с покрытием
```bash
coverage run -m unittest discover tests
coverage report
coverage html
```

## Полезные команды

### Список всех тестов
```bash
python -m unittest discover tests -v | grep "^test_"
```

### Подсчет тестов
```bash
python -m unittest discover tests -v 2>&1 | grep "^test_" | wc -l
```

### Проверка синтаксиса всех тестов
```bash
python -m py_compile tests/*.py
```

## Troubleshooting

### Ошибка импорта
```bash
# Убедитесь, что запускаете из корня проекта
cd /path/to/truffle
python tests/run_all_tests.py
```

### Тесты не находятся
```bash
# Проверьте структуру
ls -la tests/
# Должны быть файлы test_*.py
```

### Timeout в интеграционных тестах
```bash
# Увеличьте timeout в test_integration.py
# или запустите без интеграционных тестов
python -m unittest discover tests -p "test_[^i]*.py"
```

## Автоматизация

### Pre-commit hook
Создайте `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python tests/run_all_tests.py
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

```bash
chmod +x .git/hooks/pre-commit
```

### Makefile
```makefile
test:
	python tests/run_all_tests.py

test-verbose:
	python -m unittest discover tests -v

test-quick:
	python -m unittest tests/test_encoders.py tests/test_decoders.py
```

Использование:
```bash
make test
make test-verbose
make test-quick
```
