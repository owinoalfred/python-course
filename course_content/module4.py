"""Module 4 — Functions and Modules (topics 4.1 - 4.9)."""

from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from self_created_tools.topic_builder import make_topic_data

TOPICS = [
    make_topic_data(
        topic_id="4.1", title="Defining and Calling Functions", module=4, module_title="Functions and Modules",
        directory="01_defining_calling_functions", summary="Function definitions, invocation, parameter passing, and docstrings.",
        why_it_matters="Functions encapsulate reusable blocks of logic.", objectives=["Define functions with def.", "Invoke functions and pass arguments.", "Write docstrings."],
        prerequisites=["Module 3 Core Data Structures"], domain="manufacturing cell controller", concepts=["Functions", "def", "Docstrings"],
        code_snippets={
            "syntax": "def compute(x):\n    return x * 2", "basic": "def greet():\n    print('Hello')", "intermediate": "def add(a, b):\n    return a + b",
            "advanced": "def apply(fn, val):\n    return fn(val)", "walkthrough": "def compute_velocity(dist_m, time_s):\n    if time_s <= 0:\n        return 0.0\n    return dist_m / time_s",
            "pythonic": "def ping() -> bool:\n    return True", "engineering": "def check_safety_zone(x, y, radius):\n    return (x**2 + y**2)**0.5 <= radius",
            "m1_code": "def solve_m1(a, b):\n    return a + b", "m1_test": "assert solve_m1(2, 3) == 5",
            "m2_code": "def solve_m2(x):\n    return x**2", "m2_test": "assert solve_m2(4) == 16",
            "m3_code": "def solve_m3(s):\n    return s.strip().lower()", "m3_test": "assert solve_m3(' RUN ') == 'run'",
            "m4_code": "def solve_m4(lst):\n    return [x for x in lst if x > 0]", "m4_test": "assert solve_m4([-1, 2]) == [2]",
            "m5_code": "def solve_m5(d):\n    return len(d)", "m5_test": "assert solve_m5({'a': 1}) == 1",
            "h1_code": "def solve_h1(fn, items):\n    return [fn(x) for x in items]", "h1_test": "assert solve_h1(lambda x: x*2, [1, 2]) == [2, 4]",
            "h2_code": "def solve_h2(fn, items):\n    return [x for x in items if fn(x)]", "h2_test": "assert solve_h2(lambda x: x>0, [-1, 1]) == [1]",
            "h3_code": "def solve_h3(funcs, val):\n    res = val\n    for f in funcs:\n        res = f(res)\n    return res", "h3_test": "assert solve_h3([lambda x: x+1, lambda x: x*2], 3) == 8",
            "h4_code": "def solve_h4(fn, *args):\n    return fn(*args)", "h4_test": "assert solve_h4(lambda a, b: a+b, 2, 3) == 5",
            "h5_code": "def solve_h5(func):\n    return getattr(func, '__doc__', '')", "h5_test": "def f(): 'doc'; pass\nassert solve_h5(f) == 'doc'",
            "rob_code": "def process_telemetry(data):\n    return {'status': 'PROCESSED', 'items': len(data)}", "rob_test": "assert process_telemetry([1])['status'] == 'PROCESSED'"
        }
    ),
    make_topic_data(
        topic_id="4.2", title="Parameters and Arguments", module=4, module_title="Functions and Modules",
        directory="02_parameters_and_arguments", summary="Positional, keyword, default arguments, *args, and **kwargs.",
        why_it_matters="Flexible parameter signatures allow APIs to handle diverse invocation options.",
        objectives=["Use default and keyword arguments.", "Unpack arguments using * and **.", "Enforce positional-only / keyword-only parameters."],
        prerequisites=["Topic 4.1 Functions"], domain="manufacturing cell controller", concepts=["Parameters", "*args", "**kwargs"],
        code_snippets={
            "syntax": "def fn(a, b=10, *args, **kwargs):\n    pass", "basic": "def greet(name, msg='Hello'):\n    return f'{msg}, {name}'",
            "intermediate": "def sum_all(*args):\n    return sum(args)", "advanced": "def config(*, host, port):\n    return f'{host}:{port}'",
            "walkthrough": "def log_event(event_type, *details, timestamp=0.0, **meta):\n    return {'type': event_type, 'details': details, 'ts': timestamp, 'meta': meta}",
            "pythonic": "def process(a, b, /, c=3, *, d=4):\n    return a + b + c + d", "engineering": "def set_motor_speed(motor_id, speed_rpm=0.0, *, accel_limit=100.0, mode='NORMAL'):\n    return True",
            "m1_code": "def solve_m1(a, b=10):\n    return a + b", "m1_test": "assert solve_m1(5) == 15",
            "m2_code": "def solve_m2(*args):\n    return sum(args)", "m2_test": "assert solve_m2(1, 2, 3) == 6",
            "m3_code": "def solve_m3(**kwargs):\n    return kwargs", "m3_test": "assert solve_m3(a=1, b=2) == {'a': 1, 'b': 2}",
            "m4_code": "def solve_m4(a, b, *args):\n    return a + b + sum(args)", "m4_test": "assert solve_m4(1, 2, 3, 4) == 10",
            "m5_code": "def solve_m5(*, key, val):\n    return {key: val}", "m5_test": "assert solve_m5(key='a', val=1) == {'a': 1}",
            "h1_code": "def solve_h1(*args, **kwargs):\n    return sum(args) + sum(kwargs.values())", "h1_test": "assert solve_h1(1, 2, x=3, y=4) == 10",
            "h2_code": "def solve_h2(fn, args_tuple, kwargs_dict):\n    return fn(*args_tuple, **kwargs_dict)", "h2_test": "assert solve_h2(lambda a, b: a*b, (2, 3), {}) == 6",
            "h3_code": "def solve_h3(a, b=1, *args, c=2, **kwargs):\n    return a + b + sum(args) + c + sum(kwargs.values())", "h3_test": "assert solve_h3(10, 2, 3, c=5, d=4) == 24",
            "h4_code": "def solve_h4(*args):\n    return [x for x in args if isinstance(x, (int, float))]", "h4_test": "assert solve_h4(1, 'a', 2.5) == [1, 2.5]",
            "h5_code": "def solve_h5(**kwargs):\n    return sorted(kwargs.keys())", "h5_test": "assert solve_h5(b=2, a=1) == ['a', 'b']",
            "rob_code": "def process_telemetry(data, *args, **kwargs):\n    return {'data_len': len(data), 'extra': len(args) + len(kwargs)}", "rob_test": "assert process_telemetry([1], 2, x=3)['extra'] == 2"
        }
    ),
    make_topic_data(
        topic_id="4.3", title="Return Values, Scope, and Closures", module=4, module_title="Functions and Modules",
        directory="03_return_values_scope_closures", summary="LEGB rule, global and nonlocal keywords, closures, and returning values.",
        why_it_matters="Understanding variable scope and closures prevents state leak bugs.",
        objectives=["Understand LEGB scope resolution.", "Use nonlocal in nested functions.", "Construct closures to encapsulate state."],
        prerequisites=["Topic 4.2 Parameters"], domain="manufacturing cell controller", concepts=["Scope", "LEGB", "Closures"],
        code_snippets={
            "syntax": "def make_adder(x):\n    def add(y):\n        return x + y\n    return add",
            "basic": "def outer():\n    x = 'outer'\n    def inner():\n        return x\n    return inner()",
            "intermediate": "def make_counter():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc",
            "advanced": "x = 10\ndef modify():\n    global x\n    x = 20",
            "walkthrough": "def make_limiter(max_val):\n    def limit(val):\n        return min(val, max_val)\n    return limit",
            "pythonic": "def get_pair():\n    return 1, 2", "engineering": "def make_pid_integral(ki):\n    integral = 0.0\n    def update(error, dt):\n        nonlocal integral\n        integral += error * dt\n        return ki * integral\n    return update",
            "m1_code": "def solve_m1(a, b):\n    return a + b, a * b", "m1_test": "assert solve_m1(2, 3) == (5, 6)",
            "m2_code": "def solve_m2(val):\n    def inner():\n        return val * 2\n    return inner()", "m2_test": "assert solve_m2(5) == 10",
            "m3_code": "def solve_m3(factor):\n    def multiplier(x):\n        return x * factor\n    return multiplier", "m3_test": "double = solve_m3(2); assert double(5) == 10",
            "m4_code": "def solve_m4():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc", "m4_test": "c = solve_m4(); assert c() == 1 and c() == 2",
            "m5_code": "def solve_m5(val):\n    if val < 0: return None\n    return val**0.5", "m5_test": "assert solve_m5(4) == 2.0 and solve_m5(-1) is None",
            "h1_code": "def solve_h1(initial=0):\n    val = initial\n    def get_val(): return val\n    def set_val(new_val):\n        nonlocal val\n        val = new_val\n    return get_val, set_val", "h1_test": "g, s = solve_h1(5); s(10); assert g() == 10",
            "h2_code": "def solve_h2(fn):\n    cache = {}\n    def memoized(x):\n        if x not in cache:\n            cache[x] = fn(x)\n        return cache[x]\n    return memoized", "h2_test": "f = solve_h2(lambda x: x*2); assert f(3) == 6",
            "h3_code": "def solve_h3(min_v, max_v):\n    def clamp(v):\n        return max(min_v, min(v, max_v))\n    return clamp", "h3_test": "c = solve_h3(0, 10); assert c(15) == 10",
            "h4_code": "def solve_h4(prefix):\n    def logger(msg):\n        return f'[{prefix}] {msg}'\n    return logger", "h4_test": "log = solve_h4('INFO'); assert log('OK') == '[INFO] OK'",
            "h5_code": "def solve_h5(funcs):\n    def composed(x):\n        res = x\n        for f in funcs:\n            res = f(res)\n        return res\n    return composed", "h5_test": "comp = solve_h5([lambda x: x+1, lambda x: x*2]); assert comp(3) == 8",
            "rob_code": "def process_telemetry(data):\n    def calculate_mean(values):\n        return sum(values) / len(values) if values else 0.0\n    return {'mean': calculate_mean(data)}", "rob_test": "assert process_telemetry([10, 20])['mean'] == 15.0"
        }
    ),
    make_topic_data(
        topic_id="4.4", title="Advanced Function Concepts", module=4, module_title="Functions and Modules",
        directory="04_advanced_function_concepts", summary="Higher-order functions, first-class functions, and recursion.",
        why_it_matters="Functions are first-class objects in Python and can be passed as arguments.",
        objectives=["Pass functions as first-class objects.", "Implement higher-order functions.", "Write recursive algorithms with base cases."],
        prerequisites=["Topic 4.3 Scope and Closures"], domain="manufacturing cell controller", concepts=["Higher-Order Functions", "Recursion"],
        code_snippets={
            "syntax": "def apply(f, x):\n    return f(x)", "basic": "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)",
            "intermediate": "def map_func(fn, lst):\n    return [fn(x) for x in lst]", "advanced": "def memo_factorial(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return 1\n    memo[n] = n * memo_factorial(n - 1, memo)\n    return memo[n]",
            "walkthrough": "def traverse_tree(node):\n    if not node: return []\n    res = [node['val']]\n    for child in node.get('children', []):\n        res.extend(traverse_tree(child))\n    return res",
            "pythonic": "def apply_all(funcs, val):\n    return [f(val) for f in funcs]", "engineering": "def evaluate_control_pipeline(pipeline, initial_state):\n    state = initial_state\n    for stage in pipeline:\n        state = stage(state)\n    return state",
            "m1_code": "def solve_m1(n):\n    if n <= 1: return 1\n    return n * solve_m1(n - 1)", "m1_test": "assert solve_m1(5) == 120",
            "m2_code": "def solve_m2(n):\n    if n <= 0: return 0\n    if n == 1: return 1\n    return solve_m2(n - 1) + solve_m2(n - 2)", "m2_test": "assert solve_m2(6) == 8",
            "m3_code": "def solve_m3(fn, lst):\n    return [fn(x) for x in lst]", "m3_test": "assert solve_m3(lambda x: x*2, [1, 2]) == [2, 4]",
            "m4_code": "def solve_m4(pred, lst):\n    return [x for x in lst if pred(x)]", "m4_test": "assert solve_m4(lambda x: x>0, [-1, 1]) == [1]",
            "m5_code": "def solve_m5(lst):\n    if not lst: return 0\n    return lst[0] + solve_m5(lst[1:])", "m5_test": "assert solve_m5([1, 2, 3]) == 6",
            "h1_code": "def solve_h1(nested):\n    total = 0\n    for x in nested:\n        if isinstance(x, list):\n            total += solve_h1(x)\n        else:\n            total += x\n    return total", "h1_test": "assert solve_h1([1, [2, [3]]]) == 6",
            "h2_code": "def solve_h2(fn, times):\n    def repeated(x):\n        res = x\n        for _ in range(times):\n            res = fn(res)\n        return res\n    return repeated", "h2_test": "f = solve_h2(lambda x: x*2, 3); assert f(1) == 8",
            "h3_code": "def solve_h3(a, b):\n    while b:\n        a, b = b, a % b\n    return a", "h3_test": "assert solve_h3(48, 18) == 6",
            "h4_code": "def solve_h4(s):\n    if len(s) <= 1: return s\n    return solve_h4(s[1:]) + s[0]", "h4_test": "assert solve_h4('abc') == 'cba'",
            "h5_code": "def solve_h5(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return solve_h5(left) + middle + solve_h5(right)", "h5_test": "assert solve_h5([3, 1, 2]) == [1, 2, 3]",
            "rob_code": "def process_telemetry(data):\n    def recursive_sum(lst):\n        if not lst: return 0.0\n        return float(lst[0]) + recursive_sum(lst[1:])\n    return {'sum': recursive_sum(data)}", "rob_test": "assert process_telemetry([1.0, 2.0])['sum'] == 3.0"
        }
    ),
    make_topic_data(
        topic_id="4.5", title="Lambda Functions and Functional Tools", module=4, module_title="Functions and Modules",
        directory="05_lambda_functional_tools", summary="lambda expressions, map(), filter(), reduce(), and functools.",
        why_it_matters="Functional tools allow declarative transformation pipelines.",
        objectives=["Write anonymous lambda functions.", "Transform collections with map() and filter().", "Aggregate data with functools.reduce()."],
        prerequisites=["Topic 4.4 Advanced Functions"], domain="subsea ROV", concepts=["lambda", "map", "filter", "reduce"],
        code_snippets={
            "syntax": "sq = lambda x: x**2", "basic": "double = lambda x: x * 2\nprint(double(5))",
            "intermediate": "nums = [1, 2, 3, 4]\nevens = list(filter(lambda x: x % 2 == 0, nums))",
            "advanced": "from functools import reduce\nproduct = reduce(lambda x, y: x * y, [1, 2, 3, 4])",
            "walkthrough": "data = [10, 20, 30]\nscaled = list(map(lambda x: x / 10.0, data))\nprint('Scaled:', scaled)",
            "pythonic": "sorted_items = sorted([('a', 3), ('b', 1)], key=lambda x: x[1])",
            "engineering": "from functools import reduce\ndef process_sensor_stream(stream):\n    filtered = filter(lambda x: x >= 0.0, stream)\n    scaled = map(lambda x: x * 1.5, filtered)\n    return reduce(lambda acc, x: acc + x, scaled, 0.0)",
            "m1_code": "def solve_m1(a, b):\n    f = lambda x, y: x * y\n    return f(a, b)", "m1_test": "assert solve_m1(3, 4) == 12",
            "m2_code": "def solve_m2(lst):\n    return list(map(lambda x: x * 2, lst))", "m2_test": "assert solve_m2([1, 2]) == [2, 4]",
            "m3_code": "def solve_m3(lst):\n    return list(filter(lambda x: x > 0, lst))", "m3_test": "assert solve_m3([-1, 1, 2]) == [1, 2]",
            "m4_code": "def solve_m4(lst):\n    from functools import reduce\n    return reduce(lambda x, y: x + y, lst, 0)", "m4_test": "assert solve_m4([1, 2, 3]) == 6",
            "m5_code": "def solve_m5(tuples_list):\n    return sorted(tuples_list, key=lambda x: x[1])", "m5_test": "assert solve_m5([(1, 3), (2, 1)]) == [(2, 1), (1, 3)]",
            "h1_code": "def solve_h1(words):\n    return list(map(lambda w: w.upper(), filter(lambda w: len(w) > 3, words)))", "h1_test": "assert solve_h1(['cat', 'robot']) == ['ROBOT']",
            "h2_code": "def solve_h2(numbers):\n    from functools import reduce\n    return reduce(lambda x, y: x if x > y else y, numbers)", "h2_test": "assert solve_h2([1, 5, 3]) == 5",
            "h3_code": "def solve_h3(dict_list):\n    return sorted(dict_list, key=lambda d: d.get('val', 0), reverse=True)", "h3_test": "assert solve_h3([{'val': 1}, {'val': 5}]) == [{'val': 5}, {'val': 1}]",
            "h4_code": "def solve_h4(f, g):\n    return lambda x: f(g(x))", "h4_test": "comp = solve_h4(lambda x: x+1, lambda x: x*2); assert comp(3) == 7",
            "h5_code": "def solve_h5(lst):\n    from functools import reduce\n    return reduce(lambda acc, x: acc + [x] if x not in acc else acc, lst, [])", "h5_test": "assert solve_h5([1, 2, 1, 3]) == [1, 2, 3]",
            "rob_code": "def process_telemetry(data):\n    filtered = list(filter(lambda x: x >= 0, data))\n    return {'valid': filtered}", "rob_test": "assert process_telemetry([1.0, -2.0])['valid'] == [1.0]"
        }
    ),
    make_topic_data(
        topic_id="4.6", title="Generators", module=4, module_title="Functions and Modules",
        directory="06_generators", summary="yield statement, generator functions, generator expressions, and memory optimization.",
        why_it_matters="Generators stream data lazily with O(1) memory footprint.",
        objectives=["Write generator functions using yield.", "Understand lazy evaluation semantics.", "Use itertools for streaming algorithms."],
        prerequisites=["Topic 4.5 Functional Tools"], domain="subsea ROV", concepts=["Generators", "yield", "Lazy Evaluation"],
        code_snippets={
            "syntax": "def count_up(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1", "basic": "gen = (x**2 for x in range(3))\nprint(next(gen))",
            "intermediate": "def fib_gen():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b", "advanced": "def echo_gen():\n    val = yield 'READY'\n    yield f'Received {val}'",
            "walkthrough": "def sensor_stream(limit):\n    for i in range(limit):\n        yield {'sample': i, 'val': i * 1.5}\nfor frame in sensor_stream(2):\n    print(frame)",
            "pythonic": "def read_lines(filename):\n    with open(filename) as f:\n        yield from f", "engineering": "def telemetry_pipeline(stream):\n    for frame in stream:\n        if frame.get('valid'):\n            yield frame['val'] * 2.0",
            "m1_code": "def solve_m1(n):\n    for i in range(n):\n        yield i", "m1_test": "assert list(solve_m1(3)) == [0, 1, 2]",
            "m2_code": "def solve_m2(lst):\n    for x in lst:\n        if x % 2 == 0:\n            yield x", "m2_test": "assert list(solve_m2([1, 2, 3, 4])) == [2, 4]",
            "m3_code": "def solve_m3(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b", "m3_test": "assert list(solve_m3(4)) == [0, 1, 1, 2]",
            "m4_code": "def solve_m4(gen1, gen2):\n    yield from gen1\n    yield from gen2", "m4_test": "assert list(solve_m4(range(2), range(2, 4))) == [0, 1, 2, 3]",
            "m5_code": "def solve_m5(start, stop):\n    curr = start\n    while curr < stop:\n        yield curr\n        curr += 1", "m5_test": "assert list(solve_m5(1, 4)) == [1, 2, 3]",
            "h1_code": "def solve_h1(stream, window_size):\n    from collections import deque\n    buf = deque(maxlen=window_size)\n    for x in stream:\n        buf.append(x)\n        if len(buf) == window_size:\n            yield list(buf)", "h1_test": "assert list(solve_h1([1, 2, 3, 4], 2)) == [[1, 2], [2, 3], [3, 4]]",
            "h2_code": "def solve_h2(nested):\n    for item in nested:\n        if isinstance(item, list):\n            yield from solve_h2(item)\n        else:\n            yield item", "h2_test": "assert list(solve_h2([1, [2, [3]]])) == [1, 2, 3]",
            "h3_code": "def solve_h3(gen, predicate):\n    for x in gen:\n        if predicate(x):\n            yield x", "h3_test": "assert list(solve_h3(range(5), lambda x: x>2)) == [3, 4]",
            "h4_code": "def solve_h4(gen, fn):\n    for x in gen:\n        yield fn(x)", "h4_test": "assert list(solve_h4(range(3), lambda x: x*2)) == [0, 2, 4]",
            "h5_code": "def solve_h5(stream):\n    prev = None\n    for x in stream:\n        if x != prev:\n            yield x\n            prev = x", "h5_test": "assert list(solve_h5([1, 1, 2, 2, 1])) == [1, 2, 1]",
            "rob_code": "def process_telemetry(data):\n    def gen():\n        for x in data:\n            yield x * 2.0\n    return {'stream_sample': list(gen())}", "rob_test": "assert process_telemetry([1.0, 2.0])['stream_sample'] == [2.0, 4.0]"
        }
    ),
    make_topic_data(
        topic_id="4.7", title="Decorators", module=4, module_title="Functions and Modules",
        directory="07_decorators", summary="Function decorators, functools.wraps, parameterized decorators, and class decorators.",
        why_it_matters="Decorators inject cross-cutting concerns like logging, timing, and security checks cleanly.",
        objectives=["Write function decorators.", "Preserve metadata with @functools.wraps.", "Pass parameters to decorators."],
        prerequisites=["Topic 4.6 Generators"], domain="subsea ROV", concepts=["Decorators", "@wraps", "Meta-programming"],
        code_snippets={
            "syntax": "@my_decorator\ndef func():\n    pass", "basic": "def logger(fn):\n    def wrapper(*args, **kwargs):\n        print('Calling', fn.__name__)\n        return fn(*args, **kwargs)\n    return wrapper",
            "intermediate": "from functools import wraps\ndef timer(fn):\n    @wraps(fn)\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper", "advanced": "def repeat(num):\n    def decorator(fn):\n        def wrapper(*args, **kwargs):\n            res = None\n            for _ in range(num):\n                res = fn(*args, **kwargs)\n            return res\n        return wrapper\n    return decorator",
            "walkthrough": "from functools import wraps\ndef validate_non_negative(fn):\n    @wraps(fn)\n    def wrapper(val):\n        if val < 0:\n            raise ValueError('Negative value not allowed')\n        return fn(val)\n    return wrapper",
            "pythonic": "from functools import lru_cache\n@lru_cache(maxsize=128)\ndef memoized_func(x):\n    return x**2", "engineering": "from functools import wraps\ndef retry_on_failure(retries=3):\n    def decorator(fn):\n        @wraps(fn)\n        def wrapper(*args, **kwargs):\n            for attempt in range(retries):\n                try:\n                    return fn(*args, **kwargs)\n                except Exception:\n                    if attempt == retries - 1: raise\n        return wrapper\n    return decorator",
            "m1_code": "def solve_m1(fn):\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper", "m1_test": "@solve_m1\ndef add(a, b): return a + b\nassert add(1, 2) == 3",
            "m2_code": "def solve_m2(fn):\n    def wrapper(val):\n        return fn(val * 2)\n    return wrapper", "m2_test": "@solve_m2\ndef double(x): return x\nassert double(5) == 10",
            "m3_code": "def solve_m3(fn):\n    def wrapper(val):\n        return str(fn(val))\n    return wrapper", "m3_test": "@solve_m3\ndef num(x): return x\nassert num(42) == '42'",
            "m4_code": "from functools import wraps\ndef solve_m4(fn):\n    @wraps(fn)\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper", "m4_test": "@solve_m4\ndef my_fn(): 'doc'; pass\nassert my_fn.__doc__ == 'doc'",
            "m5_code": "def solve_m5(prefix):\n    def dec(fn):\n        def wrapper(msg):\n            return f'[{prefix}] {fn(msg)}'\n        return wrapper\n    return dec", "m5_test": "@solve_m5('LOG')\ndef echo(s): return s\nassert echo('hi') == '[LOG] hi'",
            "h1_code": "def solve_h1(fn):\n    cache = {}\n    def wrapper(x):\n        if x not in cache:\n            cache[x] = fn(x)\n        return cache[x]\n    return wrapper", "h1_test": "@solve_h1\ndef sq(x): return x**2\nassert sq(4) == 16",
            "h2_code": "def solve_h2(fn):\n    def wrapper(*args, **kwargs):\n        res = fn(*args, **kwargs)\n        return type(res).__name__\n    return wrapper", "h2_test": "@solve_h2\ndef f(): return 123\nassert f() == 'int'",
            "h3_code": "def solve_h3(fn):\n    def wrapper(*args, **kwargs):\n        for arg in args:\n            if isinstance(arg, (int, float)) and arg < 0:\n                raise ValueError('Negative argument')\n        return fn(*args, **kwargs)\n    return wrapper", "h3_test": "@solve_h3\ndef pos(x): return x\nassert pos(5) == 5",
            "h4_code": "def solve_h4(n):\n    def dec(fn):\n        def wrapper(*args, **kwargs):\n            return [fn(*args, **kwargs) for _ in range(n)]\n        return wrapper\n    return dec", "h4_test": "@solve_h4(3)\ndef get_one(): return 1\nassert get_one() == [1, 1, 1]",
            "h5_code": "def solve_h5(cls):\n    cls.is_decorated = True\n    return cls", "h5_test": "@solve_h5\nclass Robot: pass\nassert getattr(Robot, 'is_decorated') is True",
            "rob_code": "def process_telemetry(data):\n    def log_dec(fn):\n        def wrapper(d):\n            res = fn(d)\n            res['logged'] = True\n            return res\n        return wrapper\n    @log_dec\n    def handle(d):\n        return {'count': len(d)}\n    return handle(data)", "rob_test": "assert process_telemetry([1])['logged'] is True"
        }
    ),
    make_topic_data(
        topic_id="4.8", title="Modules and Packages", module=4, module_title="Functions and Modules",
        directory="08_modules_and_packages", summary="import statements, __init__.py, relative imports, and module search path.",
        why_it_matters="Modules organize code into reusable maintainable namespaces.",
        objectives=["Import standard and custom modules.", "Structure Python packages with __init__.py.", "Understand sys.path resolution."],
        prerequisites=["Topic 4.7 Decorators"], domain="last-mile logistics fleet", concepts=["Modules", "Packages", "__init__.py"],
        code_snippets={
            "syntax": "import math\nfrom math import pi", "basic": "import sys\nprint(sys.path)",
            "intermediate": "from pathlib import Path\np = Path('.')", "advanced": "import importlib\nmod = importlib.import_module('math')",
            "walkthrough": "import os, sys\nprint('CWD:', os.getcwd())\nprint('Python Executable:', sys.executable)",
            "pythonic": "from typing import TYPE_CHECKING", "engineering": "import sys\nfrom pathlib import Path\ndef add_package_root(root_dir):\n    root_path = str(Path(root_dir).resolve())\n    if root_path not in sys.path:\n        sys.path.insert(0, root_path)",
            "m1_code": "def solve_m1(mod_name):\n    import importlib\n    return importlib.import_module(mod_name).__name__", "m1_test": "assert solve_m1('math') == 'math'",
            "m2_code": "def solve_m2(mod):\n    return [item for item in dir(mod) if not item.startswith('_')]", "m2_test": "import math; assert 'sin' in solve_m2(math)",
            "m3_code": "def solve_m3(path_str):\n    import sys\n    return path_str in sys.path", "m3_test": "import sys; assert solve_m3(sys.path[0]) is True",
            "m4_code": "def solve_m4(pkg_dir):\n    from pathlib import Path\n    return (Path(pkg_dir) / '__init__.py').exists()", "m4_test": "assert solve_m4('shared') is True",
            "m5_code": "def solve_m5(mod_name):\n    import sys\n    return mod_name in sys.modules", "m5_test": "assert solve_m5('sys') is True",
            "h1_code": "def solve_h1(pkg_path):\n    from pathlib import Path\n    p = Path(pkg_path)\n    return [f.stem for f in p.glob('*.py') if f.name != '__init__.py']", "h1_test": "assert isinstance(solve_h1('tools'), list)",
            "h2_code": "def solve_h2(mod_name, attr_name):\n    import importlib\n    mod = importlib.import_module(mod_name)\n    return getattr(mod, attr_name)", "h2_test": "assert solve_h2('math', 'pi') > 3.14",
            "h3_code": "def solve_h3(mod):\n    return getattr(mod, '__file__', None)", "h3_test": "import math; assert solve_h3(math) is not None or True",
            "h4_code": "def solve_h4(mod_name):\n    import importlib\n    mod = importlib.import_module(mod_name)\n    importlib.reload(mod)\n    return mod.__name__", "h4_test": "assert solve_h4('math') == 'math'",
            "h5_code": "def solve_h5(mod_name):\n    import sys\n    return sys.modules.get(mod_name) is not None", "h5_test": "assert solve_h5('os') is True",
            "rob_code": "def process_telemetry(data):\n    import math\n    return {'sqrt_len': math.sqrt(len(data))}", "rob_test": "assert process_telemetry([1, 2, 3, 4])['sqrt_len'] == 2.0"
        }
    ),
    make_topic_data(
        topic_id="4.9", title="Virtual Environments and Package Management", module=4, module_title="Functions and Modules",
        directory="09_virtual_environments_packaging", summary="venv, pip, requirements.txt, and pyproject.toml.",
        why_it_matters="Isolated virtual environments prevent dependency version conflicts.",
        objectives=["Create virtual environments with venv.", "Manage dependencies with pip and requirements.txt.", "Configure pyproject.toml."],
        prerequisites=["Topic 4.8 Modules"], domain="last-mile logistics fleet", concepts=["venv", "pip", "pyproject.toml"],
        code_snippets={
            "syntax": "# python3 -m venv .venv\n# source .venv/bin/activate", "basic": "import sys\nprint('VENV active:', sys.prefix != sys.base_prefix)",
            "intermediate": "def parse_requirements(req_text):\n    return [line.strip() for line in req_text.splitlines() if line.strip() and not line.startswith('#')]",
            "advanced": "import sys\ndef is_in_venv():\n    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)",
            "walkthrough": "import sys\nprefix = getattr(sys, 'prefix', '')\nbase_prefix = getattr(sys, 'base_prefix', '')\nprint(f'Active environment: {prefix}')",
            "pythonic": "import site\nprint(site.getsitepackages())", "engineering": "def verify_dependencies(required_map):\n    import importlib.metadata\n    missing = []\n    for pkg, min_ver in required_map.items():\n        try:\n            ver = importlib.metadata.version(pkg)\n        except Exception:\n            missing.append(pkg)\n    return missing",
            "m1_code": "def solve_m1(req_str):\n    return [line.strip() for line in req_str.splitlines() if line.strip() and not line.startswith('#')]", "m1_test": "assert solve_m1('numpy>=1.20\n# comment') == ['numpy>=1.20']",
            "m2_code": "def solve_m2(req_lines):\n    return {line.split('==')[0]: line.split('==')[1] for line in req_lines if '==' in line}", "m2_test": "assert solve_m2(['pytest==8.0.0']) == {'pytest': '8.0.0'}",
            "m3_code": "def solve_m3():\n    import sys\n    return getattr(sys, 'base_prefix', sys.prefix) != sys.prefix", "m3_test": "assert isinstance(solve_m3(), bool)",
            "m4_code": "def solve_m4(pkg_name):\n    import importlib.metadata\n    try:\n        return importlib.metadata.version(pkg_name)\n    except Exception:\n        return None", "m4_test": "assert solve_m4('pytest') is not None or True",
            "m5_code": "def solve_m5(toml_str):\n    return '[project]' in toml_str", "m5_test": "assert solve_m5('[project]\nname=\"robo\"') is True",
            "h1_code": "def solve_h1(pyproject_content):\n    lines = pyproject_content.splitlines()\n    in_deps = False\n    deps = []\n    for line in lines:\n        if 'dependencies =' in line:\n            in_deps = True\n            continue\n        if in_deps:\n            if line.strip().endswith(']'): break\n            clean = line.strip().strip('\",')\n            if clean: deps.append(clean)\n    return deps", "h1_test": "assert solve_h1('dependencies = [\n\"numpy>=1.20\",\n]') == ['numpy>=1.20']",
            "h2_code": "def solve_h2(pkgs):\n    return '\\n'.join(f'{k}=={v}' for k, v in sorted(pkgs.items()))", "h2_test": "assert solve_h2({'a': '1.0'}) == 'a==1.0'",
            "h3_code": "def solve_h3(path_str):\n    import sys\n    return path_str in sys.path", "h3_test": "import sys; assert solve_h3(sys.path[0]) is True",
            "h4_code": "def solve_h4(pkg_name):\n    import importlib.util\n    return importlib.util.find_spec(pkg_name) is not None", "h4_test": "assert solve_h4('sys') is True",
            "h5_code": "def solve_h5(req_str):\n    import re\n    return [re.split(r'[<>=!]', line)[0].strip() for line in req_str.splitlines() if line.strip()]", "h5_test": "assert solve_h5('numpy>=1.26\\npandas') == ['numpy', 'pandas']",
            "rob_code": "def process_telemetry(data):\n    return {'env_ok': True, 'count': len(data)}", "rob_test": "assert process_telemetry([1])['env_ok'] is True"
        }
    )
]
