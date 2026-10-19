import re

from business_object.dependency import Dependency


class TxtService:
    """Service that handles file.txt methods"""

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies from a content (txt)
        Args:
            content (bytes): content of a file.txt
        Returns:
            List of Dependency object found in the file
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
