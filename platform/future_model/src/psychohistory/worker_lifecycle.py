"""POSIX controls for trusted fixed workers; this is not a hostile-code sandbox."""
import os
import platform
import signal
import threading
import time


def require_parent(expected_parent):
    """Never compute or publish after kernel reparenting of this worker."""
    if os.getppid() != expected_parent:
        os.killpg(os.getpgrp(), signal.SIGKILL)


def _require_session():
    if os.getpgrp() != os.getpid() or os.getsid(0) != os.getpid():
        raise ValueError('Worker must own its POSIX session and process group')


def watch_parent(expected_parent):
    """Kernel PPID changes on owner death on both Linux and macOS."""
    _require_session()
    require_parent(expected_parent)

    def watch():
        while True:
            require_parent(expected_parent)
            time.sleep(.01)

    threading.Thread(target=watch, name='worker-parent-watch', daemon=True).start()


def watch_cpu(hard_seconds):
    """Bound this trusted process's measured CPU, independently of SIGXCPU handling.

    Darwin's configured RLIMIT_CPU hard limit is not a demonstrated SIGKILL
    guarantee. The fixed Python mechanisms yield the GIL, allowing this watchdog
    to enforce the deadline against the native process CPU clock. It is not a
    kernel guarantee for arbitrary extensions that hold the GIL indefinitely.
    """
    _require_session()

    def watch():
        while time.process_time() < hard_seconds:
            time.sleep(.01)
        os.killpg(os.getpgrp(), signal.SIGKILL)

    threading.Thread(target=watch, name='worker-cpu-watch', daemon=True).start()


def configure_worker(expected_parent, *, memory_mb=512, cpu_seconds=5, establish_session=False):
    if establish_session:
        os.setsid()
    _require_session()
    # SIGTERM from parent cancellation or Linux PDEATHSIG must cover descendants.
    signal.signal(signal.SIGTERM, lambda *_: os.killpg(os.getpgrp(), signal.SIGKILL))
    limits = {'memory': 'NOT_ENFORCED', 'cpu': 'NOT_ENFORCED',
              'parent_death': 'PPID_WATCHDOG_KILLPG', 'process_group': 'OWNED_SESSION',
              'hostile_code_sandbox': False}
    if platform.system() == 'Linux':
        import ctypes
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), 'Cannot install parent-death guard')
        limits['parent_death'] = 'PR_SET_PDEATHSIG'
    require_parent(expected_parent)  # Closes death-before-guard installation race.
    import resource
    # Keep native POSIX limits configured; Darwin needs an independent hard cap.
    if platform.system() in {'Linux', 'Darwin'}:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds + 1))
        limits.update(cpu='RLIMIT_CPU', cpu_soft_seconds=cpu_seconds,
                      cpu_hard_seconds=cpu_seconds + 1)
    if platform.system() == 'Linux':
        resource.setrlimit(resource.RLIMIT_AS, (memory_mb * 1024**2,) * 2)
        limits['memory'] = 'RLIMIT_AS'
    if platform.system() == 'Darwin':
        signal.signal(signal.SIGXCPU, lambda *_: os.killpg(os.getpgrp(), signal.SIGKILL))
        watch_cpu(cpu_seconds + 1)
        limits.update(cpu='DARWIN_PROCESS_CPU_WATCHDOG',
                      cpu_kernel_limit='RLIMIT_CPU_CONFIGURED_ONLY',
                      cpu_watchdog_clock='time.process_time',
                      cpu_soft_action='SIGXCPU_KILLPG',
                      cpu_hard_action='PROCESS_CPU_WATCHDOG_KILLPG')
    watch_parent(expected_parent)
    return limits


def terminate_owned_group(process, sig):
    """Signal only our still-unreaped subprocess's verified session, never a saved PID."""
    if process.poll() is not None:
        return
    try:
        if os.getpgid(process.pid) != process.pid or os.getsid(process.pid) != process.pid:
            raise ValueError('Refusing to signal a process without its own session')
        os.killpg(process.pid, sig)
    except ProcessLookupError:
        pass
