import time
from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt

apb_freq = 2441


@dataclass
class Motor:
    duty_cycle: int = 0
    max_duty_cycle: int = 65535
    counts: int = 0
    counts_per_rev: int = 1200
    rpm: int = 0
    rpm_skew: float = 1
    target_rpm: int = 0

    @property
    def ideal_rpm(self):
        return self.duty_cycle / self.max_duty_cycle * 500

    def set_counts(self, to_add):
        self.rpm = to_add / self.counts_per_rev * apb_freq
        self.counts += to_add

    def tock(self):
        revs = self.ideal_rpm * self.rpm_skew * self.counts_per_rev / apb_freq
        self.set_counts(revs)


def run_sim(step_count=100):
    duty_cycle = lambda x: int(x / 500 * 65535)
    m = Motor(duty_cycle=duty_cycle(250), rpm_skew=0.5, target_rpm=250)

    times = []
    errors = []
    rpm = []
    step = 1
    while True:
        m.tock()

        t = step  # time.perf_counter()
        times.append(t)
        e = m.target_rpm - m.rpm
        errors.append(e)

        k_u = 1.595

        # proportional
        k_p = 0.7 * k_u
        p_out = k_p * e

        t_u = 1.6325

        # integral
        k_i = 0.4 * t_u
        e_sum = np.trapz(errors, times)
        i_out = k_i * e_sum

        # derivative
        t_d = 0.125 * t_u
        d_e = e - (errors[-2] if len(errors) > 1 else 0)
        d_t = t - (times[-2] if len(times) > 1 else 0)
        slope = d_e / d_t
        d_out = t_d * slope

        pid = p_out + i_out + d_out
        m.duty_cycle = duty_cycle(m.ideal_rpm + pid)
        # print(f'm1 current rpm:{m.rpm}, ideal:{m.ideal_rpm}')
        rpm.append(m.rpm)
        if step >= step_count:
            return rpm, errors, times
        step += 1


def main():
    maxes = []
    rpm, errors, times = run_sim(100)
    maxes.append(np.max(errors))
    plt.plot(times, rpm, label=f'rpm')
    plt.show()


if __name__ == '__main__':
    main()
