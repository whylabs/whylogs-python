import atexit
import logging
import os

_logger = logging.getLogger(__name__)

# Store the list of child process IDs
_child_pids = []

disabled = os.environ.get("WHYLOGS_NO_ASYNC")


def async_wrap(func, *args, **kwargs):
    """
    Wraps around expensive IO operation using os.fork()

    Because our operations are read-only, this should be relatively cheap as we can take advantage of
    copy-on-write for objects in memory. Note that the child inherits all the file opener such stdin/out and
    loggers.

    Args:
        func: the function to execute
        *args: the arguments to pass on to the function
        **kwargs: the **kwargs to pass on
    """
    if disabled:
        _logger.debug('WHYLOGS_NO_ASYNC is set. Execute function inline')
        func(*args, **kwargs)
        return

    child_pid = os.fork()
    _child_pids.append(child_pid)

    if child_pid == 0:
        atexit.unregister(_wait_for_children)
        _logger.info('Start executing the function inside the child process')
        try:
            func(*args, **kwargs)
        except:  # noqa
            _logger.exception('Failure during background execution')
        _logger.debug('Child process completed')
    else:
        _logger.info(f'Child process started. ID: {child_pid}')


@atexit.register
def _wait_for_children():
    """
    Wait for the child process to complete. This is to ensure that we write out the log files before the parent
    process finishes
    """
    _logger.debug(f'Waiting for children: {_child_pids}')
    for child_pid in _child_pids:
        try:
            os.waitpid(child_pid, 0)
            _logger.debug(f'Child process completed successfully: {child_pid}')
        except ChildProcessError as e:
            if e.errno == 10:
                _logger.warning(f'Child process with pid {child_pid} not found')
            else:
                _logger.exception(f'Failed to wait for process id {child_pid}')
