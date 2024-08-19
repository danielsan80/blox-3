
import blox.config as c

class Blocks:

    @staticmethod
    def l(n:int) -> float:
        return n * c.block_side

    @staticmethod
    def h(n:int, addFix:bool = False) -> float:
        return n * c.block_side + (c.box_h_fix if addFix else 0)

    @staticmethod
    def ln(l:float) -> int:
        return int(l / c.block_side)

    @staticmethod
    def hn(h:float) -> float:
        return h / c.block_side
