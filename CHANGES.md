0.3.0
-----
- Switch from PyParsing to Lark for an almost 3x speedup
- No changes to user-facing API
- Add documentation via ReadTheDocs

0.2.0
-----
- Allow message bodies to contain newlines. If you want to split on newlines, do it yourself up-front. Reported by
  GitHub user @tfogwill

0.1.6
-----
- Require `pyparsing` 2.3 or above

0.1.5
-----
- Pin `pyparsing` to less than version 2.3 until I make this work with the new API for grouping (reported by Github user @tfogwill)

0.1.4
-----
- Properly handle messages with SD pairs that have an empty value (reported by Github user @eyalleshem)
