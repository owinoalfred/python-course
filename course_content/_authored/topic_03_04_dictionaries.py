"""Topic 3.4 - Dictionaries.

Hand-authored to the Course Content Standard. The spine: a dict maps unique
hashable keys to values in (amortised) constant time - and the three silent
failures are get() masking missing data, shallow copies sharing nested state,
and mutation during iteration.
"""

from __future__ import annotations

from tools.coursegen.dsl import (
    BULLETS,
    CODE,
    CODE_CELL,
    EQUATION,
    MD,
    NOTE,
    STEPS,
    TABLE,
    TIP,
    WARN,
    exercise,
    quiz,
    solution,
    topic,
)

LESSON: dict[str, list] = {}

LESSON["conceptual_explanation"] = [
    MD(
        "A dict is Python's hash map: a set of unique, hashable **keys**, each "
        "bound to a **value**, retrievable in amortised O(1) time. It is the "
        "language's default record type - a config blob, a status snapshot, a "
        "JSON object - because it states the association directly: `config['timeout'] "
        "= 30` reads as 'timeout means 30' in a way two parallel lists never "
        "could."
    ),
    MD(
        "Three properties define the type. **Keys are unique**: assigning an "
        "existing key replaces its value, it does not create a second entry - "
        "which makes dicts natural for grouping and counting. **Keys must be "
        "hashable**: strings, numbers and tuples qualify; lists and dicts do "
        "not. **Order is insertion order**: guaranteed since Python 3.7, so a "
        "dict iterates exactly as data was added - a contract you can rely on "
        "for reproducible output."
    ),
    CODE_CELL(
        "config = {'timeout': 30, 'retries': 3}\n"
        "print('value:', config['timeout'])\n"
        "\n"
        "config['timeout'] = 45            # update in place\n"
        "config['timeout'] = 50            # unique key: REPLACES, no duplicate\n"
        "print('keys :', list(config))      # insertion order preserved\n"
        "\n"
        "try:\n"
        "    print(config['missing'])\n"
        "except KeyError as exc:\n"
        "    print('missing key raises:', exc)"
    ),
    MD(
        "The KeyError is the dict's most important behaviour: `d[k]` is a "
        "**contract** - the key must exist, or the program fails loudly at the "
        "point of use. When absence is normal, you opt into a different "
        "operation deliberately: `d.get(k, default)` for a fallback, `k in d` "
        "to test first, `d.setdefault(k, factory)` to fill on demand. Each "
        "answers a different question, and choosing `get` when you meant `[]` "
        "is how missing configuration becomes a silent wrong number."
    ),
    MD(
        "Under the hood the dict is a compact hash table with indices derived "
        "from key hashes - which is why keys must be immutable (a changing "
        "hash would lose the entry) and why lookup stays O(1) regardless of "
        "size. Values have no such restriction: anything at all may live on "
        "the value side, including other dicts and lists."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Formally a dict implements a finite mapping from hashable keys to "
        "values. Construction, indexing, deletion and membership are "
        "amortised O(1) expected; iteration walks the insertion-ordered key "
        "sequence. The identities worth memorising:"
    ),
    EQUATION("d[k] raises KeyError if k is absent   |   d.get(k, default) returns default   |   k in d tests without fetching"),
    CODE_CELL(
        "levels = {'info': 20, 'warn': 10, 'fault': 1}\n"
        "\n"
        "print('direct :', levels['warn'])\n"
        "print('get    :', levels.get('trace', 0))\n"
        "print('test   :', 'fault' in levels)\n"
        "print('pop    :', levels.pop('info'))\n"
        "print('now    :', dict(levels))"
    ),
    TABLE(
        ["Operation", "Time", "Notes"],
        [
            ["d[k], d[k] = v", "amortised O(1)", "hash + probe"],
            ["d.get(k, default)", "amortised O(1)", "absence returns the default"],
            ["k in d", "amortised O(1)", "tests presence without fetching"],
            ["del d[k]", "amortised O(1)", "KeyError if absent"],
            ["d.update(other)", "O(len(other))", "merge, overwriting on conflict"],
            ["dict(d)", "O(n)", "shallow copy - values are shared"],
            ["iteration / keys()", "O(n)", "in insertion order"],
        ],
    ),
    MD(
        "The views - `d.keys()`, `d.values()`, `d.items()` - are live, "
        "read-only views over the dict, not snapshots: iterating them while "
        "the dict changes raises RuntimeError exactly as sets do, and `list(d) "
        "- d.keys()` style set operations work because keys() behaves like a "
        "set. Values may be unhashable - `[d[v] for v in d.values()]` is "
        "perfectly legal - because only the key side must hash."
    ),
    MD(
        "Two construction forms are worth distinguishing: `dict(pairs)` builds "
        "from (key, value) pairs or from a mapping, while the literal "
        "`{k: v}` and the comprehension `{k_expr: v_expr for ...}` build "
        "directly. A comprehension that can be expressed as `dict(zip(keys, "
        "values))` is usually clearer - and zip's length rule (shortest wins) "
        "becomes a correctness question you must answer deliberately."
    ),
]

