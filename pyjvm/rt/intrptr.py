from typing import List, Dict
from .models import PyVMMethod, PyVMType, PyVMValue
from .opcodes import OPCODES, PyOpCode
from .intrpstk import IntrptEvalStack
from .intrpvars import IntrptVars
from .klassrepo import SharedRepo
from .objheap import SimpleHeap
from pyjvm.exception import PyIllegalOpcodeFound
from pyjvm.utils.converter import toint, tostring


class Intrptr(object):
    def __init__(self, repo: SharedRepo):
        self.repo: SharedRepo = repo
        self.heap: SimpleHeap = SimpleHeap()
        self.opcodes: Dict[int, PyOpCode] = OPCODES

    def __str__(self):
        return "Intrprtr :D"

    def execute(self, method: PyVMMethod, lvars: IntrptVars = IntrptVars()) -> PyVMValue:
        klass = method.klass.name
        bytecode = method.bytecode
        evalstack = IntrptEvalStack()
        description = method.name_type
        print(bytecode)

        offset = 0
        while True:
            byte = bytecode[offset]
            offset += 1
            opcode = self.opcodes[toint(byte) & 0xff]
            if not opcode:
                message = "invalid opcode:{} found at:{}, stopping.".format(opcode, byte & 0xff)
                raise PyIllegalOpcodeFound(message)

            num = opcode.params
            print("{} {} {}".format(offset-1, toint(byte), byte))

            if opcode.name == "ACONST_NULL":
                print(">> ", opcode.name)
                evalstack.aconst_null()

            elif opcode.name == "ALOAD":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                evalstack.push(lvars.aload(index))
                offset += 1

            elif opcode.name == "ALOAD_0":
                print(">> ", opcode.name)
                evalstack.push(lvars.aload(0))

            elif opcode.name == "ALOAD_1":
                print(">> ", opcode.name)
                evalstack.push(lvars.aload(1))

            elif opcode.name == "ARETURN":
                print(">> ", opcode.name)
                evalstack.pop()

            elif opcode.name == "ASTORE":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                lvars.astore(index, evalstack.pop())
                offset += 1

            elif opcode.name == "ASTORE_0":
                print(">> ", opcode.name)
                lvars.astore(0, evalstack.pop())

            elif opcode.name == "ASTORE_1":
                print(">> ", opcode.name)
                lvars.astore(1, evalstack.pop())

            elif opcode.name == "BIPUSH":
                print(">> ", opcode.name)
                evalstack.iconst(toint(bytecode[offset]))
                offset += 1

            elif opcode.name == "BREAKPOINT":
                print(">> ", opcode.name)

            elif opcode.name == "DADD":
                print(">> ", opcode.name)
                print(evalstack)
                evalstack.dadd()

            elif opcode.name == "DSUB":
                print(">> ", opcode.name)
                evalstack.dsub()

            elif opcode.name == "DMUL":
                print(">> ", opcode.name)
                evalstack.dmul()

            elif opcode.name == "DDIV":
                print(">> ", opcode.name)
                evalstack.ddiv()

            elif opcode.name == "DNEG":
                print(">> ", opcode.name)
                evalstack.dneg()

            elif opcode.name == "DREM":
                print(">> ", opcode.name)
                evalstack.drem()

            elif opcode.name == "DCONST_0":
                print(">> ", opcode.name)
                evalstack.dconst(0)

            elif opcode.name == "DCONST_1":
                print(">> ", opcode.name)
                evalstack.dconst(1)

            elif opcode.name == "DLOAD":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                evalstack.push(lvars.dload(index))
                offset += 1

            elif opcode.name == "DLOAD_0":
                print(">> ", opcode.name)
                evalstack.push(lvars.dload(0))

            elif opcode.name == "DLOAD_1":
                print(">> ", opcode.name)
                evalstack.push(lvars.dload(1))

            elif opcode.name == "DLOAD_2":
                print(">> ", opcode.name)
                evalstack.push(lvars.dload(2))

            elif opcode.name == "DLOAD_3":
                print(">> ", opcode.name)
                evalstack.push(lvars.dload(3))

            elif opcode.name == "DRETURN":
                print(">> ", opcode.name)
                print(evalstack)
                return evalstack.pop()

            elif opcode.name == "DSTORE":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                lvars.store(index, evalstack.pop())
                offset += 1

            elif opcode.name == "DSTORE_0":
                print(">> ", opcode.name)
                lvars.store(0, evalstack.pop())

            elif opcode.name == "DSTORE_1":
                print(">> ", opcode.name)
                lvars.store(1, evalstack.pop())

            elif opcode.name == "DSTORE_2":
                print(">> ", opcode.name)
                lvars.store(2, evalstack.pop())

            elif opcode.name == "DSTORE_3":
                print(">> ", opcode.name)
                lvars.store(3, evalstack.pop())

            elif opcode.name == "DUP":
                print(">> ", opcode.name)
                evalstack.dup()

            elif opcode.name == "DUP2":
                print(">> ", opcode.name)
                evalstack.dup2()

            elif opcode.name == "DUP_X1":
                print(">> ", opcode.name)
                evalstack.dup_x1()

            elif opcode.name == "GOTO":
                print(">> ", opcode.name)
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump

            elif opcode.name == "I2B":
                print(">> ", opcode.name)
                evalstack.i2b()

            elif opcode.name == "I2C":
                print(">> ", opcode.name)
                evalstack.i2c()

            elif opcode.name == "I2D":
                print(">> ", opcode.name)
                evalstack.i2d()

            elif opcode.name == "I2F":
                print(">> ", opcode.name)
                evalstack.i2f()

            elif opcode.name == "I2L":
                print(">> ", opcode.name)
                evalstack.i2l()

            elif opcode.name == "I2S":
                print(">> ", opcode.name)
                evalstack.i2s()

            elif opcode.name == "IADD":
                print(">> ", opcode.name)
                evalstack.iadd()

            elif opcode.name == "IAND":
                print(">> ", opcode.name)
                evalstack.iand()

            elif opcode.name == "ICONST_M1":
                print(">> ", opcode.name)
                evalstack.iconst(-1)

            elif opcode.name == "ICONST_0":
                print(">> ", opcode.name)
                evalstack.iconst(0)

            elif opcode.name == "ICONST_1":
                print(">> ", opcode.name)
                evalstack.iconst(1)

            elif opcode.name == "ICONST_2":
                print(">> ", opcode.name)
                evalstack.iconst(2)

            elif opcode.name == "ICONST_3":
                print(">> ", opcode.name)
                evalstack.iconst(3)

            elif opcode.name == "ICONST_4":
                print(">> ", opcode.name)
                evalstack.iconst(4)

            elif opcode.name == "ICONST_5":
                print(">> ", opcode.name)
                evalstack.iconst(5)

            elif opcode.name == "IDIV":
                print(">> ", opcode.name)
                evalstack.idiv()

            elif opcode.name == "IF_ICMPEQ":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1])
                if (val1 == val2): offset += (jump - 1)
                offset += 2

            elif opcode.name == "IF_ICMPNE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 != val2) else 2

            elif opcode.name == "IF_ICMPLT":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 < val2) else 2

            elif opcode.name == "IF_ICMPGE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 >= val2) else 2

            elif opcode.name == "IF_ICMPGT":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 > val2) else 2

            elif opcode.name == "IF_ICMPLE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 <= val2) else 2

            elif opcode.name == "IF_ICMPEQ":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1 == val2) else 2

            elif opcode.name == "IFEQ":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 == PyVMValue.pyint(0) else 2

            elif opcode.name == "IFGE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 >= PyVMValue.pyint(0) else 2

            elif opcode.name == "IFGT":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 > PyVMValue.pyint(0) else 2

            elif opcode.name == "IFLE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 <= PyVMValue.pyint(0) else 2

            elif opcode.name == "IFLT":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 < PyVMValue.pyint(0) else 2

            elif opcode.name == "IFNE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 != PyVMValue.pyint(0) else 2

            elif opcode.name == "IFNONNULL":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                #TODO: assert for reference type.
                offset += jump if val1 != PyVMValue.pyint(0) else 2

            elif opcode.name == "IFNULL":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if val1 == PyVMValue.pyint(0) else 2

            elif opcode.name == "IINC":
                print(">> ", opcode.name)
                lvars.iinc(
                    toint(bytecode[offset + 0]),
                    toint(bytecode[offset + 1])
                )
                offset += 2

            elif opcode.name == "ILOAD":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                evalstack.push(lvars.iload(index))
                offset += 1

            elif opcode.name == "ILOAD_0":
                print(">> ", opcode.name)
                evalstack.push(lvars.iload(0))

            elif opcode.name == "ILOAD_1":
                print(">> ", opcode.name)
                evalstack.push(lvars.iload(1))

            elif opcode.name == "ILOAD_2":
                print(">> ", opcode.name)
                evalstack.push(lvars.iload(2))

            elif opcode.name == "ILOAD_3":
                print(">> ", opcode.name)
                evalstack.push(lvars.iload(3))

            elif opcode.name == "IMPDEP1":
                print(">> ", opcode.name)

            elif opcode.name == "IMPDEP2":
                print(">> ", opcode.name)

            elif opcode.name == "IMUL":
                print(">> ", opcode.name)
                evalstack.imul()

            elif opcode.name == "INEG":
                print(">> ", opcode.name)
                evalstack.ineg()

            elif opcode.name == "INVOKESPECIAL":
                print(">> ", opcode.name, offset)
                index = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1])
                function = self.repo.lookupMethodExact(klass, index)
                self.dispatch_invoke(function, evalstack)
                offset += 2

            elif opcode.name == "INVOKESTATIC":
                print(">> ", opcode.name, offset)
                index = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1])
                function = self.repo.lookupMethodExact(klass, index)
                self.dispatch_invoke(function, evalstack)
                offset += 2

            elif opcode.name == "INVOKEVIRTUAL":
                print(">> ", opcode.name, offset)
                index = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1])
                function = self.repo.lookupMethodVirtual(klass, index)
                self.dispatch_invoke(function, evalstack)
                offset += 2

            elif opcode.name == "IOR":
                print(">> ", opcode.name)
                evalstack.ior()

            elif opcode.name == "IREM":
                print(">> ", opcode.name)
                evalstack.irem()

            elif opcode.name == "IRETURN":
                print(">> ", opcode.name)
                print(evalstack)
                return evalstack.pop()

            elif opcode.name == "ISTORE":
                print(">> ", opcode.name)
                index = toint(bytecode[offset])
                lvars.store(index, evalstack.pop())
                offset += 1

            elif opcode.name == "ISTORE_0":
                print(">> ", opcode.name)
                lvars.store(0, evalstack.pop())

            elif opcode.name == "ISTORE_1":
                print(">> ", opcode.name)
                lvars.store(1, evalstack.pop())

            elif opcode.name == "ISTORE_2":
                print(">> ", opcode.name)
                lvars.store(2, evalstack.pop())

            elif opcode.name == "ISTORE_3":
                print(">> ", opcode.name)
                lvars.store(3, evalstack.pop())

            elif opcode.name == "ISUB":
                print(">> ", opcode.name)
                evalstack.isub()

            elif opcode.name == "MONITOREXIT":
                print(">> ", opcode.name)
                #TODO: synchronized section end
                evalstack.pop()

            elif opcode.name == "MONITORENTER":
                print(">> ", opcode.name)
                #TODO: synchronized section start
                evalstack.pop()

            elif opcode.name == "NEW":
                print(">> ", opcode.name)
                index = (toint(bytecode[offset]) << 8) + toint(bytecode[offset + 1])
                klazz = self.repo.lookupKlass(klass, index)
                value = PyVMValue.pyref(self.heap.allocate(klazz))
                evalstack.push(value)

            elif opcode.name == "JSR":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "JSR_W":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "LDC":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "NOP":
                print(">> ", opcode.name)

            elif opcode.name == "POP":
                print(">> ", opcode.name)
                evalstack.pop()

            elif opcode.name == "POP2":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                if (val1.type == PyVMType.D) or (val1.type == PyVMType.J):
                    continue
                evalstack.pop()

            elif opcode.name == "GETFIELD":
                print(">> ", opcode.name)
                index = (toint(bytecode[offset]) << 8) + toint(bytecode[offset + 1])
                field = self.repo.lookupField(klass, index)
                receiver = evalstack.pop()
                pyobject = self.heap.find(receiver.value)
                evalstack.push(pyobject.get_field(field))
                offset += 2

            elif opcode.name == "PUTFIELD":
                print(">> ", opcode.name)
                index = (toint(bytecode[offset]) << 8) + toint(bytecode[offset + 1])
                field = self.repo.lookupField(klass, index)
                value = evalstack.pop()
                receiver = evalstack.pop()
                pyobject = self.heap.find(receiver.value)
                pyobject.set_field(field, value)

            elif opcode.name == "GETSTATIC":
                print(">> ", opcode.name)
                index = (toint(bytecode[offset]) << 8) + toint(bytecode[offset + 1])
                field = self.repo.lookupField(klass, index)
                klazz = field.klass
                evalstack.push(klazz.get_static_field(field))
                offset += 2

            elif opcode.name == "PUTSTATIC":
                print(">> ", opcode.name)
                index = (toint(bytecode[offset]) << 8) + toint(bytecode[offset + 1])
                field = self.repo.lookupField(klass, index)
                value = evalstack.pop()
                fklazz = field.klass
                fklazz.set_static_field(field.name, value)

            elif opcode.name == "RET":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "RETURN":
                print(">> ", opcode.name)
                return None

            elif opcode.name == "SIPUSH":
                print(">> ", opcode.name)
                val = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1])
                evalstack.iconst(val)

            elif opcode.name == "SWAP":
                print(">> ", opcode.name)
                evalstack.swap()

        return None

    def dispatch_invoke(self, func: PyVMMethod, evalstack: IntrptEvalStack):
        params = func.num_params - 1
        if not func.is_static(): params += 1

        args = [evalstack.pop() for x in range(params, -1, -1)]
        vars = IntrptVars(args)

        result = self.execute(func, vars)
        if result: evalstack.push(result)
