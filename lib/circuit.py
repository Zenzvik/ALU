from lib.core import C, Input, Output
from lib.utils import CircuitError


class Circuit:
    ELEMENTS = {}

    def __init__(self, **kwargs):
        self._init = kwargs
        self._elements = []
        for elem, names in self.ELEMENTS.items():
            for n in names:
                e = elem()
                self._elements.append(e)
                setattr(self, n, e)
        self._input_names = []
        for name, contact in self.inout().items():
            if not (name.startswith('in') or name.startswith('out')):
                raise CircuitError("Bad contacts name")
            if contact:
                setattr(self, name, contact)
            elif name.startswith("in"):
                setattr(self, name, Input())
                self._input_names.append(name)
            else:
                setattr(self, name, Output())
        self._conductors = []
        for c in self.connect():
            self._conductors.append(C(*c))

    def inout(self):
        return {}

    def connect(self):
        return ()

    def update(self):
        for n, value in self._init.items():
            c = getattr(self, n)
            if n.startswith('in'):
                c.value = value
            else:
                value.value = c.value
        for g in self._elements:
            g.update()
        for c in self._conductors:
            c.update()
        for n in self._input_names:
            getattr(self, n).update()

    def run(self, n=100):
        for _ in range(n):
            self.update()


class Bridge(Circuit):
    def inout(self):
        return {
            "in1": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = self.in1.value


class NOT(Circuit):
    def inout(self):
        return {
            "in1": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(not self.in1.value)


class AND(Circuit):
    def inout(self):
        return {
            "in1": None,
            "in2": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(self.in1.value and self.in2.value)


class OR(Circuit):
    def inout(self):
        return {
            "in1": None,
            "in2": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(self.in1.value or self.in2.value)


class NOR(Circuit):
    ELEMENTS = {
        OR: ("o1",),
        NOT: ("n1",)
    }

    def inout(self):
        return {
            "in1": self.o1.in1,
            "in2": self.o1.in2,
            "out1": self.n1.out1
        }

    def connect(self):
        return (
            (self.o1.out1, self.n1.in1),
        )


class NAND(Circuit):
    ELEMENTS = {
        AND: ("a1",),
        NOT: ("n1",)
    }

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "out1": self.n1.out1
        }

    def connect(self):
        return (
            (self.a1.out1, self.n1.in1),
        )


class XOR(Circuit):
    ELEMENTS = {
        AND: ("a1",),
        OR: ("o1",),
        NAND: ("n1",),
        Bridge: ("b1", "b2",)
    }

    def inout(self):
        return {
            "in1": self.b1.in1,
            "in2": self.b2.in1,
            "out1": self.a1.out1
        }

    def connect(self):
        return (
            (self.b1.out1, self.o1.in1, self.n1.in1),
            (self.b2.out1, self.o1.in2, self.n1.in2),
            (self.o1.out1, self.a1.in1),
            (self.n1.out1, self.a1.in2)
        )


class AND3(Circuit):
    ELEMENTS = {
        AND: ("a1", "a2")
    }

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "out1": self.a2.out1
        }

    def connect(self):
        return (
            (self.a2.in2, self.a1.out1),
        )


class AND4(Circuit):
    ELEMENTS = {AND: ("a1", "a2", "a3")}

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "in4": self.a2.in2,
            "out1": self.a3.out1,
        }

    def connect(self):
        return ((self.a1.out1, self.a3.in1), (self.a2.out1, self.a3.in2))


class AND5(Circuit):
    ELEMENTS = {AND: ("a1", "a2", "a3", "a4")}

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "in4": self.a2.in2,
            "in5": self.a4.in2,
            "out1": self.a4.out1,
        }

    def connect(self):
        return (
            (self.a1.out1, self.a3.in1),
            (self.a2.out1, self.a3.in2),
            (self.a3.out1, self.a4.in1),
        )


class AND6(Circuit):
    ELEMENTS = {AND: ("a1", "a2", "a3", "a4", "a5")}

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "in4": self.a2.in2,
            "in5": self.a3.in1,
            "in6": self.a3.in2,
            "out1": self.a5.out1,
        }

    def connect(self):
        return (
            (self.a1.out1, self.a4.in1),
            (self.a2.out1, self.a4.in2),
            (self.a3.out1, self.a5.in1),
            (self.a4.out1, self.a5.in2),
        )


