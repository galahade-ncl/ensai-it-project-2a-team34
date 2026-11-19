import re

from business_object.dependency import Dependency


class TxtService:
    """
    Service that parses ``.txt`` dependency files (``requirements.txt``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.txt`` file.

        Comments, empty lines and pip options (``-r``, ``-e``...) are
        ignored. Only exact versions (``==``) are kept.

        Parameters
        ----------
        content : bytes
            Content of the ``.txt`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        text = content.decode("utf-8-sig")
        list_dep = []
        for line in text.splitlines():
            line = line.split("#")[0].strip()  # remove the comments
            if not line or line.startswith("-"):  # ignore -r, -e, options
                continue
            m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:==\s*([^\s;]+))?", line)
            if m:
                list_dep.append(Dependency(name=m.group(1), version=m.group(2)))
        return list_dep
