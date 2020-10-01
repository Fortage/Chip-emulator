import random
import pickle
from tkinter import filedialog
from Interface import *
from main import *

KeysKeybord = {
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_4: 0xc,
    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_r: 0xd,
    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_f: 0xe,
    pygame.K_z: 0xa,
    pygame.K_x: 0x0,
    pygame.K_c: 0xb,
    pygame.K_v: 0xf,
}

class Chip8:
    def __init__(self):
        self.key_inputs = [0] * 16
        self.display = [0] * 64 * 32
        self.mem = [0] * 4096

        self.opcode = 0
        self.vx = 0
        self.vy = 0
        self.r = 0
        self.registers = [0] * 16
        self.sound_timer = 0
        self.delay_timer = 0
        self.index = 0
        self.pc = 0x200

        self.key_wait = False

        self.stack = []
        self.interface = Interface(64, 32, 10)

        self.fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                      0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                      0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                      0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                      0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                      0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                      0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                      0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                      0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                      0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                      0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                      0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                      0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                      0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                      0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                      0xF0, 0x80, 0xF0, 0x80, 0x80  # F
                      ]

        for i in range(80):
            self.mem[i] = self.fonts[i]

        self.funcmap = {
            0x0000: self._0ZZZ,
            0x00e0: self._00E0,
            0x00ee: self._00EE,
            0x1000: self._1NNN,
            0x2000: self._2NNN,
            0x3000: self._3XNN,
            0x4000: self._4XNN,
            0x5000: self._5XY0,
            0x6000: self._6XNN,
            0x7000: self._7XNN,
            0x8000: self._8ZZZ,
            0x8FF0: self._8XY0,
            0x8ff1: self._8XY1,
            0x8ff2: self._8XY2,
            0x8ff3: self._8XY3,
            0x8ff4: self._8XY4,
            0x8ff5: self._8XY5,
            0x8ff6: self._8XY6,
            0x8ff7: self._8XY7,
            0x8ffE: self._8XYE,
            0x9000: self._9XY0,
            0xA000: self._ANNN,
            0xB000: self._BNNN,
            0xC000: self._CXNN,
            0xD000: self._DXYN,
            0xE000: self._EZZZ,
            0xE00E: self._EX9E,
            0xE001: self._EXA1,
            0xF000: self._FZZZ,
            0xF007: self._FX07,
            0xF00A: self._FX0A,
            0xF015: self._FX15,
            0xF018: self._FX18,
            0xF01E: self._FX1E,
            0xF029: self._FX29,
            0xF033: self._FX33,
            0xF055: self._FX55,
            0xF065: self._FX65
        }

    def loadROM(self, rom):
        print("Проверка")
        romOpen = open(rom, 'rb').read()
        print(romOpen)
        for i in range(len(romOpen)):
            self.mem[i + 0x200] = romOpen[i]

        print("ГОТОВО")

    def cycle(self):
        self.opcode = (self.mem[self.pc] << 8) | self.mem[self.pc + 1]

        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4

        self.pc += 2

        extracted_opcode = self.opcode & 0xf000
        try:
            self.funcmap[extracted_opcode]()
        except:
            print("Unknown opcode: {0:x}".format(self.opcode))

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

            if self.sound_timer == 0:
                pass
                # play sounds here

    def _0ZZZ(self):
        """Поиск конкретного опкода с началом "0" """
        extracted_opcode = self.opcode & 0xf0ff
        try:
            self.funcmap[extracted_opcode]()
        except:
            print("Unknown opcode: {0:x}".format(self.opcode))


    def _00E0(self):
        """Очистить экран"""
        self.display = [0] * 64 * 32


    def _00EE(self):
        """Возвратиться из подпрограммы"""
        self.pc = self.stack.pop()


    def _1NNN(self):
        """Перейти по адресу NNN."""
        self.pc = (self.opcode & 0x0fff)


    def _2NNN(self):
        """Вызов подпрограммы по адресу NNN"""
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff


    def _3XNN(self):
        """Пропустить следующую инструкцию, если регистр Vx = NN
        """
        if self.registers[self.vx] == (self.opcode & 0x00ff):
            self.pc += 2


    def _4XNN(self):
        """Пропустить следующую инструкцию, если регистр Vx != NN
        """
        if self.registers[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2


    def _5XY0(self):
        """Пропустить следующую инструкцию, если Vx = Vy
        """
        if self.registers[self.vx] == self.registers[self.vy]:
            self.pc += 2


    def _6XNN(self):
        """Загрузить в регистр Vx число NN, т.е. Vx = NN
        """
        self.registers[self.vx] = self.opcode & 0x00ff


    def _7XNN(self):
        """Установить Vx = Vx + NN
        """
        self.registers[self.vx] += (self.opcode & 0xff)
        self.registers[self.vx] &= 0xFF

    def _8ZZZ(self):
        """Поиск конкретного опкода с началом "8" """
        extracted_opcode = self.opcode & 0xf00f
        extracted_opcode += 0xff0
        try:
            self.funcmap[extracted_opcode]()
        except:
            print("Unknown opcode: {0:x}".format(self.opcode))


    def _8XY0(self):
        """Установить Vx = Vy
        """
        self.registers[self.vx] = self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY1(self):
        """Выполнить операцию дизъюнкция (логическое “ИЛИ”) над значениями регистров Vx и Vy,
         результат сохранить в Vx. Т.е. Vx = Vx | Vy
        """
        self.registers[self.vx] |= self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY2(self):
        """Выполнить операцию конъюнкция (логическое “И”) над значениями регистров Vx и Vy,
        результат сохранить в Vx. Т.е. Vx = Vx & Vy
        """
        self.registers[self.vx] &= self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY3(self):
        """Выполнить операцию “исключающее ИЛИ” над значениями регистров Vx и Vy,
        результат сохранить в Vx. Т.е. Vx = Vx ^ Vy
        """
        self.registers[self.vx] ^= self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY4(self):
        """Значения Vx и Vy суммируются. Если результат больше, чем 8 бит (т.е.> 255) VF устанавливается в 1, иначе 0.
        Только младшие 8 бит результата сохраняются в Vx. Т.е. Vx = Vx + Vy
        """
        if self.registers[self.vx] + self.registers[self.vy] > 0xff:
            self.registers[0xf] = 1
        else:
            self.registers[0xf] = 0
        self.registers[self.vx] += self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY5(self):
        """Если Vx >= Vy, то VF устанавливается в 1, иначе 0. Затем Vy вычитается из Vx,
        а результат сохраняется в Vx. Т.е. Vx = Vx - Vy
        """
        if self.registers[self.vy] > self.registers[self.vx]:
            self.registers[0xf] = 0
        else:
            self.registers[0xf] = 1

        self.registers[self.vx] -= self.registers[self.vy]
        self.registers[self.vx] &= 0xff


    def _8XY6(self):
        """Операция сдвига вправо на 1 бит. Сдвигается регистр Vx. Т.е. Vx = Vx >> 1.
        До операции сдвига выполняется следующее:
        если младший бит (самый правый) регистра Vx равен 1, то VF = 1, иначе VF = 0
        """
        self.registers[0xf] = self.registers[self.vx] & 0x0001
        self.registers[self.vx] = self.registers[self.vx] >> 1


    def _8XY7(self):
        """Если Vy >= Vx, то VF устанавливается в 1, иначе 0.
        Тогда Vx вычитается из Vy, и результат сохраняется в Vx.
        Т.е. Vx = Vy - Vx
        """
        if self.registers[self.vy] > self.registers[self.vx]:
            self.registers[0xf] = 1
        else:
            self.registers[0xf] = 0

        self.registers[self.vy] -= self.registers[self.vx]
        self.registers[self.vx] &= 0xff


    def _8XYE(self):
        """Операция сдвига влево на 1 бит. Сдвигается регистр Vx. Т.е. Vx = Vx << 1.
        До операции сдвига выполняется следующее:
        если младший бит (самый правый) регистра Vx равен 1, то VF = 1, иначе VF = 0
        """
        self.registers[0xf] = self.registers[self.vx] & 0x0001
        self.registers[self.vx] = self.registers[self.vx] << 1


    def _9XY0(self):
        """Пропустить следующую инструкцию, если Vx != Vy"""
        if self.registers[self.vx] != self.registers[self.vy]:
            self.pc += 2


    def _ANNN(self):
        """Значение регистра I устанавливается в nnn
        """
        self.index = self.opcode & 0x0fff


    def _BNNN(self):
        """Перейти по адресу nnn + значение в регистре V0.
        """
        self.pc = (self.opcode & 0x0fff) + self.registers[0]


    def _CXNN(self):
        """ Устанавливается Vx = (случайное число от 0 до 255) & kk
        """
        self.r = int(random.random() * 0xff)
        self.registers[self.vx] = self.r & (self.opcode & 0x00ff)
        self.registers[self.vx] &= 0xff


    def _DXYN(self):
        """Нарисовать на экране спрайт.
        Эта инструкция считывает n байт по адресу содержащемуся в регистре I
        и рисует их на экране в виде спрайта c координатой Vx, Vy.
        Спрайты рисуются на экран по методу операции XOR,
        то есть если в том месте где мы рисуем спрайт уже есть нарисованные пиксели - они стираются,
        если их нет - рисуются. Если хоть один пиксель был стерт, то VF устанавливается в 1, иначе в 0.
        """
        self.registers[0xf] = 0
        x_loc = self.registers[self.vx] & 0xff
        y_loc = self.registers[self.vy] & 0xff
        height = self.opcode & 0x000f
        for y in range(height):
            pixel = self.mem[y + self.index]
            for x in range(8):
                loc = x + x_loc + ((y+y_loc)*64)
                if pixel & (0x80 >> x) != 0 and not (y + y_loc >= 32 or x + x_loc >= 64):
                    if self.display[loc] == 1:
                        self.registers[0xf] = 1;
                    self.display[loc] ^= 1

    def _EZZZ(self):
        """Поиск конкретного опкода с началом "E" """
        extracted_opcode = self.opcode & 0xf00f
        try:
            self.funcmap[extracted_opcode]()
        except:
            print("Unknown opcode: {0:x}".format(self.opcode))


    def _EX9E(self):
        """Пропустить следующую команду если клавиша, номер которой хранится в регистре Vx, нажата
        """
        key = self.registers[self.vx] & 0xf
        if self.key_inputs[key] == 1:
            self.pc += 2


    def _EXA1(self):
        """Пропустить следующую команду если клавиша, номер которой хранится в регистре Vx, не нажата
        """
        key = self.registers[self.vx] & 0xf
        if self.key_inputs[key] == 0:
            self.pc += 2
        else:
            self.pc - 2


    def _FZZZ(self):
        """Поиск конкретного опкода с началом "F" """
        extracted_opcode = self.opcode & 0xf0ff
        try:
            self.funcmap[extracted_opcode]()
        except:
            print("Unknown opcode: {0:x}".format(self.opcode))


    def _FX07(self):
        """Скопировать значение таймера задержки в регистр Vx
        """
        self.registers[self.vx] = self.delay_timer


    def _FX0A(self):
        """Ждать нажатия любой клавиши.
        Как только клавиша будет нажата записать ее номер в регистр Vx и перейти к выполнению следующей инструкции.
        """
        ret = self.get_key()
        if ret >= 0:
            self.registers[self.vx] = ret
        else:
            self.pc -= 2


    def _FX15(self):
        """Установить значение таймера задержки равным значению регистра Vx
        """
        self.delay_timer = self.registers[self.vx]


    def _FX18(self):
        """Установить значение звукового таймера равным значению регистра Vx
        """
        self.sound_timer = self.registers[self.vx]


    def _FX1E(self):
        """Сложить значения регистров I и Vx, результат сохранить в I. Т.е. I = I + Vx
        """
        self.index += self.registers[self.vx]
        if self.index > 0xfff:
            self.registers[0xf] = 1
            self.index &= 0xfff
        else:
            self.registers[0xf] = 0


    def _FX29(self):
        """Используется для вывода на экран символов встроенного шрифта размером 4x5 пикселей.
        Команда загружает в регистр I адрес спрайта, значение которого находится в Vx.
        Например, нам надо вывести на экран цифру 5. Для этого загружаем в Vx число 5.
        Потом команда LD F, Vx загрузит адрес спрайта, содержащего цифру 5, в регистр I
        """
        self.index = (5*(self.registers[self.vx])) & 0xfff


    def _FX33(self):
        """Сохранить значение регистра Vx в двоично-десятичном (BCD) представлении по адресам I, I+1 и I+2
        """
        self.mem[self.index] = self.registers[self.vx] // 100
        self.mem[self.index+1] = (self.registers[self.vx] % 100) // 10
        self.mem[self.index+2] = self.registers[self.vx] % 10


    def _FX55(self):
        """Сохранить значения регистров от V0 до Vx в памяти, начиная с адреса находящегося в I
        """
        for i in range(self.vx):
            self.mem[self.index+i] = self.registers[i]
        self.index += self.vx + 1


    def _FX65(self):
        """Загрузить значения регистров от V0 до Vx из памяти, начиная с адреса находящегося в I
        """
        for i in range(self.vx):
            self.registers[i] = self.mem[self.index + i]
        self.index += self.vx + 1


    def handle_keys(self):
        events = self.interface.handle_events()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.on_key_press(event)
            elif event.type == pygame.KEYUP:
                self.on_key_release(event)


    def get_key(self):
        for i in range(0xf):
            if self.key_inputs[i] == 1:
                return i
        return -1

    def on_key_press(self, event):
        if event.key == pygame.K_F1:
            setSave = {
                'key_inputs': self.key_inputs,
                'display': self.display,
                'mem': self.mem,
                'opcode': self.opcode,
                'vx': self.vx,
                'vy': self.vy,
                'r': self.r,
                'registers': self.registers,
                'sound_timer': self.sound_timer,
                'delay_timer': self.delay_timer,
                'index': self.index,
                'pc': self.pc,
                'key_wait': self.key_wait,
                'stack': self.stack,
                'fonts': self.fonts,
            }
            with open(filedialog.asksaveasfilename(filetypes=[('Save File', '.save')]), 'wb') as output:
                pickle.dump(setSave, output, pickle.HIGHEST_PROTOCOL)
        if event.key in KeysKeybord.keys():
            self.key_inputs[KeysKeybord[event.key]] = 1
            if self.key_wait:
                self.key_wait = False

    def on_key_release(self, event):
        if event.key in KeysKeybord.keys():
            self.key_inputs[KeysKeybord[event.key]] = 0


