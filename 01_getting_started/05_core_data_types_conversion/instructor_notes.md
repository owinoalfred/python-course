# Instructor notes — 1.5 Core Data Types and Type Conversion

**Module 1: Getting Started with Python**

## Teaching objectives

- Make external-text conversion the centrepiece of the topic.
- Install the conversion ladder as the default reflex for configuration.
- Show that bool being a subclass of int is a real, not theoretical, hazard.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Python converts types automatically when arithmetic needs them. | Only int and float promote; everything else needs an explicit call. |
| 0 is truthy because it is a number. | Zero is falsy, which is why `if value:` skips a legitimate zero reading. |
| 0.1 + 0.2 equals 0.3. | Binary floating point cannot represent either value exactly. |
| A numeric check automatically rejects booleans. | bool inherits from int, so True passes an int check unless excluded. |

## Difficult concepts

- Convincing students that partial success beats raising at a system boundary.
- Reasoning about representation error rather than treating it as a quirk.
- Seeing where the type boundary is in their own pipeline.

## Demonstration suggestions

- Print 0.1 + 0.2 at full precision and then compare with 0.3.
- Show float(True) returning 1.0 while isinstance(True, int) is True.
- Parse a deliberately corrupt telemetry frame and show the good channels survive.

## Discussion questions

- Where in a real robot system would you place the conversion boundary?
- When is Decimal worth its cost, and when is a tolerance sufficient?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| A zero reading is ignored by a guard | Truthiness was used where an explicit comparison was meant | Test with `value is not None` or compare to a bound |
| ValueError raised on a text sensor field | Conversion happened inside the control loop rather than at the boundary | Parse once at the edge and pass typed values downstream |
| A boolean passes a numeric range check | isinstance(value, int) also admits bool | Exclude bool before the numeric check |

## Recommended pacing

90 minutes of lesson, then 2 hours on exercises. Spend time on the conversion ladder; it recurs in Modules 4, 7, 8 and 9.

## Extension activities

- Ask students to write a validator for their own domain's units.
- Introduce the difference between float and Decimal for a billing use case.

## Assessment advice

Grade against rubric.md. Exercises 6, 9 and 10 carry the signal: they require partial success, tolerance reasoning and ordered fallback.

## Differentiation

**If students are struggling:** ('Give students a table of values with their type, repr and bool result, and have them predict the missing column before running anything.',)

**If students finish early:** ('Ask for a short design note on how the same validator would handle binary protobuf payloads instead of text.',)
