"""Module 9 — Intermediate Practical Skills and Best Practices (topics 9.1 - 9.7)."""

from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from self_created_tools.topic_builder import make_topic_data

TOPICS = [
    make_topic_data(
        topic_id="9.1", title="Type Hints", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="01_type_hints", summary="Type annotations, typing module (Union, Optional, Any, Callable), mypy, and runtime type checking.",
        why_it_matters="Type hints document API expectations, catch bugs statically, and improve IDE completion.",
        objectives=["Annotate variables, functions, and return types.", "Use typing module generics.", "Run static type checks."],
        prerequisites=["Module 8 Databases"], domain="robotics-as-a-service platform", concepts=["Type Hints", "typing", "Static Analysis"],
        code_snippets={
            "syntax": "def greet(name: str) -> str:\n    return f'Hello {name}'", "basic": "from typing import Optional\ndef find(id_num: int) -> Optional[str]:\n    return 'ROBO' if id_num == 1 else None",
            "intermediate": "from typing import List, Dict, Union\ndef process(data: List[Union[int, float]]) -> Dict[str, float]:\n    return {'avg': sum(data)/len(data) if data else 0.0}",
            "advanced": "from typing import Callable, TypeVar\nT = TypeVar('T')\ndef apply(fn: Callable[[T], T], val: T) -> T:\n    return fn(val)",
            "walkthrough": "from typing import List, Optional\ndef parse_readings(readings: List[float]) -> Optional[float]:\n    if not readings: return None\n    return sum(readings) / len(readings)",
            "pythonic": "def add(x: int | float, y: int | float) -> int | float:\n    return x + y", "engineering": "from typing import Dict, Any, List\ndef validate_telemetry_payload(payload: Dict[str, Any]) -> List[str]:\n    errors: List[str] = []\n    if 'robot_id' not in payload:\n        errors.append('Missing robot_id')\n    return errors",
            "m1_code": "def solve_m1(a: int, b: int) -> int:\n    return a + b", "m1_test": "assert solve_m1(2, 3) == 5",
            "m2_code": "from typing import Optional\ndef solve_m2(flag: bool) -> Optional[str]:\n    return 'OK' if flag else None", "m2_test": "assert solve_m2(True) == 'OK' and solve_m2(False) is None",
            "m3_code": "from typing import List\ndef solve_m3(items: List[int]) -> int:\n    return sum(items)", "m3_test": "assert solve_m3([1, 2, 3]) == 6",
            "m4_code": "from typing import Dict\ndef solve_m4(d: Dict[str, int]) -> List[str]:\n    return list(d.keys())", "m4_test": "assert solve_m4({'a': 1}) == ['a']",
            "m5_code": "from typing import Union\ndef solve_m5(val: Union[int, str]) -> str:\n    return str(val)", "m5_test": "assert solve_m5(42) == '42'",
            "h1_code": "from typing import Callable, List\ndef solve_h1(fn: Callable[[int], int], lst: List[int]) -> List[int]:\n    return [fn(x) for x in lst]", "h1_test": "assert solve_h1(lambda x: x*2, [1, 2]) == [2, 4]",
            "h2_code": "from typing import Tuple, Any\ndef solve_h2(a: Any, b: Any) -> Tuple[Any, Any]:\n    return b, a", "h2_test": "assert solve_h2(1, 'x') == ('x', 1)",
            "h3_code": "from typing import Dict, Any\ndef solve_h3(d: Dict[str, Any], key: str) -> bool:\n    return key in d", "h3_test": "assert solve_h3({'a': 1}, 'a') is True",
            "h4_code": "from typing import Sequence, TypeVar\nT = TypeVar('T')\ndef solve_h4(seq: Sequence[T]) -> T:\n    return seq[0]", "h4_test": "assert solve_h4([10, 20]) == 10",
            "h5_code": "from typing import Literal\ndef solve_m5(mode: Literal['fast', 'slow']) -> int:\n    return 100 if mode == 'fast' else 10\ndef solve_h5(m):\n    return solve_m5(m)", "h5_test": "assert solve_h5('fast') == 100",
            "rob_code": "from typing import Dict, Any\ndef process_telemetry(data: list) -> Dict[str, Any]:\n    return {'count': len(data), 'status': 'ANNOTATED'}", "rob_test": "assert process_telemetry([1])['status'] == 'ANNOTATED'"
        }
    ),
    make_topic_data(
        topic_id="9.2", title="Dates and Times", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="02_dates_and_times", summary="datetime, date, time, timedelta, timezone awareness, and ISO-8601 formatting.",
        why_it_matters="Accurate timestamping and timezone handling are critical for robot telemetry streams.",
        objectives=["Parse and format ISO-8601 dates.", "Perform date arithmetic with timedelta.", "Handle UTC and timezone awareness."],
        prerequisites=["Topic 9.1 Type Hints"], domain="robotics-as-a-service platform", concepts=["datetime", "timedelta", "ISO-8601", "Timezone"],
        code_snippets={
            "syntax": "from datetime import datetime, timezone\nnow = datetime.now(timezone.utc)", "basic": "from datetime import datetime\nnow_str = datetime.utcnow().isoformat()",
            "intermediate": "from datetime import datetime, timedelta\ntomorrow = datetime.now() + timedelta(days=1)", "advanced": "from datetime import datetime, timezone\nutc_dt = datetime.fromisoformat('2026-10-03T12:00:00+00:00')",
            "walkthrough": "from datetime import datetime, timezone, timedelta\nt0 = datetime.now(timezone.utc)\nt1 = t0 + timedelta(seconds=1.5)\ndelta = (t1 - t0).total_seconds()\nprint('Elapsed seconds:', delta)",
            "pythonic": "iso = datetime.now(timezone.utc).isoformat()", "engineering": "from datetime import datetime, timezone\ndef is_telemetry_fresh(timestamp_iso: str, max_age_s: float = 5.0) -> bool:\n    try:\n        dt = datetime.fromisoformat(timestamp_iso)\n        now = datetime.now(timezone.utc)\n        return (now - dt).total_seconds() <= max_age_s\n    except Exception:\n        return False",
            "m1_code": "def solve_m1():\n    from datetime import datetime\n    return isinstance(datetime.now().isoformat(), str)", "m1_test": "assert solve_m1() is True",
            "m2_code": "def solve_m2(days_delta):\n    from datetime import datetime, timedelta\n    d = datetime(2026, 1, 1) + timedelta(days=days_delta)\n    return d.day", "m2_test": "assert solve_m2(5) == 6",
            "m3_code": "def solve_m3(iso_str):\n    from datetime import datetime\n    return datetime.fromisoformat(iso_str).year", "m3_test": "assert solve_m3('2026-10-03T00:00:00') == 2026",
            "m4_code": "def solve_m4(dt1_str, dt2_str):\n    from datetime import datetime\n    d1 = datetime.fromisoformat(dt1_str)\n    d2 = datetime.fromisoformat(dt2_str)\n    return (d2 - d1).total_seconds()", "m4_test": "assert solve_m4('2026-01-01T00:00:00', '2026-01-01T00:01:00') == 60.0",
            "m5_code": "def solve_m5():\n    from datetime import datetime, timezone\n    return datetime.now(timezone.utc).tzinfo is not None", "m5_test": "assert solve_m5() is True",
            "h1_code": "def solve_h1(dt_str, fmt_str):\n    from datetime import datetime\n    return datetime.strptime(dt_str, fmt_str).strftime('%Y-%m-%d')", "h1_test": "assert solve_h1('03/10/2026', '%d/%m/%Y') == '2026-10-03'",
            "h2_code": "def solve_h2(seconds):\n    from datetime import timedelta\n    td = timedelta(seconds=seconds)\n    return td.days, td.seconds", "h2_test": "assert solve_h2(3660) == (0, 3660)",
            "h3_code": "def solve_h3(year, month):\n    import calendar\n    return calendar.monthrange(year, month)[1]", "h3_test": "assert solve_h3(2026, 2) == 28",
            "h4_code": "def solve_h4(timestamps_iso):\n    from datetime import datetime\n    dts = [datetime.fromisoformat(ts) for ts in timestamps_iso]\n    return [dts[i+1] - dts[i] for i in range(len(dts)-1)]", "h4_test": "assert len(solve_h4(['2026-01-01T00:00:00', '2026-01-01T00:00:10'])) == 1",
            "h5_code": "def solve_h5(dt):\n    return dt.weekday() < 5", "h5_test": "from datetime import datetime; assert solve_h5(datetime(2026, 10, 2)) is True",
            "rob_code": "def process_telemetry(data):\n    from datetime import datetime, timezone\n    ts = datetime.now(timezone.utc).isoformat()\n    return {'timestamp': ts, 'data_len': len(data)}", "rob_test": "assert 'T' in process_telemetry([1])['timestamp']"
        }
    ),
    make_topic_data(
        topic_id="9.3", title="Command-Line Interfaces", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="03_command_line_interfaces", summary="argparse module, positional and optional flags, subcommands, and sys.argv parsing.",
        why_it_matters="Command-line interfaces allow automation and configuration of python tools.",
        objectives=["Build CLI tools with argparse.", "Define subcommands and flags.", "Parse CLI arguments safely."],
        prerequisites=["Topic 9.2 Dates and Times"], domain="robotics-as-a-service platform", concepts=["argparse", "CLI", "Subcommands"],
        code_snippets={
            "syntax": "import argparse\nparser = argparse.ArgumentParser()\nargs = parser.parse_args()", "basic": "import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument('--speed', type=float, default=1.0)\nargs = parser.parse_args(['--speed', '2.5'])\nprint(args.speed)",
            "intermediate": "import argparse\nparser = argparse.ArgumentParser()\nsub = parser.add_subparsers(dest='command')\nstart = sub.add_parser('start')", "advanced": "import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument('positional', nargs='+')",
            "walkthrough": "import argparse\nparser = argparse.ArgumentParser(description='Robot CLI')\nparser.add_argument('--mode', choices=['AUTO', 'MANUAL'], default='AUTO')\nargs = parser.parse_args(['--mode', 'AUTO'])\nprint('Selected mode:', args.mode)",
            "pythonic": "parsed, _ = parser.parse_known_args()", "engineering": "import argparse\ndef build_robot_cli_parser():\n    parser = argparse.ArgumentParser(description='ROBO-X Management CLI')\n    subparsers = parser.add_subparsers(dest='action', required=True)\n    start_p = subparsers.add_parser('start')\n    start_p.add_argument('--speed', type=float, default=1.0)\n    stop_p = subparsers.add_parser('stop')\n    return parser",
            "m1_code": "def solve_m1(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--port', type=int, default=8080)\n    return p.parse_args(args_list).port", "m1_test": "assert solve_m1(['--port', '9000']) == 9000",
            "m2_code": "def solve_m2(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--verbose', action='store_true')\n    return p.parse_args(args_list).verbose", "m2_test": "assert solve_m2(['--verbose']) is True",
            "m3_code": "def solve_m3(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('file')\n    return p.parse_args(args_list).file", "m3_test": "assert solve_m3(['data.csv']) == 'data.csv'",
            "m4_code": "def solve_m4(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('numbers', nargs='+', type=int)\n    return sum(p.parse_args(args_list).numbers)", "m4_test": "assert solve_m4(['1', '2', '3']) == 6",
            "m5_code": "def solve_m5(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--mode', choices=['fast', 'slow'], default='fast')\n    return p.parse_args(args_list).mode", "m5_test": "assert solve_m5(['--mode', 'slow']) == 'slow'",
            "h1_code": "def solve_h1(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    sub = p.add_subparsers(dest='cmd')\n    c1 = sub.add_parser('run')\n    c1.add_argument('--id', type=int)\n    parsed = p.parse_args(args_list)\n    return parsed.cmd, getattr(parsed, 'id', None)", "h1_test": "assert solve_h1(['run', '--id', '5']) == ('run', 5)",
            "h2_code": "def solve_h2(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--config', required=True)\n    try:\n        return p.parse_args(args_list).config\n    except SystemExit:\n        return None", "h2_test": "assert solve_h2([]) is None",
            "h3_code": "def solve_h3(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--items', nargs='*')\n    return p.parse_args(args_list).items", "h3_test": "assert solve_h3(['--items', 'a', 'b']) == ['a', 'b']",
            "h4_code": "def solve_h4(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--val', type=float, default=0.0)\n    parsed, unknown = p.parse_known_args(args_list)\n    return parsed.val, unknown", "h4_test": "assert solve_h4(['--val', '1.5', '--extra']) == (1.5, ['--extra'])",
            "h5_code": "def solve_h5(args_list):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('-v', '--verbose', action='count', default=0)\n    return p.parse_args(args_list).verbose", "h5_test": "assert solve_h5(['-v', '-v']) == 2",
            "rob_code": "def process_telemetry(data):\n    import argparse\n    p = argparse.ArgumentParser()\n    p.add_argument('--rate', type=float, default=10.0)\n    args = p.parse_args([])\n    return {'rate': args.rate, 'count': len(data)}", "rob_test": "assert process_telemetry([1])['rate'] == 10.0"
        }
    ),
    make_topic_data(
        topic_id="9.4", title="HTTP Requests and APIs", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="04_http_requests_apis", summary="requests library, REST APIs, HTTP methods (GET, POST, PUT, DELETE), status codes, and error handling.",
        why_it_matters="APIs connect robot systems to cloud backends and web services.",
        objectives=["Make HTTP requests with requests module.", "Parse JSON API responses.", "Handle status codes and HTTP timeouts."],
        prerequisites=["Topic 9.3 CLI"], domain="robotics-as-a-service platform", concepts=["requests", "REST API", "HTTP Methods"],
        code_snippets={
            "syntax": "import requests\nresp = requests.get('https://api.github.com')", "basic": "import requests\nr = requests.get('https://httpbin.org/get')\nprint(r.status_code)",
            "intermediate": "import requests\nr = requests.post('https://httpbin.org/post', json={'key': 'val'})\ndata = r.json()", "advanced": "import requests\ntry:\n    r = requests.get('https://httpbin.org/delay/1', timeout=2.0)\nexcept requests.Timeout:\n    print('Timed out')",
            "walkthrough": "import requests\nresponse = requests.get('https://httpbin.org/get', params={'robot_id': 'R1'})\nif response.status_code == 200:\n    print('Response received:', response.json().get('args'))",
            "pythonic": "response.raise_for_status()", "engineering": "import requests\ndef post_robot_telemetry(api_url, payload, timeout_s=3.0):\n    try:\n        resp = requests.post(api_url, json=payload, timeout=timeout_s)\n        resp.raise_for_status()\n        return True, resp.json()\n    except requests.RequestException as e:\n        return False, {'error': str(e)}",
            "m1_code": "def solve_m1(status_code):\n    return 200 <= status_code < 300", "m1_test": "assert solve_m1(200) is True and solve_m1(404) is False",
            "m2_code": "def solve_m2(url, params_dict):\n    import requests\n    req = requests.Request('GET', url, params=params_dict).prepare()\n    return req.url", "m2_test": "assert '?' in solve_m2('http://api.com', {'a': 1})",
            "m3_code": "def solve_m3(json_data):\n    import requests\n    req = requests.Request('POST', 'http://api.com', json=json_data).prepare()\n    return req.body.decode()", "m3_test": "assert '\"a\": 1' in solve_m3({'a': 1})",
            "m4_code": "def solve_m4(headers_dict):\n    import requests\n    req = requests.Request('GET', 'http://api.com', headers=headers_dict).prepare()\n    return req.headers.get('User-Agent')", "m4_test": "assert solve_m4({'User-Agent': 'Bot'}) == 'Bot'",
            "m5_code": "def solve_m5(status_code):\n    import requests\n    resp = requests.Response()\n    resp.status_code = status_code\n    try:\n        resp.raise_for_status()\n        return True\n    except requests.HTTPError:\n        return False", "m5_test": "assert solve_m5(200) is True and solve_m5(500) is False",
            "h1_code": "def solve_h1(status_code):\n    categories = {2: 'SUCCESS', 3: 'REDIRECT', 4: 'CLIENT_ERROR', 5: 'SERVER_ERROR'}\n    return categories.get(status_code // 100, 'UNKNOWN')", "h1_test": "assert solve_h1(404) == 'CLIENT_ERROR'",
            "h2_code": "def solve_h2(base_url, endpoint):\n    from urllib.parse import urljoin\n    return urljoin(base_url, endpoint)", "h2_test": "assert solve_h2('http://api.com/v1/', 'robots') == 'http://api.com/v1/robots'",
            "h3_code": "def solve_h3(token):\n    return {'Authorization': f'Bearer {token}'}", "h3_test": "assert solve_h3('secret') == {'Authorization': 'Bearer secret'}",
            "h4_code": "def solve_h4(d):\n    import json\n    return json.dumps(d)", "h4_test": "assert solve_h4({'x': 1}) == '{\"x\": 1}'",
            "h5_code": "def solve_h5(params_list):\n    from urllib.parse import urlencode\n    return urlencode(params_list)", "h5_test": "assert solve_h5([('a', 1), ('b', 2)]) == 'a=1&b=2'",
            "rob_code": "def process_telemetry(data):\n    mock_resp = {'status_code': 200, 'items_received': len(data)}\n    return mock_resp", "rob_test": "assert process_telemetry([1])['status_code'] == 200"
        }
    ),
    make_topic_data(
        topic_id="9.5", title="Unit Testing", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="05_unit_testing", summary="pytest framework, assert statements, fixtures, test discovery, and mocking.",
        why_it_matters="Automated unit testing prevents regressions and validates component specifications.",
        objectives=["Write pytest test functions with assertions.", "Use pytest fixtures.", "Mock external dependencies with unittest.mock."],
        prerequisites=["Topic 9.4 HTTP Requests"], domain="robotics-as-a-service platform", concepts=["pytest", "Unit Testing", "Fixtures", "Mocking"],
        code_snippets={
            "syntax": "def test_example():\n    assert 1 + 1 == 2", "basic": "import pytest\ndef add(a, b): return a + b\ndef test_add():\n    assert add(2, 3) == 5",
            "intermediate": "import pytest\n@pytest.fixture\ndef sample_robot():\n    return {'name': 'ROBO-X', 'battery': 100}\ndef test_robot(sample_robot):\n    assert sample_robot['battery'] == 100",
            "advanced": "from unittest.mock import MagicMock\ndef test_sensor():\n    sensor = MagicMock()\n    sensor.read.return_value = 42.0\n    assert sensor.read() == 42.0",
            "walkthrough": "import pytest\ndef divide(a, b):\n    if b == 0:\n        raise ValueError('Divide by zero')\n    return a / b\ndef test_divide_zero():\n    with pytest.raises(ValueError):\n        divide(10, 0)",
            "pythonic": "with pytest.raises(ValueError):\n    int('invalid')", "engineering": "import pytest\nfrom unittest.mock import patch\ndef test_telemetry_post():\n    with patch('requests.post') as mock_post:\n        mock_post.return_value.status_code = 200\n        # Call function that triggers requests.post\n        assert mock_post.called is False or True",
            "m1_code": "def solve_m1(a, b):\n    assert a == b\n    return True", "m1_test": "assert solve_m1(5, 5) is True",
            "m2_code": "def solve_m2(fn, exc_type):\n    try:\n        fn()\n        return False\n    except exc_type:\n        return True", "m2_test": "assert solve_m2(lambda: 1/0, ZeroDivisionError) is True",
            "m3_code": "def solve_m3():\n    from unittest.mock import MagicMock\n    m = MagicMock()\n    m.get_val.return_value = 100\n    return m.get_val()", "m3_test": "assert solve_m3() == 100",
            "m4_code": "def solve_m4(val):\n    assert isinstance(val, int)\n    return val", "m4_test": "assert solve_m4(10) == 10",
            "m5_code": "def solve_m5(lst):\n    assert len(lst) > 0\n    return lst[0]", "m5_test": "assert solve_m5([1]) == 1",
            "h1_code": "def solve_h1(target_fn, mock_val):\n    from unittest.mock import patch\n    with patch(target_fn) as mock:\n        mock.return_value = mock_val\n        return mock()\n    return None", "h1_test": "assert solve_h1('os.getcwd', '/mock/dir') == '/mock/dir'",
            "h2_code": "def solve_h2(fn, inputs, expected_outputs):\n    for x, y in zip(inputs, expected_outputs):\n        assert fn(x) == y\n    return True", "h2_test": "assert solve_h2(lambda x: x*2, [1, 2], [2, 4]) is True",
            "h3_code": "def solve_h3(fn):\n    from unittest.mock import MagicMock\n    m = MagicMock()\n    fn(m)\n    return m.called", "h3_test": "assert solve_h3(lambda m: m()) is True",
            "h4_code": "def solve_h4(m, arg):\n    m(arg)\n    m.assert_called_with(arg)\n    return True", "h4_test": "from unittest.mock import MagicMock; assert solve_h4(MagicMock(), 'x') is True",
            "h5_code": "def solve_h5(fn, exc_msg_substr):\n    try:\n        fn()\n        return False\n    except Exception as e:\n        return exc_msg_substr in str(e)", "h5_test": "assert solve_h5(lambda: ValueError('invalid state'), 'invalid') is True",
            "rob_code": "def process_telemetry(data):\n    assert isinstance(data, list)\n    return {'tested_count': len(data)}", "rob_test": "assert process_telemetry([1, 2])['tested_count'] == 2"
        }
    ),
    make_topic_data(
        topic_id="9.6", title="Code Style and Best Practices", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="06_code_style_best_practices", summary="PEP 8 compliance, flake8, black, isort, docstrings, and refactoring clean code.",
        why_it_matters="Consistent code style improves code maintainability across engineering teams.",
        objectives=["Adhere to PEP 8 style guidelines.", "Use automated formatters like black and flake8.", "Refactor messy code into clean idiomatic Python."],
        prerequisites=["Topic 9.5 Unit Testing"], domain="robotics-as-a-service platform", concepts=["PEP 8", "Code Style", "Refactoring", "Clean Code"],
        code_snippets={
            "syntax": "# PEP 8 style example:\ndef calculate_velocity(distance_m: float, time_s: float) -> float:\n    return distance_m / time_s",
            "basic": "def clean_name(raw_name: str) -> str:\n    \"\"\"Strip whitespace and uppercase string.\"\"\"\n    return raw_name.strip().upper()",
            "intermediate": "class RobotController:\n    \"\"\"Manages high-level robot state transitions.\"\"\"\n    def __init__(self, robot_id: str) -> None:\n        self.robot_id = robot_id",
            "advanced": "def refactored_pipeline(records):\n    \"\"\"Process valid telemetry records cleanly.\"\"\"\n    return [r for r in records if r.is_valid()]",
            "walkthrough": "def calculate_bmi(weight_kg: float, height_m: float) -> float:\n    \"\"\"Calculate BMI given weight in kg and height in meters.\"\"\"\n    if height_m <= 0:\n        raise ValueError('Height must be positive')\n    return weight_kg / (height_m ** 2)",
            "pythonic": "is_valid = bool(data)", "engineering": "def sanitize_config_dict(raw_config: dict) -> dict:\n    \"\"\"Clean and normalize configuration key-value pairs.\"\"\"\n    return {str(k).lower().strip(): v for k, v in raw_config.items()}",
            "m1_code": "def solve_m1(s: str) -> str:\n    return s.strip()", "m1_test": "assert solve_m1(' hi ') == 'hi'",
            "m2_code": "def solve_m2(name: str) -> bool:\n    return name.isidentifier() and name.islower()", "m2_test": "assert solve_m2('valid_var') is True",
            "m3_code": "def solve_m3(s: str) -> str:\n    return ' '.join(s.split())", "m3_test": "assert solve_m3('a   b') == 'a b'",
            "m4_code": "def solve_m4(line: str) -> bool:\n    return len(line) <= 79", "m4_test": "assert solve_m4('short line') is True",
            "m5_code": "def solve_m5(fn) -> str:\n    return getattr(fn, '__doc__', '') or ''", "m5_test": "def f(): 'doc'; pass\nassert solve_m5(f) == 'doc'",
            "h1_code": "def solve_h1(code_lines: list[str]) -> list[str]:\n    return [line.rstrip() for line in code_lines]", "h1_test": "assert solve_h1(['a  ', 'b ']) == ['a', 'b']",
            "h2_code": "def solve_h2(code_lines: list[str]) -> list[str]:\n    return [line.replace('\t', '    ') for line in code_lines]", "h2_test": "assert solve_h2(['\tx=1']) == ['    x=1']",
            "h3_code": "def solve_h3(imports: list[str]) -> list[str]:\n    return sorted(imports)", "h3_test": "assert solve_h3(['import sys', 'import os']) == ['import os', 'import sys']",
            "h4_code": "def solve_h4(camel_str: str) -> str:\n    import re\n    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()", "h4_test": "assert solve_h4('robotSpeed') == 'robot_speed'",
            "h5_code": "def solve_h5(d: dict) -> dict:\n    return {k: v for k, v in sorted(d.items())}", "h5_test": "assert list(solve_h5({'b': 1, 'a': 2}).keys()) == ['a', 'b']",
            "rob_code": "def process_telemetry(data: list) -> dict:\n    \"\"\"Process incoming robot telemetry data.\"\"\"\n    return {'clean': True, 'count': len(data)}", "rob_test": "assert process_telemetry([1])['clean'] is True"
        }
    ),
    make_topic_data(
        topic_id="9.7", title="Project Structure and Packaging", module=9, module_title="Intermediate Practical Skills and Best Practices",
        directory="07_project_structure_packaging", summary="src layout vs flat layout, pyproject.toml configuration, setuptools, and wheel generation.",
        why_it_matters="Professional project structure allows Python libraries to be distributed and installed.",
        objectives=["Organize code into src/ package layout.", "Configure pyproject.toml with setuptools build-backend.", "Build installable wheels."],
        prerequisites=["Topic 9.6 Code Style"], domain="robotics-as-a-service platform", concepts=["Project Structure", "pyproject.toml", "Packaging", "Wheels"],
        code_snippets={
            "syntax": "# pyproject.toml structure:\n[build-system]\nrequires = [\"setuptools>=61.0\"]\nbuild-backend = \"setuptools.build_meta\"",
            "basic": "def check_src_layout(root_dir):\n    from pathlib import Path\n    return (Path(root_dir) / 'src').exists()",
            "intermediate": "def generate_pyproject_toml(project_name, version):\n    return f'''[build-system]\nrequires = [\"setuptools>=61.0\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"{project_name}\"\nversion = \"{version}\"\n'''",
            "advanced": "def is_valid_package_name(name):\n    import re\n    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))",
            "walkthrough": "from pathlib import Path\nroot = Path('.')\nsrc_dir = root / 'src'\nprint('src layout exists:', src_dir.exists())",
            "pythonic": "toml_content = '[project]\\nname = \"robo_x\"\\nversion = \"1.0.0\"'",
            "engineering": "from pathlib import Path\ndef init_package_structure(target_dir, pkg_name):\n    root = Path(target_dir)\n    pkg_dir = root / 'src' / pkg_name\n    pkg_dir.mkdir(parents=True, exist_ok=True)\n    (pkg_dir / '__init__.py').write_text(f'\"\"\"{pkg_name} package\"\"\"\\n__version__ = \"0.1.0\"\\n')",
            "m1_code": "def solve_m1(pkg_name):\n    from pathlib import Path\n    p = Path('src') / pkg_name\n    return str(p)", "m1_test": "assert solve_m1('robo') == 'src/robo'",
            "m2_code": "def solve_m2(toml_str):\n    return '[build-system]' in toml_str and '[project]' in toml_str", "m2_test": "assert solve_m2('[build-system]\n[project]') is True",
            "m3_code": "def solve_m3(ver_str):\n    import re\n    return bool(re.match(r'^\\d+\\.\\d+\\.\\d+$', ver_str))", "m3_test": "assert solve_m3('1.0.0') is True and solve_m3('invalid') is False",
            "m4_code": "def solve_m4(pkg_dir):\n    from pathlib import Path\n    return (Path(pkg_dir) / '__init__.py').exists()", "m4_test": "assert solve_m4('shared') is True",
            "m5_code": "def solve_m5(name_str):\n    return name_str.replace('-', '_').lower()", "m5_test": "assert solve_m5('Robo-X') == 'robo_x'",
            "h1_code": "def solve_h1(proj_name, version, deps):\n    dep_str = ', '.join(f'\"{d}\"' for d in deps)\n    return f'[project]\\nname = \"{proj_name}\"\\nversion = \"{version}\"\\ndependencies = [{dep_str}]'", "h1_test": "assert 'dependencies = [\"numpy\"]' in solve_h1('p', '1.0', ['numpy'])",
            "h2_code": "def solve_h2(wheel_filename):\n    return wheel_filename.endswith('.whl')", "h2_test": "assert solve_h2('robo_x-1.0-py3-none-any.whl') is True",
            "h3_code": "def solve_h3(files_list):\n    return any(f.endswith('pyproject.toml') for f in files_list)", "h3_test": "assert solve_h3(['a.txt', 'pyproject.toml']) is True",
            "h4_code": "def solve_h4(pkg_root):\n    from pathlib import Path\n    return [str(f.relative_to(pkg_root)) for f in Path(pkg_root).rglob('*.py') if '__pycache__' not in f.parts]", "h4_test": "assert isinstance(solve_h4('shared'), list)",
            "h5_code": "def solve_h5(raw_version):\n    import re\n    parts = re.findall(r'\\d+', raw_version)\n    return '.'.join(parts[:3]) if len(parts) >= 3 else '0.1.0'", "h5_test": "assert solve_h5('v1.2.3-alpha') == '1.2.3'",
            "rob_code": "def process_telemetry(data):\n    return {'package_status': 'PACKAGED', 'count': len(data)}", "rob_test": "assert process_telemetry([1])['package_status'] == 'PACKAGED'"
        }
    )
]
