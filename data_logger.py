from datetime import datetime


class DataLogger:
    __timestamp_format = '%Y_%m_%d_%H_%M_%S'

    def __init__(self):
        self.__file = open('out/ga_result_%s.csv' %
                           datetime.now().strftime(self.__timestamp_format), 'w')
        self.__file.write('nr_pokolenia, najlepsza_ocena, srednia_ocen, najgorsza_ocena\n')

    def write_log(self, gen_nr, best, average, worst):
        self.__file.write('%s,%s,%s,%s\n' % (gen_nr, best, average, worst))

    def close(self):
        self.__file.close()
