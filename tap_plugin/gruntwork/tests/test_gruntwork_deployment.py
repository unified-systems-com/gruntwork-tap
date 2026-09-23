"""Behaviour tests for gruntwork__gruntwork_deployment (req-gruntwork-model)."""

from __future__ import annotations

import pytest
from tap_plugin.gruntwork.models import GruntworkDeployment

from tap_grid.caller_context import CallerContext
from tap_grid.services import WriteOperation, write_batch

TYPE = "gruntwork__gruntwork_deployment"


@pytest.mark.django_db
class TestGruntworkDeployment:
    def test_create_with_name_only(self) -> None:
        """req-gruntwork-model-1: a design-phase node needs only its name."""
        result = write_batch(
            [WriteOperation(verb="create_node", type_slug=TYPE, payload={"name": "staging"})],
            caller_context=CallerContext(),
        )
        assert result.results[0].success
        row = GruntworkDeployment.all_objects.get(entity_id=result.results[0].entity_id)
        assert row.name == "staging"
        assert row.repository_url == ""

    def test_name_required(self) -> None:
        """req-gruntwork-model-2: a write without a name is refused."""
        result = write_batch(
            [WriteOperation(verb="create_node", type_slug=TYPE, payload={"repository_url": "x"})],
            caller_context=CallerContext(),
        )
        assert not result.results[0].success


def test_keyed_by_name() -> None:
    """req-gruntwork-model-3: the key rests only on a field the model carries."""
    assert GruntworkDeployment.NATURAL_KEY == ("name",)
    names = {f.name for f in GruntworkDeployment._meta.get_fields()}
    assert all(k in names for k in GruntworkDeployment.NATURAL_KEY)
