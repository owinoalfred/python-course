"""Module 5 — Error Handling and Debugging (topics 5.1 - 5.6)."""

from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from self_created_tools.topic_builder import make_topic_data

TOPICS = [
    make_topic_data(
        topic_id="5.1", title="Exceptions vs Errors", module=5, module_title="Error Handling and Debugging",
        directory="01_exceptions_vs_errors", summary="Syntax errors vs runtime exceptions, CPython exception hierarchy, and traceback analysis.",
        why_it_matters="Distinguishing syntax errors from runtime exceptions is vital for system reliability.",
        objectives=["Identify syntax vs runtime errors.", "Understand the Exception hierarchy.", "Parse tracebacks."],
        prerequisites=["Module 4 Functions and Modules"], domain="patient-care robot monitoring", concepts=["Exceptions", "Errors", "Tracebacks"],
        code_snippets={
            "syntax": "try:\n    1 / 0\nexcept ZeroDivisionError:\n    pass", "basic": "try:\n    val = int('invalid')\nexcept ValueError as e:\n    print(e)",
            "intermediate": "import traceback\ntry:\n    raise KeyError('missing')\nexcept Exception as e:\n    traceback.print_exc()",
            "advanced": "def safe_eval(expr):\n    try:\n        return eval(expr)\n    except Exception as e:\n        return str(e)",
            "walkthrough": "try:\n    res = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f'Handled division error: {e}')",
            "pythonic": "try:\n    val = d['key']\nexcept KeyError:\n    val = None", "engineering": "def parse_sensor_reading(raw):\n    try:\n        return float(raw)\n    except (ValueError, TypeError):\n        return None",
            "m1_code": "def solve_m1(s):\n    try:\n        return int(s)\n    except ValueError:\n        return None", "m1_test": "assert solve_m1('123') == 123 and solve_m1('abc') is None",
            "m2_code": "def solve_m2(lst, idx):\n    try:\n        return lst[idx]\n    except IndexError:\n        return None", "m2_test": "assert solve_m2([1], 0) == 1 and solve_m2([1], 5) is None",
            "m3_code": "def solve_m3(d, key):\n    try:\n        return d[key]\n    except KeyError:\n        return None", "m3_test": "assert solve_m3({'a': 1}, 'a') == 1 and solve_m3({}, 'b') is None",
            "m4_code": "def solve_m4(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return 0.0", "m4_test": "assert solve_m4(10, 2) == 5.0 and solve_m4(10, 0) == 0.0",
            "m5_code": "def solve_m5(val):\n    try:\n        return len(val)\n    except TypeError:\n        return -1", "m5_test": "assert solve_m5([1, 2]) == 2 and solve_m5(123) == -1",
            "h1_code": "def solve_h1(expr):\n    try:\n        return eval(expr, {\"__builtins__\": {}})\n    except Exception as e:\n        return type(e).__name__", "h1_test": "assert solve_h1('1 / 0') == 'ZeroDivisionError'",
            "h2_code": "def solve_h2(fn, *args):\n    try:\n        return True, fn(*args)\n    except Exception as e:\n        return False, str(e)", "h2_test": "assert solve_h2(lambda x: x+1, 2)[0] is True",
            "h3_code": "def solve_h3(exc_obj):\n    return issubclass(type(exc_obj), Exception)", "h3_test": "assert solve_h3(ValueError('err')) is True",
            "h4_code": "def solve_h4(data_list):\n    success, errors = [], []\n    for item in data_list:\n        try:\n            success.append(int(item))\n        except Exception as e:\n            errors.append((item, type(e).__name__))\n    return success, errors", "h4_test": "assert solve_h4(['1', 'a'])[0] == [1]",
            "h5_code": "def solve_h5(fn, *args):\n    import sys\n    try:\n        fn(*args)\n        return None\n    except Exception:\n        return sys.exc_info()[0].__name__", "h5_test": "assert solve_h5(lambda: 1/0) == 'ZeroDivisionError'",
            "rob_code": "def process_telemetry(data):\n    try:\n        val = float(data[0]) if data else 0.0\n        return {'status': 'OK', 'val': val}\n    except Exception as e:\n        return {'status': 'ERROR', 'msg': str(e)}", "rob_test": "assert process_telemetry(['10.5'])['status'] == 'OK'"
        }
    ),
    make_topic_data(
        topic_id="5.2", title="Exception Handling", module=5, module_title="Error Handling and Debugging",
        directory="02_exception_handling", summary="try, except, else, finally blocks and exception chaining.",
        why_it_matters="finally blocks guarantee resource cleanup regardless of execution success or error.",
        objectives=["Construct try-except-else-finally blocks.", "Avoid bare except clauses.", "Clean up system resources in finally."],
        prerequisites=["Topic 5.1 Exceptions vs Errors"], domain="patient-care robot monitoring", concepts=["try", "except", "finally", "else"],
        code_snippets={
            "syntax": "try:\n    pass\nexcept Exception:\n    pass\nelse:\n    pass\nfinally:\n    pass", "basic": "try:\n    res = 10 / 2\nexcept ZeroDivisionError:\n    print('Error')\nelse:\n    print('Success:', res)",
            "intermediate": "f = None\ntry:\n    f = open('data.txt', 'w')\n    f.write('test')\nfinally:\n    if f: f.close()", "advanced": "try:\n    1 / 0\nexcept ZeroDivisionError as e:\n    raise RuntimeError('Division failed') from e",
            "walkthrough": "state = 'INIT'\ntry:\n    state = 'RUNNING'\n    res = 100 / 5\nexcept Exception:\n    state = 'ERROR'\nelse:\n    state = 'COMPLETED'\nfinally:\n    print(f'Final state: {state}')",
            "pythonic": "with open('file.txt', 'w') as f:\n    f.write('data')", "engineering": "def execute_transaction(action_fn, cleanup_fn):\n    try:\n        return action_fn()\n    except Exception as e:\n        raise\n    finally:\n        cleanup_fn()",
            "m1_code": "def solve_m1(a, b):\n    try:\n        res = a / b\n    except ZeroDivisionError:\n        return 'DIV_ZERO'\n    else:\n        return res", "m1_test": "assert solve_m1(10, 2) == 5.0 and solve_m1(1, 0) == 'DIV_ZERO'",
            "m2_code": "def solve_m2(fn):\n    cleaned = False\n    try:\n        fn()\n    finally:\n        cleaned = True\n    return cleaned", "m2_test": "assert solve_m2(lambda: None) is True",
            "m3_code": "def solve_m3(d, k, default):\n    try:\n        return d[k]\n    except KeyError:\n        return default", "m3_test": "assert solve_m3({'a': 1}, 'a', 0) == 1",
            "m4_code": "def solve_m4(a, b):\n    try:\n        res = a + b\n    except TypeError:\n        res = None\n    finally:\n        pass\n    return res", "m4_test": "assert solve_m4(1, '2') is None",
            "m5_code": "def solve_m5(items):\n    try:\n        return items[0]\n    except IndexError:\n        return 'EMPTY'", "m5_test": "assert solve_m5([]) == 'EMPTY'",
            "h1_code": "def solve_h1(fn, fallback_fn):\n    try:\n        return fn()\n    except Exception:\n        return fallback_fn()", "h1_test": "assert solve_h1(lambda: 1/0, lambda: 'fallback') == 'fallback'",
            "h2_code": "def solve_h2(fn):\n    try:\n        fn()\n        return 'SUCCESS'\n    except ValueError:\n        return 'VALUE_ERROR'\n    except TypeError:\n        return 'TYPE_ERROR'\n    except Exception:\n        return 'OTHER_ERROR'", "h2_test": "assert solve_h2(lambda: int('x')) == 'VALUE_ERROR'",
            "h3_code": "def solve_h3(fn):\n    try:\n        fn()\n    except Exception as e:\n        raise RuntimeError('Wrapped') from e", "h3_test": "try: solve_h3(lambda: 1/0)\nexcept RuntimeError as e: assert e.__cause__ is not None",
            "h4_code": "def solve_h4(tasks):\n    results = []\n    for task in tasks:\n        try:\n            results.append((True, task()))\n        except Exception as e:\n            results.append((False, str(e)))\n    return results", "h4_test": "assert solve_h4([lambda: 1])[0] == (True, 1)",
            "h5_code": "def solve_h5(actions, cleanup):\n    log = []\n    try:\n        for a in actions:\n            a()\n            log.append('ACTION')\n    finally:\n        cleanup()\n        log.append('CLEANUP')\n    return log", "h5_test": "assert solve_h5([lambda: None], lambda: None) == ['ACTION', 'CLEANUP']",
            "rob_code": "def process_telemetry(data):\n    status = 'FAIL'\n    try:\n        val = data[0]\n        status = 'OK'\n    except Exception:\n        status = 'ERROR'\n    finally:\n        pass\n    return {'status': status}", "rob_test": "assert process_telemetry([1])['status'] == 'OK'"
        }
    ),
    make_topic_data(
        topic_id="5.3", title="Advanced Exception Handling", module=5, module_title="Error Handling and Debugging",
        directory="03_advanced_exception_handling", summary="Exception groups (Python 3.11+), except*, raising exceptions with context, and suppression.",
        why_it_matters="Exception groups handle concurrent or batched errors in modern Python.",
        objectives=["Work with ExceptionGroup and except*.", "Suppress non-critical exceptions cleanly.", "Chain error contexts."],
        prerequisites=["Topic 5.2 Exception Handling"], domain="patient-care robot monitoring", concepts=["ExceptionGroup", "except*", "suppress"],
        code_snippets={
            "syntax": "from contextlib import suppress\nwith suppress(FileNotFoundError):\n    pass", "basic": "eg = ExceptionGroup('batch', [ValueError('a'), TypeError('b')])\nprint(len(eg.exceptions))",
            "intermediate": "from contextlib import suppress\nwith suppress(ZeroDivisionError):\n    x = 1 / 0", "advanced": "try:\n    raise ExceptionGroup('concurrent', [ValueError(1), KeyError(2)])\nexcept* ValueError as e:\n    print('Caught value errors')\nexcept* KeyError as e:\n    print('Caught key errors')",
            "walkthrough": "from contextlib import suppress\nd = {'a': 1}\nwith suppress(KeyError):\n    del d['b']\nprint('Done suppressing missing key removal')",
            "pythonic": "with suppress(ValueError):\n    val = int('not_a_num')", "engineering": "def execute_concurrent_tasks(task_list):\n    errors = []\n    for task in task_list:\n        try:\n            task()\n        except Exception as e:\n            errors.append(e)\n    if errors:\n        raise ExceptionGroup('Batch task failures', errors)",
            "m1_code": "def solve_m1(d, key):\n    from contextlib import suppress\n    with suppress(KeyError):\n        del d[key]\n    return d", "m1_test": "assert solve_m1({'a': 1}, 'b') == {'a': 1}",
            "m2_code": "def solve_m2(errs):\n    return ExceptionGroup('group', errs)", "m2_test": "eg = solve_m2([ValueError('a')]); assert len(eg.exceptions) == 1",
            "m3_code": "def solve_m3(val_str):\n    from contextlib import suppress\n    res = None\n    with suppress(ValueError):\n        res = int(val_str)\n    return res", "m3_test": "assert solve_m3('42') == 42 and solve_m3('x') is None",
            "m4_code": "def solve_m4(eg):\n    return [type(e).__name__ for e in eg.exceptions]", "m4_test": "eg = ExceptionGroup('g', [ValueError('a')]); assert solve_m4(eg) == ['ValueError']",
            "m5_code": "def solve_m5(fn):\n    from contextlib import suppress\n    with suppress(Exception):\n        fn()\n    return True", "m5_test": "assert solve_m5(lambda: 1/0) is True",
            "h1_code": "def solve_h1(tasks):\n    errs = []\n    for t in tasks:\n        try:\n            t()\n        except Exception as e:\n            errs.append(e)\n    if errs:\n        return ExceptionGroup('Task errors', errs)\n    return None", "h1_test": "assert solve_h1([lambda: 1/0]) is not None",
            "h2_code": "def solve_h2(fn, exc_type):\n    from contextlib import suppress\n    with suppress(exc_type):\n        return fn()\n    return None", "h2_test": "assert solve_h2(lambda: int('a'), ValueError) is None",
            "h3_code": "def solve_h3(eg, target_type):\n    matching = [e for e in eg.exceptions if isinstance(e, target_type)]\n    return matching", "h3_test": "eg = ExceptionGroup('g', [ValueError('a'), TypeError('b')]); assert len(solve_h3(eg, ValueError)) == 1",
            "h4_code": "def solve_h4(fn):\n    try:\n        fn()\n    except Exception as e:\n        return getattr(e, '__notes__', [])\n    return []", "h4_test": "def f(): e = ValueError('a'); e.add_note('note'); raise e\nassert solve_h4(f) == ['note']",
            "h5_code": "def solve_h5(fn):\n    try:\n        fn()\n        return None\n    except Exception as e:\n        return type(e).__name__", "h5_test": "assert solve_h5(lambda: 1/0) == 'ZeroDivisionError'",
            "rob_code": "def process_telemetry(data):\n    from contextlib import suppress\n    val = 0.0\n    with suppress(Exception):\n        val = float(data[0])\n    return {'val': val}", "rob_test": "assert process_telemetry(['invalid'])['val'] == 0.0"
        }
    ),
    make_topic_data(
        topic_id="5.4", title="Custom Exceptions", module=5, module_title="Error Handling and Debugging",
        directory="04_custom_exceptions", summary="Inheriting from Exception, designing exception hierarchies, and domain-specific attributes.",
        why_it_matters="Custom exception classes convey domain-specific failure contexts.",
        objectives=["Derive custom exceptions from Exception.", "Design domain exception hierarchies.", "Attach contextual metadata to errors."],
        prerequisites=["Topic 5.3 Advanced Exceptions"], domain="patient-care robot monitoring", concepts=["Custom Exceptions", "Inheritance"],
        code_snippets={
            "syntax": "class RobotError(Exception):\n    pass", "basic": "class SensorFault(Exception):\n    def __init__(self, sensor_id):\n        super().__init__(f'Sensor {sensor_id} failed')\n        self.sensor_id = sensor_id",
            "intermediate": "class SafetyViolationError(RobotError):\n    def __init__(self, zone):\n        self.zone = zone", "advanced": "class BatteryDepletedError(RobotError):\n    pass",
            "walkthrough": "class RobotFault(Exception):\n    def __init__(self, code, msg):\n        self.code = code\n        super().__init__(f'[{code}] {msg}')\ntry:\n    raise RobotFault(101, 'Motor stall')\nexcept RobotFault as e:\n    print(f'Caught code {e.code}: {e}')",
            "pythonic": "class DomainError(Exception): '''Base domain error'''", "engineering": "class RobotSafetyError(Exception):\n    def __init__(self, message, sensor_readings):\n        super().__init__(message)\n        self.readings = sensor_readings",
            "m1_code": "class CustomErr(Exception): pass\ndef solve_m1(): raise CustomErr('test')", "m1_test": "try: solve_m1()\nexcept Exception as e: assert type(e).__name__ == 'CustomErr'",
            "m2_code": "class ValueErr(Exception):\n    def __init__(self, code):\n        self.code = code\ndef solve_m2(): return ValueErr(404).code", "m2_test": "assert solve_m2() == 404",
            "m3_code": "class Base(Exception): pass\nclass Sub(Base): pass\ndef solve_m3(): return issubclass(Sub, Base)", "m3_test": "assert solve_m3() is True",
            "m4_code": "class Fault(Exception): pass\ndef solve_m4(flag):\n    if flag:\n        raise Fault('fault')\n    return 'OK'", "m4_test": "assert solve_m4(False) == 'OK'",
            "m5_code": "class CustomMsg(Exception):\n    def __str__(self): return 'CUSTOM_STRING'\ndef solve_m5(): return str(CustomMsg())", "m5_test": "assert solve_m5() == 'CUSTOM_STRING'",
            "h1_code": "class RobotBaseError(Exception): pass\nclass SensorError(RobotBaseError): pass\nclass ActuatorError(RobotBaseError): pass\ndef solve_h1(err_type):\n    if err_type == 'sensor': raise SensorError('s')\n    if err_type == 'actuator': raise ActuatorError('a')\n    return 'OK'", "h1_test": "try: solve_h1('sensor')\nexcept RobotBaseError: pass",
            "h2_code": "class DetailedError(Exception):\n    def __init__(self, msg, context_dict):\n        super().__init__(msg)\n        self.context = context_dict\ndef solve_h2(): err = DetailedError('fail', {'id': 1}); return err.context", "h2_test": "assert solve_h2() == {'id': 1}",
            "h3_code": "class RetryableError(Exception):\n    def __init__(self, retries_left): self.retries = retries_left\ndef solve_h3(r):\n    if r > 0: raise RetryableError(r - 1)\n    return 'DONE'", "h3_test": "try: solve_h3(3)\nexcept RetryableError as e: assert e.retries == 2",
            "h4_code": "class CustomExc(Exception): pass\ndef solve_h4(fn):\n    try:\n        fn()\n    except CustomExc as e:\n        return True\n    return False", "h4_test": "class LocalErr(CustomExc): pass\nassert solve_h4(lambda: (_ for _ in ()).throw(LocalErr())) is True",
            "h5_code": "class AppError(Exception):\n    def to_dict(self): return {'error': str(self)}\ndef solve_h5(): return AppError('msg').to_dict()", "h5_test": "assert solve_h5() == {'error': 'msg'}",
            "rob_code": "class TelemetryError(Exception): pass\ndef process_telemetry(data):\n    if not data:\n        raise TelemetryError('Empty telemetry')\n    return {'status': 'OK'}", "rob_test": "try: process_telemetry([])\nexcept TelemetryError: pass"
        }
    ),
    make_topic_data(
        topic_id="5.5", title="Debugging Techniques", module=5, module_title="Error Handling and Debugging",
        directory="05_debugging_techniques", summary="pdb, breakpoint(), inspection methods, and post-mortem analysis.",
        why_it_matters="Systematic debugging skills reduce mean time to resolution.",
        objectives=["Use breakpoint() for interactive debugging.", "Inspect runtime scope using dir(), vars(), and type().", "Perform post-mortem stack inspection."],
        prerequisites=["Topic 5.4 Custom Exceptions"], domain="patient-care robot monitoring", concepts=["pdb", "breakpoint()", "Inspection"],
        code_snippets={
            "syntax": "breakpoint()  # Drops into pdb", "basic": "x = 10\n# breakpoint()\ny = x * 2",
            "intermediate": "import pdb\ndef debug_me(val):\n    # pdb.set_trace()\n    return val * 2", "advanced": "import sys, traceback\ndef handle_uncaught():\n    extype, value, tb = sys.exc_info()\n    traceback.print_tb(tb)",
            "walkthrough": "data = {'x': 10, 'y': 20}\n# Inspect keys and types\nprint('Keys:', list(data.keys()))\nprint('Types:', {k: type(v).__name__ for k, v in data.items()})",
            "pythonic": "print(f'{x=}, {y=}')", "engineering": "def inspect_object(obj):\n    return {'type': type(obj).__name__, 'methods': [m for m in dir(obj) if not m.startswith('_')]}",
            "m1_code": "def solve_m1(obj):\n    return type(obj).__name__", "m1_test": "assert solve_m1(123) == 'int'",
            "m2_code": "def solve_m2(obj):\n    return [attr for attr in dir(obj) if not attr.startswith('_')]", "m2_test": "assert isinstance(solve_m2([]), list)",
            "m3_code": "def solve_m3(obj):\n    try:\n        return vars(obj)\n    except TypeError:\n        return {}", "m3_test": "class Dummy: pass\nd = Dummy(); d.a = 1; assert solve_m3(d) == {'a': 1}",
            "m4_code": "def solve_m4(obj, attr_name):\n    return hasattr(obj, attr_name)", "m4_test": "assert solve_m4('test', 'upper') is True",
            "m5_code": "def solve_m5(obj, attr_name, default_val):\n    return getattr(obj, attr_name, default_val)", "m5_test": "assert solve_m5('test', 'missing', 'default') == 'default'",
            "h1_code": "def solve_h1(fn, *args):\n    import sys, io\n    old_stdout = sys.stdout\n    sys.stdout = io.StringIO()\n    try:\n        fn(*args)\n        return sys.stdout.getvalue()\n    finally:\n        sys.stdout = old_stdout", "h1_test": "assert solve_h1(print, 'hello').strip() == 'hello'",
            "h2_code": "def solve_h2(fn):\n    import traceback\n    try:\n        fn()\n        return ''\n    except Exception as e:\n        return traceback.format_exc()", "h2_test": "assert 'ZeroDivisionError' in solve_h2(lambda: 1/0)",
            "h3_code": "def solve_h3(obj):\n    res = {}\n    for attr in dir(obj):\n        if not attr.startswith('_'):\n            val = getattr(obj, attr)\n            if not callable(val):\n                res[attr] = val\n    return res", "h3_test": "class Robot: speed = 1.5\nassert solve_h3(Robot) == {'speed': 1.5}",
            "h4_code": "def solve_h4(stack_depth):\n    import inspect\n    return len(inspect.stack()) >= stack_depth", "h4_test": "assert solve_h4(1) is True",
            "h5_code": "def solve_h5(var_map):\n    return '\\n'.join(f'{k}={v!r} ({type(v).__name__})' for k, v in sorted(var_map.items()))", "h5_test": "assert 'x=10 (int)' in solve_h5({'x': 10})",
            "rob_code": "def process_telemetry(data):\n    diag = {'len': len(data), 'type': type(data).__name__}\n    return {'diagnostics': diag}", "rob_test": "assert process_telemetry([1])['diagnostics']['len'] == 1"
        }
    ),
    make_topic_data(
        topic_id="5.6", title="Introduction to Logging", module=5, module_title="Error Handling and Debugging",
        directory="06_intro_to_logging", summary="logging module, log levels, formatters, handlers, and configuration.",
        why_it_matters="Logging replaces ephemeral print statements with structured runtime audit trails.",
        objectives=["Configure logging with logging.basicConfig().", "Use log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).", "Add custom formatters and handlers."],
        prerequisites=["Topic 5.5 Debugging Techniques"], domain="patient-care robot monitoring", concepts=["logging", "LogLevels", "Handlers"],
        code_snippets={
            "syntax": "import logging\nlogging.basicConfig(level=logging.INFO)\nlogging.info('Ready')", "basic": "import logging\nlogger = logging.getLogger('robot')\nlogger.info('System online')",
            "intermediate": "import logging\nlogging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')",
            "advanced": "import logging\nhandler = logging.StreamHandler()\nhandler.setFormatter(logging.Formatter('%(name)s: %(message)s'))",
            "walkthrough": "import logging\nlogger = logging.getLogger('telemetry')\nlogger.setLevel(logging.INFO)\nlogger.info('Telemetry feed active')",
            "pythonic": "import logging\nlogger = logging.getLogger(__name__)", "engineering": "import logging\ndef setup_robot_logger(name, log_file):\n    logger = logging.getLogger(name)\n    logger.setLevel(logging.DEBUG)\n    handler = logging.FileHandler(log_file)\n    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))\n    logger.addHandler(handler)\n    return logger",
            "m1_code": "def solve_m1(level_name):\n    import logging\n    return getattr(logging, level_name.upper(), logging.INFO)", "m1_test": "import logging; assert solve_m1('debug') == logging.DEBUG",
            "m2_code": "def solve_m2(msg):\n    import logging, io\n    stream = io.StringIO()\n    handler = logging.StreamHandler(stream)\n    logger = logging.getLogger('m2')\n    logger.addHandler(handler)\n    logger.setLevel(logging.INFO)\n    logger.info(msg)\n    return stream.getvalue()", "m2_test": "assert 'test' in solve_m2('test')",
            "m3_code": "def solve_m3(logger_name):\n    import logging\n    return logging.getLogger(logger_name).name", "m3_test": "assert solve_m3('robot_log') == 'robot_log'",
            "m4_code": "def solve_m4(fmt_str):\n    import logging\n    return logging.Formatter(fmt_str)", "m4_test": "import logging; assert isinstance(solve_m4('%(message)s'), logging.Formatter)",
            "m5_code": "def solve_m5(log_dict):\n    import logging\n    return f'[{log_dict.get(\"level\", \"INFO\")}] {log_dict.get(\"msg\", \"\")}'", "m5_test": "assert solve_m5({'msg': 'hi'}) == '[INFO] hi'",
            "h1_code": "def solve_h1(name, level):\n    import logging\n    logger = logging.getLogger(name)\n    logger.setLevel(level)\n    return logger.level == level", "h1_test": "import logging; assert solve_h1('h1', logging.WARNING) is True",
            "h2_code": "def solve_h2(msg, level_str):\n    import logging, io\n    stream = io.StringIO()\n    handler = logging.StreamHandler(stream)\n    handler.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))\n    logger = logging.getLogger('h2')\n    logger.addHandler(handler)\n    logger.setLevel(logging.DEBUG)\n    getattr(logger, level_str.lower())(msg)\n    return stream.getvalue().strip()", "h2_test": "assert solve_h2('hello', 'info') == 'INFO:hello'",
            "h3_code": "def solve_h3(logger_name):\n    import logging\n    logger = logging.getLogger(logger_name)\n    return len(logger.handlers)", "h3_test": "import logging; assert isinstance(solve_h3('h3'), int)",
            "h4_code": "def solve_h4(logger_name):\n    import logging\n    logger = logging.getLogger(logger_name)\n    for h in list(logger.handlers):\n        logger.removeHandler(h)\n    return len(logger.handlers)", "h4_test": "assert solve_h4('h4') == 0",
            "h5_code": "def solve_h5(msg, extra_dict):\n    import logging, io\n    stream = io.StringIO()\n    handler = logging.StreamHandler(stream)\n    logger = logging.getLogger('h5')\n    logger.addHandler(handler)\n    logger.setLevel(logging.INFO)\n    logger.info(f'{msg} - {extra_dict}')\n    return stream.getvalue().strip()", "h5_test": "assert 'id' in solve_h5('status', {'id': 1})",
            "rob_code": "def process_telemetry(data):\n    import logging\n    logger = logging.getLogger('robo_telemetry')\n    logger.info(f'Processing {len(data)} items')\n    return {'status': 'LOGGED', 'count': len(data)}", "rob_test": "assert process_telemetry([1, 2])['status'] == 'LOGGED'"
        }
    )
]
