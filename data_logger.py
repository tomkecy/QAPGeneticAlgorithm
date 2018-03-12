from datetime import datetime


class DataLogger:
    __timestamp_format = '%Y_%m_%d_%H_%M_%S'

    def __init__(self, title_prefix=''):
        self.__file = open('out/%sga_result_%s.csv' % (title_prefix + '_' if title_prefix != '' else '',
                           datetime.now().strftime(self.__timestamp_format)), 'w')

    def write_log(self, gen_nr, best, average, worst):
        self.__file.write('%s,%s,%s,%s\n' % (gen_nr, best, average, worst))

    def write_header(self):
        self.__file.write('nr_pokolenia, najlepsza_ocena, srednia_ocen, najgorsza_ocena\n')

    def write_line_separator(self, times=1):
        self.__file.write('\n'*times)

    def close(self):
        self.__file.close()
