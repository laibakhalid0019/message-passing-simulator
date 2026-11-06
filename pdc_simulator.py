"""
PDC Assignment 3 - Message-Passing Simulator
Hard-coded inputs from Questions 2-5.
Run: python pdc_simulator.py
"""

from math import log2

# Each process executes its own list from top to bottom.
# S = send to destination; R = receive from source.
FRAGMENTS = {
    "A": {
        0: [("S", 1), ("R", 1)],
        1: [("S", 0), ("R", 0)],
    },
    "B": {
        0: [("R", 1), ("S", 1)],
        1: [("R", 0), ("S", 0)],
    },
    "C": {
        0: [("S", 1), ("R", 2)],
        1: [("S", 2), ("R", 0)],
        2: [("S", 0), ("R", 1)],
    },
    "D": {
        0: [("R", 2), ("S", 1)],
        1: [("R", 0), ("S", 2)],
        2: [("R", 1), ("S", 0)],
    },
}

# Q3
SCENARIOS = {
    "send first": (2, 9),
    "together": (5, 5),
    "receive first": (8, 3),
}
L = 4
COPY_TIME = 1

# Q4
N_Q4 = 512
P_VALUES = [4, 16, 64]

# Q5
TS_Q5 = 400
Q5_RUNS = {2: 220, 4: 136, 8: 102.5}


def op_name(pid, op):
    kind, peer = op
    if kind == "S":
        return f"P{pid}: send -> P{peer}"
    return f"P{pid}: receive <- P{peer}"


def simulate_fragment(fragment, buffered):
    """Event-driven simulation for blocking rendezvous/buffered messaging."""
    pc = {pid: 0 for pid in fragment}
    pending_sends = {}       # (sender, receiver) -> operation waiting
    completed_messages = set()
    completed = []
    total_ops = sum(len(ops) for ops in fragment.values())

    # At most total_ops operations can complete. Iterate until no progress.
    while len(completed) < total_ops:
        progress = False

        # Process currently enabled operations in stable process-ID order.
        for pid in sorted(fragment):
            if pc[pid] >= len(fragment[pid]):
                continue

            kind, peer = fragment[pid][pc[pid]]
            key = (pid, peer)

            if kind == "S":
                if buffered:
                    # Unlimited buffering: send completes as soon as posted.
                    completed.append(op_name(pid, (kind, peer)))
                    completed_messages.add((pid, peer))
                    pc[pid] += 1
                    progress = True
                else:
                    # A non-buffered send completes only when its receive is posted.
                    pending_sends[key] = True
                    if (peer, pid) in waiting_receives:
                        # Matching receive was already waiting.
                        completed.append(op_name(peer, ("R", pid)))
                        completed.append(op_name(pid, ("S", peer)))
                        waiting_receives.remove((peer, pid))
                        pc[peer] += 1
                        pc[pid] += 1
                        pending_sends.pop(key, None)
                    else:
                        # The send remains blocked at this operation.
                        pass

            else:  # receive
                msg_key = (peer, pid)
                if buffered:
                    if msg_key in completed_messages:
                        completed.append(op_name(pid, (kind, peer)))
                        pc[pid] += 1
                        progress = True
                    else:
                        # Receive waits until matching send has completed.
                        waiting_receives.add((pid, peer))
                else:
                    if msg_key in pending_sends:
                        completed.append(op_name(pid, (kind, peer)))
                        completed.append(op_name(peer, ("S", pid)))
                        pending_sends.pop(msg_key, None)
                        pc[pid] += 1
                        pc[peer] += 1
                        progress = True
                    else:
                        waiting_receives.add((pid, peer))

            # Keep looping when rendezvous advances two processes.
        if not progress:
            break

    stuck = {}
    for pid in sorted(fragment):
        if pc[pid] < len(fragment[pid]):
            op = fragment[pid][pc[pid]]
            stuck[pid] = op_name(pid, op)

    deadlock = bool(stuck)
    return {
        "deadlock": deadlock,
        "stuck": stuck,
        "completed": completed,
    }


def run_fragment(fragment, buffered):
    # Each run needs its own receive-wait set.
    global waiting_receives
    waiting_receives = set()
    return simulate_fragment(fragment, buffered)


def reverse_process_one(fragment):
    """Bonus fix: reverse P1's two operations, when P1 exists."""
    changed = {pid: list(ops) for pid, ops in fragment.items()}
    if 1 in changed and len(changed[1]) == 2:
        changed[1] = list(reversed(changed[1]))
    return changed


