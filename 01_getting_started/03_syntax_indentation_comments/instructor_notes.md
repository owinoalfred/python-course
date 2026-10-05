# Instructor notes — 1.3 Python Syntax, Indentation, Comments, and Code Structure

**Module 1: Getting Started with Python**

## Teaching objectives

- Make indentation-as-grammar explicit rather than assumed.
- Distinguish comments, which vanish, from docstrings, which persist.
- Show that Python's parser is a tool for reading code as data.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Indentation is only cosmetic in Python. | It is part of the grammar; inconsistent indentation is a parse error. |
| Docstrings are just comments with nicer formatting. | They are real string objects retrievable at runtime via __doc__. |
| Semicolons make code more compact and therefore better. | They make every line a line the reader must mentally split again. |
| An IndentationError means the file has stray spaces at the end. | It usually means tabs and spaces are mixed within one block. |

## Difficult concepts

- Believing that structure lives in brackets rather than in the margin.
- Using an explicit stack to mirror what the parser does with INDENT and DEDENT.
- Reading an AST as data rather than as a curiosity.

## Demonstration suggestions

- Deliberately break indentation in a file and let Python refuse to parse it.
- Run tokenize over a small file and show INDENT and DEDENT tokens directly.
- Print a function's __doc__ after defining it, then show that a comment cannot be retrieved at all.

## Discussion questions

- Why did Python's designers give up braces? What did they gain and what did they lose?
- When would you accept a machine-generated file that uses a different indent width?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| TabError after pasting code from somewhere else | The source used tabs while the file uses spaces | Convert the file to spaces in one mechanical pass |
| Unexpected indent on a line that looks correct | A previous block header was deleted, leaving the body dangling | Re-indent the selection and inspect the block above |
| Docstring appears in the class but not the function | It was written as a comment, or placed after another statement | Place the string first in the body, with no preceding statement |

## Recommended pacing

90 minutes of lesson with live demonstrations, then 2 hours on exercises. Give extra time to the stack-based parser: it is the first genuinely algorithmic task in the course.

## Extension activities

- Have students implement the parser recursively and compare stack usage on deep input.
- Ask them to write a formatter that re-indents a whole file using ast.

## Assessment advice

Grade against rubric.md. Exercises 7 to 10 carry the signal; a student who can explain the pop loop has understood the grammar in operational terms.

## Differentiation

**If students are struggling:** ('Draw the stack on paper with them for a three-level sample before they write any code.',)

**If students finish early:** ('Ask for a tokenize-based version of parse_blocks and a short comparison of the two.',)