class AND7(Circuit):
    ELEMENTS = {AND: ("a1", "a2", "a3", "a4", "a5", "a6")}

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "in4": self.a2.in2,
            "in5": self.a3.in1,
            "in6": self.a3.in2,
            "in7": self.a6.in2,
            "out1": self.a6.out1,
        }

    def connect(self):
        return (
            (self.a1.out1, self.a4.in1),
            (self.a2.out1, self.a4.in2),
            (self.a3.out1, self.a5.in1),
            (self.a4.out1, self.a5.in2),
            (self.a5.out1, self.a6.in1),
        )


class OR3(Circuit):
    ELEMENTS = {
        OR: ("o1", "o2")
    }

    def inout(self):
        return {
            "in1": self.o1.in1,
            "in2": self.o1.in2,
            "in3": self.o2.in1,
            "out1": self.o2.out1
        }

    def connect(self):
        return (
            (self.o2.in2, self.o1.out1),
        )


class XOR3(Circuit):
    ELEMENTS = {
        OR: ("x1", "x2")
    }

    def inout(self):
        return {
            "in1": self.x1.in1,
            "in2": self.x1.in2,
            "in3": self.x2.in1,
            "out1": self.x2.out1
        }

    def connect(self):
        return (
            (self.x2.in2, self.x1.out1),
        )


class XNOR(Circuit):
    ELEMENTS = {
        XOR: ("x1",),
        NOT: ("n1",)
    }

    def inout(self):
        return {
            "in1": self.x1.in1,
            "in2": self.x1.in2,
            "out1": self.n1.out1
        }

    def connect(self):
        return (
            (self.x1.out1, self.n1.in1),
        )


class ODD(Circuit):
    ELEMENTS = {
        XOR: ('x1', 'x2', 'x3')
    }

    def inout(self):
        return {
            'in1': self.x1.in1,
            'in2': self.x1.in2,
            'in3': self.x2.in1,
            'in4': self.x2.in2,
            'out1': self.x3.out1
        }

    def connect(self):
        return {
            (self.x1.out1, self.x3.in1),
            (self.x2.out1, self.x3.in2)
        }


class MT1(Circuit):
    ELEMENTS = {
        Bridge: ('b1', 'b2', 'b3', 'b4'),
        AND: ('a1', 'a2', 'a3', 'a4', 'a5', 'a6'),
        OR3: ('o31', 'o32'),
        OR: ('o1',)
    }

    def inout(self):
        return {
            'in1': self.b1.in1,
            'in2': self.b2.in1,
            'in3': self.b3.in1,
            'in4': self.b4.in1,
            'out1': self.o1.out1
        }

    def connect(self):
        return {
            (self.b1.out1, self.a1.in1, self.a2.in1, self.a3.in1),
            (self.b2.out1, self.a1.in2, self.a4.in1, self.a5.in1),
            (self.b3.out1, self.a2.in2, self.a4.in2, self.a6.in1),
            (self.b4.out1, self.a3.in2, self.a5.in2, self.a6.in2),
            (self.o31.in1, self.a1.out1),
            (self.o31.in2, self.a2.out1),
            (self.o31.in3, self.a3.out1),
            (self.o32.in1, self.a4.out1),
            (self.o32.in2, self.a5.out1),
            (self.o32.in3, self.a6.out1),
            (self.o31.out1, self.o1.in1),
            (self.o32.out1, self.o1.in2)
        }


class SC(Circuit):
    ELEMENTS = {
        Bridge: ('b1', 'b2', 'b3'),
        OR3: ('o1', 'o2'),
        AND3: ('a1', 'a2', 'a3', 'a4', 'a5'),
        NOT: ('n1', 'n2', 'n3', 'n4', 'n5', 'n6'),
    }

    def inout(self):
        return {
            'in1': self.b1.in1,
            'in2': self.b2.in1,
            'in3': self.b3.in1,
            'out1': self.n1.out1,
            'out2': self.o2.out1,
            'out3': self.a5.out1,
            'out4': self.a1.out1,
        }

    def connect(self):
        return (
            (self.b1.out1, self.o1.in1, self.a1.in1, self.a2.in1, self.n2.in1),
            (self.b2.out1, self.o1.in2, self.a1.in2, self.a3.in1, self.n3.in1),
            (self.b3.out1, self.o1.in3, self.a1.in3, self.a4.in1, self.n4.in1),
            (self.o1.out1, self.n1.in1),
            (self.n2.out1, self.a3.in2, self.a4.in2),
            (self.n3.out1, self.a2.in2, self.a4.in3),
            (self.n4.out1, self.a3.in3, self.a2.in3),
            (self.a2.out1, self.o2.in1),
            (self.a3.out1, self.o2.in2),
            (self.a4.out1, self.o2.in3),
            (self.o2.out1, self.n5.in1),
            (self.o1.out1, self.a5.in1),
            (self.a1.out1, self.n6.in1),
            (self.n6.out1, self.a5.in2),
            (self.n5.out1, self.a5.in3),
        )


