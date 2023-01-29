from enum import StrEnum, IntEnum
from typing import Type, Optional
from typing_extensions import Self

from pydantic import BaseModel
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
        """ Return the dominions server flag corresponding to this StoryEvents value."""
        if self.value == "all":
            return "--allstoryevents"
        elif self.value == "some":
            return "--storyevents"
        return "--nostoryevents"

class Game(BaseModel):
    name: str
    era: Era
    master_password: str

    renaming: bool = True
    hof_size: int = 20
    cataclysm: Optional[int] = None
    story_events: StoryEvents = StoryEvents.some

    port: int = 9191
    cheat_detection: bool = False
    steam: bool = False
    text_only: bool = True
    tcp_server: bool = True

    def to_server_args(self) -> str:
        """ Create dominions server script arguments based on the configuration stored
        in this class.
        """
        args = ""

        args += f"--era {self.era.to_int()}"
        args += f"--masterpass {self.master_password}"

        args += f"--hofsize {self.hof_size}"
        args += self.story_events.to_arg()

        if self.cataclysm:
            args += f"--cataclysm {self.cataclysm}"

        if self.text_only:
            args += "--textonly"

        if not self.cheat_detection:
            args += "--nocheatdet"

        if not self.steam:
            args += "--nosteam"

        args += self.name

    @classmethod
    def from_yaml_file(cls: Type[Self], path: str) -> Self:

        with open(path, "r") as stream:
            parsed = yaml.safe_load(stream)

        return cls(**parsed)
