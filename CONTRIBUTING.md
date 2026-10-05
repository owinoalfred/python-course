# Contributing Guidelines

Thank you for contributing to the Python Master Course!

## Content authoring workflow

The course is being migrated from generated boilerplate to hand-authored
material **one topic at a time**. A topic is "authored" once it lives in
`course_content/_authored/` and passes the linter with zero findings.

### Authoring a new topic (the real path)

1. Copy an existing authored topic as a starting point:
   `course_content/_authored/topic_01_introduction.py`
2. Write the topic using the DSL in `tools/coursegen/dsl.py`
   (`MD`, `CODE`, `CODE_CELL`, `BULLETS`, `STEPS`, `TABLE`, `NOTE`, `TIP`, `WARN`,
   `EQUATION`). Use `CODE_CELL` for anything the learner should be able to run.
3. Register it in `course_content/_authored/__init__.py`:
   ```python
   from . import topic_01_introduction, topic_02_your_topic

   AUTHORED = {
       topic_01_introduction.TOPIC.topic_id: topic_01_introduction.TOPIC,
       topic_02_your_topic.TOPIC.topic_id: topic_02_your_topic.TOPIC,
   }
   ```
4. Rebuild and check:
   ```bash
   python tools/build_course.py --topic <topic-id>
   python tools/coursegen/lint.py --topic <topic-id>
   ```

The build stays green throughout because unregistered topics simply fall back to
the generated baseline.

### The placeholder generator (legacy)

`self_created_tools/topic_builder.py` produces the *baseline* content for topics
that have not been authored yet. It is scaffolding only — do not extend it, and
do not add new topics to it. Its output deliberately fails the linter so the
remaining work stays visible.

## Validation

```bash
python tools/build_course.py --check    # schema validation, writes nothing
python tools/build_course.py --lint     # content-quality dashboard
python tools/course_integrity_checker.py
python tools/notebook_validator.py
python -m pytest
```

The test suite asserts that every **authored** topic still meets the Content
Standard, so a regression fails CI immediately.

## Pull request checklist

- [ ] `python tools/build_course.py` succeeds
- [ ] `python tools/coursegen/lint.py --topic <id>` reports zero findings
- [ ] `python -m pytest` passes
- [ ] Committed notebooks match a fresh build (the build is deterministic)