LESSON["syntax"] = [
    MD("Literal creation, safe access, merging, and the comprehension form."),
    CODE_CELL(
        "telemetry = {'rate_hz': 100, 'channel': 'imu'}   # literal\n"
        "empty = {}                                       # a real dict\n"
        "from_pairs = dict([('a', 1), ('b', 2)])          # from pairs\n"
        "from_keys = dict.fromkeys(('x', 'y'), 0)         # shared default\n"
        "\n"
        "print('literal:', telemetry)\n"
        "print('pairs  :', from_pairs)\n"
        "print('defaults:', from_keys)\n"
        "\n"
        "rate = telemetry.get('rate_hz', 0)\n"
        "absent = telemetry.get('gain', 1.0)\n"
        "print('rate:', rate, ' absent default:', absent)"
    ),
    MD("The anti-pattern - get() with a default where a missing key is a real error:"),
    CODE(
        "timeout = config.get('timeout')      # None when missing...\n"
        "socket.settimeout(timeout)           # ...and fails HERE, far away\n"
        "\n"
        "timeout = config['timeout']          # fails at the source: KeyError\n"
        "# names the exact missing key, at the line that assumed it exists",
        lang="text",
    ),
    WARN(
        "get() hides provenance",
        "`d.get(k, 0)` turns a typo'd key into a plausible zero that flows "
        "downstream. Use `[]` when the key must exist, and `get` only when "
        "absence is a documented, expected case with a meaningful default.",
    ),
    MD("Merging and the mutating update, plus the comprehension that reads like its SQL:"),
    CODE_CELL(
        "base = {'host': 'localhost', 'port': 8080}\n"
        "override = {'port': 9090, 'debug': True}\n"
        "\n"
        "merged = base | override                 # new dict, override wins\n"
        "print('merged :', merged)\n"
        "\n"
        "combined = {k: v for k, v in merged.items() if v is not None}\n"
        "print('filtered:', combined)\n"
        "\n"
        "counts = {}\n"
        "for tag in ('a', 'b', 'a'):\n"
        "    counts[tag] = counts.get(tag, 0) + 1\n"
        "print('counts :', counts)"
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - build, fetch, and update a status record.**"),
    CODE_CELL(
        "status = {}\n"
        "status['name'] = 'rover-01'\n"
        "status['battery_pct'] = 88.5\n"
        "status.update({'mode': 'explore'})\n"
        "\n"
        "print('status :', status)\n"
        "print('name   :', status['name'])\n"
        "print('keys   :', list(status))\n"
        "print('values :', list(status.values()))"
    ),
    MD("**Example 2 - iterate items in insertion order.**"),
    CODE_CELL(
        "limits = {'temp_max': 60.0, 'temp_min': -10.0, 'rate_max': 250}\n"
        "for name, limit in limits.items():\n"
        "    print(f'{name:<10} {limit}')\n"
        "\n"
        "print('all names sorted:', sorted(limits))"
    ),
    MD("**Example 3 - counting with get(), the pattern behind Counter.**"),
    CODE_CELL(
        "words = 'go hold go stop go'.split()\n"
        "counts = {}\n"
        "for word in words:\n"
        "    counts[word] = counts.get(word, 0) + 1\n"
        "print('counts:', counts)\n"
        "print('most frequent:', max(counts, key=counts.get))"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "**Grouping with setdefault** - the one-liner that builds "
        "dict-of-lists: the key's list is created on first sight, appended to "
        "on every sight after."
    ),
    CODE_CELL(
        "by_kind = {}\n"
        "events = [('imu', 'boot'), ('gps', 'fix'), ('imu', 'drift')]\n"
        "\n"
        "for kind, detail in events:\n"
        "    by_kind.setdefault(kind, []).append(detail)\n"
        "\n"
        "print('grouped:', by_kind)"
    ),
    MD(
        "**Reversing a mapping** exposes the uniqueness rule: two keys with "
        "the same value collapse under inversion, so the design must say which "
        "one wins."
    ),
    CODE_CELL(
        "ports = {'http': 80, 'https': 443, 'alt_https': 443}\n"
        "reversed_map = {v: k for k, v in ports.items()}\n"
        "print('reversed:', reversed_map)   # 443 appears once - last key wins\n"
        "\n"
        "ambiguous = [v for v in ports.values() if list(ports.values()).count(v) > 1]\n"
        "print('collision values:', sorted(set(ambiguous)))"
    ),
    MD(
        "**Nested records and the copy trap preview.** Reading through two "
        "levels is ordinary; copying the outer dict and editing the nested "
        "record is where aliasing returns."
    ),
    CODE_CELL(
        "robots = {\n"
        "    'rover-01': {'x': 0.0, 'y': 0.0},\n"
        "    'rover-02': {'x': 3.0, 'y': 1.0},\n"
        "}\n"
        "\n"
        "snapshot = dict(robots)             # SHALLOW copy\n"
        "snapshot['rover-01']['x'] = 99.0    # mutates the SHARED inner dict\n"
        "print('original x :', robots['rover-01']['x'])   # 99.0 - corrupted!\n"
        "print('snapshot x :', snapshot['rover-01']['x'])"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "**Mutation during iteration** raises RuntimeError the moment a key "
        "is added or deleted - the guard exists because a resizing table "
        "invalidates the iterator. The clean patterns: iterate a snapshot of "
        "the keys, or rebuild into a new dict."
    ),
    CODE_CELL(
        "thresholds = {'a': 1, 'b': 2, 'c': 3}\n"
        "try:\n"
        "    for key in thresholds:\n"
        "        if thresholds[key] < 2:\n"
        "            del thresholds[key]\n"
        "except RuntimeError as exc:\n"
        "    print('caught:', exc)\n"
        "\n"
        "thresholds = {'a': 1, 'b': 2, 'c': 3}\n"
        "kept = {k: v for k, v in thresholds.items() if v >= 2}\n"
        "print('rebuilt :', kept)"
    ),
    MD(
        "**setdefault's dark side.** It eagerly builds the default even when "
        "the key exists - so `d.setdefault(k, [])` inside a loop over a "
        "million keys allocates a million empty lists that are immediately "
        "discarded. The `get`-then-branch form or a `defaultdict` avoids it."
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "keys = [f'k{i}' for i in range(200000)]\n"
        "\n"
        "start = time.perf_counter()\n"
        "d1 = {}\n"
        "for k in keys:\n"
        "    d1.setdefault(k, [])       # builds a throwaway list every hit\n"
        "setdefault_s = time.perf_counter() - start\n"
        "\n"
        "start = time.perf_counter()\n"
        "d2 = {}\n"
        "for k in keys:\n"
        "    if k not in d2:\n"
        "        d2[k] = []             # allocate only on a real miss\n"
        "branch_s = time.perf_counter() - start\n"
        "\n"
        "print(f'setdefault {setdefault_s:.3f}s vs branch {branch_s:.3f}s')"
    ),
    TIP(
        "dict.fromkeys shares one default",
        "`dict.fromkeys(names, 0)` is fine for immutable defaults - but "
        "`dict.fromkeys(names, [])` gives every key the SAME list. Build with "
        "a comprehension instead whenever the default is mutable.",
    ),
    CODE_CELL(
        "bad = dict.fromkeys(('a', 'b'), [])\n"
        "bad['a'].append(1)\n"
        "print('shared!', bad)                 # {'a': [1], 'b': [1]}\n"
        "\n"
        "good = {k: [] for k in ('a', 'b')}\n"
        "good['a'].append(1)\n"
        "print('independent:', good)"
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "**A telemetry aggregator that cannot silently drop data.** It "
        "counts per-channel samples, tracks a running sum for means, rejects "
        "unknown channels loudly, and never mutates while iterating."
    ),
    CODE_CELL(
        "def summarise(samples, known_channels):\n"
        "    \"\"\"Aggregate (channel, value) pairs into per-channel stats.\"\"\"\n"
        "    counts = dict.fromkeys(known_channels, 0)\n"
        "    totals = dict.fromkeys(known_channels, 0.0)\n"
        "    for channel, value in samples:\n"
        "        if channel not in counts:\n"
        "            raise KeyError(f'unknown channel {channel!r}')\n"
        "        counts[channel] += 1\n"
        "        totals[channel] += value\n"
        "    means = {\n"
        "        ch: round(totals[ch] / counts[ch], 3)\n"
        "        for ch in counts\n"
        "        if counts[ch]           # zero-division guard per channel\n"
        "    }\n"
        "    return {'counts': counts, 'means': means}\n"
        "\n"
        "out = summarise([('imu', 1.0), ('imu', 3.0), ('gps', 2.0)], ['imu', 'gps'])\n"
        "print('counts:', out['counts'])\n"
        "print('means :', out['means'])"
    ),
    BULLETS(
        [
            "`dict.fromkeys(channels, 0)` seeds both tables from the known "
            "channel list - the counts table doubles as the whitelist.",
            "The `channel not in counts` guard turns an unknown channel into "
            "a loud KeyError instead of a quietly created entry - the get() "
            "trap avoided by design.",
            "Totals stay separate from counts so the mean divides by real "
            "observations, not by channel count.",
            "The means comprehension filters `if counts[ch]`, handling "
            "channels that received zero samples without a ZeroDivisionError.",
        ]
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`counts = dict.fromkeys(known_channels, 0)` - zero counts for "
            "every legal channel; immutable default 0, so sharing is safe.",
            "`for channel, value in samples:` - unpacks each pair directly; "
            "no indexing into tuples.",
            "`if channel not in counts: raise KeyError(...)` - membership "
            "first, so the error names the channel and no phantom key is "
            "created.",
            "`counts[channel] += 1` - fetch-add-store on an existing key; "
            "amortised O(1).",
            "`totals[channel] += value` - a parallel table, so means need no "
            "second pass over samples.",
            "`{ch: round(...) for ch in counts if counts[ch]}` - the filter "
            "guards division; channels with no samples simply do not appear "
            "in the means.",
            "`return {'counts': counts, 'means': means}` - a record of "
            "records - dicts nesting naturally is what makes the return type "
            "self-describing.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - get() where the key must exist.**"),
    CODE(
        "cfg = {'port': 8080}          # 'host' forgotten\n"
        "host = cfg.get('host')        # None - the bug escapes\n"
        "url = f'http://{host}:{cfg.get(\"port\")}'\n"
        "print(url)                    # 'http://None:8080' - plausible garbage\n"
        "\n"
        "host = cfg['host']            # KeyError AT THE SOURCE - fixed fast",
        lang="text",
    ),
    MD("**Mistake 2 - assuming a copy is independent at every level.**"),
    CODE(
        "original = {'cfg': {'mode': 'a'}}\n"
        "clone = original.copy()          # shallow!\n"
        "clone['cfg']['mode'] = 'b'\n"
        "print(original['cfg']['mode'])   # 'b' - the inner dict is shared",
        lang="text",
    ),
    MD("**Mistake 3 - mutating the dict while iterating it.**"),
    CODE(
        "d = {'a': 1, 'b': 2}\n"
        "for k in d:\n"
        "    if d[k] == 1:\n"
        "        d['c'] = 3        # RuntimeError: dictionary changed size\n"
        "\n"
        "for k in list(d):         # snapshot the keys first\n"
        "    ...",
        lang="text",
    ),
    MD("**Mistake 4 - keys that cannot hash.**"),
    CODE(
        "d = {}\n"
        "d[['x', 'y']] = 1         # TypeError: unhashable type: 'list'\n"
        "d[('x', 'y')] = 1         # tuple key - the fix",
        lang="text",
    ),
    MD("**Mistake 5 - iterating .values() while assigning keys.**"),
    CODE(
        "for v in d.values():\n"
        "    d['derived'] = v * 2   # RuntimeError - the view is live\n"
        "\n"
        "for v in list(d.values()):  # snapshot the view\n"
        "    ...",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a dict 'loses' an entry, print the keys BEFORE the suspect write "
        "- a KeyError with the exact name, plus a sorted key dump, identifies "
        "typos and case mismatches in one step."
    ),
    CODE_CELL(
        "config = {'Timeout': 30}          # capital T - the classic typo\n"
        "print('keys:', sorted(config))\n"
        "try:\n"
        "    config['timeout']\n"
        "except KeyError as exc:\n"
        "    print('missing:', exc)\n"
        "    folded = {k.lower(): k for k in config}\n"
        "    print('case-insensitive hit?', folded.get('timeout'))"
    ),
    MD(
        "When a copy changed the original, print identity of the nested "
        "values - `id()` proves whether two paths reach one object."
    ),
    CODE_CELL(
        "original = {'cfg': {'mode': 'a'}}\n"
        "clone = dict(original)\n"
        "\n"
        "print('outer distinct?', original is not clone)                 # True\n"
        "print('inner shared  ?', original['cfg'] is clone['cfg'])   # True\n"
        "print('fix: copy.deepcopy or rebuild inner dicts')"
    ),
    NOTE(
        "views are live, not snapshots",
        "`list(d.items())` snapshots; `d.items()` does not. If a RuntimeError "
        "mentions changed size mid-loop, the view is the culprit - wrap the "
        "iteration target in list().",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Use `d[k]` for required keys - let KeyError fail fast at the "
            "source; reserve `get(k, default)` for documented optional keys.",
            "Never mutate a dict while iterating it; snapshot with list() or "
            "rebuild with a comprehension.",
            "Copy nested data with copy.deepcopy (or rebuild inner dicts "
            "explicitly) - dict() and .copy() are shallow.",
            "Prefer `d | other` or update-into-a-new-dict over mutating a "
            "shared mapping.",
            "Keys: strings for config, tuples for coordinates - keep them "
            "hashable and stable.",
            "Values: anything goes, but document when a value is itself "
            "mutable state.",
            "Iterate .items() when both key and value are needed - it is one "
            "lookup, not two.",
            "Use dict.fromkeys only with immutable defaults; comprehension "
            "for mutable ones.",
            "Sort at the boundary (sorted(d)) when output order must be "
            "reproducible.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "The dict is the reason Python beats linear-scan languages at "
        "key-value work: amortised O(1) lookup from a hash probe, regardless "
        "of size. Everything expensive in dict-land is either O(n) by nature "
        "(iteration, copying, merging many) or a misuse (building keys by "
        "string concatenation, scanning values for a key)."
    ),
    TABLE(
        ["Pattern", "Cost", "Preferred alternative"],
        [
            ["`k in d.values()` to find a key", "O(n) per call", "invert the mapping once, then O(1)"],
            ["`d.get(k, 0) + 1` counting", "O(1) - correct", "collections.Counter for richer stats"],
            ["Rebuilding d in a loop", "O(n) per rebuild", "update in place or accumulate elsewhere"],
            ["`dict.copy()` for nested state", "shallow O(n)", "copy.deepcopy when inner state is shared"],
            ["`d[k] = d.get(k, 0) + 1`", "O(1) amortised", "the right pattern - keep it"],
            ["Searching every value for x", "O(n)", "build a reverse index: {v: k for k, v in d.items()}"],
        ],
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "n = 100_000\n"
        "mapping = {f'key{i}': i for i in range(n)}\n"
        "keys = list(mapping)\n"
        "\n"
        "start = time.perf_counter()\n"
        "hits = sum(1 for k in keys if k in mapping)\n"
        "dict_s = time.perf_counter() - start\n"
        "\n"
        "pairs = list(mapping.items())\n"
        "start = time.perf_counter()\n"
        "hits2 = sum(1 for k in keys if any(pk == k for pk, _ in pairs))\n"
        "scan_s = time.perf_counter() - start\n"
        "\n"
        "print(f'dict lookup {dict_s:.4f}s vs linear scan {scan_s:.4f}s')\n"
        "print(f'dict is {scan_s / max(dict_s, 1e-9):.0f}x faster here')"
    ),
    MD(
        "Two structural notes. Insertion is amortised O(1) but *deletion* "
        "leaves the table's slot bookkeeping to be maintained lazily - still "
        "amortised constant. And iteration cost is O(n) whether you walk "
        "keys, values or items, because all three views traverse the same "
        "table; `list(d.items())` doubles the peak memory for the snapshot, "
        "which matters at a million entries."
    ),
]

LESSON["pythonic_approaches"] = [
    MD(
        "Idiomatic dict code exploits three affordances: items() iteration, "
        "comprehensions that build the whole mapping in one expression, and "
        "the merge operator - each replacing an explicit loop the reader "
        "would otherwise have to audit."
    ),
    CODE_CELL(
        "names = ('ada', 'grace', 'alan')\n"
        "scores = (91, 88, 95)\n"
        "\n"
        "# not pythonic\n"
        "board = {}\n"
        "for i in range(len(names)):\n"
        "    board[names[i]] = scores[i]\n"
        "\n"
        "# pythonic - zip pairs them, the comprehension names the result\n"
        "board = {name: score for name, score in zip(names, scores)}\n"
        "print('board:', board)\n"
        "print('above 90:', {n: s for n, s in board.items() if s > 90})"
    ),
    BULLETS(
        [
            "Iterate `.items()` when you need both sides - it is one "
            "traversal, not two lookups.",
            "`dict(zip(keys, values))` beats an index loop for parallel "
            "sequences.",
            "`{**base, **overrides}` or `base | overrides` merges without "
            "mutating either operand.",
            "Invert deliberately: `{v: k for k, v in d.items()}` - and "
            "document which key wins collisions.",
            "`d.keys() & other.keys()` answers set questions about mappings "
            "directly.",
            "Use `sorted(d, key=d.get)` to order by value in one readable "
            "expression.",
            "defaultdict(list) or Counter when grouping/counting - but know "
            "what mutates on access.",
        ]
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A rover's parameter server is a dict: hundreds of tunables keyed by "
        "name, read on every control tick, updated between runs. The safety "
        "requirements map directly onto dict semantics - missing keys must "
        "fail loudly, updates must not mutate a config another component is "
        "reading, and the hot read path must stay O(1)."
    ),
    CODE_CELL(
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "here = Path.cwd()\n"
        "root = next((p for p in [here, *here.parents] if (p / 'shared').is_dir()), None)\n"
        "if root is not None:\n"
        "    sys.path.insert(0, str(root))\n"
        "\n"
        "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
        "\n"
        "robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
        "params = {'speed_mps': 0.4, 'gains': {'kp': 1.2, 'ki': 0.05}}\n"
        "\n"
        "snapshot = {'speed_mps': params['speed_mps'],\n"
        "            'gains': dict(params['gains'])}      # isolate the nest\n"
        "snapshot['gains']['kp'] = 2.0                    # tuning this run\n"
        "\n"
        "print('live kp :', params['gains']['kp'])         # unchanged\n"
        "print('snap kp :', snapshot['gains']['kp'])\n"
        "print('battery :', round(robot.status()['battery_pct'], 1), '%')"
    ),
    MD(
        "The boundary-copy habit is the engineering rule: a component that "
        "reads parameters takes a snapshot with nested copies; a component "
        "that publishes new parameters returns a fresh dict rather than "
        "editing the shared one. Pair it with `params['required_key']` for "
        "mandatory tunables so a typo fails at load time, not at the moment "
        "the rover depends on the value."
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A rate limiter keyed by client id is classic dict engineering: each "
        "client's window lives in its own nested record, absence is normal "
        "(first request), and the design must not leak state between clients "
        "or between windows."
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "def make_limiter(max_per_window=5, window_s=60.0):\n"
        "    \"\"\"Return an allow(client_id) callable - dict-backed window counter.\"\"\"\n"
        "    windows = {}\n"
        "\n"
        "    def allow(client_id):\n"
        "        now = time.monotonic()\n"
        "        window = windows.get(client_id)\n"
        "        if window is None or now - window['reset'] > window_s:\n"
        "            windows[client_id] = {'count': 1, 'reset': now}\n"
        "            return True\n"
        "        if window['count'] >= max_per_window:\n"
        "            return False\n"
        "        window['count'] += 1          # nested dict mutated in place\n"
        "        return True\n"
        "\n"
        "    return allow\n"
        "\n"
        "allow = make_limiter(max_per_window=2, window_s=60.0)\n"
        "print('first  :', allow('alpha'))\n"
        "print('second :', allow('alpha'))\n"
        "print('third  :', allow('alpha'))   # over the limit\n"
        "print('other  :', allow('beta'))    # independent record"
    ),
    MD(
        "Note the shape: a closure over one dict, `.get` for the genuinely "
        "optional first sighting, `[]` once the record exists, and a nested "
        "dict mutated in place for the counter. Each client's record is "
        "independent precisely because the inner dicts are built fresh on "
        "first use - not shared via fromkeys."
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Build a dict three ways - literal, dict(pairs) and fromkeys - "
            "and print each with its type.",
            "Fetch a missing key with `[]` (read the KeyError) and with "
            ".get(k, default); explain when each is correct.",
            "Count word frequencies with .get(), then find the most frequent "
            "word with max(..., key=counts.get).",
            "Reproduce the shallow-copy corruption on a nested record, then "
            "fix it with a dict rebuild of the inner level.",
            "Trigger the RuntimeError by adding a key during iteration, then "
            "iterate list(d) and confirm it succeeds.",
        ]
    ),
    CODE_CELL(
        "pairs = [('rate', 100), ('channel', 'imu')]\n"
        "print('literal:', {'rate': 100})\n"
        "print('pairs  :', dict(pairs))\n"
        "print('fromkeys:', dict.fromkeys(('a', 'b'), 0))\n"
        "\n"
        "cfg = {'port': 8080}\n"
        "try:\n"
        "    cfg['host']\n"
        "except KeyError as exc:\n"
        "    print('[] raises:', exc)\n"
        "print('get default:', cfg.get('host', 'localhost'))\n"
        "\n"
        "words = 'go hold go stop go'.split()\n"
        "counts = {}\n"
        "for w in words:\n"
        "    counts[w] = counts.get(w, 0) + 1\n"
        "print('counts:', counts, ' top:', max(counts, key=counts.get))"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a dict is a wall of numbered pigeonholes with the "
        "numbers written on the items, not on the holes.** The hash of a key "
        "says which section of the wall to visit; the key is checked at the "
        "slot. Retrieval is a direct walk, not a search - but an unknown item "
        "has no hole at all, which is why `d[k]` raises rather than guesses."
    ),
    TABLE(
        ["Question", "Answer", "Consequence"],
        [
            ["Can two keys share a slot?", "no - keys are unique", "re-assignment replaces, never duplicates"],
            ["What if the key is missing?", "`[]` raises KeyError", "get(k, default) is the explicit opt-out"],
            ["Is a copy independent?", "outer yes, values shared", "deepcopy or rebuild nested levels"],
            ["Iteration order?", "insertion order (3.7+)", "reproducible output without sorting"],
            ["Mutable keys?", "impossible - they would not hash", "lists/dicts as keys raise TypeError"],
            ["Mutating while iterating?", "RuntimeError", "snapshot with list(d) first"],
        ],
    ),
]

