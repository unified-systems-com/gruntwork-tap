"""Gruntwork Deployment — a Gruntwork deployment: the Gruntwork-managed estate (account factory, infrastructure-live repository and pipelines) that provisions and governs a set of cloud accounts."""

from typing import Any, ClassVar

from django.db import models

from tap_grid.models import BaseModel


class GruntworkDeployment(BaseModel):
    """A Gruntwork deployment: the Gruntwork-managed estate (account factory, infrastructure-live repository and pipelines) that provisions and governs a set of cloud accounts.

    v0 is the outer node only: a design can place it before any access exists, so its one
    identifying field stays blank (not observed) until a collector reads it.

    Spec: specs/spec-gruntwork-v0.md (req-gruntwork-model).
    """

    ENTITY_TYPE: ClassVar[str] = "gruntwork__gruntwork_deployment"
    ENTITY_NAME: ClassVar[str] = "Gruntwork Deployment"
    ENTITY_DESCRIPTION: ClassVar[str] = "A Gruntwork deployment: the Gruntwork-managed estate (account factory, infrastructure-live repository and pipelines) that provisions and governs a set of cloud accounts."
    ENTITY_ICON: ClassVar[str] = "gruntwork-deployment"
    # No default dimension: the dcom value belongs to the observation (a seeded design node is
    # `design`, a collected one `configuration`), so the bundle that seeds a node stamps it.
    DEFAULT_DIMENSIONS: ClassVar[dict[str, str]] = {}
    # A design-phase node has no observed identifier; its name is the only fact it carries.
    # Revisit when the collector makes repository_url observable (req-gruntwork-collector).
    NATURAL_KEY: ClassVar[tuple[str, ...]] = ("name",)
    DEFAULT_DISPLAY: ClassVar[dict[str, Any]] = {
        "tap_viz": {
            "shape": "round-rectangle",
            "colors": {"fill": "#FFFFFF", "border": "#1D2B3A", "label": "#1D2B3A"},
            "label": {"valign": "bottom", "halign": "center", "position": "outside"},
        }
    }

    FIELD_CRUD_SCHEMA: ClassVar[dict[str, Any]] = {
        "name": {"type": "string", "minLength": 1},
        "repository_url": {"type": "string"},
        "tags": {"type": "object"},
    }
    FIELD_VALIDATION_SCHEMA: ClassVar[dict[str, Any]] = {
        "name": {"validation": "jsonschema", "schema": {"type": "string", "minLength": 1}},
        "repository_url": {"validation": "jsonschema", "schema": {"type": "string"}},
        "tags": {"validation": "jsonschema", "schema": {"type": "object"}},
    }
    CREATE_REQUIRED: ClassVar[list[str]] = ["name"]

    name = models.CharField(max_length=255, blank=True, default="", db_index=True)
    # The infrastructure-live repository the deployment is driven from. Blank until observed.
    repository_url = models.CharField(max_length=512, blank=True, default="")
    tags = models.JSONField(default=dict, blank=True)

    class Meta(BaseModel.Meta):
        db_table = "gruntwork__gruntwork_deployment"

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.get_name()
