"""Smoke and presentation-model tests for the Streamlit application."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIRECTORY = PROJECT_ROOT / "app"
sys.path.insert(0, str(APP_DIRECTORY))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app_model import allocation_rows, build_dashboard_state, metric_rows, path_rows, turnover_rows, verdict_rows
from streamlit_app import PROJECT_DOCUMENTS, read_project_document


class AppModelTests(unittest.TestCase):
    def test_base_state_uses_three_engine_results_and_is_not_decision_ready(self) -> None:
        state = build_dashboard_state()
        self.assertEqual([result.name for result in state.results], ["Equal weight", "Policy benchmark", "Constrained minimum-volatility"])
        self.assertEqual(len(state.table.labels), 60)
        self.assertTrue(all(not assessment.decision_ready for assessment in state.assessments))
        equal_turnover_rule = next(rule for rule in state.assessments[0].rules if rule.rule == "Annual turnover <= 25%")
        self.assertEqual(equal_turnover_rule.status, "FAIL")

    def test_scenario_is_explicit_and_not_a_base_mandate_change(self) -> None:
        base = build_dashboard_state()
        scenario = build_dashboard_state(True)
        self.assertFalse(base.bil_scenario_enabled)
        self.assertTrue(scenario.bil_scenario_enabled)
        self.assertEqual(scenario.results[-1].scenario_label, "10% BIL scenario")
        scenario_rule = next(rule for rule in scenario.assessments[-1].rules if rule.rule == "10% BIL minimum")
        self.assertEqual(scenario_rule.status, "SCENARIO")

    def test_display_paths_are_engine_aligned(self) -> None:
        state = build_dashboard_state()
        self.assertEqual(len(metric_rows(state)), 3)
        self.assertEqual(len(allocation_rows(state)), 12)
        for metric in ("Wealth index", "Drawdown"):
            rows = path_rows(state, metric)
            self.assertEqual(len(rows), 3 * len(state.table.labels))
            self.assertEqual(rows[0]["Date"], state.table.labels[0])
        self.assertEqual(len(turnover_rows(state.results[-1].analytics)), 5)
        self.assertTrue(any(row["Status"] == "UNVERIFIED" for row in verdict_rows(state.assessments[-1])))
        self.assertEqual({row["Portfolio"] for row in allocation_rows(state)}, {"Equal Weight", "60/40 Benchmark", "Constrained"})

    def test_streamlit_module_imports_without_running_the_server(self) -> None:
        specification = importlib.util.spec_from_file_location("phase4_streamlit_app", APP_DIRECTORY / "streamlit_app.py")
        self.assertIsNotNone(specification)
        module = importlib.util.module_from_spec(specification)
        assert specification.loader is not None
        specification.loader.exec_module(module)
        self.assertTrue(callable(module.main))

    def test_streamlit_page_renders_base_state_without_exception(self) -> None:
        app_test = AppTest.from_file(str(APP_DIRECTORY / "streamlit_app.py"))
        app_test.run(timeout=30)
        self.assertFalse(app_test.exception)
        self.assertEqual(app_test.title[0].value, "Meridian Foundation Reserve")
        self.assertTrue(any("NOT DECISION-READY" in element.value for element in app_test.error))

    def test_documentation_viewer_reads_and_renders_the_three_project_documents(self) -> None:
        expected_headings = {
            "Data integrity and point-in-time": "# Phase 2B data integrity and point-in-time documentation",
            "Portfolio-engine methodology": "# Phase 3B portfolio-engine methodology",
            "Phase 3B validation report": "# Phase 3B validation report",
        }
        self.assertEqual({title for title, _ in PROJECT_DOCUMENTS}, set(expected_headings))
        for title, path in PROJECT_DOCUMENTS:
            self.assertIn(expected_headings[title], read_project_document(path))

        app_test = AppTest.from_file(str(APP_DIRECTORY / "streamlit_app.py"))
        app_test.run(timeout=30)
        self.assertFalse(app_test.exception)
        rendered_markdown = "\n".join(element.value for element in app_test.markdown)
        for heading in expected_headings.values():
            self.assertIn(heading, rendered_markdown)

    def test_scenario_checkbox_can_enable_reset_and_enable_again(self) -> None:
        app_test = AppTest.from_file(str(APP_DIRECTORY / "streamlit_app.py"))
        app_test.run(timeout=30)
        self.assertFalse(app_test.checkbox[0].value)

        app_test.checkbox[0].check().run(timeout=30)
        self.assertFalse(app_test.exception)
        self.assertTrue(app_test.checkbox[0].value)
        self.assertTrue(any("Scenario active" in element.value for element in app_test.warning))

        reset_button = next(button for button in app_test.button if button.label == "Reset to base")
        reset_button.click().run(timeout=30)
        self.assertFalse(app_test.exception)
        self.assertFalse(app_test.checkbox[0].value)
        self.assertFalse(any("Scenario active" in element.value for element in app_test.warning))

        app_test.checkbox[0].check().run(timeout=30)
        self.assertFalse(app_test.exception)
        self.assertTrue(app_test.checkbox[0].value)
        self.assertTrue(any("Scenario active" in element.value for element in app_test.warning))

    def test_nonlocked_stress_button_renders_stop_statuses(self) -> None:
        app_test = AppTest.from_file(str(APP_DIRECTORY / "streamlit_app.py"))
        app_test.run(timeout=30)
        stress_button = next(button for button in app_test.button if button.key == "run_nonlocked_stresses")
        stress_button.click().run(timeout=60)
        self.assertFalse(app_test.exception)
        self.assertTrue(any("NOT DECISION-READY" in element.value for element in app_test.error))
        stress_frame = next(element.value for element in app_test.dataframe if "Case" in element.value.columns)
        self.assertIn("Hypothetical return shift: -10 bps monthly", stress_frame["Case"].tolist())


