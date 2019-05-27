# :D
from .models import PyVMMethod, PyVMType, PyVMValue
from .opcodes import OPCODES
from .intrpstk import IntrptEvalStack
from .intrpvars import IntrptVars
from .klassrepo import SharedRepo
from pyjvm.exception import PyIllegalOpcodeFound
from pyjvm.utils.converter import toint, tostring


class Intrptr(object):
    def __init__(self, repo: SharedRepo):
        self.repo = repo
        self.opcodes = OPCODES

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
                evalstack.push()

            elif opcode.name == "ALOAD_0":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "ALOAD_1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "ARETURN":
                print(">> ", opcode.name)
                evalstack.pop()

            elif opcode.name == "ASTORE":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "ASTORE_0":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "ASTORE_1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "BIPUSH":
                print(">> ", opcode.name)
                evalstack.iconst(toint(bytecode[offset]))
                offset += 1

            elif opcode.name == "BREAKPOINT":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DADD":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DCONST_0":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DCONST_1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DLOAD":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DLOAD_0":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DLOAD_1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DLOAD_2":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DLOAD_3":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DRETURN":
                print(">> ", opcode.name)
                evalstack.pop()

            elif opcode.name == "DSTORE":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DSTORE_0":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DSTORE_1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DSTORE_2":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DSTORE_3":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DSUB":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DUP":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "DUP_X1":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "GETFIELD":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "GETSTATIC":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "GOTO":
                print(">> ", opcode.name)
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump

            elif opcode.name == "I2D":
                print(">> ", opcode.name)
                pass

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
                if (val1.value == val2.value): offset += (jump - 1)
                offset += 2

            elif opcode.name == "IF_ICMPNE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1.value != val2.value) else 2

            elif opcode.name == "IF_ICMPLT":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IF_ICMPGE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1.value >= val2.value) else 2

            elif opcode.name == "IF_ICMPGT":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IF_ICMPLE":
                print(">> ", opcode.name)
                val1 = evalstack.pop()
                val2 = evalstack.pop()
                jump = (toint(bytecode[offset + 0]) << 8) + toint(bytecode[offset + 1]) - 1
                offset += jump if (val1.value <= val2.value) else 2

            elif opcode.name == "IF_ICMPEQ":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFEQ":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFGE":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFGT":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFLE":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFLT":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFNE":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFNONNULL":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IFNULL":
                print(">> ", opcode.name)
                pass

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
                value = lvars.iload(index)
                evalstack.iconst(value)
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
                pass

            elif opcode.name == "IMPDEP2":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IMUL":
                print(">> ", opcode.name)
                evalstack.imul()

            elif opcode.name == "INEG":
                print(">> ", opcode.name)
                evalstack.ineg()

            elif opcode.name == "INVOKESPECIAL":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "INVOKESTATIC":
                print(">> ", opcode.name, offset)
                p1 = (toint(bytecode[offset + 0]) << 8)
                p2 = (toint(bytecode[offset + 1]) << 0)
                offset += 2
                index = p1 + p2
                function = self.repo.lookupMethodExact(klass, index) 
                self.dispatch_invoke(function, evalstack)

            elif opcode.name == "INVOKEVIRTUAL":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "IOR":
                print(">> ", opcode.name)
                evalstack.ior()

            elif opcode.name == "IREM":
                print(">> ", opcode.name)
                evalstack.irem()

            elif opcode.name == "IRETURN":
                print(">> ", opcode.name)
                print (evalstack)
                pyvalue = evalstack.pop()
                return pyvalue

            elif opcode.name == "ISTORE":
                print(">> ", opcode.name)
                pass

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

            elif opcode.name == "MONITORENTER":
                print(">> ", opcode.name)
                #TODO
                evalstack.pop()

            elif opcode.name == "MONITOREXIT":
                print(">> ", opcode.name)
                #TODO
                evalstack.pop()

            elif opcode.name == "NEW":
                print(">> ", opcode.name)
                pass

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
                pass

            elif opcode.name == "POP":
                print(">> ", opcode.name)
                evalstack.pop()

            elif opcode.name == "POP2":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "PUTFIELD":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "PUTSTATIC":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "RET":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "RETURN":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "SIPUSH":
                print(">> ", opcode.name)
                pass

            elif opcode.name == "SWAP":
                print(">> ", opcode.name)
                pass

        return None

    def dispatch_invoke(self, func: PyVMMethod, evalstack: IntrptEvalStack):
        params = func.num_params - 1
        if not func.is_static(): params += 1

        args = [evalstack.pop() for x in range(params, -1, -1)]
        vars = IntrptVars(args)

        result = self.execute(func, vars)
        if result: evalstack.push(result)
