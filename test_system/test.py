from data import db_session
from data.tests import Test

def test_code(problem_id):
    db_sess = db_session.create_session()
    tests = db_sess.query(Test).filter(Test.problem_id == problem_id)
    test_data = ((test.input, test.output) for test in tests)
    i = 0
    for input_s, correct_output_s in test_data:
        f = open('test_system/INPUT.txt', 'w')
        f.write(input_s)
        f.close()
        try:
            from .code import main
            main()
        except Exception:
            pass
        try:
            from .code import main
            main()
            f = open('test_system/OUTPUT.txt')
            output_s = f.read()
            f.close()
        except TypeError as E:
            if correct_output_s is None:
                continue
            else:
                return False, f'Ошибка: {E}', i
        except Exception as E:
            return False, f'Ошибка: {E}', i
        else:
            if output_s != correct_output_s:
                return False, f'Ошибка! Входные данные: {input_s}. Ответ программы: {output_s}. Верный ответ "{correct_output_s}"', i
        i += 1
    return True, 'Все тесты пройдены успешно', i