TERMS = [
    ["Dictionary", "A mutable mapping from unique hashable keys to values."],
    ["Key", "A hashable object identifying one entry; unique per dict."],
    ["Value", "Any object bound to a key; may itself be mutable."],
    ["KeyError", "Raised by d[k] when the key is absent - fail-fast access."],
    ["get(k, default)", "Absent-safe access returning an explicit default."],
    ["View", "A live, read-only window over keys, values or items."],
    ["Insertion order", "The guaranteed iteration order of a dict since 3.7."],
    ["Shallow copy", "A new dict whose values are references to the originals."],
    ["Hash table", "The array-of-slots structure giving amortised O(1) lookup."],
    ["Mapping", "The protocol of key-based access a dict implements."],
]

LESSON["summary"] = [
    MD(
        "A dict maps unique hashable keys to values in amortised O(1) time, "
        "iterates in insertion order, and replaces - never duplicates - a key "
        "that is assigned twice. It is Python's record type: config, status, "
        "counters, indices - anywhere data is a set of named fields rather "
        "than a sequence."
    ),
    MD(
        "The three failure modes structure the topic. **Silent absence**: "
        "`d[k]` raises loudly at the source, while `.get(k, default)` can "
        "turn a typo into plausible garbage downstream - reserve it for "
        "documented optional keys. **Shared nesting**: every built-in copy is "
        "shallow, so editing a copied record mutates the original's inner "
        "dict; deepcopy or rebuild inner levels at boundaries. **Mutation "
        "during iteration**: views are live and raise RuntimeError - snapshot "
        "with list(d) or rebuild with a comprehension."
    ),
    MD(
        "The performance story is why dicts dominate: constant-time membership "
        "and fetch mean an inverted mapping replaces every value scan, "
        "counting is one get-and-add per item, and grouping is a "
        "setdefault/comprehension one-liner. Practise the discipline - `[]` "
        "for required keys, get for optional, sorted output at boundaries - "
        "and the record type stops being a source of bugs."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Dicts map unique hashable keys to values; assigning an existing "
            "key replaces it.",
            "`d[k]` raises KeyError on absence - use it for required keys; "
            ".get(k, default) only for documented optional ones.",
            "Iteration follows insertion order (guaranteed since 3.7); sort "
            "when output must be canonical.",
            "Every built-in copy is shallow - nested dicts stay shared; "
            "deepcopy or rebuild at boundaries.",
            "Never mutate a dict while iterating it - snapshot with list(d) "
            "or rebuild with a comprehension.",
            "Keys must be hashable (str, int, tuple); values can be anything.",
            "Invert a mapping ({v: k for ...}) instead of scanning values, "
            "and document collision policy.",
            "dict.fromkeys shares one default object - use a comprehension "
            "for mutable defaults.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "Read about dict's compact insertion-order layout (PEP 468 and "
            "the How Dicts Work section of the docs).",
            "Time 100000 lookups against a dict versus a list of pairs, and "
            "plot both against n.",
            "Explore collections.defaultdict, Counter and OrderedDict - and "
            "write one paragraph on when each earns its place.",
            "Investigate `d | other` versus update(): which mutates, and "
            "which operands survive?",
            "Study json.dumps(..., sort_keys=True) as the reproducible "
            "serialisation of a dict.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Fetch required and optional config keys correctly",
        difficulty="MEDIUM",
        learning_objectives=["Choose [] versus .get by optionality.", "Fail fast on required keys."],
        concepts_tested=["KeyError", "get defaults", "contract design"],
        problem_statement=(
            "Write `read_config(config)` returning `(host, timeout)` where "
            "host is REQUIRED (a missing host must raise KeyError from your "
            "code) and timeout is optional with default 30."
        ),
        requirements=[
            "Access host with d[k], not get.",
            "Use config.get('timeout', 30).",
            "Coerce timeout to int.",
        ],
        constraints=["Do not use try/except to emulate the required access."],
        input_description="A dict of configuration entries.",
        expected_output="A (str, int) tuple.",
        example_input="read_config({'host': 'mars.local', 'timeout': 5})",
        example_output="('mars.local', 5)",
        edge_cases=[
            "Missing host raises KeyError naming 'host'.",
            "Missing timeout returns default 30.",
            "A string timeout '15' coerces to 15.",
        ],
        hints=["Two different access styles for two different contracts - that is the point."],
        success_criteria=["The example matches.", "read_config({'timeout': 9}) raises KeyError."],
        optional_extension="Return a dict of all parsed keys with unknown keys flagged.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Count frequencies with a dict",
        difficulty="MEDIUM",
        learning_objectives=["Accumulate counts keyed by value.", "Find a maximum by key function."],
        concepts_tested=["counting idiom", "get", "max with key"],
        problem_statement=(
            "Write `frequencies(items)` returning a dict mapping each item to "
            "its occurrence count, and `most_common(counts)` returning the "
            "item with the highest count (ties broken by first insertion "
            "order)."
        ),
        requirements=["Single pass for counting.", "most_common returns the KEY, not the count."],
        constraints=["No collections.Counter."],
        input_description="A list of hashable items.",
        expected_output="A dict of item -> int; most_common returns an item.",
        example_input="frequencies(['a', 'b', 'a']) then most_common of it",
        example_output="{'a': 2, 'b': 1} then 'a'",
        edge_cases=[
            "An empty list gives {} and most_common raises ValueError.",
            "All-unique input gives counts of 1; the first key wins the tie.",
        ],
        hints=["counts[x] = counts.get(x, 0) + 1; max(counts, key=counts.get)."],
        success_criteria=["The example matches.", "Ties resolve to the earliest inserted key."],
        optional_extension="Return (item, count) and sort by count descending.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Merge parameter sets with override semantics",
        difficulty="MEDIUM",
        learning_objectives=["Merge dicts non-destructively.", "Document which side wins."],
        concepts_tested=["merge operator", "update", "immutability of inputs"],
        problem_statement=(
            "Write `merge_params(base, override)` returning a NEW dict where "
            "override wins on key conflicts. Neither input may be modified."
        ),
        requirements=["Use | or a copy plus update.", "Return a new dict."],
        constraints=["Do not mutate base or override in place."],
        input_description="Two dicts of parameters.",
        expected_output="A merged dict; override values on conflict.",
        example_input="merge_params({'port': 80}, {'port': 443, 'tls': True})",
        example_output="{'port': 443, 'tls': True}",
        edge_cases=[
            "Empty override returns an equal (but new) dict.",
            "Empty base returns a copy of override.",
            "Disjoint keys union cleanly.",
        ],
        hints=["base | override already implements exactly this precedence."],
        success_criteria=["The example matches.", "Both inputs are unchanged after the call."],
        optional_extension="Accept a list of dicts merged left to right.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Group events into a dict of lists",
        difficulty="MEDIUM",
        learning_objectives=["Group with setdefault or get-branch.", "Preserve encounter order."],
        concepts_tested=["grouping", "setdefault", "append"],
        problem_statement=(
            "Write `group(events)` taking (kind, detail) pairs and returning a "
            "dict mapping each kind to the list of its details in encounter "
            "order."
        ),
        requirements=["Groups appear in first-encounter key order.", "Details preserve input order."],
        constraints=["No collections.defaultdict."],
        input_description="A list of (kind, detail) tuples.",
        expected_output="A dict of kind -> list of details.",
        example_input="group([('imu', 'boot'), ('gps', 'fix'), ('imu', 'drift')])",
        example_output="{'imu': ['boot', 'drift'], 'gps': ['fix']}",
        edge_cases=[
            "An empty input gives an empty dict.",
            "A single kind collects all its details.",
        ],
        hints=["by_kind.setdefault(kind, []).append(detail) is one line."],
        success_criteria=["The example matches exactly (key order as shown)."],
        optional_extension="Also return the number of groups.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Invert a mapping with an explicit collision policy",
        difficulty="MEDIUM",
        learning_objectives=["Build a reverse dict.", "Handle duplicate values deliberately."],
        concepts_tested=["dict comprehension", "collision policy", "reverse index"],
        problem_statement=(
            "Write `invert(mapping, policy='last')` returning value -> key. "
            "When several keys share a value, policy 'last' keeps the "
            "last-inserted key and 'first' keeps the first; anything else "
            "raises ValueError."
        ),
        requirements=["Insertion order decides first/last.", "Validate the policy argument."],
        constraints=["Single pass over mapping.items()."],
        input_description="A dict and a policy string.",
        expected_output="An inverted dict.",
        example_input="invert({'a': 1, 'b': 1}, 'first')",
        example_output="{1: 'a'}",
        edge_cases=[
            "'last' on the same input gives {1: 'b'}.",
            "An empty dict inverts to {}.",
            "policy='middle' raises ValueError.",
        ],
        hints=["Loop and assign unconditionally for 'last'; assign only if the key is absent for 'first'."],
        success_criteria=["Both policies give the documented winner.", "Invalid policy raises ValueError."],
        optional_extension="Return a dict of value -> list of ALL colliding keys instead.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Deep-copy a nested record without sharing state",
        difficulty="HARD",
        learning_objectives=["Clone nested mappings manually.", "Prove independence with assertions."],
        concepts_tested=["shallow vs deep copy", "recursion", "isolation"],
        problem_statement=(
            "Write `deep_copy(record)` returning a fully independent clone of "
            "a dict whose values may be scalars, lists or nested dicts - no "
            "element of the result may be `is` any element of the input. Do "
            "not import copy."
        ),
        requirements=["Handle dict, list and scalar values recursively.", "Return a new top-level dict."],
        constraints=["No copy module, no json round-trip."],
        input_description="A nested dict/list/scalar structure.",
        expected_output="An independent clone.",
        example_input="deep_copy({'cfg': {'mode': 'a'}, 'tags': [1]})",
        example_output="{'cfg': {'mode': 'a'}, 'tags': [1]}  (new objects)",
        edge_cases=[
            "An empty dict returns a new empty dict.",
            "Tuples pass through as tuples but any dict/list inside them is cloned.",
            "Mutating the clone never changes the source at any depth.",
        ],
        hints=["isinstance checks: dict -> comprehension of deep_copy(v), list -> list of deep_copy(v), else return as-is."],
        success_criteria=["id() differs for every container after cloning.", "Mutation of the clone leaves the source unchanged."],
        optional_extension="Handle sets as frozensets and state the trade-off.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Build an O(1) reverse lookup with collision handling",
        difficulty="HARD",
        learning_objectives=["Index by value once.", "Serve lookups without scanning."],
        concepts_tested=["reverse index", "precomputation", "collision lists"],
        problem_statement=(
            "Write `ReverseIndex(mapping)` that precomputes value -> list of "
            "keys (values may be unhashable - skip them and count them in "
            "`unindexable`). `lookup(value)` returns the sorted key list or [] "
            "in O(1) expected; `size` reports the indexed entry count."
        ),
        requirements=["lookup never scans the original mapping.", "Unhashable values are counted, not raised on."],
        constraints=["Precompute in the constructor - no per-lookup rebuild."],
        input_description="A dict with possibly repeated and unhashable values.",
        expected_output="An object with lookup(value), unindexable and size.",
        example_input="ReverseIndex({'a': 1, 'b': 1, 'c': [2]}).lookup(1)",
        example_output="['a', 'b']  (unindexable == 1)",
        edge_cases=[
            "An empty mapping gives size 0 and lookup returns [].",
            "A list value increments unindexable and is absent from the index.",
        ],
        hints=["try: hash(value) except TypeError - count and skip; else bucket the key."],
        success_criteria=["lookup(1) returns ['a', 'b'] as shown.", "No loop over the original mapping appears in lookup."],
        optional_extension="Add lookup_sorted(value) returning keys in insertion order instead.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Detect and repair aliasing in a settings tree",
        difficulty="HARD",
        learning_objectives=["Diagnose shared references.", "Return a repaired independent tree."],
        concepts_tested=["identity testing", "alias detection", "repair"],
        problem_statement=(
            "Write `is_independent(tree)` returning True only when no dict or "
            "list inside `tree` is reachable twice (no shared nodes), and "
            "`detach(tree)` returning an independent clone in which that "
            "property holds. Do not import copy."
        ),
        requirements=[
            "is_independent detects a node reachable by two paths.",
            "detach guarantees is_independent(result) is True.",
        ],
        constraints=["No copy module; traverse with isinstance checks."],
        input_description="A nested dict/list tree that may contain shared or cyclic nodes.",
        expected_output="(bool, new tree).",
        example_input="shared = {}; is_independent({'a': shared, 'b': shared})",
        example_output="(False, {'a': {}, 'b': {}})",
        edge_cases=[
            "A tree with only scalars is independent.",
            "detach of an already-independent tree still returns a clone.",
            "A cycle must not hang - detect via an id() seen-set.",
        ],
        hints=["Track visited node ids in a set during traversal; clone with the deep_copy recursion, breaking cycles by memoising."],
        success_criteria=["The example matches.", "detach output passes is_independent."],
        optional_extension="Return the pair of paths that share a node when not independent.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Implement a typed settings table with validation",
        difficulty="HARD",
        learning_objectives=["Validate against a schema dict.", "Report all errors at once."],
        concepts_tested=["schema-driven validation", "type checks", "error accumulation"],
        problem_statement=(
            "Write `validate_settings(values, schema)` where schema maps each "
            "required key to an expected type. Return `(clean, errors)`: "
            "clean holds the coerced-valid entries in schema order; errors is "
            "a sorted list of messages - one per missing key, wrong type or "
            "unexpected key."
        ),
        requirements=[
            "All schema keys are required.",
            "Messages: 'missing: <k>', 'type: <k>', 'unexpected: <k>'.",
            "Errors sorted; clean follows schema insertion order.",
        ],
        constraints=["Do not raise - every problem is reported."],
        input_description="A values dict and a schema dict of key -> type.",
        expected_output="(dict, sorted list of strings).",
        example_input="validate_settings({'rate': 10}, {'rate': int, 'host': str})",
        example_output="({'rate': 10}, ['missing: host'])",
        edge_cases=[
            "Exact match returns (values_copy, []).",
            "bool is not accepted where int is expected.",
            "An unexpected extra key produces 'unexpected: <k>'.",
        ],
        hints=["Iterate the schema first for missing/type, then values for unexpected; accumulate, never raise."],
        success_criteria=["The example matches.", "Multiple simultaneous problems all appear in the errors list."],
        optional_extension="Support optional keys marked with a (type, default) tuple.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Simulate a parameter-server update cycle",
        difficulty="HARD",
        learning_objectives=["Stage updates without mutating live state.", "Swap atomically by rebinding."],
        concepts_tested=["snapshot isolation", "staged updates", "nested merge"],
        problem_statement=(
            "Write `apply_updates(live, updates)` returning a NEW nested dict "
            "with updates deep-merged into live (updates win at every level), "
            "leaving `live` completely unchanged. Keys removed by a None "
            "value in updates must be deleted from the result only."
        ),
        requirements=[
            "Nested dicts merge recursively; non-dicts replace.",
            "updates[k] is None deletes k from the result.",
            "live is untouched at every depth.",
        ],
        constraints=["No copy module; build as you merge."],
        input_description="Two nested dicts.",
        expected_output="A new merged dict; live unchanged.",
        example_input="apply_updates({'a': {'x': 1, 'y': 2}}, {'a': {'y': 9, 'z': 3}})",
        example_output="{'a': {'x': 1, 'y': 9, 'z': 3}}",
        edge_cases=[
            "An empty updates returns a full clone of live.",
            "A None deletion of a missing key is a no-op.",
            "Non-dict values in updates replace wholesale, not merge.",
        ],
        hints=["Recurse only when both sides are dicts; clone every dict you emit so live's inner dicts are never shared."],
        success_criteria=["The example matches.", "Mutating the result leaves live unchanged at any depth."],
        optional_extension="Return (result, changelog) listing each path that changed.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def read_config(config):\n"
            "    \"\"\"host is required (KeyError if absent); timeout defaults to 30.\"\"\"\n"
            "    host = config['host']                  # contract: must exist\n"
            "    timeout = int(config.get('timeout', 30))\n"
            "    return host, timeout"
        ),
        explanation=(
            "The two access styles encode two contracts on adjacent lines: "
            "bracket access fails AT THE SOURCE with the missing key named, "
            "while get() treats absence as a documented default. A try/except "
            "would work but would also swallow real KeyErrors raised by "
            "mistake inside the block."
        ),
        complexity="Time O(1) average per access; space O(1).",
        edge_cases="Missing host raises KeyError('host'). Missing timeout returns 30. String timeouts coerce.",
        alternative_approaches="config.pop('timeout', 30) reads the default too but destroys the caller's dict.",
        testing=(
            "assert read_config({'host': 'mars.local', 'timeout': 5}) == ('mars.local', 5)\n"
            "assert read_config({'host': 'x'}) == ('x', 30)\n"
            "try:\n"
            "    read_config({'timeout': 9})\n"
            "    raise AssertionError('should raise')\n"
            "except KeyError as exc:\n"
            "    assert 'host' in str(exc)"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def frequencies(items):\n"
            "    \"\"\"item -> occurrence count, one pass.\"\"\"\n"
            "    counts = {}\n"
            "    for item in items:\n"
            "        counts[item] = counts.get(item, 0) + 1\n"
            "    return counts\n"
            "\n"
            "\n"
            "def most_common(counts):\n"
            "    \"\"\"Key with the highest count; ties go to first insertion.\"\"\"\n"
            "    if not counts:\n"
            "        raise ValueError('no counts to inspect')\n"
            "    return max(counts, key=counts.get)"
        ),
        explanation=(
            "get(item, 0) + 1 is the counting idiom: the default only exists "
            "to seed the first sighting, and insertion order then guarantees "
            "max() walks candidates in first-seen order - so ties resolve to "
            "the earliest key deterministically because max keeps the first "
            "maximum it meets."
        ),
        complexity="Time O(n) expected for counting, O(k) for the max; space O(k) for k distinct keys.",
        edge_cases="Empty input counts to {} and most_common raises ValueError. All-unique input gives first key.",
        alternative_approaches="collections.Counter(items).most_common(1) does both but hides the mechanism being taught.",
        testing=(
            "counts = frequencies(['a', 'b', 'a'])\n"
            "assert counts == {'a': 2, 'b': 1}\n"
            "assert most_common(counts) == 'a'\n"
            "assert most_common({'x': 1, 'y': 1}) == 'x'\n"
            "try:\n"
            "    most_common({})\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def merge_params(base, override):\n"
            "    \"\"\"New dict with override winning; inputs untouched.\"\"\"\n"
            "    return {**base, **override}"
        ),
        explanation=(
            "The {**d} unpacking form builds a fresh dict from each operand's "
            "items, so precedence falls out of evaluation order (the later "
            "unpack overwrites) and neither input is touched. `base | override` "
            "is equivalent and equally non-mutating - both beat update(), "
            "which would edit base in the caller's hands."
        ),
        complexity="Time O(len(base) + len(override)); space O(same) for the result.",
        edge_cases="Empty override returns an equal new dict. Empty base returns a copy of override.",
        alternative_approaches="dict(base); merged.update(override) is two statements saying the same thing.",
        testing=(
            "base = {'port': 80}\n"
            "over = {'port': 443, 'tls': True}\n"
            "out = merge_params(base, over)\n"
            "assert out == {'port': 443, 'tls': True}\n"
            "assert base == {'port': 80} and over == {'port': 443, 'tls': True}"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def group(events):\n"
            "    \"\"\"kind -> list of details, in encounter order.\"\"\"\n"
            "    groups = {}\n"
            "    for kind, detail in events:\n"
            "        groups.setdefault(kind, []).append(detail)\n"
            "    return groups"
        ),
        explanation=(
            "setdefault(kind, []) returns the existing list when the key is "
            "present and installs-and-returns it on the first sighting, so "
            "one line covers both branches. Dict insertion order then gives "
            "first-encounter key order, and list order gives detail order - "
            "both required by the specification."
        ),
        complexity="Time O(total details) expected; space O(total details).",
        edge_cases="Empty input gives {}. A single kind collects every detail.",
        alternative_approaches="The explicit get-then-create avoids building a throwaway list on hits (see lesson advanced examples).",
        testing=(
            "out = group([('imu', 'boot'), ('gps', 'fix'), ('imu', 'drift')])\n"
            "assert out == {'imu': ['boot', 'drift'], 'gps': ['fix']}\n"
            "assert group([]) == {}"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def invert(mapping, policy='last'):\n"
            "    \"\"\"value -> key with an explicit collision policy.\"\"\"\n"
            "    if policy not in ('first', 'last'):\n"
            "        raise ValueError(f'unknown policy {policy!r}')\n"
            "    reversed_map = {}\n"
            "    for key, value in mapping.items():\n"
            "        if policy == 'first' and value in reversed_map:\n"
            "            continue                 # keep the earliest key\n"
            "        reversed_map[value] = key      # 'last' simply overwrites\n"
            "    return reversed_map"
        ),
        explanation=(
            "Insertion order makes both policies mechanical: 'first' skips "
            "values already present (the first key got there first), 'last' "
            "overwrites unconditionally (the last writer wins). Validating "
            "the policy up front turns a silent wrong answer on a typo into a "
            "loud failure."
        ),
        complexity="Time O(n) expected; space O(n).",
        edge_cases="Empty dict inverts to {}. Invalid policy raises ValueError before any work.",
        alternative_approaches="collections.defaultdict(list) of ALL keys per value trades the policy for more structure.",
        testing=(
            "m = {'a': 1, 'b': 1}\n"
            "assert invert(m, 'first') == {1: 'a'}\n"
            "assert invert(m, 'last') == {1: 'b'}\n"
            "assert invert({}) == {}\n"
            "try:\n"
            "    invert(m, 'middle')\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def deep_copy(record):\n"
            "    \"\"\"Recursively clone dicts/lists; scalars pass through.\"\"\"\n"
            "    if isinstance(record, dict):\n"
            "        return {k: deep_copy(v) for k, v in record.items()}\n"
            "    if isinstance(record, list):\n"
            "        return [deep_copy(v) for v in record]\n"
            "    if isinstance(record, tuple):\n"
            "        return tuple(deep_copy(v) for v in record)\n"
            "    return record   # scalars are immutable - sharing is safe"
        ),
        explanation=(
            "Each container type is rebuilt rather than referenced, so no "
            "result node is `is` a source node - the property the exercise's "
            "assertions check with id(). Scalars are returned as-is because "
            "sharing immutable objects is both safe and free; cloning them "
            "would cost memory for nothing."
        ),
        complexity="Time O(n) over all nodes; space O(n) for the clone.",
        edge_cases="Empty dicts return new empties. Tuples are rebuilt so nested dicts inside them are still cloned.",
        alternative_approaches="copy.deepcopy is one line but is exactly the library call the exercise asks you to understand.",
        testing=(
            "src = {'cfg': {'mode': 'a'}, 'tags': [1, 2]}\n"
            "clone = deep_copy(src)\n"
            "assert clone == src\n"
            "assert clone['cfg'] is not src['cfg']\n"
            "clone['cfg']['mode'] = 'b'\n"
            "assert src['cfg']['mode'] == 'a'"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "class ReverseIndex:\n"
            "    \"\"\"Precomputed value -> keys index with unhashable tracking.\"\"\"\n"
            "\n"
            "    def __init__(self, mapping):\n"
            "        self._index = {}\n"
            "        self.unindexable = 0\n"
            "        for key, value in mapping.items():\n"
            "            try:\n"
            "                bucket = self._index.setdefault(value, [])\n"
            "            except TypeError:            # unhashable value\n"
            "                self.unindexable += 1\n"
            "                continue\n"
            "            bucket.append(key)\n"
            "        for value in self._index:\n"
            "            self._index[value].sort()\n"
            "        self.size = len(mapping)\n"
            "\n"
            "    def lookup(self, value):\n"
            "        \"\"\"Sorted keys for a hashable value; [] when absent.\"\"\"\n"
            "        return list(self._index.get(value, ()))"
        ),
        explanation=(
            "All the work happens once in the constructor, so lookup is a "
            "single get - O(1) expected, never a scan. try/except around "
            "setdefault catches the TypeError that hashing an unhashable "
            "value raises, counting it instead of failing the build, and "
            "sorting buckets up front keeps lookups reproducible."
        ),
        complexity="Build O(n log n) from bucket sorts; lookup O(1) expected.",
        edge_cases="Empty mapping gives size 0. List values increment unindexable and never enter the index.",
        alternative_approaches="Skipping the try/except and pre-checking with hash(value) doubles the hashing work per entry.",
        testing=(
            "idx = ReverseIndex({'a': 1, 'b': 1, 'c': [2]})\n"
            "assert idx.lookup(1) == ['a', 'b']\n"
            "assert idx.unindexable == 1 and idx.size == 3\n"
            "assert idx.lookup(99) == []\n"
            "assert ReverseIndex({}).size == 0"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def is_independent(tree):\n"
            "    \"\"\"True when no dict/list node is reachable twice.\"\"\"\n"
            "    visited = set()\n"
            "\n"
            "    def walk(node):\n"
            "        if not isinstance(node, (dict, list)):\n"
            "            return True\n"
            "        if id(node) in visited:\n"
            "            return False\n"
            "        visited.add(id(node))\n"
            "        children = node.values() if isinstance(node, dict) else node\n"
            "        return all(walk(child) for child in children)\n"
            "\n"
            "    return walk(tree)\n"
            "\n"
            "\n"
            "def detach(tree):\n"
            "    \"\"\"Clone the tree, memoising nodes so shared/cyclic paths stay consistent.\"\"\"\n"
            "    memo = {}\n"
            "\n"
            "    def clone(node):\n"
            "        if not isinstance(node, (dict, list)):\n"
            "            return node\n"
            "        if id(node) in memo:\n"
            "            return memo[id(node)]\n"
            "        if isinstance(node, dict):\n"
            "            copy_node = {}\n"
            "        else:\n"
            "            copy_node = []\n"
            "        memo[id(node)] = copy_node\n"
            "        if isinstance(node, dict):\n"
            "            for k, v in node.items():\n"
            "                copy_node[k] = clone(v)\n"
            "        else:\n"
            "            copy_node.extend(clone(v) for v in node)\n"
            "        return copy_node\n"
            "\n"
            "    return clone(tree)"
        ),
        explanation=(
            "Both functions key their bookkeeping on id(): is_independent "
            "flags any container whose id it has already seen (a shared node, "
            "or a cycle), and detach memoises clones so a node reached twice "
            "is cloned once - the memo doubles as the cycle breaker, which is "
            "why clone can never recurse forever."
        ),
        complexity="Time O(n) per pass; space O(depth) plus the visited/memo sets.",
        edge_cases="Scalar-only trees are independent. detach of an independent tree still returns a fresh clone. Cycles terminate.",
        alternative_approaches="copy.deepcopy handles cycles too, but hides the id()-memo mechanism this exercise is about.",
        testing=(
            "shared = {}\n"
            "assert is_independent({'a': shared, 'b': shared}) is False\n"
            "fixed = detach({'a': shared, 'b': shared})\n"
            "assert is_independent(fixed) is True\n"
            "assert is_independent({'x': [1, {'y': 2}]}) is True"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def validate_settings(values, schema):\n"
            "    \"\"\"(clean in schema order, sorted error messages) - never raises.\"\"\"\n"
            "    clean, errors = {}, []\n"
            "    for key, expected in schema.items():\n"
            "        if key not in values:\n"
            "            errors.append(f'missing: {key}')\n"
            "        elif isinstance(values[key], expected) and not (\n"
            "            expected is int and isinstance(values[key], bool)\n"
            "        ):\n"
            "            clean[key] = values[key]\n"
            "        else:\n"
            "            errors.append(f'type: {key}')\n"
            "    for key in values:\n"
            "        if key not in schema:\n"
            "            errors.append(f'unexpected: {key}')\n"
            "    return clean, sorted(errors)"
        ),
        explanation=(
            "Three passes' worth of checks run in two loops over already-known "
            "keys: schema-first gives missing/type in schema order (so `clean` "
            "inherits that order), values-second finds extras, and sorting at "
            "the end makes the error report reproducible regardless of dict "
            "order. The explicit bool guard prevents True from satisfying int "
            "because bool subclasses int."
        ),
        complexity="Time O(s + v + e log e); space O(s + e).",
        edge_cases="Exact match gives (copy, []). bool for int reports a type error. Extras report 'unexpected'.",
        alternative_approaches="Raising on the first error is simpler but forces repair loops - the exercise demands a full report.",
        testing=(
            "clean, errors = validate_settings({'rate': 10}, {'rate': int, 'host': str})\n"
            "assert clean == {'rate': 10}\n"
            "assert errors == ['missing: host']\n"
            "clean, errors = validate_settings({'rate': True, 'x': 1}, {'rate': int})\n"
            "assert errors == ['type: rate', 'unexpected: x']"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def apply_updates(live, updates):\n"
            "    \"\"\"Deep-merge updates into a NEW tree; None deletes; live untouched.\"\"\"\n"
            "    result = {}\n"
            "    for key, value in live.items():\n"
            "        if isinstance(value, dict):\n"
            "            result[key] = apply_updates(value, {})\n"
            "        elif isinstance(value, list):\n"
            "            result[key] = list(value)\n"
            "        else:\n"
            "            result[key] = value\n"
            "    for key, value in updates.items():\n"
            "        if value is None:\n"
            "            result.pop(key, None)          # delete from RESULT only\n"
            "        elif isinstance(value, dict) and isinstance(result.get(key), dict):\n"
            "            result[key] = apply_updates(result[key], value)\n"
            "        else:\n"
            "            result[key] = value\n"
            "    return result"
        ),
        explanation=(
            "The first loop deep-clones live so every container in the result "
            "is fresh - the isolation guarantee that lets the second loop "
            "mutate `result` freely without touching live at any depth. The "
            "merge recurses only when BOTH sides are dicts (otherwise "
            "updates' non-dict value replaces wholesale), and the None "
            "sentinel pops from the clone, so deletions never reach the "
            "caller's live tree."
        ),
        complexity="Time O(size of both trees); space O(size of live) for the clone.",
        edge_cases="Empty updates returns a full clone. None on a missing key is a no-op. Type mismatches replace.",
        alternative_approaches="copy.deepcopy(live) then recursive update is shorter but imports the copy module the exercise forbids.",
        testing=(
            "live = {'a': {'x': 1, 'y': 2}, 'b': 3}\n"
            "out = apply_updates(live, {'a': {'y': 9, 'z': 3}, 'b': None})\n"
            "assert out == {'a': {'x': 1, 'y': 9, 'z': 3}}\n"
            "assert live == {'a': {'x': 1, 'y': 2}, 'b': 3}\n"
            "clone = apply_updates(live, {})\n"
            "clone['a']['x'] = 999\n"
            "assert live['a']['x'] == 1"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=11,
        code=(
            "import sys\n"
            "from pathlib import Path\n"
            "\n"
            "_here = Path.cwd()\n"
            "_root = next((p for p in [_here, *_here.parents] if (p / 'shared').is_dir()), None)\n"
            "if _root is not None:\n"
            "    sys.path.insert(0, str(_root))\n"
            "\n"
            "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
            "\n"
            "\n"
            "def load_params(robot, overrides=None):\n"
            "    \"\"\"Merge defaults with overrides into an independent tree.\"\"\"\n"
            "    defaults = {\n"
            "        'speed_mps': 0.4,\n"
            "        'gains': {'kp': 1.2, 'ki': 0.05},\n"
            "        'name': robot.name,\n"
            "    }\n"
            "    merged = apply_updates(defaults, overrides or {})\n"
            "    if merged['speed_mps'] <= 0:\n"
            "        raise ValueError('speed_mps must be positive')\n"
            "    return merged"
        ),
        explanation=(
            "Reusing the deep-merge from exercise 10 makes the parameter "
            "server's update cycle non-destructive by construction: defaults "
            "are cloned, overrides win per key, None deletes from the staged "
            "tree, and validation runs on the staged result BEFORE anyone "
            "binds it as live - so a rejected update cannot half-apply."
        ),
        complexity="Time O(params); space O(params) for the independent tree.",
        edge_cases="No overrides returns a full clone of defaults. A zero speed raises before returning.",
        alternative_approaches="Mutating defaults in place would alias every future load to the first caller's overrides.",
        testing=(
            "robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "p = load_params(robot, {'gains': {'kp': 2.0}})\n"
            "assert p['gains'] == {'kp': 2.0, 'ki': 0.05}\n"
            "try:\n"
            "    load_params(robot, {'speed_mps': 0})\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `cfg.get('timeout')` return when 'timeout' is absent?",
        choices=[
            "None - which is only safe if None is an acceptable value.",
            "KeyError naming the missing key.",
            "0 - get defaults to zero.",
            "The dict's last value.",
        ],
        answer=0,
        kind="conceptual",
        explanation=(
            "get() with no default returns None, and None flowing into "
            "arithmetic or a socket call fails far from the typo that created "
            "it. Bracket access raises at the source; get is correct only "
            "when None (or an explicit default) is genuinely meaningful."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="After `d = {'a': 1}; d['b'] = d.get('b', 0) + 1; d['b'] = d.get('b', 0) + 1`, what is d?",
        choices=["{'a': 1, 'b': 1}", "{'a': 1, 'b': 2}", "{'b': 2}", "KeyError on the first line."],
        answer=1,
        kind="code_output",
        explanation=(
            "The first call seeds b with 0 + 1; the second finds that 1 and "
            "adds one more. This get-and-add pair is the counting idiom in "
            "two lines - collections.Counter packages exactly this loop."
        ),
        reference="lesson.ipynb - Basic Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why does `original['cfg']['mode'] = 'b'` change `clone['cfg']['mode']` after `clone = original.copy()`?",
        choices=[
            "copy() is broken for dicts with nested keys.",
            "The copy is shallow: clone's 'cfg' key references the SAME inner dict.",
            "Dicts always share values until reassignment.",
            "The assignment syntax mutates both paths deliberately.",
        ],
        answer=1,
        kind="debugging",
        explanation=(
            "dict()/.copy() build a new outer table of the SAME value "
            "references. One 'cfg' inner dict exists, reachable from both "
            "outers, so any write through either path is visible through "
            "both. deepcopy - or rebuilding the inner dict - is the fix."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A loop adds a computed key to a dict it is iterating and raises RuntimeError. The right fix is:",
        choices=[
            "Iterate a snapshot - `for k in list(d):` - or rebuild with a comprehension.",
            "Catch RuntimeError and continue.",
            "Switch to iterating d.values().",
            "Pre-size the dict so it never resizes.",
        ],
        answer=0,
        kind="implementation_choice",
        explanation=(
            "The guard fires because resizing invalidates the live iterator's "
            "bookkeeping; a snapshot decouples traversal from mutation, and a "
            "comprehension expresses 'transform into a new dict' directly. "
            "Catching the error hides half-applied changes, and values() is "
            "just as live as keys()."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Which key type is legal in a dict?",
        choices=["['x', 'y'] - a list of two strings", "{'mode': 'a'} - a nested dict", "('cell', 3) - a tuple of ints", "Any object - dicts accept everything."],
        answer=2,
        kind="reasoning",
        explanation=(
            "Keys must hash, and a key whose hash could change would vanish "
            "from its slot. Tuples of hashables hash structurally and never "
            "change, while lists and dicts are mutable and therefore "
            "unhashable - TypeError at the moment you assign them as keys."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Why does `dict.fromkeys(('a', 'b'), [])` behave dangerously?",
        choices=[
            "It raises TypeError for tuple keys.",
            "Every key receives the SAME list object, so appends leak across keys.",
            "It creates a set instead of a dict.",
            "The default is silently dropped.",
        ],
        answer=1,
        kind="identify_error",
        explanation=(
            "fromkeys evaluates the default once and binds every key to that "
            "one object. Appending through d['a'] is visible in d['b'] - the "
            "aliasing bug wearing a dict costume. A comprehension "
            "({k: [] for k in keys}) evaluates the default per key."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A rover parameter server must update its config without disturbing readers mid-tick. Which design is safest?",
        choices=[
            "Edit the live dict in place; readers usually finish in time.",
            "Lock readers out with a global flag and mutate in place.",
            "Store updates in a side dict and merge on every read.",
            "Build a staged copy with updates applied, then rebind the name readers use to the new dict.",
        ],
        answer=3,
        kind="robotics",
        explanation=(
            "Build-then-rebind gives atomic publication: readers holding the "
            "old dict finish against a consistent snapshot, new readers get "
            "the new one, and no partially-updated state is ever visible. "
            "In-place editing leaks half-applied updates; per-read merging "
            "costs O(n) on the hot path."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="What is the cost of finding a VALUE's key by scanning a dict?",
        choices=["O(1) - dicts are always fast.", "O(log n) - the table is sorted.", "O(n) - values are not indexed; invert the mapping instead.", "O(n^2) - values must be sorted first."],
        answer=2,
        kind="reasoning",
        explanation=(
            "Hash tables index by key, not by value: every values() search is "
            "a linear walk. Building the reverse dict once - {v: k for k, v "
            "in d.items()} - converts all subsequent reverse questions to "
            "O(1), trading memory for the lookup you actually need."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="Iteration order of a Python dict is:",
        choices=[
            "Alphabetical by key.",
            "Arbitrary and may change run to run.",
            "Insertion order - guaranteed since Python 3.7.",
            "Hash order, deterministic across runs.",
        ],
        answer=2,
        kind="conceptual",
        explanation=(
            "CPython 3.7+ guarantees insertion order as part of the language, "
            "not an implementation detail - which is why reproducible output "
            "often needs no sort. It is NOT alphabetical or hash order; sort "
            "explicitly when canonical ordering, not insertion ordering, is "
            "the requirement."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="You must report ALL config problems in one pass (missing, wrong type, extra keys). The right shape is:",
        choices=[
            "Accumulate messages in a list while walking schema and values, then return them sorted.",
            "Raise on the first problem - fail fast beats completeness.",
            "Print each problem and continue silently.",
            "Delete offending keys and return the clean dict alone.",
        ],
        answer=0,
        kind="implementation_choice",
        explanation=(
            "Validation-for-reporting is a different contract from "
            "fail-fast access: the caller needs the complete picture to "
            "repair in one edit. Accumulate-then-sort produces a "
            "reproducible report; raising and printing both lose "
            "information the exercise explicitly requires."
        ),
        reference="exercises.ipynb - Exercise 9",
    )
)

RESEARCH = {
    "question": (
        "How much faster is a dict lookup than a linear scan over items for "
        "membership, and does the gap follow the O(1)-versus-O(n) model as n "
        "grows?"
    ),
    "hypothesis": (
        "The dict's advantage grows linearly with n: at each doubling of the "
        "key count, the scan doubles while the lookup stays flat, so the "
        "ratio should roughly double too."
    ),
    "experiment": [
        STEPS(
            [
                "Generate key sets of n = 1000, 5000, 25000, 100000.",
                "For each n, run 2000 membership probes: once against a dict, "
                "once against a list of the same keys, with identical probe "
                "sequences.",
                "Time dict construction separately from probing.",
                "Record every run's raw probe time, then compute the "
                "dict-versus-list ratio per n.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | n | variant | run | build_s | probe_s |"
        ),
    ],
    "analysis": [
        MD(
            "Plot probe time against n for both variants: the list line should "
            "climb with n while the dict line stays nearly flat. The ratio "
            "column is the headline - report it per n rather than averaging "
            "across sizes."
        ),
    ],
    "result": [
        MD(
            "State the ratio at the smallest and largest n and whether it "
            "roughly tracked the hypothesis. Include any n where the dict "
            "lost (small n plus noisy neighbours) and explain it."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the flat dict line via hash probing versus the list's "
            "element-by-element walk, and note why construction is a "
            "one-off cost that amortises over probes. Name two threats: "
            "hash collisions and CPU cache effects on the contiguous list."
        ),
    ],
    "conclusion": [
        MD(
            "Give a production rule: how many probes justify building a dict "
            "index, and when is a single list scan simply better because you "
            "search only once? Defend both halves with numbers."
        ),
    ],
    "extensions": [
        "Add a set-based variant and compare it with the dict's keys().",
        "Measure the cost of dict construction from a sorted list versus an "
        "unsorted one (insertion-order effects).",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Parameter Server with Atomic Updates",
    "context": (
        "The flight software reads hundreds of parameters by name on every "
        "control tick. A reload must be atomic - no reader ever sees a "
        "half-merged configuration - and a bad update must be rejected "
        "before it can reach the hot path."
    ),
    "mission": (
        "Implement `ParameterServer` supporting snapshot reads, staged "
        "updates validated in full before publication, and deletion via a "
        "None sentinel - publishing by rebinding, never by in-place edits."
    ),
    "requirements": [
        "get(name) reads the CURRENT published snapshot in O(1); a missing "
        "name raises KeyError naming it.",
        "stage(overrides) returns a validated merged candidate (nested "
        "deep-merge, None deletes) WITHOUT changing live state.",
        "commit(candidate) atomically swaps the live snapshot by rebinding "
        "one attribute.",
        "reject(candidate) discards the stage; live remains byte-identical.",
        "A staged candidate must be an independent tree - mutating it after "
        "commit cannot affect the server.",
    ],
    "constraints": [
        "No locks needed - rebinding is the atomicity mechanism; state that "
        "in the docstring.",
        "Standard library only; no copy module.",
        "Validation must report ALL problems before commit is attempted.",
    ],
    "interface": "class ParameterServer: def get(self, name): ...; def stage(self, overrides) -> dict; ...",
    "success_criteria": [
        "A rejected update leaves get() results identical at every depth.",
        "Deleting a parameter via None works only through stage/commit.",
        "Mutating a committed snapshot from outside is impossible - "
        "returning get_all() hands out a deep clone.",
        "A KeyError from get() names the missing parameter.",
    ],
    "extension": (
        "Add a version counter incremented on each commit and expose "
        "history(n) returning the last n snapshots - then explain why each "
        "snapshot must be independent rather than a diff.",
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Telemetry Schema Registry",
    "brief": (
        "Build a registry that knows every telemetry channel's schema, "
        "validates incoming records against it, groups samples by channel, "
        "and reports anomalies - all as dict operations in linear time."
    ),
    "scenario": (
        "A ground station receives interleaved records from many channels. "
        "Each channel has a schema (units, range, type); records that violate "
        "it must be reported with every problem at once, and per-channel "
        "aggregates must be reproducible across runs."
    ),
    "rationale": (
        "The registry is the dict topic assembled: schema dicts drive "
        "validation (exercise 9), grouping is the setdefault idiom (exercise "
        "4), aggregates use counting (exercise 2), and snapshot isolation "
        "keeps reader and writer apart (exercise 10)."
    ),
    "requirements": [
        "`register(channel, schema)` stores the schema; duplicate channel "
        "registration raises ValueError.",
        "`validate(record)` returns (clean, errors) with ALL violations "
        "sorted, as in exercise 9.",
        "`feed(records)` groups valid samples per channel in encounter "
        "order, counting and summing each.",
        "`stats(channel)` returns count, mean and last value without exposing "
        "internal dicts.",
        "`get_all()` returns a deep clone so callers cannot mutate registry "
        "state.",
    ],
    "constraints": [
        "Standard library only; no copy module.",
        "Every membership test O(1); feed is a single pass.",
        "Invalid records never partially enter the aggregates.",
    ],
    "deliverables": [
        "`registry.py` with the SchemaRegistry class.",
        "`test_registry.py` with at least twelve assertions, including one "
        "proving get_all() isolation and one proving sorted reproducible "
        "errors.",
        "A README section explaining validation-before-aggregation and why "
        "get_all clones.",
    ],
    "steps": [
        "Implement register() with duplicate detection; test ValueError.",
        "Implement validate() accumulating all errors; test missing, type "
        "and unexpected together.",
        "Implement feed() with per-channel counts/totals; test an invalid "
        "record leaves aggregates unchanged.",
        "Implement stats() and get_all(); assert clone isolation by mutating "
        "the clone.",
        "Integration test: 100 mixed records, assert aggregates and that two "
        "runs over shuffled input give identical stats.",
    ],
    "expected_behavior": (
        "A record with two problems reports both sorted messages and "
        "contributes nothing to aggregates, stats() never leaks internals, "
        "and shuffling input order across channels changes nothing in the "
        "per-channel results."
    ),
    "acceptance": [
        "All assertions pass from a clean kernel.",
        "get_all() mutation is proven harmless by a dedicated test.",
        "Duplicate registration and invalid records both fail loudly with "
        "named messages.",
        "README states the complexity of register, validate, feed and stats.",
    ],
    "extensions": [
        "Add a sliding-window mean per channel using deque.",
        "Track per-channel error rates and flag any channel above a "
        "threshold.",
        "Serialise the registry with json.dumps(..., sort_keys=True) and "
        "prove byte-identical round trips.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make the []-versus-get contract a conscious choice, never a habit.",
        "Have students draw the shared-inner-dict picture before they meet "
        "the bug in code.",
        "Turn 'snapshot then rebind' into their default update pattern.",
    ],
    "misconceptions": [
        [
            "copy() gives a fully independent dict.",
            "It is shallow - inner dicts remain shared objects.",
        ],
        [
            "get() is the safe version of [].",
            "It is a different contract; unsafe when absence is a real error.",
        ],
        [
            "Dicts keep sorted order.",
            "They keep insertion order; sort() only when you need sorted.",
        ],
        [
            "Mutating during iteration sometimes works.",
            "It raises RuntimeError the moment the table resizes - never rely on it.",
        ],
    ],
    "difficult_concepts": [
        "Why hashability is required of keys but not values.",
        "Atomic publication by rebinding versus in-place mutation.",
        "The cost model: what is O(1), what is O(n), and why values scans "
        "are the latter.",
    ],
    "demonstrations": [
        "Live shallow-copy corruption: clone = d.copy(); clone['cfg']['x'] = 1; "
        "print(d).",
        "Time dict lookup against linear scan at 100000 keys on the projector.",
        "Trigger RuntimeError by adding a key mid-loop, then fix with "
        "list(d).",
    ],
    "discussion": [
        "When is a KeyError better than a default? Argue both sides using "
        "the config example.",
        "Is a dict ever the wrong structure for a record? (Ordered "
        "fields with methods -> dataclass; schema validation -> pydantic.)",
    ],
    "student_errors": [
        [
            "None appears where a value should be",
            "get() without a meaningful default on a required key",
            "Use [] for required keys and let KeyError name it",
        ],
        [
            "Editing a clone changed the original",
            "Shallow copy shared the inner dict",
            "deepcopy or rebuild inner levels at the boundary",
        ],
        [
            "RuntimeError: dictionary changed size",
            "Key added/removed during iteration",
            "Snapshot with list(d) or rebuild with a comprehension",
        ],
    ],
    "pacing": (
        "65 min: pigeonhole model and access contracts (15), shallow-copy "
        "corruption live (10), views and mutation guard (10), counting and "
        "grouping idioms (10), atomic-update pattern (10), practice start (10)."
    ),
    "extensions": [
        "Compare dict insertion-order guarantee with set's arbitrary order.",
        "Explore collections.defaultdict and Counter for the counting idiom.",
    ],
    "assessment": (
        "Exercise 6 (deep copy without the module) and Exercise 10 (atomic "
        "merge) separate dict users from dict understanders."
    ),
    "support": (
        "Give struggling students the pigeonhole diagram and have them draw "
        "hash, slot and key check before writing lookups. For copy issues, "
        "require id() prints as evidence before any prose explanation.",
    ),
    "extension_fast": (
        "Fast finishers implement a tiny JSON-like serialiser for nested "
        "dicts and prove a round trip preserves insertion order.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["[`exercises.ipynb`](exercises.ipynb)", "40%", "All 10 exercises: contracts, copies and merges proven."],
        ["[`mini_project.ipynb`](mini_project.ipynb)", "25%", "SchemaRegistry with validation-before-aggregation."],
        ["[`robotics_challenge.ipynb`](robotics_challenge.ipynb)", "25%", "ParameterServer publishes atomically by rebinding."],
        ["[`research.ipynb`](research.ipynb)", "10%", "Dict-vs-scan ratios measured across four sizes."],
    ],
    "criteria": [
        ["Correctness", "30", "Every contract, error path and merge rule behaves as specified."],
        ["Isolation discipline", "25", "No shared inner state escapes; clones proven by identity assertions."],
        ["Code quality", "25", "PEP 8, docstrings, sorted output, small focused helpers."],
        ["Reasoning", "20", "Access contracts and atomicity justified in writing."],
    ],
    "bands": [
        ["Distinction", "85-100", "Correct, tested, clearly reasoned, production-shaped."],
        ["Merit", "70-84", "Correct with minor gaps in testing or documentation."],
        ["Pass", "50-69", "Core requirement met; edge cases or tests incomplete."],
        ["Fail", "0-49", "Core requirement not met, or the code does not run."],
    ],
    "band_details": [
        [
            "Distinction",
            "All exercises correct, get_all isolation proven by identity, and "
            "the parameter server rejects a bad update with zero visible "
            "change.",
        ],
        [
            "Merit",
            "Most exercises correct; one shallow-copy case untested or one "
            "sorted-output boundary missing.",
        ],
        [
            "Pass",
            "Core dict use right, but get() appears on required keys or a "
            "clone shares inner state.",
        ],
        [
            "Fail",
            "Live dict mutated during iteration, or validation partially "
            "applies an invalid record.",
        ],
    ],
}

TOPIC = topic(
    topic_id="3.4",
    title="Dictionaries",
    module=3,
    module_title="Core Data Structures",
    directory="04_dictionaries",
    summary=(
        "Python's hash map: unique hashable keys to values in amortised O(1), "
        "insertion-ordered iteration, and the three silent failures - get() "
        "masking absence, shallow copies sharing state, mutation during "
        "iteration."
    ),
    why_it_matters=(
        "Config, counters, indices, JSON payloads and parameter servers are "
        "all dicts, and the bugs are silent ones: a get() typo produces "
        "plausible garbage, a shallow copy corrupts live settings through a "
        "shared inner object, and a half-applied update is visible to every "
        "reader. The dict is where reference semantics meets production data."
    ),
    objectives=[
        "Choose [] versus .get based on whether absence is an error.",
        "Count, group and index with dict idioms in linear time.",
        "Explain why keys must be hashable and how lookup stays O(1).",
        "Diagnose and repair shallow-copy aliasing in nested records.",
        "Iterate safely by snapshotting or rebuilding instead of mutating.",
        "Publish updated mappings atomically by building then rebinding.",
    ],
    prerequisites=["Topic 3.3 Sets"],
    mental_model=LESSON["mental_model"],
    terminology=TERMS,
    lesson=LESSON,
    exercises=EXERCISES,
    solutions=SOLUTIONS,
    mini_project=MINI_PROJECT,
    research=RESEARCH,
    quiz_questions=QUIZ,
    robotics_challenge=CHALLENGE,
    instructor_notes=INSTRUCTOR_NOTES,
    rubric=RUBRIC,
    robo_x_milestone="M3",
    robo_x_package="robo_x.core",
)
