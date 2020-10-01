import unittest
from Chip8 import *

class MyTestCase(unittest.TestCase):
    def test_00EE(self):
        chip = Chip8()
        for address in range(0x200, 0xFFFF, 0x10):
            chip.stack.append(address)
            chip._00EE()
            self.assertEqual(chip.pc, address)


    def test_1NNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip._1NNN()
            self.assertEqual(chip.pc, address & 0x0fff)


    def test_2NNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip.pc = 0
            chip.stack.append(chip.pc)
            chip._2NNN()
            self.assertEqual(chip.stack.pop(), 0)
            self.assertEqual(chip.pc,address & 0x0fff)


    def test_3XNN(self):
        chip = Chip8()
        chip.pc = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip.registers[chip.vx] = 0x3f30
            chip._3XNN()
            if chip.registers[chip.vx] == chip.opcode & 0x00ff:
                self.assertEqual(chip.pc, 2)


    def test_4XNN(self):
        chip = Chip8()
        chip.pc = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip.registers[chip.vx] = 0x4f33
            chip._4XNN()
            if chip.registers[chip.vx] == chip.opcode & 0x00ff:
                self.assertEqual(chip.pc, 0)


    def test_5XY0(self):
        chip = Chip8()
        chip.pc = 0
        chip.vx = 1
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            chip.registers[chip.vx] = 0x5f30
            chip._5XY0()
            if chip.registers[chip.vx] == chip.registers[chip.vy]:
                self.assertEqual(chip.pc, 2)


    def test_6XNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip._6XNN()
            self.assertEqual(chip.registers[chip.vx], address & 0x00ff)


    def test_7XNN(self):
        chip = Chip8()
        test_vx = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip._7XNN()
            test_vx += address & 0xFF
            self.assertEqual(chip.registers[chip.vx],test_vx & 0xFF)


    def test_8XY0(self):
        chip = Chip8()
        chip.vy = 1
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            chip._8XY0()
            self.assertEqual(chip.registers[chip.vx], address & 0xFF)


    def test_8XY1(self):
        chip = Chip8()
        chip.vy = 1
        res = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            res |= address
            chip._8XY1()
            self.assertEqual(chip.registers[chip.vx], res & 0xFF)


    def test_8XY2(self):
        chip = Chip8()
        chip.vy = 1
        res = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            res &= address
            chip._8XY2()
            self.assertEqual(chip.registers[chip.vx], res & 0xFF)


    def test_8XY3(self):
        chip = Chip8()
        chip.vy = 1
        res = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            res ^= address
            chip._8XY3()
            self.assertEqual(chip.registers[chip.vx], res & 0xFF)


    def test_8XY4(self):
        chip = Chip8()
        chip.vy = 1
        for addressX in range(0x0, 0xFF, 0x10):
            for addressY in range(0x0, 0xFF, 0x10):
                chip.registers[chip.vx] = addressX
                chip.registers[chip.vy] = addressY
                chip._8XY4()
                if addressY + addressX > 0xFF:
                    self.assertEqual(chip.registers[0xf], 1)
                else:
                    self.assertEqual(chip.registers[0xf], 0)
                self.assertEqual(chip.registers[chip.vx],(addressY+addressX)&0xFF)

    def test_8XY5(self):
        chip = Chip8()
        chip.vy = 1
        for addressX in range(0x0, 0xFF, 0x10):
            for addressY in range(0x0, 0xFF, 0x10):
                chip.registers[chip.vx] = addressX
                chip.registers[chip.vy] = addressY
                chip._8XY5()
                if addressY > addressX:
                    self.assertEqual(chip.registers[0xf], 0)
                else:
                    self.assertEqual(chip.registers[0xf], 1)
                self.assertEqual(chip.registers[chip.vx], (addressX - addressY) & 0xFF)

    def test_8XY6(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._8XY6()
            self.assertEqual(chip.registers[0xf], address & 0x0001)
            self.assertEqual(chip.registers[chip.vx], address >> 1)


    def test_8XY7(self):
        chip = Chip8()
        chip.vy = 1
        for addressX in range(0x0, 0xFF, 0x10):
            for addressY in range(0x0, 0xFF, 0x10):
                chip.registers[chip.vx] = addressX
                chip.registers[chip.vy] = addressY
                chip._8XY7()
                if addressY > addressX:
                    self.assertEqual(chip.registers[0xf], 1)
                else:
                    self.assertEqual(chip.registers[0xf], 0)
                self.assertEqual(chip.registers[chip.vy], addressY - addressX)
                self.assertEqual(chip.registers[chip.vx], addressX & 0xFF)


    def test_8XYE(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._8XYE()
            self.assertEqual(chip.registers[0xf], address & 0x0001)
            self.assertEqual(chip.registers[chip.vx], address << 1)


    def test_9XY0(self):
        chip = Chip8()
        chip.pc = 0
        chip.vx = 1
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vy] = address
            chip.registers[chip.vx] = 0x9f33
            chip._9XY0()
            if chip.registers[chip.vx] == address:
                self.assertEqual(chip.pc, 0)


    def test_ANNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip._ANNN()
            self.assertEqual(chip.index, address & 0x0fff)


    def test_BNNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            chip._BNNN()
            self.assertEqual(chip.pc, (address & 0x0fff) + chip.registers[0])


    def test_CXNN(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.opcode = address
            self.assertEqual(chip.registers[chip.vx], (chip.r & (address & 0x00ff)) & 0xff)


    def test_EX9E(self):
        chip = Chip8()
        chip.pc = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._EX9E()
            if chip.key_inputs[address & 0xf] != 1:
                self.assertEqual(chip.pc, 0)


    def test_EXA1(self):
        chip = Chip8()
        chip.pc = 0
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._EXA1()
            if chip.key_inputs[address & 0xf] == 1:
                self.assertEqual(chip.pc, 0)


    def test_FX07(self):
        chip = Chip8()
        for timer in range (0x0, 0xFF, 0x10):
            chip.delay_timer = timer
            chip._FX07()
            self.assertEqual(chip.registers[chip.vx], timer)


    def test_FX0A(self):
        chip = Chip8()
        test_ret = chip.get_key()
        chip._FX0A()
        if test_ret >= 0:
            self.assertEqual(chip.registers[chip.vx], test_ret)


    def test_FX15(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._FX15()
            self.assertEqual(chip.delay_timer, address)


    def test_FX18(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._FX18()
            self.assertEqual(chip.sound_timer, address)


    def test_FX1E(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._FX1E()
            if chip.index > 0xfff:
                self.assertEqual(chip.registers[0xf] , 1)
                self.assertEqual(chip.index, (chip.index & 0xfff))


    def test_FX29(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._FX29()
            self.assertEqual(chip.index, ((address*5) & 0xfff))


    def test_FX33(self):
        chip = Chip8()
        for address in range(0x0, 0xFFFF, 0x10):
            chip.registers[chip.vx] = address
            chip._FX33()
            self.assertEqual(chip.mem[chip.index], address // 100)
            self.assertEqual(chip.mem[chip.index+1], (address % 100) // 10)
            self.assertEqual(chip.mem[chip.index+2], address % 10)


    def test_FX55(self):
        chip = Chip8()
        chip._FX55()
        for i in range(chip.vx):
            self.assertEqual(chip.mem[chip.index+i], chip.registers[i])


    def test_FX65(self):
        chip = Chip8()
        chip._FX65()
        for i in range(chip.vx):
            self.assertEqual(chip.mem[chip.index + i], chip.registers[i])


if __name__ == '__main__':
    unittest.main()