class HADD(Circuit):
    ELEMENTS = {
        XOR: ('x1',),
        AND: ('a1',),
        Bridge: ('b1', 'b2')
    }

    def inout(self):
        return {
            'in1': self.b1.in1,
            'in2': self.b2.in1,
            'out1': self.x1.out1,
            'out2': self.a1.out1
        }

    def connect(self):
        return {
            (self.b1.out1, self.x1.in1, self.a1.in1),
            (self.b2.out1, self.x1.in2, self.a1.in2)
        }


class ADD(Circuit):
    ELEMENTS = {
        HADD: ('h1', 'h2'),
        OR: ('o1',)
    }

    def inout(self):
        return {
            'in1': self.h1.in1,
            'in2': self.h1.in2,
            'in3': self.h2.in2,
            'out1': self.h2.out1,
            'out2': self.o1.out1
        }

    def connect(self):
        return {
            (self.h1.out1, self.h2.in1),
            (self.h1.out2, self.o1.in1),
            (self.h2.out2, self.o1.in2),
        }


class AND8el(Circuit):
    ELEMENTS = {
        AND: ('a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7')
    }

    def inout(self):
        return {
            'in1': self.a1.in1,
            'in2': self.a1.in2,
            'in3': self.a2.in1,
            'in4': self.a2.in2,
            'in5': self.a3.in1,
            'in6': self.a3.in2,
            'in7': self.a4.in1,
            'in8': self.a4.in2,
            'out1': self.a7.out1,
        }

    def connect(self):
        return (
            (self.a1.out1, self.a5.in1),
            (self.a2.out1, self.a5.in2),
            (self.a3.out1, self.a6.in1),
            (self.a4.out1, self.a6.in2),
            (self.a5.out1, self.a7.in1),
            (self.a6.out1, self.a7.in2),
        )


class NOT8(Circuit):
    ELEMENTS = {
        NOT: ('n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8')
    }

    def inout(self):
        return {
            'in1': self.n1.in1,
            'in2': self.n2.in1,
            'in3': self.n3.in1,
            'in4': self.n4.in1,
            'in5': self.n5.in1,
            'in6': self.n6.in1,
            'in7': self.n7.in1,
            'in8': self.n8.in1,
            'out1': self.n1.out1,
            'out2': self.n2.out1,
            'out3': self.n3.out1,
            'out4': self.n4.out1,
            'out5': self.n5.out1,
            'out6': self.n6.out1,
            'out7': self.n7.out1,
            'out8': self.n8.out1
        }


class OR8(Circuit):
    ELEMENTS = {
        OR: ('o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8')
    }

    def inout(self):
        return {
            'in1': self.o1.in1,
            'in2': self.o2.in1,
            'in3': self.o3.in1,
            'in4': self.o4.in1,
            'in5': self.o5.in1,
            'in6': self.o6.in1,
            'in7': self.o7.in1,
            'in8': self.o8.in1,
            'in9': self.o1.in2,
            'in10': self.o2.in2,
            'in11': self.o3.in2,
            'in12': self.o4.in2,
            'in13': self.o5.in2,
            'in14': self.o6.in2,
            'in15': self.o7.in2,
            'in16': self.o8.in2,
            'out1': self.o1.out1,
            'out2': self.o2.out1,
            'out3': self.o3.out1,
            'out4': self.o4.out1,
            'out5': self.o5.out1,
            'out6': self.o6.out1,
            'out7': self.o7.out1,
            'out8': self.o8.out1
        }


