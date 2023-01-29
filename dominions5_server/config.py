from enum import StrEnum, IntEnum
from typing import Type, Optional
from typing_extensions import Self

from pydantic import BaseModel, root_validator
import yaml


class Era(StrEnum):
    EA = "EA"
    MA = "MA"
    LA = "LA"

    def to_int(self) -> int:
        """Return the int representation of this era."""
        if self.value == "EA":
            return 1
        elif self.value == "MA":
            return 2
        return 3


class StoryEvents(StrEnum):
    all = "all"
    some = "some"
    none = "none"

    def to_arg(self) -> str:
        """Return the dominions server flag corresponding to this StoryEvents value."""
        if self.value == "all":
            return "--allstoryevents"
        elif self.value == "some":
            return "--storyevents"
        return "--nostoryevents"


class VictoryOptions(BaseModel):
    l1_thrones: int = 0
    l2_thrones: int = 0
    l3_thrones: int = 0
    ascension_points: Optional[int] = None

    cataclysm: Optional[int] = None

    conquer_all: bool = False

    def to_args(self) -> str:
        args = (
            f"--thrones {self.l1_thrones} {self.l2_thrones} {self.l3_thrones} --requiredap {self.ascension_points}"
            if not self.conquer_all
            else "--conqall"
        )

        if self.cataclysm:
            args += f" --cataclysm {self.cataclysm}"

        return args

    @root_validator
    def check_which_victory_condition(cls, values):
        """Validate that either throne or conquer all victory condition is used, not both."""
        if values.get("conquer_all"):
            assert (
                values.get("ascension_points") is None
            ), "Conquer all and and ascension points cannot both be set"
        else:
            assert (
                values.get("ascension_points") is not None
            ), "Either Conquer all or ascension points must be set as the victory condition."
        return values


class Game(BaseModel):
    name: str
    era: Era
    master_password: str

    renaming: bool = True
    hof_size: int = 20

    story_events: StoryEvents = StoryEvents.some
    victory: VictoryOptions

    port: int = 9191
    cheat_detection: bool = False
    steam: bool = False
    text_only: bool = True
    tcp_server: bool = True

    def to_server_args(self) -> str:
        """Create dominions server script arguments based on the configuration stored
        in this class.
        """
        args = ""

        args += f"--era {self.era.to_int()}"
        args += f"--masterpass {self.master_password}"

        args += f"--hofsize {self.hof_size}"
        args += self.story_events.to_arg()

        if self.text_only:
            args += "--textonly"

        if not self.cheat_detection:
            args += "--nocheatdet"

        if not self.steam:
            args += "--nosteam"

        args += self.name

    @classmethod
    def from_yaml_file(cls: Type[Self], path: str) -> Self:
        """Read settigns from a yaml file in the given path."""

        with open(path, "r") as stream:
            parsed = yaml.safe_load(stream)

        return cls(**parsed)
