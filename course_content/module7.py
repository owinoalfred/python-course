"""Module 7 — File Handling and Working with Data (topics 7.1 - 7.6)."""

from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from self_created_tools.topic_builder import make_topic_data

TOPICS = [
    make_topic_data(
        topic_id="7.1", title="File Operations", module=7, module_title="File Handling and Working with Data",
        directory="01_file_operations", summary="open(), context managers (with statement), reading/writing text and binary files.",
        why_it_matters="File operations persist runtime state, logs, and telemetry data across program runs.",
        objectives=["Open files using open().", "Use context managers for safe cleanup.", "Read and write text and binary data."],
        prerequisites=["Module 6 Object-Oriented Programming"], domain="flight-test data pipeline", concepts=["File I/O", "open()", "with statement", "Context Managers"],
        code_snippets={
            "syntax": "with open('test.txt', 'w') as f:\n    f.write('hello')", "basic": "with open('test.txt', 'r') as f:\n    data = f.read()",
            "intermediate": "with open('lines.txt', 'w') as f:\n    f.writelines(['line1\\n', 'line2\\n'])", "advanced": "with open('binary.bin', 'wb') as f:\n    f.write(b'\\x00\\x01\\x02')",
            "walkthrough": "content = 'log_entry_01'\nwith open('log.txt', 'w') as f:\n    f.write(content)\nwith open('log.txt', 'r') as f:\n    read_back = f.read()\nprint('Read back:', read_back)",
            "pythonic": "lines = [line.strip() for line in open('test.txt')]", "engineering": "def write_telemetry_file(filepath, records):\n    with open(filepath, 'w') as f:\n        for r in records:\n            f.write(f'{r}\\n')",
            "m1_code": "def solve_m1(content):\n    import io\n    buf = io.StringIO()\n    buf.write(content)\n    return buf.getvalue()", "m1_test": "assert solve_m1('hello') == 'hello'",
            "m2_code": "def solve_m2(lines):\n    import io\n    buf = io.StringIO()\n    buf.writelines(lines)\n    return buf.getvalue()", "m2_test": "assert solve_m2(['a\\n', 'b\\n']) == 'a\\nb\\n'",
            "m3_code": "def solve_m3(text):\n    import io\n    buf = io.StringIO(text)\n    return buf.readlines()", "m3_test": "assert solve_m3('a\\nb\\n') == ['a\\n', 'b\\n']",
            "m4_code": "def solve_m4(data_bytes):\n    import io\n    buf = io.BytesIO(data_bytes)\n    return buf.read()", "m4_test": "assert solve_m4(b'123') == b'123'",
            "m5_code": "def solve_m5(text):\n    import io\n    buf = io.StringIO(text)\n    buf.seek(0)\n    return buf.read()", "m5_test": "assert solve_m5('test') == 'test'",
            "h1_code": "def solve_h1(text_stream):\n    import io\n    buf = io.StringIO(text_stream)\n    return sum(1 for line in buf if line.strip())", "h1_test": "assert solve_h1('a\\n\\nb\\n') == 2",
            "h2_code": "def solve_h2(text_stream):\n    import io\n    buf = io.StringIO(text_stream)\n    return [line.strip() for line in buf if not line.strip().startswith('#')]", "h2_test": "assert solve_h2('a\\n# comment\\nb') == ['a', 'b']",
            "h3_code": "def solve_h3(kv_text):\n    import io\n    buf = io.StringIO(kv_text)\n    d = {}\n    for line in buf:\n        if '=' in line:\n            k, v = line.strip().split('=', 1)\n            d[k] = v\n    return d", "h3_test": "assert solve_h3('a=1\\nb=2') == {'a': '1', 'b': '2'}",
            "h4_code": "def solve_h4(data_bytes):\n    import io\n    buf = io.BytesIO(data_bytes)\n    return len(buf.getvalue())", "h4_test": "assert solve_h4(b'abc') == 3",
            "h5_code": "def solve_h5(lines):\n    import io\n    buf = io.StringIO()\n    for i, line in enumerate(lines, 1):\n        buf.write(f'{i}: {line}\\n')\n    return buf.getvalue()", "h5_test": "assert '1: hello' in solve_h5(['hello'])",
            "rob_code": "def process_telemetry(data):\n    import io\n    buf = io.StringIO()\n    for item in data:\n        buf.write(f'{item}\\n')\n    return {'size': len(buf.getvalue())}", "rob_test": "assert process_telemetry(['10.5'])['size'] > 0"
        }
    ),
    make_topic_data(
        topic_id="7.2", title="Working with Paths", module=7, module_title="File Handling and Working with Data",
        directory="02_working_with_paths", summary="pathlib module, Path objects, path manipulation, and cross-platform file paths.",
        why_it_matters="pathlib provides object-oriented, cross-platform filesystem paths.",
        objectives=["Create and manipulate Path objects.", "Check file existence, extension, and parent directories.", "Glob directory trees."],
        prerequisites=["Topic 7.1 File Operations"], domain="flight-test data pipeline", concepts=["pathlib", "Path", "glob"],
        code_snippets={
            "syntax": "from pathlib import Path\np = Path('data') / 'sub' / 'file.txt'", "basic": "from pathlib import Path\np = Path('.')\nprint(p.resolve())",
            "intermediate": "from pathlib import Path\np = Path('logs/telemetry.csv')\nprint(p.suffix, p.stem, p.parent)", "advanced": "from pathlib import Path\nfiles = list(Path('.').glob('*.py'))",
            "walkthrough": "from pathlib import Path\np = Path('build/logs/data.txt')\nprint('Stem:', p.stem)\nprint('Suffix:', p.suffix)\nprint('Parent:', p.parent)",
            "pythonic": "p = Path('a/b/c.txt').with_suffix('.json')", "engineering": "from pathlib import Path\ndef ensure_dir(dir_path):\n    p = Path(dir_path)\n    p.mkdir(parents=True, exist_ok=True)\n    return p.exists()",
            "m1_code": "def solve_m1(path_str):\n    from pathlib import Path\n    return Path(path_str).suffix", "m1_test": "assert solve_m1('data.csv') == '.csv'",
            "m2_code": "def solve_m2(path_str):\n    from pathlib import Path\n    return Path(path_str).stem", "m2_test": "assert solve_m2('data.csv') == 'data'",
            "m3_code": "def solve_m3(p1, p2):\n    from pathlib import Path\n    return str(Path(p1) / p2)", "m3_test": "assert 'a' in solve_m3('a', 'b')",
            "m4_code": "def solve_m4(path_str, new_ext):\n    from pathlib import Path\n    return str(Path(path_str).with_suffix(new_ext))", "m4_test": "assert solve_m4('file.txt', '.json') == 'file.json'",
            "m5_code": "def solve_m5(path_str):\n    from pathlib import Path\n    return str(Path(path_str).parent)", "m5_test": "assert solve_m5('a/b/c.txt') == 'a/b'",
            "h1_code": "def solve_h1(path_str):\n    from pathlib import Path\n    p = Path(path_str)\n    return {'name': p.name, 'stem': p.stem, 'suffix': p.suffix, 'parent': str(p.parent)}", "h1_test": "assert solve_h1('a/b.csv')['suffix'] == '.csv'",
            "h2_code": "def solve_h2(dir_path, ext):\n    from pathlib import Path\n    return [f.name for f in Path(dir_path).glob(f'*{ext}')]", "h2_test": "assert isinstance(solve_h2('tools', '.py'), list)",
            "h3_code": "def solve_h3(path_str):\n    from pathlib import Path\n    return Path(path_str).is_absolute()", "h3_test": "assert solve_h3('/tmp/test') is True or solve_h3('C:\\\\test') is True",
            "h4_code": "def solve_h4(path_str):\n    from pathlib import Path\n    return str(Path(path_str).resolve())", "h4_test": "assert isinstance(solve_h4('.'), str)",
            "h5_code": "def solve_h5(paths_list):\n    from pathlib import Path\n    return [str(Path(p)) for p in paths_list if Path(p).suffix == '.json']", "h5_test": "assert solve_h5(['a.json', 'b.txt']) == ['a.json']",
            "rob_code": "def process_telemetry(data):\n    from pathlib import Path\n    p = Path('telemetry/readings.csv')\n    return {'ext': p.suffix, 'count': len(data)}", "rob_test": "assert process_telemetry([1])['ext'] == '.csv'"
        }
    ),
    make_topic_data(
        topic_id="7.3", title="JSON and CSV", module=7, module_title="File Handling and Working with Data",
        directory="03_json_and_csv", summary="json module (dumps, loads, dump, load) and csv module (reader, writer, DictReader, DictWriter).",
        why_it_matters="JSON and CSV are universal formats for configuration, serialization, and telemetry datasets.",
        objectives=["Serialize and deserialize JSON.", "Read and write CSV files with csv.reader and csv.DictReader.", "Handle parsing errors."],
        prerequisites=["Topic 7.2 Working with Paths"], domain="flight-test data pipeline", concepts=["JSON", "CSV", "Serialization"],
        code_snippets={
            "syntax": "import json, csv\ndata = json.loads('{\"x\": 1}')", "basic": "import json\ntext = json.dumps({'id': 'ROBO-X', 'battery': 98.5})",
            "intermediate": "import csv, io\nstream = io.StringIO('a,b\\n1,2\\n')\nreader = csv.DictReader(stream)\nfor row in reader:\n    print(row)", "advanced": "import json\nclass RobotEncoder(json.JSONEncoder):\n    def default(self, o):\n        return o.__dict__",
            "walkthrough": "import json, csv, io\njson_str = '{\"status\": \"OK\", \"code\": 200}'\nparsed = json.loads(json_str)\nprint('Code:', parsed['code'])",
            "pythonic": "parsed = json.loads(raw_json_string)", "engineering": "import csv, io\ndef export_telemetry_csv(records):\n    stream = io.StringIO()\n    if not records: return ''\n    writer = csv.DictWriter(stream, fieldnames=records[0].keys())\n    writer.writeheader()\n    writer.writerows(records)\n    return stream.getvalue()",
            "m1_code": "def solve_m1(d):\n    import json\n    return json.dumps(d)", "m1_test": "assert solve_m1({'a': 1}) == '{\"a\": 1}'",
            "m2_code": "def solve_m2(json_str):\n    import json\n    return json.loads(json_str)", "m2_test": "assert solve_m2('{\"a\": 1}') == {'a': 1}",
            "m3_code": "def solve_m3(csv_text):\n    import csv, io\n    buf = io.StringIO(csv_text)\n    return list(csv.reader(buf))", "m3_test": "assert solve_m3('a,b\\n1,2') == [['a', 'b'], ['1', '2']]",
            "m4_code": "def solve_m4(csv_text):\n    import csv, io\n    buf = io.StringIO(csv_text)\n    return list(csv.DictReader(buf))", "m4_test": "assert solve_m4('a,b\\n1,2')[0] == {'a': '1', 'b': '2'}",
            "m5_code": "def solve_m5(rows):\n    import csv, io\n    buf = io.StringIO()\n    w = csv.writer(buf)\n    w.writerows(rows)\n    return buf.getvalue()", "m5_test": "assert 'a,b' in solve_m5([['a', 'b']])",
            "h1_code": "def solve_h1(d_list):\n    import json\n    return [json.dumps(d) for d in d_list]", "h1_test": "assert solve_h1([{'a': 1}]) == ['{\"a\": 1}']",
            "h2_code": "def solve_h2(records):\n    import csv, io\n    buf = io.StringIO()\n    if records:\n        w = csv.DictWriter(buf, fieldnames=records[0].keys())\n        w.writeheader()\n        w.writerows(records)\n    return buf.getvalue()", "h2_test": "assert 'a' in solve_h2([{'a': 1}])",
            "h3_code": "def solve_h3(json_str):\n    import json\n    try:\n        return True, json.loads(json_str)\n    except Exception as e:\n        return False, str(e)", "h3_test": "assert solve_h3('{\"a\": 1}')[0] is True",
            "h4_code": "def solve_h4(d):\n    import json\n    return json.dumps(d, indent=2, sort_keys=True)", "h4_test": "assert '\\n' in solve_h4({'b': 2, 'a': 1})",
            "h5_code": "def solve_h5(csv_text, col_name):\n    import csv, io\n    buf = io.StringIO(csv_text)\n    r = csv.DictReader(buf)\n    return [row[col_name] for row in r if col_name in row]", "h5_test": "assert solve_h5('id,val\\n1,10\\n2,20', 'val') == ['10', '20']",
            "rob_code": "def process_telemetry(data):\n    import json\n    payload = json.dumps({'readings': data, 'valid': True})\n    return {'json_payload': payload}", "rob_test": "assert 'readings' in process_telemetry([1.0])['json_payload']"
        }
    ),
    make_topic_data(
        topic_id="7.4", title="Error Handling in File Operations", module=7, module_title="File Handling and Working with Data",
        directory="04_error_handling_file_operations", summary="Handling FileNotFoundError, PermissionError, OSError, and corrupted files.",
        why_it_matters="Robust file handling defends against missing files, permissions issues, and corrupted media.",
        objectives=["Catch FileNotFoundError and PermissionError.", "Implement fallback default files.", "Safely handle corrupt data."],
        prerequisites=["Topic 7.3 JSON and CSV"], domain="flight-test data pipeline", concepts=["FileNotFoundError", "PermissionError", "OSError"],
        code_snippets={
            "syntax": "try:\n    open('missing.txt')\nexcept FileNotFoundError:\n    pass", "basic": "try:\n    with open('nonexistent.txt') as f:\n        data = f.read()\nexcept FileNotFoundError:\n    data = ''",
            "intermediate": "import json\ndef safe_load_json(filepath, default={}):\n    try:\n        with open(filepath) as f:\n            return json.load(f)\n    except (FileNotFoundError, json.JSONDecodeError):\n        return default", "advanced": "try:\n    with open('/root/protected.txt', 'w') as f:\n        f.write('x')\nexcept PermissionError:\n    print('Access denied')",
            "walkthrough": "def load_config(path):\n    try:\n        with open(path) as f:\n            return f.read()\n    except FileNotFoundError:\n        return 'DEFAULT_CONFIG'",
            "pythonic": "from pathlib import Path\ntext = Path('file.txt').read_text() if Path('file.txt').exists() else ''", "engineering": "import json\ndef load_robot_params(filepath):\n    try:\n        with open(filepath) as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return {'status': 'DEFAULT_PARAMS'}\n    except json.JSONDecodeError:\n        return {'status': 'CORRUPTED_FILE'}",
            "m1_code": "def solve_m1(filename):\n    try:\n        with open(filename) as f: return f.read()\n    except FileNotFoundError: return 'MISSING'", "m1_test": "assert solve_m1('nonexistent_file_xyz.txt') == 'MISSING'",
            "m2_code": "def solve_m2(filename):\n    try:\n        with open(filename, 'w') as f: f.write('x')\n        return True\n    except PermissionError: return False\n    except Exception: return False", "m2_test": "assert solve_m2('/invalid_dir/file.txt') is False",
            "m3_code": "def solve_m3(json_text):\n    import json\n    try:\n        return json.loads(json_text)\n    except json.JSONDecodeError:\n        return {}", "m3_test": "assert solve_m3('invalid json') == {}",
            "m4_code": "def solve_m4(filename):\n    try:\n        open(filename)\n        return True\n    except OSError:\n        return False", "m4_test": "assert solve_m4('missing_123.txt') is False",
            "m5_code": "def solve_m5(filename, default_text):\n    try:\n        with open(filename) as f: return f.read()\n    except FileNotFoundError: return default_text", "m5_test": "assert solve_m5('missing.txt', 'default') == 'default'",
            "h1_code": "def solve_h1(filenames):\n    results = {}\n    for fname in filenames:\n        try:\n            with open(fname) as f:\n                results[fname] = f.read()\n        except Exception as e:\n            results[fname] = type(e).__name__\n    return results", "h1_test": "assert solve_h1(['missing.txt']) == {'missing.txt': 'FileNotFoundError'}",
            "h2_code": "def solve_h2(filepath, content):\n    from pathlib import Path\n    try:\n        p = Path(filepath)\n        p.parent.mkdir(parents=True, exist_ok=True)\n        p.write_text(content)\n        return True\n    except Exception:\n        return False", "h2_test": "assert solve_h2('test_out/f.txt', 'hi') is True",
            "h3_code": "def solve_h3(json_str_list):\n    import json\n    valid = []\n    for s in json_str_list:\n        try:\n            valid.append(json.loads(s))\n        except json.JSONDecodeError:\n            continue\n    return valid", "h3_test": "assert solve_h3(['{\"a\": 1}', 'bad']) == [{'a': 1}]",
            "h4_code": "def solve_h4(csv_str):\n    import csv, io\n    try:\n        buf = io.StringIO(csv_str)\n        return list(csv.reader(buf))\n    except Exception:\n        return []", "h4_test": "assert solve_h4('a,b\\n1,2') == [['a', 'b'], ['1', '2']]",
            "h5_code": "def solve_h5(filename):\n    import os\n    try:\n        os.remove(filename)\n        return True\n    except FileNotFoundError:\n        return False", "h5_test": "assert solve_h5('nonexistent.file') is False",
            "rob_code": "def process_telemetry(data):\n    status = 'OK'\n    try:\n        if not data: raise FileNotFoundError('No data file')\n    except FileNotFoundError:\n        status = 'FILE_NOT_FOUND'\n    return {'status': status}", "rob_test": "assert process_telemetry([])['status'] == 'FILE_NOT_FOUND'"
        }
    ),
    make_topic_data(
        topic_id="7.5", title="Regular Expressions", module=7, module_title="File Handling and Working with Data",
        directory="05_regular_expressions", summary="re module (search, match, findall, sub), regex syntax, capture groups, and flags.",
        why_it_matters="Regular expressions parse complex text patterns in logs and telemetry strings.",
        objectives=["Search text using re.search and re.findall.", "Extract pattern groups.", "Replace text with re.sub."],
        prerequisites=["Topic 7.4 Error Handling in Files"], domain="flight-test data pipeline", concepts=["Regex", "re", "Pattern Matching"],
        code_snippets={
            "syntax": "import re\nmatch = re.search(r'\\d+', 'item 42')", "basic": "import re\nfound = re.findall(r'\\b[A-Z]+\\b', 'INFO: System OK')",
            "intermediate": "import re\npattern = r'(\\d{4})-(\\d{2})-(\\d{2})'\nm = re.match(pattern, '2026-10-03')\nif m: print(m.groups())", "advanced": "import re\nclean = re.sub(r'\\s+', ' ', '  too   many   spaces  ')",
            "walkthrough": "import re\nline = 'SENSOR_1: TEMP=42.5 C'\nm = re.search(r'TEMP=(\\d+\\.\\d+)', line)\nif m:\n    print('Temperature:', m.group(1))",
            "pythonic": "import re\nis_valid = bool(re.match(r'^[a-zA-Z0-9_]+$', 'valid_name'))", "engineering": "import re\ndef parse_log_line(line):\n    pattern = r'^\\[(?P<level>\\w+)\\]\\s+(?P<msg>.*)$'\n    m = re.match(pattern, line)\n    return m.groupdict() if m else {}",
            "m1_code": "def solve_m1(text):\n    import re\n    return re.findall(r'\\d+', text)", "m1_test": "assert solve_m1('a12b34') == ['12', '34']",
            "m2_code": "def solve_m2(text):\n    import re\n    return bool(re.search(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b', text))", "m2_test": "assert solve_m2('user@test.com') is True",
            "m3_code": "def solve_m3(text, target, replacement):\n    import re\n    return re.sub(target, replacement, text)", "m3_test": "assert solve_m3('a1b2', r'\\d', 'X') == 'aXbX'",
            "m4_code": "def solve_m4(text):\n    import re\n    m = re.search(r'(\\d{4})-(\\d{2})-(\\d{2})', text)\n    return m.groups() if m else ()", "m4_test": "assert solve_m4('Date: 2026-10-03') == ('2026', '10', '03')",
            "m5_code": "def solve_m5(text):\n    import re\n    return re.split(r'[,;\\s]+', text.strip())", "m5_test": "assert solve_m5('a, b; c') == ['a', 'b', 'c']",
            "h1_code": "def solve_h1(text):\n    import re\n    return re.findall(r'\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b', text)", "h1_test": "assert solve_h1('IP: 10.0.0.1') == ['10.0.0.1']",
            "h2_code": "def solve_h2(text):\n    import re\n    pattern = r'^(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})$'\n    m = re.match(pattern, text)\n    return m.groupdict() if m else {}", "h2_test": "assert solve_h2('2026-10-03')['year'] == '2026'",
            "h3_code": "def solve_h3(text):\n    import re\n    return re.sub(r'<[^>]+>', '', text)", "h3_test": "assert solve_h3('<p>text</p>') == 'text'",
            "h4_code": "def solve_h4(text):\n    import re\n    return re.findall(r'#\\w+', text)", "h4_test": "assert solve_h4('Hello #python #robotics') == ['#python', '#robotics']",
            "h5_code": "def solve_h5(text):\n    import re\n    return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d).{8,}$', text))", "h5_test": "assert solve_h5('Pass1234') is True and solve_h5('weak') is False",
            "rob_code": "def process_telemetry(data):\n    import re\n    raw_str = ' '.join(str(x) for x in data)\n    numbers = [float(n) for n in re.findall(r'[-+]?\\d*\\.?\\d+', raw_str)]\n    return {'parsed_numbers': numbers}", "rob_test": "assert process_telemetry(['speed=12.5m/s'])['parsed_numbers'] == [12.5]"
        }
    ),
    make_topic_data(
        topic_id="7.6", title="Core Data Libraries", module=7, module_title="File Handling and Working with Data",
        directory="06_core_data_libraries", summary="NumPy, Pandas, Matplotlib, and Seaborn for data manipulation and visualization.",
        why_it_matters="NumPy and Pandas power modern scientific data processing pipelines.",
        objectives=["Process multi-dimensional arrays with NumPy.", "Manipulate DataFrames with Pandas.", "Plot telemetry data using Matplotlib."],
        prerequisites=["Topic 7.5 Regular Expressions"], domain="flight-test data pipeline", concepts=["NumPy", "Pandas", "Matplotlib", "Seaborn"],
        code_snippets={
            "syntax": "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt", "basic": "import numpy as np\narr = np.array([1, 2, 3])\nprint(arr.mean())",
            "intermediate": "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2], 'b': [10, 20]})\nprint(df['a'].mean())", "advanced": "import numpy as np\nmatrix = np.zeros((3, 3))\nmatrix[1, 1] = 1.0",
            "walkthrough": "import pandas as pd\ndata = {'time_s': [0.0, 1.0, 2.0], 'speed': [0.0, 1.5, 3.0]}\ndf = pd.DataFrame(data)\nprint('Mean speed:', df['speed'].mean())",
            "pythonic": "import numpy as np\nfiltered = arr[arr > 0.0]", "engineering": "import pandas as pd\ndef summarize_telemetry_df(df):\n    return {'mean_speed': float(df['speed'].mean()), 'max_speed': float(df['speed'].max())}",
            "m1_code": "def solve_m1(lst):\n    import numpy as np\n    return float(np.array(lst).mean())", "m1_test": "assert solve_m1([1, 2, 3]) == 2.0",
            "m2_code": "def solve_m2(lst):\n    import numpy as np\n    return float(np.array(lst).std())", "m2_test": "assert solve_m2([2, 2, 2]) == 0.0",
            "m3_code": "def solve_m3(d):\n    import pandas as pd\n    df = pd.DataFrame(d)\n    return list(df.columns)", "m3_test": "assert solve_m3({'a': [1], 'b': [2]}) == ['a', 'b']",
            "m4_code": "def solve_m4(d, col_name):\n    import pandas as pd\n    df = pd.DataFrame(d)\n    return float(df[col_name].sum())", "m4_test": "assert solve_m4({'val': [10, 20]}, 'val') == 30.0",
            "m5_code": "def solve_m5(n):\n    import numpy as np\n    return np.zeros(n).tolist()", "m5_test": "assert solve_m5(3) == [0.0, 0.0, 0.0]",
            "h1_code": "def solve_h1(matrix_list):\n    import numpy as np\n    arr = np.array(matrix_list)\n    return arr.T.tolist()", "h1_test": "assert solve_h1([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]",
            "h2_code": "def solve_h2(d, col, threshold):\n    import pandas as pd\n    df = pd.DataFrame(d)\n    filtered = df[df[col] > threshold]\n    return filtered.to_dict(orient='records')", "h2_test": "assert solve_h2({'val': [1, 5]}, 'val', 2) == [{'val': 5}]",
            "h3_code": "def solve_h3(lst):\n    import numpy as np\n    arr = np.array(lst)\n    return arr[arr > 0].tolist()", "h3_test": "assert solve_h3([-1, 1, 2]) == [1, 2]",
            "h4_code": "def solve_h4(d1, d2, key):\n    import pandas as pd\n    df1 = pd.DataFrame(d1)\n    df2 = pd.DataFrame(d2)\n    merged = pd.merge(df1, df2, on=key)\n    return merged.to_dict(orient='records')", "h4_test": "assert solve_h4({'id': [1], 'a': [10]}, {'id': [1], 'b': [20]}, 'id') == [{'id': 1, 'a': 10, 'b': 20}]",
            "h5_code": "def solve_h5(rows, cols):\n    import numpy as np\n    return np.eye(rows, cols).tolist()", "h5_test": "assert solve_h5(2, 2) == [[1.0, 0.0], [0.0, 1.0]]",
            "rob_code": "def process_telemetry(data):\n    import pandas as pd\n    df = pd.DataFrame({'sensor_val': data})\n    return {'avg_val': float(df['sensor_val'].mean()) if not df.empty else 0.0}", "rob_test": "assert process_telemetry([10.0, 20.0])['avg_val'] == 15.0"
        }
    )
]
