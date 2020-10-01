import sys
from tkinter import filedialog
from tkinter import Tk
import argparse
from Chip8 import *
import pygame

def savegame():
    setSave = {
        'key_inputs': chip.key_inputs,
        'display': chip.display,
        'mem': chip.mem,
        'opcode': chip.opcode,
        'vx': chip.vx,
        'vy': chip.vy,
        'r': chip.r,
        'registers': chip.registers,
        'sound_timer': chip.sound_timer,
        'delay_timer': chip.delay_timer,
        'index': chip.index,
        'pc': chip.pc,
        'key_wait': chip.key_wait,
        'stack': chip.stack,
        'fonts': chip.fonts,

    }
    with open(filedialog.asksaveasfilename(filetypes=[('Save File', '.save')]), 'wb') as output:
        pickle.dump(setSave, output, pickle.HIGHEST_PROTOCOL)

def check_save():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                savegame()
                break;

def args_parse():
    parser = argparse.ArgumentParser(description='Chip8 Emulator')
    parser.add_argument('-i', '--info', action='store_true', help='check info')
    parser.add_argument('-f', '--file', action='store', type=str, help='open file')
    parser.add_argument('-fscr', '--fullscreen', action='store_true', help='Fullscreen Mode')
    return parser.parse_args()

if __name__=='__main__':
    args = args_parse()
    if args.info:
        print("Chip8 Emulator by dimka")
        exit()
    root = Tk()
    'root.withdraw()'
    if args.file:
        file_path = args.file
    else:
        file_path = filedialog.askopenfilename()
    root.destroy()
    chip = Chip8()
    if file_path[-5:] == ".save":
        with open(file_path, 'rb') as f:
            new_chip = pickle.load(f)
        chip.key_inputs = new_chip['key_inputs']
        chip.display = new_chip['display']
        chip.mem = new_chip['mem']
        chip.opcode = new_chip['opcode']
        chip.vx = new_chip['vx']
        chip.vy = new_chip['vy']
        chip.r = new_chip['r']
        chip.registers = new_chip['registers']
        chip.sound_timer = new_chip['sound_timer']
        chip.delay_timer = new_chip['delay_timer']
        chip.index = new_chip['index']
        chip.pc = new_chip['pc']
        chip.key_wait = new_chip['key_wait']
        chip.stack = new_chip['stack']
        chip.fonts = new_chip['fonts']

    else:
        chip.loadROM(file_path)
    'chip.loadROM(sys.argv[1])'
    'chip.loadROM("c:/ChipGame/wipeoff")'




    while True:
        chip.cycle()
        chip.handle_keys()
        chip.interface.draw(chip.display)

