class AND8(Circuit):
    ELEMENTS = {
        AND: ('a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8')
    }

    def inout(self):
        return {
            'in1': self.a1.in1,
            'in2': self.a2.in1,
            'in3': self.a3.in1,
            'in4': self.a4.in1,
            'in5': self.a5.in1,
            'in6': self.a6.in1,
            'in7': self.a7.in1,
            'in8': self.a8.in1,
            'in9': self.a1.in2,
            'in10': self.a2.in2,
            'in11': self.a3.in2,
            'in12': self.a4.in2,
            'in13': self.a5.in2,
            'in14': self.a6.in2,
            'in15': self.a7.in2,
            'in16': self.a8.in2,
            'out1': self.a1.out1,
            'out2': self.a2.out1,
            'out3': self.a3.out1,
            'out4': self.a4.out1,
            'out5': self.a5.out1,
            'out6': self.a6.out1,
            'out7': self.a7.out1,
            'out8': self.a8.out1
        }


class OR8el(Circuit):
    ELEMENTS = {OR: ('o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7')}

    def inout(self):
        return {
            'in1': self.o1.in1,
            'in2': self.o1.in2,
            'in3': self.o2.in1,
            'in4': self.o2.in2,
            'in5': self.o3.in1,
            'in6': self.o3.in2,
            'in7': self.o4.in1,
            'in8': self.o4.in2,
            'out1': self.o7.out1,
        }

    def connect(self):
        return {
            (self.o1.out1, self.o5.in1),
            (self.o2.out1, self.o5.in2),
            (self.o3.out1, self.o6.in1),
            (self.o4.out1, self.o6.in2),
            (self.o5.out1, self.o7.in1),
            (self.o6.out1, self.o7.in2),
        }


class EQ8(Circuit):
    ELEMENTS = {
        XNOR: ('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'),
        AND8el: ('a1',)
    }

    def inout(self):
        return {
            'in1': self.x1.in1,
            'in2': self.x2.in1,
            'in3': self.x3.in1,
            'in4': self.x4.in1,
            'in5': self.x5.in1,
            'in6': self.x6.in1,
            'in7': self.x7.in1,
            'in8': self.x8.in1,
            'in9': self.x1.in2,
            'in10': self.x2.in2,
            'in11': self.x3.in2,
            'in12': self.x4.in2,
            'in13': self.x5.in2,
            'in14': self.x6.in2,
            'in15': self.x7.in2,
            'in16': self.x8.in2,
            'out1': self.a1.out1
        }

    def connect(self):
        return {
            (self.x1.out1, self.a1.in1),
            (self.x2.out1, self.a1.in2),
            (self.x3.out1, self.a1.in3),
            (self.x4.out1, self.a1.in4),
            (self.x5.out1, self.a1.in5),
            (self.x6.out1, self.a1.in6),
            (self.x7.out1, self.a1.in7),
            (self.x8.out1, self.a1.in8)
        }


class NEQ8(Circuit):
    ELEMENTS = {
        EQ8: ('e1',),
        NOT: ('n1',),
    }

    def inout(self):
        return {
            'in1': self.e1.in1,
            'in2': self.e1.in2,
            'in3': self.e1.in3,
            'in4': self.e1.in4,
            'in5': self.e1.in5,
            'in6': self.e1.in6,
            'in7': self.e1.in7,
            'in8': self.e1.in8,
            'in9': self.e1.in9,
            'in10': self.e1.in10,
            'in11': self.e1.in11,
            'in12': self.e1.in12,
            'in13': self.e1.in13,
            'in14': self.e1.in14,
            'in15': self.e1.in15,
            'in16': self.e1.in16,
            'out1': self.n1.out1
        }

    def connect(self):
        return {
            (self.e1.out1, self.n1.in1)
        }


class GT(Circuit):
    ELEMENTS = {
        AND: ('a1',), NOT: ('n1',)
    }

    def inout(self):
        return {
            'in1': self.a1.in1,
            'in2': self.n1.in1,
            'out1': self.a1.out1
        }

    def connect(self):
        return (
            (self.n1.out1, self.a1.in2),
        )


