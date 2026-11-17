from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TOOL_NAMES = (
    "find_entity",
    "get_transactions",
    "get_connected_entities",
    "get_fund_paths",
    "get_risk_findings",
    "get_timeline",
    "generate_case_brief",
    "get_email_findings",
)


class StrictArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EntityArguments(StrictArguments):
    entity_type: str = Field(min_length=1, max_length=40)
    entity_value: str = Field(min_length=1, max_length=255)


class ConnectedEntityArguments(StrictArguments):
    entity_type: str | None = Field(default=None, max_length=40)
    entity_value: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_entity_pair(self):
        if (self.entity_type is None) != (self.entity_value is None):
            raise ValueError("entity_type and entity_value must be provided together")
        return self


class TransactionArguments(StrictArguments):
    entity_type: str | None = Field(default=None, max_length=40)
    entity_value: str | None = Field(default=None, max_length=255)
    transaction_id: str | None = Field(default=None, max_length=255)
    high_value_only: bool = False
    min_amount: float | None = Field(default=None, ge=0)


class ToolSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool: Literal[TOOL_NAMES]
    arguments: dict[str, Any] = Field(default_factory=dict)


class CopilotQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
