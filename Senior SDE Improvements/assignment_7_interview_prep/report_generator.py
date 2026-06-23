"""
ReportGenerator — a working monolith.

This is the kind of code an interviewer will hand you and say:
    "It works. The tests pass. Clean it up."

The class works. The single method generate() is doing five different things.
Your job in Part B is to refactor it into focused classes WITHOUT changing
behavior. The tests in test_report_generator.py must still pass.

You may modify this file freely. Add new files if you want.
The only public contract you must preserve is:
    rg = ReportGenerator(rows, recipient)
    rg.generate() -> dict with same shape as before
"""
from datetime import datetime


class ReportGenerator:
    """
    Loads sales rows, filters out invalid ones, formats them into a report,
    exports to a string, "emails" the result. All in one method.

    This is real legacy code shape. Trace it before you touch it.
    """

    def __init__(self, rows: list[dict], recipient: str):
        self.rows = rows
        self.recipient = recipient
        self.sent_inbox: list[dict] = []  # simulated email inbox

    def generate(self, min_amount: float = 0.0) -> dict:
        # --- LOAD / VALIDATE ----------------------------------------------
        valid_rows = []
        skipped = 0
        for row in self.rows:
            if "amount" not in row or "product" not in row or "region" not in row:
                skipped += 1
                continue
            if not isinstance(row["amount"], (int, float)):
                skipped += 1
                continue
            if row["amount"] < 0:
                skipped += 1
                continue
            valid_rows.append(row)

        # --- FILTER -------------------------------------------------------
        filtered = [r for r in valid_rows if r["amount"] >= min_amount]

        # --- AGGREGATE ----------------------------------------------------
        by_region: dict[str, float] = {}
        by_product: dict[str, float] = {}
        for r in filtered:
            by_region[r["region"]] = by_region.get(r["region"], 0.0) + r["amount"]
            by_product[r["product"]] = by_product.get(r["product"], 0.0) + r["amount"]
        total = sum(r["amount"] for r in filtered)

        # --- FORMAT -------------------------------------------------------
        lines = []
        lines.append(f"=== Sales Report ===")
        lines.append(f"Generated: {datetime(2026, 1, 1).isoformat()}")
        lines.append(f"Total: ${total:.2f}")
        lines.append(f"Rows: {len(filtered)} (skipped {skipped})")
        lines.append("")
        lines.append("By region:")
        for region, amt in sorted(by_region.items()):
            lines.append(f"  {region}: ${amt:.2f}")
        lines.append("")
        lines.append("By product:")
        for product, amt in sorted(by_product.items()):
            lines.append(f"  {product}: ${amt:.2f}")
        body = "\n".join(lines)

        # --- DELIVER ------------------------------------------------------
        self.sent_inbox.append({
            "to": self.recipient,
            "subject": f"Sales Report (${total:.2f})",
            "body": body,
        })

        # --- RETURN -------------------------------------------------------
        return {
            "total": total,
            "by_region": by_region,
            "by_product": by_product,
            "rows_included": len(filtered),
            "rows_skipped": skipped,
            "body": body,
        }
