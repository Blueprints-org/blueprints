"""Language utilities for Blueprints.

This package provides translation and language-related tools.

Wildcard translation option:
----------------------------
The Translate class supports manual translations with wildcards using '**' in the source string.
If a manual translation entry contains '**', it acts as a placeholder for any substring in that position.
For example, if the dictionary contains:
    {"With formula **:": "Met formule **:"}
then Translate("With formula 6.83:", "nl") will return "Met formule 6.83:".

See `Translate._wildcard_match` for implementation details. The amount of wildcards can be increased as needed.
"""