class GT8(Circuit):
    ELEMENTS = {
        Bridge: ('b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16'),
        XNOR: ('x8', 'x7', 'x6', 'x5', 'x4', 'x3', 'x2'),
        GT: ('g8', 'g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'g1'),
        AND: ('a11',),
        AND3: ('a31',),
        AND4: ('a41',),
        AND5: ('a51',),
        AND6: ('a61',),
        AND7: ('a71',),
        AND8el: ('a81',),
        OR8el: ('o1',),
    }

    def inout(self):
        return {
            'in1': self.b8.in1,
            'in2': self.b7.in1,
            'in3': self.b6.in1,
            'in4': self.b5.in1,
            'in5': self.b4.in1,
            'in6': self.b3.in1,
            'in7': self.b2.in1,
            'in8': self.b1.in1,
            'in9': self.b16.in1,
            'in10': self.b15.in1,
            'in11': self.b14.in1,
            'in12': self.b13.in1,
            'in13': self.b12.in1,
            'in14': self.b11.in1,
            'in15': self.b10.in1,
            'in16': self.b9.in1,
            'out1': self.o1.out1,
        }

    def connect(self):
        return (

            (self.b1.out1, self.g1.in1),
            (self.b2.out1, self.g2.in1, self.x2.in1),
            (self.b3.out1, self.g3.in1, self.x3.in1),
            (self.b4.out1, self.g4.in1, self.x4.in1),
            (self.b5.out1, self.g5.in1, self.x5.in1),
            (self.b6.out1, self.g6.in1, self.x6.in1),
            (self.b7.out1, self.g7.in1, self.x7.in1),
            (self.b8.out1, self.g8.in1, self.x8.in1),
            (self.b9.out1, self.g1.in2),
            (self.b10.out1, self.g2.in2, self.x2.in2),
            (self.b11.out1, self.g3.in2, self.x3.in2),
            (self.b12.out1, self.g4.in2, self.x4.in2),
            (self.b13.out1, self.g5.in2, self.x5.in2),
            (self.b14.out1, self.g6.in2, self.x6.in2),
            (self.b15.out1, self.g7.in2, self.x7.in2),
            (self.b16.out1, self.g8.in2, self.x8.in2),

            (self.g1.out1, self.a81.in1),
            (self.g2.out1, self.a71.in1),
            (self.g3.out1, self.a61.in1),
            (self.g4.out1, self.a51.in1),
            (self.g5.out1, self.a41.in1),
            (self.g6.out1, self.a31.in1),
            (self.g7.out1, self.a11.in1),
            (self.g8.out1, self.o1.in1),
            (self.x2.out1, self.a81.in2),
            (self.x3.out1, self.a71.in2, self.a81.in3),
            (self.x4.out1, self.a61.in2, self.a71.in3, self.a81.in4),
            (
                self.x5.out1,
                self.a51.in2,
                self.a61.in3,
                self.a71.in4,
                self.a81.in5,
            ),
            (
                self.x6.out1,
                self.a41.in2,
                self.a51.in3,
                self.a61.in4,
                self.a71.in5,
                self.a81.in6,
            ),
            (
                self.x7.out1,
                self.a31.in2,
                self.a41.in3,
                self.a51.in4,
                self.a61.in5,
                self.a71.in6,
                self.a81.in7,
            ),
            (
                self.x8.out1,
                self.a11.in2,
                self.a31.in3,
                self.a41.in4,
                self.a51.in5,
                self.a61.in6,
                self.a71.in7,
                self.a81.in8,
            ),

            (self.a11.out1, self.o1.in2),
            (self.a31.out1, self.o1.in3),
            (self.a41.out1, self.o1.in4),
            (self.a51.out1, self.o1.in5),
            (self.a61.out1, self.o1.in6),
            (self.a71.out1, self.o1.in7),
            (self.a81.out1, self.o1.in8),
        )


class GTE8(Circuit):
    ELEMENTS = {
        Bridge: ('b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16'),
        GT8: ('g1',),
        EQ8: ('e1',),
        OR: ('o1',),
    }

    def inout(self):
        return {
            'in1': self.b1.in1,
            'in2': self.b2.in1,
            'in3': self.b3.in1,
            'in4': self.b4.in1,
            'in5': self.b5.in1,
            'in6': self.b6.in1,
            'in7': self.b7.in1,
            'in8': self.b8.in1,
            'in9': self.b9.in1,
            'in10': self.b10.in1,
            'in11': self.b11.in1,
            'in12': self.b12.in1,
            'in13': self.b13.in1,
            'in14': self.b14.in1,
            'in15': self.b15.in1,
            'in16': self.b16.in1,
            'out1': self.o1.out1,
        }

    def connect(self):
        return (
            (self.b1.out1, self.g1.in1, self.e1.in1),
            (self.b2.out1, self.g1.in2, self.e1.in2),
            (self.b3.out1, self.g1.in3, self.e1.in3),
            (self.b4.out1, self.g1.in4, self.e1.in4),
            (self.b5.out1, self.g1.in5, self.e1.in5),
            (self.b6.out1, self.g1.in6, self.e1.in6),
            (self.b7.out1, self.g1.in7, self.e1.in7),
            (self.b8.out1, self.g1.in8, self.e1.in8),
            (self.b9.out1, self.g1.in9, self.e1.in9),
            (self.b10.out1, self.g1.in10, self.e1.in10),
            (self.b11.out1, self.g1.in11, self.e1.in11),
            (self.b12.out1, self.g1.in12, self.e1.in12),
            (self.b13.out1, self.g1.in13, self.e1.in13),
            (self.b14.out1, self.g1.in14, self.e1.in14),
            (self.b15.out1, self.g1.in15, self.e1.in15),
            (self.b16.out1, self.g1.in16, self.e1.in16),
            (self.g1.out1, self.o1.in1),
            (self.e1.out1, self.o1.in2)
        )


class LT8(Circuit):
    ELEMENTS = {
        GTE8: ('g1',),
        NOT: ('n1',)
    }

    def inout(self):
        return {
            'in1': self.g1.in1,
            'in2': self.g1.in2,
            'in3': self.g1.in3,
            'in4': self.g1.in4,
            'in5': self.g1.in5,
            'in6': self.g1.in6,
            'in7': self.g1.in7,
            'in8': self.g1.in8,
            'in9': self.g1.in9,
            'in10': self.g1.in10,
            'in11': self.g1.in11,
            'in12': self.g1.in12,
            'in13': self.g1.in13,
            'in14': self.g1.in14,
            'in15': self.g1.in15,
            'in16': self.g1.in16,
            'out1': self.n1.out1
        }

    def connect(self):
        return {
            (self.g1.out1, self.n1.in1)
        }


class LTE8(Circuit):
    ELEMENTS = {
        GT8: ('g1',),
        NOT: ('n1',)
    }

    def inout(self):
        return {
            'in1': self.g1.in1,
            'in2': self.g1.in2,
            'in3': self.g1.in3,
            'in4': self.g1.in4,
            'in5': self.g1.in5,
            'in6': self.g1.in6,
            'in7': self.g1.in7,
            'in8': self.g1.in8,
            'in9': self.g1.in9,
            'in10': self.g1.in10,
            'in11': self.g1.in11,
            'in12': self.g1.in12,
            'in13': self.g1.in13,
            'in14': self.g1.in14,
            'in15': self.g1.in15,
            'in16': self.g1.in16,
            'out1': self.n1.out1
        }

    def connect(self):
        return {
            (self.g1.out1, self.n1.in1)
        }


class ADD8(Circuit):
    ELEMENTS = {
        ADD: ('a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9'),
    }

    def inout(self):
        return {
            'in1': self.a8.in1,
            'in2': self.a7.in1,
            'in3': self.a6.in1,
            'in4': self.a5.in1,
            'in5': self.a4.in1,
            'in6': self.a3.in1,
            'in7': self.a2.in1,
            'in8': self.a1.in1,
            'in9': self.a8.in2,
            'in10': self.a7.in2,
            'in11': self.a6.in2,
            'in12': self.a5.in2,
            'in13': self.a4.in2,
            'in14': self.a3.in2,
            'in15': self.a2.in2,
            'in16': self.a1.in2,
            'out1': self.a1.out1,
            'out2': self.a2.out1,
            'out3': self.a3.out1,
            'out4': self.a4.out1,
            'out5': self.a5.out1,
            'out6': self.a6.out1,
            'out7': self.a7.out1,
            'out8': self.a8.out1,
            'out9': self.a8.out2,
        }

    def connect(self):
        return (
            (self.a1.out2, self.a2.in3),
            (self.a2.out2, self.a3.in3),
            (self.a3.out2, self.a4.in3),
            (self.a4.out2, self.a5.in3),
            (self.a5.out2, self.a6.in3),
            (self.a6.out2, self.a7.in3),
            (self.a7.out2, self.a8.in3),
        )


class ALU(Circuit):
    pass
