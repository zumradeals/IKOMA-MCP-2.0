from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ikoma_mcp.core.evidence.primary import EvidencePrimary
from ikoma_mcp.core.state.integration import IntegrationState
from ikoma_mcp.gateway.exposure import GatewayExposure, GatewaySnapshot
from ikoma_mcp.gateway.views import derive_gateway_view


def test_gateway_snapshot_is_read_only():
    snapshot = GatewaySnapshot(
        target="app-1",
        state=IntegrationState.AVAILABLE,
        primary=EvidencePrimary(description="gateway available"),
        secondary=(),
    )

    with pytest.raises(FrozenInstanceError):
        snapshot.target = "app-2"


def test_gateway_exposure_is_read_only():
    snapshot = GatewaySnapshot(
        target="app-1",
        state=IntegrationState.AVAILABLE,
        primary=EvidencePrimary(description="gateway available"),
        secondary=(),
    )
    exposure = GatewayExposure(snapshots=(snapshot,))

    with pytest.raises(FrozenInstanceError):
        exposure.snapshots = ()


def test_gateway_view_unknown_without_primary_evidence():
    snapshot = GatewaySnapshot(
        target="app-2",
        state=IntegrationState.AVAILABLE,
        primary=None,
        secondary=(),
    )

    view = derive_gateway_view(snapshot)

    assert view.state is IntegrationState.UNKNOWN


def test_gateway_contracts_do_not_import_deployer_runtime():
    import ikoma_mcp.gateway.exposure as exposure_module
    import ikoma_mcp.gateway.interfaces as interfaces_module
    import ikoma_mcp.gateway.views as views_module

    for module in (exposure_module, interfaces_module, views_module):
        contents = Path(module.__file__).read_text()
        assert "ikoma_mcp.deployer" not in contents
        assert "deployer.runtime" not in contents
        assert "ikoma_mcp.runner" not in contents
        assert "runner.runtime" not in contents
