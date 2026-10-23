import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtWidgets import QApplication

from policy_bridge.policybridge_gui import GuiPolicyBridgeNode, PolicySummary


def test_soft_cost_bar_uses_full_scale_at_252():
    app = QApplication.instance() or QApplication(["soft_cost_gui_test"])
    summary = PolicySummary()
    summary.update_policy({
        "configured_zones": ["A", "F"],
        "soft_costs": {"A": 252, "F": 200},
    })
    app.processEvents()
    for bar in summary.cost_bars.values():
        assert bar.minimum() == 0
        assert bar.maximum() == 252
    assert summary.cost_bars["A"].value() == 252
    assert summary.cost_values["A"].text() == "252"
    assert summary.cost_bars["F"].value() == 200
    summary.close()


@pytest.mark.parametrize("percentage,expected", [(-5, 0), (17, 17), (120, 100)])
def test_gui_battery_event_uses_english_command(percentage, expected):
    messages = []
    node = SimpleNamespace(_gui_event_pub=SimpleNamespace(publish=messages.append))

    GuiPolicyBridgeNode.set_battery_from_gui(node, percentage)

    assert len(messages) == 1
    assert messages[0].data == f"battery {expected}%"

