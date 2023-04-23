from data import db_session
from data.tests import Test
from .code import main

def test_code(problem_id):
    db_sess = db_session.create_session()
    tests = db_sess.query(Test).filter(Test.problem_id == problem_id)
    test_data = ((test.input, test.output) for test in tests)
    for input_s, correct_output_s in test_data:
        f = open('test_system/INPUT.txt', 'w')
        f.write(input_s)
        f.close()
        try:
            main()
        except Exception:
            pass
        try:
            main()
            f = open('test_system/OUTPUT.txt')
            output_s = f.read()
            f.close()
        except TypeError as E:
            if correct_output_s is None:
                continue
            else:
                print(f'Ошибка! Ошибка: {E}')
                return False
        except Exception as E:
            print(f'Ошибка! Ошибка: {E}')
            return False
        else:
            if output_s != correct_output_s:
                print(f'Ошибка! Входные данные: {input_s}. Ответ программы: {output_s}. Верный ответ "{correct_output_s}"')
                return False
    print('Все тесты пройдены успешно')
    return True