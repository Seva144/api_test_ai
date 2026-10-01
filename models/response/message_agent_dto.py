# models/response/test_case_dto.py
from pydantic import BaseModel, ConfigDict, Field


class TestStepDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore", str_strip_whitespace=False)

    step: str
    test_data: str = Field(alias="testData")
    expected_result: str = Field(alias="expectedResult")


class TestCaseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore", str_strip_whitespace=False)

    id: str
    key: str
    name: str
    status: str
    precondition: str | None = None
    objective: str | None = None
    folder: str | None = None
    priority: str | None = None
    component: str | None = None
    labels: str | None = None
    owner: str | None = None
    estimated_time: str | None = Field(default=None, alias="estimatedTime")
    coverage_issues: str | None = Field(default=None, alias="coverageIssues")
    coverage_pages: str | None = Field(default=None, alias="coveragePages")
    steps: list[TestStepDTO] = []

    test_script_plain_text: str | None = Field(default=None, alias="testScriptPlainText")
    test_script_bdd: str | None = Field(default=None, alias="testScriptBDD")
    markdown: str | None = None
    source: str | None = None
    requirement_id: str | None = Field(default=None, alias="requirementId")
    order_index: int | None = Field(default=None, alias="orderIndex")