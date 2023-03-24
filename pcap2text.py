#!/usr/bin/env python
# coding:utf-8
import argparse
import os
from tempfile import NamedTemporaryFile

BOOT_KEYBOARD_MAP = {
    0x00: (None, None),                         # Reserved (no event indicated)
    0x01: ('', ''),                             # ErrorRollOver
    0x02: ('', ''),                             # POSTFail
    0x03: ('', ''),                             # ErrorUndefined
    0x04: ('a', 'A'),                           # a
    0x05: ('b', 'B'),                           # b
    0x06: ('c', 'C'),                           # c
    0x07: ('d', 'D'),                           # d
    0x08: ('e', 'E'),                           # e
    0x09: ('f', 'F'),                           # f
    0x0a: ('g', 'G'),                           # g
    0x0b: ('h', 'H'),                           # h
    0x0c: ('i', 'I'),                           # i
    0x0d: ('j', 'J'),                           # j
    0x0e: ('k', 'K'),                           # k
    0x0f: ('l', 'L'),                           # l
    0x10: ('m', 'M'),                           # m
    0x11: ('n', 'N'),                           # n
    0x12: ('o', 'O'),                           # o
    0x13: ('p', 'P'),                           # p
    0x14: ('q', 'Q'),                           # q
    0x15: ('r', 'R'),                           # r
    0x16: ('s', 'S'),                           # s
    0x17: ('t', 'T'),                           # t
    0x18: ('u', 'U'),                           # u
    0x19: ('v', 'V'),                           # v
    0x1a: ('w', 'W'),                           # w
    0x1b: ('x', 'X'),                           # x
    0x1c: ('y', 'Y'),                           # y
    0x1d: ('z', 'Z'),                           # z
    0x1e: ('1', '!'),                           # 1
    0x1f: ('2', '@'),                           # 2
    0x20: ('3', '#'),                           # 3
    0x21: ('4', '$'),                           # 4
    0x22: ('5', '%'),                           # 5
    0x23: ('6', '^'),                           # 6
    0x24: ('7', '&'),                           # 7
    0x25: ('8', '*'),                           # 8
    0x26: ('9', '('),                           # 9
    0x27: ('0', ')'),                           # 0
    0x28: ('\n', '\n'),                         # Return (ENTER)
    0x29: ('[ESC]', '[ESC]'),                   # Escape
    0x2a: ('\b', '\b'),                         # Backspace
    0x2b: ('\t', '\t'),                         # Tab
    0x2c: (' ', ' '),                           # Spacebar
    0x2d: ('-', '_'),                           # -
    0x2e: ('=', '+'),                           # =
    0x2f: ('[', '{'),                           # [
    0x30: (']', '}'),                           # ]
    0x31: ('\\', '|'),                          # \
    0x32: ('', ''),                             # Non-US # and ~
    0x33: (';', ':'),                           # ;
    0x34: ('\'', '"'),                          # '
    0x35: ('`', '~'),                           # `
    0x36: (',', '<'),                           # ,
    0x37: ('.', '>'),                           # .
    0x38: ('/', '?'),                           # /
    0x39: ('[CAPSLOCK]', '[CAPSLOCK]'),         # Caps Lock
    0x3a: ('[F1]', '[F1]'),                     # F1
    0x3b: ('[F2]', '[F2]'),                     # F2
    0x3c: ('[F3]', '[F3]'),                     # F3
    0x3d: ('[F4]', '[F4]'),                     # F4
    0x3e: ('[F5]', '[F5]'),                     # F5
    0x3f: ('[F6]', '[F6]'),                     # F6
    0x40: ('[F7]', '[F7]'),                     # F7
    0x41: ('[F8]', '[F8]'),                     # F8
    0x42: ('[F9]', '[F9]'),                     # F9
    0x43: ('[F10]', '[F10]'),                   # F10
    0x44: ('[F11]', '[F11]'),                   # F11
    0x45: ('[F12]', '[F12]'),                   # F12
    0x46: ('[PRINTSCREEN]', '[PRINTSCREEN]'),   # Print Screen
    0x47: ('[SCROLLLOCK]', '[SCROLLLOCK]'),     # Scroll Lock
    0x48: ('[PAUSE]', '[PAUSE]'),               # Pause
    0x49: ('[INSERT]', '[INSERT]'),             # Insert
    0x4a: ('[HOME]', '[HOME]'),                 # Home
    0x4b: ('[PAGEUP]', '[PAGEUP]'),             # Page Up
    0x4c: ('[DELETE]', '[DELETE]'),             # Delete Forward
    0x4d: ('[END]', '[END]'),                   # End
    0x4e: ('[PAGEDOWN]', '[PAGEDOWN]'),         # Page Down
    0x4f: ('[RIGHTARROW]', '[RIGHTARROW]'),     # Right Arrow
    0x50: ('[LEFTARROW]', '[LEFTARROW]'),       # Left Arrow
    0x51: ('[DOWNARROW]', '[DOWNARROW]'),       # Down Arrow
    0x52: ('[UPARROW]', '[UPARROW]'),           # Up Arrow
    0x53: ('[NUMLOCK]', '[NUMLOCK]'),           # Num Lock
    0x54: ('[KEYPADSLASH]', '/'),               # Keypad /
    0x55: ('[KEYPADASTERISK]', '*'),            # Keypad *
    0x56: ('[KEYPADMINUS]', '-'),               # Keypad -
    0x57: ('[KEYPADPLUS]', '+'),                # Keypad +
    0x58: ('[KEYPADENTER]', '[KEYPADENTER]'),   # Keypad ENTER
    0x59: ('[KEYPAD1]', '1'),                   # Keypad 1 and End
    0x5a: ('[KEYPAD2]', '2'),                   # Keypad 2 and Down Arrow
    0x5b: ('[KEYPAD3]', '3'),                   # Keypad 3 and PageDn
    0x5c: ('[KEYPAD4]', '4'),                   # Keypad 4 and Left Arrow
    0x5d: ('[KEYPAD5]', '5'),                   # Keypad 5
    0x5e: ('[KEYPAD6]', '6'),                   # Keypad 6 and Right Arrow
    0x5f: ('[KEYPAD7]', '7'),                   # Keypad 7 and Home
    0x60: ('[KEYPAD8]', '8'),                   # Keypad 8 and Up Arrow
    0x61: ('[KEYPAD9]', '9'),                   # Keypad 9 and Page Up
    0x62: ('[KEYPAD0]', '0'),                   # Keypad 0 and Insert
    0x63: ('[KEYPADPERIOD]', '.'),              # Keypad . and Delete
    0x64: ('', ''),                             # Non-US \ and |
    0x65: ('', ''),                             # Application
    0x66: ('', ''),                             # Power
    0x67: ('[KEYPADEQUALS]', '='),              # Keypad =
    0x68: ('[F13]', '[F13]'),                   # F13
    0x69: ('[F14]', '[F14]'),                   # F14
    0x6a: ('[F15]', '[F15]'),                   # F15
    0x6b: ('[F16]', '[F16]'),                   # F16
    0x6c: ('[F17]', '[F17]'),                   # F17
    0x6d: ('[F18]', '[F18]'),                   # F18
    0x6e: ('[F19]', '[F19]'),                   # F19
    0x6f: ('[F20]', '[F20]'),                   # F20
    0x70: ('[F21]', '[F21]'),                   # F21
    0x71: ('[F22]', '[F22]'),                   # F22
    0x72: ('[F23]', '[F23]'),                   # F23
    0x73: ('[F24]', '[F24]'),                   # F24
    0x74: ('', ''),                             # Execute
    0x75: ('', ''),                             # Help
    0x76: ('', ''),                             # Menu
    0x77: ('', ''),                             # Select
    0x78: ('', ''),                             # Stop
    0x79: ('', ''),                             # Again
    0x7a: ('', ''),                             # Undo
    0x7b: ('', ''),                             # Cut
    0x7c: ('', ''),                             # Copy
    0x7d: ('', ''),                             # Paste
    0x7e: ('', ''),                             # Find
    0x7f: ('', ''),                             # Mute
    0x80: ('', ''),                             # Volume Up
    0x81: ('', ''),                             # Volume Down
    0x82: ('', ''),                             # Locking Caps Lock
    0x83: ('', ''),                             # Locking Num Lock
    0x84: ('', ''),                             # Locking Scroll Lock
    0x85: ('', ''),                             # Keypad Comma
    0x86: ('', ''),                             # Keypad Equal Sign
    0x87: ('', ''),                             # International1
    0x88: ('', ''),                             # International2
    0x89: ('', ''),                             # International3
    0x8a: ('', ''),                             # International4
    0x8b: ('', ''),                             # International5
    0x8c: ('', ''),                             # International6
    0x8d: ('', ''),                             # International7
    0x8e: ('', ''),                             # International8
    0x8f: ('', ''),                             # International9
    0x90: ('', ''),                             # LANG1
    0x91: ('', ''),                             # LANG2
    0x92: ('', ''),                             # LANG3
    0x93: ('', ''),                             # LANG4
    0x94: ('', ''),                             # LANG5
    0x95: ('', ''),                             # LANG6
    0x96: ('', ''),                             # LANG7
    0x97: ('', ''),                             # LANG8
    0x98: ('', ''),                             # LANG9
    0x99: ('', ''),                             # Alternate Erase
    0x9a: ('', ''),                             # SysReq/Attention
    0x9b: ('', ''),                             # Cancel
    0x9c: ('', ''),                             # Clear
    0x9d: ('', ''),                             # Prior
    0x9e: ('', ''),                             # Return
    0x9f: ('', ''),                             # Separator
    0xa0: ('', ''),                             # Out
    0xa1: ('', ''),                             # Oper
    0xa2: ('', ''),                             # Clear/Again
    0xa3: ('', ''),                             # CrSel/Props
    0xa4: ('', ''),                             # ExSel
    0xa5: ('', ''),                             # Reserved
    0xa6: ('', ''),                             # Reserved
    0xa7: ('', ''),                             # Reserved
    0xa8: ('', ''),                             # Reserved
    0xa9: ('', ''),                             # Reserved
    0xaa: ('', ''),                             # Reserved
    0xab: ('', ''),                             # Reserved
    0xac: ('', ''),                             # Reserved
    0xad: ('', ''),                             # Reserved
    0xae: ('', ''),                             # Reserved
    0xaf: ('', ''),                             # Reserved
    0xb0: ('', ''),                             # Keypad 00
    0xb1: ('', ''),                             # Keypad 000
    0xb2: ('', ''),                             # Thousands Separator
    0xb3: ('', ''),                             # Decimal Separator
    0xb4: ('', ''),                             # Currency Unit
    0xb5: ('', ''),                             # Currency Sub-unit
    0xb6: ('', ''),                             # Keypad (
    0xb7: ('', ''),                             # Keypad )
    0xb8: ('', ''),                             # Keypad {
    0xb9: ('', ''),                             # Keypad }
    0xba: ('', ''),                             # Keypad Tab
    0xbb: ('', ''),                             # Keypad Backspace
    0xbc: ('', ''),                             # Keypad A
    0xbd: ('', ''),                             # Keypad B
    0xbe: ('', ''),                             # Keypad C
    0xbf: ('', ''),                             # Keypad D
    0xc0: ('', ''),                             # Keypad E
    0xc1: ('', ''),                             # Keypad F
    0xc2: ('', ''),                             # Keypad XOR
    0xc3: ('', ''),                             # Keypad ^
    0xc4: ('', ''),                             # Keypad %
    0xc5: ('', ''),                             # Keypad <
    0xc6: ('', ''),                             # Keypad >
    0xc7: ('', ''),                             # Keypad &
    0xc8: ('', ''),                             # Keypad &&
    0xc9: ('', ''),                             # Keypad |
    0xca: ('', ''),                             # Keypad ||
    0xcb: ('', ''),                             # Keypad :
    0xcc: ('', ''),                             # Keypad #
    0xcd: ('', ''),                             # Keypad Space
    0xce: ('', ''),                             # Keypad @
    0xcf: ('', ''),                             # Keypad !
    0xd0: ('', ''),                             # Keypad Memory Store
    0xd1: ('', ''),                             # Keypad Memory Recall
    0xd2: ('', ''),                             # Keypad Memory Clear
    0xd3: ('', ''),                             # Keypad Memory Add
    0xd4: ('', ''),                             # Keypad Memory Subtract
    0xd5: ('', ''),                             # Keypad Memory Multiply
    0xd6: ('', ''),                             # Keypad Memory Divide
    0xd7: ('', ''),                             # Keypad +/-
    0xd8: ('', ''),                             # Keypad Clear
    0xd9: ('', ''),                             # Keypad Clear Entry
    0xda: ('', ''),                             # Keypad Binary
    0xdb: ('', ''),                             # Keypad Octal
    0xdc: ('', ''),                             # Keypad Decimal
    0xdd: ('', ''),                             # Keypad Hexadecimal
    0xde: ('', ''),                             # Reserved
    0xdf: ('', ''),                             # Reserved
    0xe0: ('', ''),                             # Left Control
    0xe1: ('', ''),                             # Left Shift
    0xe2: ('', ''),                             # Left Alt
    0xe3: ('', ''),                             # Left GUI
    0xe4: ('', ''),                             # Right Control
    0xe5: ('', ''),                             # Right Shift
    0xe6: ('', ''),                             # Right Alt
    0xe7: ('', ''),                             # Right GUI
}


