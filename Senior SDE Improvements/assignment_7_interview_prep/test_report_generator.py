"""
Tests for ReportGenerator (Part B — refactor without breaking these).

DO NOT MODIFY THIS FILE.
Run with: pytest test_report_generator.py -v

These tests describe the BEHAVIOR contract. Your refactor must keep them all
passing. If you find yourself wanting to change a test, you're refactoring
behavior, not structure — stop and rethink.
"""
from report_generator import ReportGenerator


SAMPLE_ROWS = [
    {"product": "Widget", "region": "North", "amount": 100.0},
    {"product": "Gadget", "region": "South", "amount": 50.0},
    {"product": "Widget", "region": "South", "amount": 200.0},
    {"product": "Sprocket", "region": "North", "amount": 75.0},
    {"product": "Gadget", "region": "North", "amount": 30.0},
]


class TestBasicReport:

    def test_total_is_sum_of_amounts(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        result = rg.generate()
        assert result["total"] == 455.0

    def test_by_region_aggregates(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        result = rg.generate()
        assert result["by_region"]["North"] == 205.0
        assert result["by_region"]["South"] == 250.0

    def test_by_product_aggregates(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        result = rg.generate()
        assert result["by_product"]["Widget"] == 300.0
        assert result["by_product"]["Gadget"] == 80.0
        assert result["by_product"]["Sprocket"] == 75.0

    def test_rows_included_count(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        result = rg.generate()
        assert result["rows_included"] == 5
        assert result["rows_skipped"] == 0


class TestValidation:

    def test_skips_missing_fields(self):
        rows = [
            {"product": "A", "region": "X", "amount": 10.0},
            {"product": "B", "amount": 20.0},  # missing region
            {"region": "Z", "amount": 30.0},   # missing product
        ]
        rg = ReportGenerator(rows, "x@y.com")
        result = rg.generate()
        assert result["rows_included"] == 1
        assert result["rows_skipped"] == 2
        assert result["total"] == 10.0

    def test_skips_non_numeric_amount(self):
        rows = [
            {"product": "A", "region": "X", "amount": 10.0},
            {"product": "B", "region": "Y", "amount": "twenty"},
        ]
        rg = ReportGenerator(rows, "x@y.com")
        result = rg.generate()
        assert result["rows_included"] == 1
        assert result["rows_skipped"] == 1

    def test_skips_negative_amount(self):
        rows = [
            {"product": "A", "region": "X", "amount": 10.0},
            {"product": "B", "region": "Y", "amount": -5.0},
        ]
        rg = ReportGenerator(rows, "x@y.com")
        result = rg.generate()
        assert result["rows_included"] == 1
        assert result["rows_skipped"] == 1


class TestFiltering:

    def test_min_amount_excludes_below_threshold(self):
        rg = ReportGenerator(SAMPLE_ROWS, "x@y.com")
        result = rg.generate(min_amount=80.0)
        # Only 100, 200, and... wait — 75 and 50 and 30 are out.
        # Included: 100 (Widget/North), 200 (Widget/South). Total = 300.
        assert result["total"] == 300.0
        assert result["rows_included"] == 2

    def test_min_amount_zero_includes_all(self):
        rg = ReportGenerator(SAMPLE_ROWS, "x@y.com")
        result = rg.generate(min_amount=0.0)
        assert result["rows_included"] == 5


class TestFormatting:

    def test_body_contains_total(self):
        rg = ReportGenerator(SAMPLE_ROWS, "x@y.com")
        result = rg.generate()
        assert "$455.00" in result["body"]

    def test_body_contains_region_breakdown(self):
        rg = ReportGenerator(SAMPLE_ROWS, "x@y.com")
        result = rg.generate()
        assert "North" in result["body"]
        assert "South" in result["body"]

    def test_body_contains_product_breakdown(self):
        rg = ReportGenerator(SAMPLE_ROWS, "x@y.com")
        result = rg.generate()
        assert "Widget" in result["body"]
        assert "Gadget" in result["body"]


class TestDelivery:

    def test_sends_to_recipient(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        rg.generate()
        assert len(rg.sent_inbox) == 1
        assert rg.sent_inbox[0]["to"] == "ceo@acme.com"

    def test_subject_contains_total(self):
        rg = ReportGenerator(SAMPLE_ROWS, "ceo@acme.com")
        rg.generate()
        assert "455.00" in rg.sent_inbox[0]["subject"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
