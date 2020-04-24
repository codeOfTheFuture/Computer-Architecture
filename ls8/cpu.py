"""CPU functionality."""

import sys


ADD = 0b10100000 # Add value in two registers, store result in registerA
AND = 0b10101000 # Bitwise-AND the values registerA, registerB, store result in registerA
CALL = 0b01010000 # Calls a subroutine a the address stored in the register
CMP = 0b10100111 # Compare the values in two registers.
DEC = 0b01100110 # Decrement by 1 value in a register.
DIV = 0b10100011 # Divide the value in the first register by the val in the second, stores result in registerA
HLT = 0b00000001 # Halt and Exit
INC = 0b01100101 # Increment by 1 the val in a register
INT = 0b01010010 # Issue the interrupt number stored in a register
IRET = 0b00010011 # Return from an interrupt handler
JEQ = 0b01010101 # If equal flag is true, jump to the address stored in a register
JGE = 0b01011010 # If greater-than or equal flag is true, jump to the address stored in the given register
JGT = 0b01010111 # If greater-than is true, jump to the address stored in a register
JLE = 0b01011001 # If less-than or equal flag is true, jump to the address stored in a register
JLT = 0b01011000 # If less-than flag is true, jump to the address stored in a register
JMP = 0b01010100 # Jump to the address stored in a register
JNE = 0b01010110 # If E flag is falsy, jump to the address in a register
LD = 0b10000011 # Loads registerA with value at memory address stored in registerB
LDI = 0b10000010 # Set the value of a register to an int.
MOD = 0b10100100 # Divide the value in first register by value in second, remainder of result stored in registerA
MUL = 0b10100010 # Multiply the values in two registers, store result in registerA
NOP = 0b00000000 # Do nothing
NOT = 0b01101001 # Perform a bitwise-NOT on value in register, storing result in register
OR = 0b10101010 # Bitwise-OR between values in registerA and registerB, result stored in registerA
POP = 0b01000110 # Pop the value at the top of the stack into a register
PRA = 0b01001000 # Print alpha character val stored in a register
PRN = 0b01000111 # Print numeric value stored in a register
PUSH = 0b01000101 # Push val in a register on the stack
RET = 0b00010001 # Return from subroutine
SHL = 0b10101100 # Shift the val in registerA left by number of bits specified in registerB, filling low bits with 0
SHR = 0b10101101 # Shift val in registerA right by the number of bits in registerB, filling high bits with 0
ST = 0b10000100 # Store value in registerB in address stored in registerA
SUB = 0b10100001 # Subtract the val in the second register from first, storing result in registerA
XOR = 0b10101011 # bitwise-XOR between vals in registerA and registerB, storeing result in registerA
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.reg[SP] = 0xF4
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[POP] = self.handle_pop
        self.branchtable[PUSH] = self.handle_push

    
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, file_path):
        """Load a program into memory."""
        address = 0
        try:    
            with open(file_path) as file:
                for line in file:
                    line = line.split('#')[0]
                    line = line.strip()
                    
                    if line == '':
                        continue
                    i = int(line, 2)
                    self.ram[address] = i
                    address += 1
        except FileExistsError:
            print('File not found')
            sys.exit()

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        print(op, reg_a, reg_b)
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL": 
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while True:
            try:
                ir = self.ram[self.pc] # Instruction
                a = self.ram_read(self.pc + 1) # operand_a
                b = self.ram_read(self.pc + 2) # operand_b

                self.branchtable[ir](a, b)

            except:
                print(f'Instruction at {self.pc} index is unknown')
                sys.exit()


    def handle_hlt(self):
        sys.exit()

    def handle_jmp(self, a, b=None):
        self.pc = a

    def handle_ldi(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def handle_prn(self, a):
        print(self.reg[a])
        self.pc += 2

    def handle_mul(self, a, b):
        op = "MUL"
        print(op, a, b)
        self.alu(op, a, b)
        self.pc += 3

    def handle_pop(self, a, b=None):
        value = self.ram[self.reg[SP]]
        self.reg[a] = value
        self.reg[SP] += 1
        self.pc += 2

    def handle_push(self, a, b=None):
        self.reg[SP] -= 1
        value = self.reg[a]
        self.ram[self.reg[SP]] = value
        self.pc += 2

