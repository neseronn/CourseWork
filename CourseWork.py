import sys
import webbrowser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtWidgets import QApplication, QWidget


class Programm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.n_v = 1.0
        self.E_s = 200000
        self.alpha_m = 0.0

    def initUI(self):
        uic.loadUi('Qt.ui', self)
        self.setWindowTitle('Проверка прочности верхнего опорного сечения')
        self.input_btn.clicked.connect(self.input_data)
        self.clear_btn.clicked.connect(self.clear_data)
        self.output_btn.clicked.connect(self.output_results)
        self.history_btn.clicked.connect(self.open_history)
        self.clear_history_btn.clicked.connect(self.clear_file)
        self.help_btn.clicked.connect(self.output_help)
        self.exit_btn.clicked.connect(self.close)
        self.open_table_Astot_btn.clicked.connect(self.open_Astot_table)

        self.comboBox_1.addItem('B15')
        self.comboBox_1.addItem('B20')
        self.comboBox_1.addItem('B25')
        self.comboBox_1.addItem('B30')
        self.comboBox_1.addItem('B35')
        self.comboBox_1.addItem('B40')
        self.comboBox_1.addItem('B45')
        self.comboBox_1.addItem('B50')
        self.comboBox_1.addItem('B55')
        self.comboBox_1.addItem('B60')
        self.comboBox_1.activated[str].connect(self.on_changed_concrete)

        self.comboBox_2.addItem('A240')
        self.comboBox_2.addItem('A400')
        self.comboBox_2.addItem('A500')
        self.comboBox_2.activated[str].connect(self.on_changed_armature)

        self.line_a.setText('35.0')
        self.line_D_cir.setText('400.0')
        self.line_A_s_tot.setText('3140.0')
        self.line_l.setText('4.8')
        self.line_N_v.setText('1700.0')
        self.line_M_v.setText('60.0')
        self.line_N_h.setText('100.0')
        self.line_M_h.setText('45.0')

    def on_changed_concrete(self):
        self.concrete = str(self.comboBox_1.currentText())
        if self.concrete == 'B15':
            self.E_b = 24000.0
            self.R_b = 8.5
        elif self.concrete == 'B20':
            self.E_b = 27500.0
            self.R_b = 11.5
        elif self.concrete == 'B25':
            self.E_b = 30000.0
            self.R_b = 14.5
        elif self.concrete == 'B30':
            self.E_b = 32500.0
            self.R_b = 17.0
        elif self.concrete == 'B35':
            self.E_b = 34500.0
            self.R_b = 19.5
        elif self.concrete == 'B40':
            self.E_b = 36000.0
            self.R_b = 22.0
        elif self.concrete == 'B45':
            self.E_b = 37000.0
            self.R_b = 25.0
        elif self.concrete == 'B50':
            self.E_b = 38000.0
            self.R_b = 27.5
        elif self.concrete == 'B55':
            self.E_b = 39000.0
            self.R_b = 30.0
        elif self.concrete == 'B60':
            self.E_b = 39500.0
            self.R_b = 33.0

    def on_changed_armature(self):
        self.armature = str(self.comboBox_2.currentText())
        if self.armature == 'A240':
            self.R_s = 210.0
            self.R_sc = 210.0
        elif self.armature == 'A400':
            self.R_s = 340.0
            self.R_sc = 340.0
        elif self.armature == 'A500':
            self.R_s = 435.0
            self.R_sc = 435.0

    def input_data(self):
        self.all_errors = ''
        self.D_cir = self.line_D_cir.text()
        self.a = self.line_a.text()
        self.N_v = self.line_N_v.text()
        self.M_v = self.line_M_v.text()
        self.N_h = self.line_N_h.text()
        self.M_h = self.line_M_h.text()
        self.A_s_tot = self.line_A_s_tot.text()
        self.l = self.line_l.text()
        #D_cir от 100мм до 8000мм
        #a не больше половины D_cir

        # Проверка на пустую строку, если не всё ввели
        if not self.D_cir.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение D_cir.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.D_cir)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.D_cir[i].isdigit() == False and self.D_cir[i] != '.':
                    self.str_error += 'Некорректный ввод переменной D_cir. Смотрите Help.\n'
                    break
            if self.str_error == '':
                if float(self.D_cir) < 100 or float(self.D_cir) > 8000:
                    self.all_errors += 'Недопустимое значение D_cir. Смотрите Help.\n'
                else:
                    self.D_cir = float(self.line_D_cir.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.a.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение a.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.a)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.a[i].isdigit() == False and self.a[i] != '.':
                    self.str_error += 'Некорректный ввод переменной a. Смотрите Help.\n'
                    break
            if self.str_error == '' and type(self.D_cir) == float:
                if float(self.a) > (self.D_cir/2.0) :
                    self.all_errors += 'Недопустимое значение a. Смотрите Help.\n'
                else:
                    self.a = float(self.line_a.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.N_v.strip():    # Если строка пустая вернется False
            self.all_errors += 'Не введено значение N_v.\n'
        else:   # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.N_v)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.N_v[i].isdigit() == False and self.N_v[i] != '.':
                    self.str_error += 'Некорректный ввод переменной N_v. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.N_v = float(self.line_N_v.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.M_v.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение M_v.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.M_v)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.M_v[i].isdigit() == False and self.M_v[i] != '.':
                    self.str_error += 'Некорректный ввод переменной M_v. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.M_v = float(self.line_M_v.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.N_h.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение N_h.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.N_h)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.N_h[i].isdigit() == False and self.N_h[i] != '.':
                    self.str_error += 'Некорректный ввод переменной N_h. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.N_h = float(self.line_N_h.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.M_h.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение M_h.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.M_h)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.M_h[i].isdigit() == False and self.M_h[i] != '.':
                    self.str_error += 'Некорректный ввод переменной M_h. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.M_h = float(self.line_M_h.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.A_s_tot.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение A_s_tot.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.A_s_tot)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.A_s_tot[i].isdigit() == False and self.A_s_tot[i] != '.':
                    self.str_error += 'Некорректный ввод переменной A_s_tot. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.A_s_tot = float(self.line_A_s_tot.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        # Проверка на пустую строку, если не всё ввели
        if not self.l.strip():  # Если строка пустая вернется False
            self.all_errors += 'Не введено значение l.\n'
        else:  # Если строка не пустая вернется True
            self.str_error = ''
            for i in range(len(self.l)):
                # Если элемент НЕ число или элемент НЕ равен точке
                if self.l[i].isdigit() == False and self.l[i] != '.':
                    self.str_error += 'Некорректный ввод переменной l. Смотрите Help.\n'
                    break
            if self.str_error == '':
                self.l = float(self.line_l.text())
            elif self.str_error != '':
                self.all_errors += self.str_error

        #################################################
        if self.all_errors != '':
            self.dialog_error = DialogError(self.all_errors)
            self.dialog_error.show()

    def clear_data(self):
        self.line_a.clear()
        self.line_D_cir.clear()
        self.line_A_s_tot.clear()
        self.line_l.clear()
        self.line_N_v.clear()
        self.line_M_v.clear()
        self.line_N_h.clear()
        self.line_M_h.clear()

        self.a.clear()
        self.D_cir.clear()
        self.A_s_tot.clear()
        self.l.clear()
        self.N_v.clear()
        self.M_v.clear()
        self.N_h.clear()
        self.M_h.clear()
        self.E_b = 0.0
        self.R_b = 0.0
        self.R_s = 0.0
        self.R_sc = 0.0
        self.alpha_m = 0.0

    def open_history(self):
        self.history = History()
        self.history.read_from_file()
        self.history.show()

    def output_results(self):
        ######### Расчеты ####################################################
        given = ''
        given += f'ДАНО: D_cir = {self.D_cir} мм; A_s,tot = {self.A_s_tot} мм^2; a = {self.a} мм;'
        given += f' l = {self.l} мм; N_v = {self.N_v} мм^2; M_v = {self.M_v} мм;'
        given += f' N_h = {self.N_h} мм; M_h = {self.M_h} мм^2.\n'
        res = ''
        res += '\nПоскольку рассматриваемое сечение расположено ' \
              'у податливой заделки, '
        res += f'n_v = {self.n_v}.'
        res += '\n\nОпределяем коэффициент n_h.'
        self.l_0 = self.l
        res += f'\nРасчётную длину принимаем равной l_0 = l = {self.l_0} (м)'
        self.l_0 = self.l_0*1000
        res += f' = {self.l_0} (мм)'
        res += '\nУсилия от всех нагрузок равны:'
        self.M = self.M_v + self.M_h
        res += f'\nM = M_v + M_h = {self.M_v} + {self.M_h} = {self.M} (кН*м);'
        self.N = self.N_v + self.N_h
        res += f'\nN = N_v + N_h = {self.N_v} + {self.N_h} = {self.N} (кН).'
        self.e_0 = self.M/self.N
        self.e_0 = round(self.e_0, 4)
        res += f'\ne_0 = M/N = {self.M} / {self.N} = {self.e_0} (м) = '
        self.e_0 = self.e_0 * 1000.0
        res += f'{self.e_0} (мм).'
        res += '\n\nОпределяем жёсткость D.'
        res += '\nДля этого вычисляем:'
        self.r = self.D_cir/2.0
        res += f'\nr = D_cir/2 = {self.D_cir}/2 = {self.r} (мм),'
        self.r_s = self.r - self.a
        res += f'\nr_s = r - a = {self.r} - {self.a} = {self.r_s} (мм) = '
        self.r_s = self.r_s/1000.0
        res += f'{self.r_s} (м);'
        self.M1 = self.M + (self.N * self.r_s)
        res += f'\nM1 = M + N*r_s = {self.M} + {self.N}*{self.r_s} = {self.M1} (кН*м).'
        res += '\n\nВ связи с отсутствием вертикальных кратковременных нагрузок'
        self.M_l = self.M_v
        res += f'\nM_l = M_v = {self.M_l} (кН*м);'
        self.N_l = self.N_v
        res += f'\nN_l = N_v = {self.N_l} (кН);'
        res += '\nтогда:'
        self.M1_l = self.M_l + (self.N_l * self.r_s)
        res += f'\nM1_l = M_l + N_l * r_s = {self.M_l} + {self.N_l} * {self.r_s} = {self.M1_l} (кН*м);'
        self.phi_l = 1.0 + (self.M1_l/self.M1)
        self.phi_l = round(self.phi_l, 3)
        res += f'\nphi_l = 1 + M1_l/M1 = 1 + {self.M1_l}/{self.M1} = {self.phi_l}.'
        res += f'\n\nТак как e_0/D_cir = {self.e_0}/{self.D_cir} = {round(self.e_0/self.D_cir), 3} < 0.15,'
        self.delta_e = 0.15
        res += f' принимаем delta_e = {self.delta_e}.'
        res += '\n\nМомент инерции бетонного сечения и всей арматуры соответственно равны:'
        self.I = (3.14 * (self.D_cir**4))/64.0
        res += f'\nI = П*(D_cir)**4/64 = 3.14 * {self.D_cir}**4/64 = {self.I} (мм**4) ' \
               f'= {int(round(self.I/1000000, 0))}*10**6 (мм**4);'
        self.r_s = self.r_s * 1000.0
        self.I_s = (self.A_s_tot * (self.r_s ** 2))/2.0
        self.I_s = round(self.I_s/1000000, 2) * 1000000
        res += f'\nI_s = (A_s,tot * r_s**2)/2 = ({self.A_s_tot} * {self.r_s}**2)/2 = {self.I_s} (мм**4) = ' \
               f'{round(self.I_s/1000000, 2)}*10**6 (мм**4).'
        res += '\n\nТогда'
        self.D = ((0.15 * self.E_b * self.I)/(self.phi_l * (0.3 + self.delta_e))) + (0.7 * self.E_s * self.I_s)
        self.D = round(self.D/10000000000000, 2) * 10000000000000
        res += '\nD = (0.15 * E_b * I)/(phi_l * (0.3 + delta_e)) + 0.7 * E_s * I_s = '
        res += f'(0.15 * {int(self.E_b/10000)}*10**4 * {int(round(self.I/1000000, 0))}*10**6)/' \
               f'({self.phi_l} * (0.3 + {self.delta_e})) + 0.7 * {int(self.E_s/100000)}*10**5 * ' \
               f'{round(self.I_s/1000000, 2)}*10**6 = {self.D} = {round(self.D/10000000000000, 2)}*10**13 (мм**2).'
        res += '\n\nОтсюда'
        self.N_cr = ((3.14**2)*self.D)/(self.l_0**2)
        self.N_cr = round(self.N_cr/1000, 0)*1000
        res += '\nN_cr = (П**2*D)/(l_0)**2 '
        res += f'= (3.14**2*{round(self.D/10000000000000, 2)}*10**13)/({int(self.l_0)}**2) = {int(self.N_cr/1000)}*10**3 (Н)'
        self.N_cr = self.N_cr/1000
        res += f' = {int(self.N_cr)} (кН);'
        self.n_h = round((1.0/(1.0 - (self.N/self.N_cr))), 3)
        res += f'\nn_h = 1/(1 - (N/N_cr)) = 1/(1 - ({self.N}/{self.N_cr})) = {self.n_h} .'
        res += '\n\nРасчётный момент с учётом прогиба равен'
        self.M = round((self.M_v + (self.M_h*self.n_h)), 0)
        res += f'\nM = M_v + M_h*n_h = {self.M_v} + {self.M_h}*{self.n_h} = {self.M} (кН*м).'
        res += '\n\nОпределим площадь бетонного сечения'
        self.A = (3.14*(self.D_cir**2))/4.0
        res += f'\nA = (П*(D_cir)**2)/4 = (3.14*({self.D_cir})**2)/4 = {self.A} (мм**2).'
        self.N = self.N*1000
        self.alpha_n = round(((self.N)/(self.R_b * self.A)), 3)
        res += f'\n\nalpha_n = N/(R_b*A) = {self.N}/({self.R_b}*{self.A}) = {self.alpha_n};'
        self.alpha_s = round(((self.R_s*self.A_s_tot)/(self.R_b*self.A)), 3)
        res += f'\nalpha_s = (R_s*A_s,tot)/(R_b*A) = ({self.R_s}*{self.A_s_tot})/({self.R_b}*{self.A}) = {self.alpha_s};'
        self.delta = self.a/self.D_cir
        res += f'\ndelta = a/D_cir = {self.a}/{self.D_cir} = {self.delta}.'

        self.output_results = OutputResults(self.alpha_n, self.alpha_s, self.delta, given, self.R_b, self.A, self.r, self.M)
        res = given + res
        self.output_results.return_results(res)
        self.output_results.show()
        ######################################################################################################


    def open_Astot_table(self):
        self.Astot_table = AstotTable()
        self.Astot_table.show()

    def output_help(self):
        self.help = Help()
        self.help.show()

    def clear_file(self):
        with open('file.txt', 'w'):
            pass


class AstotTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('A_s_tot_table.ui', self)


class Grafic(QWidget):
    def __init__(self, alpha_n, alpha_s, delta, given, R_b, A, r, M):
        super().__init__()
        self.alpha_n = alpha_n
        self.alpha_s = alpha_s
        self.delta = delta
        self.str = given
        self.R_b = R_b
        self.A = A
        self.r = r
        self.M = M
        self.alpha_m = 0.0
        self.initUI()

    def initUI(self):
        uic.loadUi('tabl_graph.ui', self)
        self.ok_btn_alpha.clicked.connect(self.return_alpha_m)
        s = f'По значениям α_n = {self.alpha_n}, α_s = {self.alpha_s} и δ = a/D_cir = {self.delta}'
        s += '\nнайдите значение α_m, введите его в поле ввода и нажмите ок:'
        self.label_all.setText(s)

    def return_alpha_m(self):
        end_str = ''
        self.alpha_m = float(self.line_alpha_m.text())
        self.close()
        end_str += 'На графике находим'
        end_str += f'\nalpha_m = {self.alpha_m}'
        self.product = self.alpha_m * self.R_b * self.A * self.r
        end_str += f'\nalpha_m*R_b*A*r = {self.alpha_m}*{self.R_b}*{self.A}*{self.r} = {self.product} (H*мм)'
        self.product = self.product / 1000000
        end_str += f' = {self.product} (кH*м)'
        if self.product > self.M:
            end_str += f' > M = {self.M} (кH*м),'
            end_str += '\nт.е. прочность сечения ОБЕСПЕЧЕНА.'
        else:
            end_str += f' < M = {self.M} (кH*м),'
            end_str += '\nт.е. прочность сечения НЕ обеспечена.'
        self.end_res = EndResults(end_str)
        self.end_res.show()

        self.str += '\n' + end_str
        self.write_file(self.str)

    def write_file(self, res):
        text = open('file.txt')
        strr = text.read()
        text.close()
        with open('file.txt', 'w'):
            pass
        text = open('file.txt', 'a+')
        text.write(res)
        text.write('\n\n____________________________________________________________________\n\n')
        text.write(strr)
        text.close()


class EndResults(QWidget):
    def __init__(self, end_str):
        super().__init__()
        self.end_str = end_str
        self.initUI()

    def initUI(self):
        uic.loadUi('end_result.ui', self)
        self.close_btn.clicked.connect(self.close)
        self.line_result.setText(self.end_str)


class DialogError(QDialog):
    def __init__(self, str):
        super().__init__()
        self.all_errors = str
        self.initUI()

    def initUI(self):
        uic.loadUi('Dialog.ui', self)
        self.label.setText(self.all_errors)
        self.ok_btn.clicked.connect(self.close)


class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('help.ui', self)
        self.vk_btn.clicked.connect(lambda: webbrowser.open('https://vk.com/avdeenko_l'))
        self.git_btn.clicked.connect(lambda: webbrowser.open('https://github.com/neseronn/CourseWork'))


class History(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('History.ui', self)

    def read_from_file(self):
        text = open('file.txt')
        text1 = text.read()
        text.close()
        self.text_history.setText(text1)


class OutputResults(QWidget):
    def __init__(self, alpha_n, alpha_s, delta, str, R_b, A, r, M):
        super().__init__()
        self.alpha_n = alpha_n
        self.alpha_s = alpha_s
        self.delta = delta
        self.str = str
        self.R_b = R_b
        self.A = A
        self.r = r
        self.M = M
        self.initUI()

    def initUI(self):
        uic.loadUi('OutputResults.ui', self)
        self.open_graph_btn.clicked.connect(self.open_form_alpha_m)

    def return_results(self, res):
        self.results.setText(res)

    def open_form_alpha_m(self):
        self.gragh = Grafic(self.alpha_n, self.alpha_s, self.delta, self.str, self.R_b, self.A, self.r, self.M)
        self.gragh.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Programm()
    ex.show()
    sys.exit(app.exec_())
