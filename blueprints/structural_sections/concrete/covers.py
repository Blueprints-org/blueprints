"""Module with the representation of the covers for cross-sections."""

from dataclasses import dataclass

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
        text = "Cover:"

        all_equal = bool(len({self.upper, self.lower, self.right, self.left}) == 1)
        if all_equal:
            return f"Cover: {self.upper:.0f} mm"

        covers = {cover: "" for cover in list({self.upper, self.lower, self.right, self.left})}
        covers[self.upper] = "upper"

        if covers[self.lower]:
            covers[self.lower] += "|lower"
        else:
            covers[self.lower] = "lower"

        if covers[self.left]:
            covers[self.left] += "|left"
        else:
            covers[self.left] = "left"

        if covers[self.right]:
            covers[self.right] += "|right"
        else:
            covers[self.right] = "right"

        for cover, names in covers.items():
            text += f"\n  {names}: {cover:.0f} mm"

        return text

    def validate(self) -> None:
        """Validate the covers."""
        raise_if_negative(upper=self.upper, right=self.right, lower=self.lower, left=self.left)
