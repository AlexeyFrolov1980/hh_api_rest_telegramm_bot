import hh_functions

class UserState:
    def __init__(self, user_id):
        self.user = user_id
        self._command = ''
        self._area = ''
        self._keywords = ''
        self.current_step = 0

    @property
    def command(self):

        return self._command

        # now, using the setter function

    @command.setter
    def command(self, x):
        self.current_step = 0
        self._command = x

    def message_to_chat(self, message):
        print(self.command, '  ', self.current_step)

        #Ожидаем команду
        if self.current_step == 0:
            if self.command in ['/get_vacancies', '/getstat'] :
                self.current_step = 1
                return 'Введите ключевые слова для поиска'
            return 'неизвестная команда'

        elif self.current_step == 1:
        #Ожидаем ввода ключевых слов
            self.current_step = 2
            self._keywords = message.text
            return 'Введите город/субъект для поиска'
        elif self.current_step == 2:
            #Получаем регион для поиска и проверяем его. Если все ОК - запускаем поиск.

            reg_id=hh_functions.get_area_code(message.text)
            if reg_id<=0:
                return 'Такой регион не найден. Повторите ввод.'

            params = hh_functions.make_params(self._keywords, reg_id)
            if self.command == '/getstat':
                stat_stucture  =hh_functions.get_stat(params,10)
                print(stat_stucture)
                self.current_step = 0
                return hh_functions.stat_structure_to_str(stat_stucture)



    def __str__(self):
        res = "user: " + str(self.user) + "\n"
        res += "command: " + str(self.command) + "\n"
        res += "area: " + str(self._area) + "\n"
        res += "keywords: " + str(self._keywords) + "\n"
        res += "current_step: " + str(self.current_step)
        return res