import pydantic

from api_reflector.models import Endpoint
from api_reflector.rules_engine import TemplatableRequest, render_rule_arg


class DeconstructedRule(pydantic.BaseModel):
    template: str
    rendered: str


class DeconstructedResponse(pydantic.BaseModel):
    name: str
    rules: list[DeconstructedRule]

    def __str__(self) -> str:
        return self.name


class DeconstructedEndpoint(pydantic.BaseModel):
    name: str
    method: str
    path: str
    responses: list[DeconstructedResponse]

    def __str__(self) -> str:
        return f"{self.name} ({self.method} {self.path})"


def render_rule(rule: Rule) -> str:
    request = TemplatableRequest()
    args = [render_rule_arg(arg, request) for arg in rule.arguments]


def deconstruct(endpoint: Endpoint) -> DeconstructedEndpoint:
    return DeconstructedEndpoint(
        name=endpoint.name,
        method=endpoint.method.value,
        path=endpoint.path,
        responses=[
            DeconstructedResponse(
                name=response.name,
                rules=[DeconstructedRule(template=str(rule), rendered=render_rule(rule)) for rule in response.rules],
            )
            for response in endpoint.responses
        ],
    )
