"""Module with the representation of the covers for cross-sections."""

from dataclasses import dataclass

from blueprints.type_alias import MM


@dataclass
class CoversRectangular:
    """Representation of the covers of a rectangular cross-section."""

    upper: MM = 50.0
    right: MM = 50.0
    lower: MM = 50.0
    left: MM = 50.0

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
