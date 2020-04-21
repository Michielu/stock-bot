from enum import Enum


class ParabolicState(Enum):
    LONG = 1
    SHORT = 2
    INIT = 3


class ParabolicTrend:
    parabolic_acc_limit = .2
    extreme = []
    sar = []
    last_high = 0
    last_low = 0

    def __init__(self, para_acc):
        self.state = ParabolicState.INIT
        self.acc = [para_acc]
        self.const_acc = para_acc

    def next(self, high, low):
        if self.state == ParabolicState.INIT:
            self.state = ParabolicState.LONG
            self.extreme = [high]
            self.sar = [low]
            self.last_high = high
            self.last_low = low

        elif self.state == ParabolicState.SHORT:
            if self.sar[-1] < high:
                self.state = ParabolicState.LONG
                self.acc.append(self.const_acc)
                self.sar.append(self.extreme[-1])
                self.extreme.append(high)
            else:
                # Not setting State bc it doesn't change
                if low < self.extreme[-1]:
                    self.acc.append(min(
                        [self.acc[-1] + self.const_acc, self.parabolic_acc_limit]))
                    self.extreme.append(low)
                else:
                    self.acc.append(self.acc[-1])
                    self.extreme.append(self.extreme[-1])

                self.sar.append(max([max(
                    [high, self.last_high]), self.sar[-1] + self.acc[-1] * (self.extreme[-1] - self.sar[-1])]))

        else:
            # In ParabolicState.LONG
            if self.sar[-1] > low:
                self.state = ParabolicState.SHORT
                self.acc.append(self.const_acc)
                self.sar.append(self.extreme[-1])
                self.extreme.append(low)
            else:
                # Not setting State bc it doesn't change
                if high > self.extreme[-1]:
                    self.acc.append(
                        min([self.acc[-1]+self.const_acc, self.parabolic_acc_limit]))
                    self.extreme.append(high)
                else:
                    self.acc.append(self.acc[-1])
                    self.extreme.append(self.extreme[-1])
                self.sar.append(min([min([low, self.last_low]), self.sar[-1] +
                                     self.acc[-1] * (self.extreme[-1] - self.sar[-1])]))

        self.last_high = high
        self.last_low = low
        return self.sar[-1]

    def get_sar(self):
        return self.sar
