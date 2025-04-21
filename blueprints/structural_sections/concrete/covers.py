"""Module with the representation of the covers for cross-sections."""

from collections import defaultdict
from dataclasses import asdict, dataclass

from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative

DEFAULT_COVER = 50  # mm


@dataclass(frozen=True)
class CoversRectangular:
    """Representation of the covers of a rectangular cross-section."""

    upper: MM = DEFAULT_COVER
    right: MM = DEFAULT_COVER
    lower: MM = DEFAULT_COVER
    left: MM = DEFAULT_COVER

    def __post_init__(self) -> None:
        """Post initialization of the covers."""
        self.validate()

    def get_covers_info(self) -> str:
        """Return a string with the covers of the cross-section."""
        caption_text = "Cover:"

        covers = defaultdict(list)

        for key, value in asdict(self).items():
            covers[value].append(key)

        if len(covers) == 1:
            return f"{caption_text} {self.upper:.0f} mm"

        cover_texts = [caption_text]

        for cover, names in covers.items():
            cover_texts.append(f"{'|'.join(names)}: {cover:.0f} mm")

        return "\n  ".join(cover_texts)

    def validate(self) -> None:
        """Validate the covers."""
        raise_if_negative(upper=self.upper, right=self.right, lower=self.lower, left=self.left)
