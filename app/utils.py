import re


def pars_mail(path_mail):
    """FUNCTION OF SEARCH URL IN STRING, input string, output list [uid, token] """

    # регулярка url
    reg = r'(https?://[^\"\s]+)'
    # search url
    match = re.search(reg, path_mail)[0]
    # return list [uid, token]
    return match.strip().split('/')[-2:]

    # в случае необходимости сохранять письма в файл используем код ниже

    # top_log_files = Path(path_mail) # from pathlib import Path
    # # берем путь к файлу
    # file = list(top_log_files.glob('*.log'))[0]
    #
    # if file.is_file():
    #     with file.open() as f:
    #         for n, line in enumerate(f):
    #             if n == 17:
    #                 data = line.strip().split('/')[-2:]
    #                 f.close()
    #                 # удаляем файл
    #                 file.unlink()
    #                 return data
    # else:
    #     assert "В директории нет файла"
