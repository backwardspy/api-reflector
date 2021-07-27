# model classes are inherently just data structures, so pylint's warning here isn't particularly useful.
# pylint: disable=too-few-public-methods

"""
Contains definitions of SQLAlchemy database models.
"""

from sqlalchemy import Column, Integer, String, Enum, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeMeta

from api_reflector import db, endpoint, rules_engine, actions


Model = db.Model  # type: DeclarativeMeta


class Endpoint(Model):
    """
    Models a mock API endpoint with method and path.
    """

    __tablename__ = "endpoint"

    id = Column(Integer, primary_key=True)

    method = Column(Enum(endpoint.Method), nullable=False)
    path = Column(String, nullable=False)

    UniqueConstraint(method, path)

    responses = relationship("Response", back_populates="endpoint")

    def __str__(self) -> str:
        return f"{self.method} {self.path}"


class Response(Model):
    """
    Models a mock API response.
    """

    __tablename__ = "response"

    id = Column(Integer, primary_key=True)

    endpoint_id = Column(Integer, ForeignKey("endpoint.id"), nullable=False)

    status_code = Column(Integer, nullable=False, default=200)
    content_type = Column(String, nullable=False, default="application/json")
    content = Column(String, nullable=False, default="")

    endpoint = relationship("Endpoint", back_populates="responses")
    rules = relationship("Rule", back_populates="response")
    actions = relationship("Action", back_populates="response")

    def __str__(self) -> str:
        max_body_length = 20
        if len(self.content) > max_body_length:
            body = self.content[:max_body_length] + "..."
        else:
            body = self.content
        return f"{self.status_code} {body}"


class Rule(Model):
    """
    Models a rule used to score mock API responses for a given request.
    """

    __tablename__ = "response_rule"

    id = Column(Integer, primary_key=True)

    response_id = Column(Integer, ForeignKey("response.id"), nullable=False)

    operator = Column(Enum(rules_engine.Operator), nullable=False)
    arguments = Column(ARRAY(String), nullable=False)

    response = relationship("Response", back_populates="rules")

    def __str__(self) -> str:
        rule_str = {
            rules_engine.Operator.EQUAL: "{} == {}",
            rules_engine.Operator.NOT_EQUAL: "{} != {}",
            rules_engine.Operator.LESS_THAN: "{} < {}",
            rules_engine.Operator.LESS_THAN_EQUAL: "{} <= {}",
            rules_engine.Operator.GREATER_THAN: "{} > {}",
            rules_engine.Operator.GREATER_THAN_EQUAL: "{} >= {}",
            rules_engine.Operator.IS_EMPTY: "{} is empty",
            rules_engine.Operator.IS_NOT_EMPTY: "{} is not empty",
            rules_engine.Operator.CONTAINS: "{} contains {}",
            rules_engine.Operator.NOT_CONTAINS: "{} does not contain {}",
        }[self.operator]
        return rule_str.format(*self.arguments)


class Action(Model):
    """
    Models an additional action to be taken when a response is chosen.
    """

    __tablename__ = "response_action"

    id = Column(Integer, primary_key=True)

    response_id = Column(Integer, ForeignKey("response.id"), nullable=False)

    action = Column(Enum(actions.Action), nullable=False)
    arguments = Column(ARRAY(String), nullable=False)

    response = relationship("Response", back_populates="actions")

    def __str__(self) -> str:
        action_str = {
            actions.Action.DELAY: "Delay for {} second(s)",
        }[self.action]
        return action_str.format(*self.arguments)
