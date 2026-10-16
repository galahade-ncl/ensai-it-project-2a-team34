import pytest

# from datetime import datetime
from src.service.file_services.xml_service import XmlService

# from src.business_object.dependency import Dependency

POM = b"""<project xmlns="http://maven.apache.org/POM/4.0.0">
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>5.3.0</version>
    </dependency>
  </dependencies>
</project>"""


def test_parse_dependencies_xml_parses_maven_dependency():
    # GIVEN
    list_result = [("org.springframework:spring-core", "5.3.0")]

    # WHEN
    list_dep = XmlService().parse_dependencies(POM)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_xml_invalid_raises():
    # GIVEN
    content = b"<project>"

    # THEN
    with pytest.raises(Exception):  # ruff: ignore[assert-raises-exception]
        XmlService.parse_dependencies(content)