def parse_boot_keyboard_report(data: bytearray):
    # 数据解析
    modifiers = data[0]  # 修改键字节
    keys = data[2:8]      # 键码字节

    # 将修改键字节中的位解码为按键修饰符
    ctrl = (modifiers & 0x11) != 0
    shift = (modifiers & 0x22) != 0
    alt = (modifiers & 0x44) != 0
    gui = (modifiers & 0x88) != 0

    # 解析键码字节并将其映射为字符
    characters = []
    for key in keys:
        if key != 0:
            # 键码不为0则查询映射表
            if key in BOOT_KEYBOARD_MAP:
                characters.append(BOOT_KEYBOARD_MAP[key][shift])
            else:
                characters.append(None)
    return (ctrl, shift, alt, gui, characters)


def help_formatter(prog):
    return argparse.HelpFormatter(prog, max_help_position=40)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='Parse keyboard report data and output as text', formatter_class=help_formatter)
    parser.add_argument('pcapng_file', help='path to the pcapng file')
    args = parser.parse_args()

    # 通过tshark解析pcapng文件，获取键盘数据包
    tmpfile = NamedTemporaryFile(delete=False)
    tmpfile.close()

    command = "tshark -r %s -T fields -e usbhid.data -e usb.capdata > %s" % (
        args.pcapng_file, tmpfile.name)
    os.system(command)

    with open(tmpfile.name, 'r') as f:
        lines = f.readlines()

    os.unlink(tmpfile.name)

    # 解析键盘数据包，获取输入字符
    text = ""
    last_characters_count = {}
    repeat_limit = 2
    for line in lines:
        capdata = line.strip().replace(':', '')
        if capdata:
            data = bytearray.fromhex(capdata)
            characters = parse_boot_keyboard_report(data)[-1]
            if not characters:
                last_characters_count = {}
            else:
                for character in characters:
                    if character:
                        last_characters_count = {character: count for character,
                                                count in last_characters_count.items() if character in characters}
                        if character in last_characters_count:
                            last_characters_count[character] += 1
                            if last_characters_count[character] <= repeat_limit:
                                continue
                        else:
                            last_characters_count[character] = 1
                        text += character
        else:
            pass

    raw_text = repr(text)
    print(f'Raw output:\n{raw_text}')
    print(f'Text output:\n{text}')


if __name__ == "__main__":
    main()
