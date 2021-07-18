from django.conf import settings
from pathlib import Path

def pars_mail(path_mail):
# path_mail = '/home/mkl/PycharmProjects/orginizer1_5/mail_messages_test'

    top_log_files = Path(path_mail)
    # берем путь к файлу
    file = list(top_log_files.glob('*.log'))[0]

    if file.is_file():
        with file.open() as f:
            for n, line in enumerate(f):
                if n == 17:
                    data = line.strip().split('/')[-2:]
                    f.close()
                    # удаляем файл
                    file.unlink()
                    return data
    else:
        assert "В директории нет файла"