def print_q2():
    print("=" * 72)
    print("Q2 - MESSAGE-PASSING FRAGMENTS")
    for name, fragment in FRAGMENTS.items():
        print(f"\nFragment {name}")
        for buffered, label in [(False, "Non-buffered"), (True, "Buffered")]:
            result = run_fragment(fragment, buffered)
            print(f"  {label}: {'DEADLOCK' if result['deadlock'] else 'NO DEADLOCK'}")
            if result["stuck"]:
                for pid, operation in result["stuck"].items():
                    print(f"    P{pid} waits at: {operation}")
            else:
                print("    Completed operations:")
                for item in result["completed"]:
                    print(f"      {item}")

    # Bonus: A is a fragment that deadlocks only without buffering.
    print("\nBONUS - Fix Fragment A by reversing P1's operations")
    fixed = reverse_process_one(FRAGMENTS["A"])
    for buffered, label in [(False, "Non-buffered"), (True, "Buffered")]:
        result = run_fragment(fixed, buffered)
        print(f"  {label}: {'DEADLOCK' if result['deadlock'] else 'NO DEADLOCK'}")
        if result["stuck"]:
            for pid, operation in result["stuck"].items():
                print(f"    P{pid} waits at: {operation}")
        else:
            for item in result["completed"]:
                print(f"    {item}")


def print_q3():
    print("\n" + "=" * 72)
    print("Q3 - IDLING OVERHEAD AND BUFFERED TRANSFERS")
    print(f"L = {L}, copy time c = {COPY_TIME}")
    print("\nNon-buffered blocking:")
    print(f"{'Scenario':<16}{'Sender idle':>14}{'Receiver idle':>16}{'Complete':>13}")
    for name, (ts, tr) in SCENARIOS.items():
        sender_idle = max(0, tr - ts)
        receiver_idle = max(0, ts - tr)
        complete = max(ts, tr) + L
        print(f"{name:<16}{sender_idle:>14}{receiver_idle:>16}{complete:>13}")

    print("\nBuffered blocking:")
    print(f"{'Scenario':<16}{'Sender blocked':>16}{'Receiver idle':>15}{'Data available':>17}")
    for name, (ts, tr) in SCENARIOS.items():
        arrival = ts + COPY_TIME + L
        sender_blocked = COPY_TIME
        receiver_idle = max(0, arrival - tr)
        available = max(arrival, tr) + COPY_TIME
        print(f"{name:<16}{sender_blocked:>16}{receiver_idle:>15}{available:>17}")


def q4_metrics(n, p):
    tp = n / p + 2 * log2(p)
    speedup = n / tp
    efficiency = speedup / p
    cost = p * tp
    overhead = cost - n
    return tp, speedup, efficiency, cost, overhead


def print_q4():
    print("\n" + "=" * 72)
    print("Q4 - ADDING N NUMBERS")
    print(f"{'p':>5}{'Tp':>12}{'Speedup':>12}{'Efficiency':>13}{'Cost':>12}{'Overhead':>12}")
    for p in P_VALUES:
        tp, s, e, cost, overhead = q4_metrics(N_Q4, p)
        print(f"{p:>5}{tp:>12.3f}{s:>12.3f}{e:>13.3f}{cost:>12.3f}{overhead:>12.3f}")

    e_at_16 = q4_metrics(N_Q4, 16)[2]
    n_at_64 = (2 * e_at_16 / (1 - e_at_16)) * 64 * log2(64)
    print(f"\nEfficiency at p=16: {e_at_16:.3f}")
    print(f"Problem size at p=64 for same efficiency: n = {n_at_64:.0f}")
    print("Isoefficiency: n = Theta(p log p)")


def print_q5():
    print("\n" + "=" * 72)
    print("Q5 - SERIAL FRACTION")
    print(f"{'p':>5}{'Tp (s)':>12}{'Speedup':>12}{'Efficiency':>13}{'Serial f':>12}")
    f_values = {}
    for p, tp in Q5_RUNS.items():
        speedup = TS_Q5 / tp
        efficiency = speedup / p
        f = (p / speedup - 1) / (p - 1)
        f_values[p] = f
        print(f"{p:>5}{tp:>12.3f}{speedup:>12.3f}{efficiency:>13.3f}{f:>12.3f}")

    f8 = f_values[8]
    max_speedup = 1 / f8
    predicted_32 = 1 / (f8 + (1 - f8) / 32)
    print(f"\nUsing f at p=8 ({f8:.3f}):")
    print(f"Maximum speedup as p -> infinity: {max_speedup:.3f}")
    print(f"Predicted speedup at p=32: {predicted_32:.3f}")


def main():
    print("PDC ASSIGNMENT 3 - MESSAGE-PASSING SIMULATOR")
    print_q2()
    print_q3()
    print_q4()
    print_q5()


if __name__ == "__main__":
    main()
