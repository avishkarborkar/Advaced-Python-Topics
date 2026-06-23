"""
Tests for Assignment 3.1 — Library Checkout System

Run with: python -m pytest test_library.py -v
"""
import pytest
import datetime


# ─────────────────────────────────────────────
# 1. LibraryItem hierarchy
# ─────────────────────────────────────────────

class TestLibraryItemClasses:

    def test_item_base_class_exists(self):
        from items import LibraryItem
        assert LibraryItem is not None

    def test_book_is_library_item(self):
        from items import Book, LibraryItem
        book = Book(item_id="B1", title="Clean Code")
        assert isinstance(book, LibraryItem)

    def test_magazine_is_library_item(self):
        from items import Magazine, LibraryItem
        mag = Magazine(item_id="M1", title="Nature")
        assert isinstance(mag, LibraryItem)

    def test_dvd_is_library_item(self):
        from items import DVD, LibraryItem
        dvd = DVD(item_id="D1", title="Inception")
        assert isinstance(dvd, LibraryItem)

    def test_item_has_id_and_title(self):
        from items import Book
        book = Book(item_id="B1", title="Clean Code")
        assert book.item_id == "B1"
        assert book.title == "Clean Code"

    def test_item_knows_loan_period(self):
        from items import Book, Magazine, DVD
        assert Book("B1", "x").loan_period_days == 14
        assert Magazine("M1", "x").loan_period_days == 7
        assert DVD("D1", "x").loan_period_days == 3

    def test_library_item_is_abstract(self):
        from items import LibraryItem
        with pytest.raises(TypeError):
            LibraryItem("X1", "test")


# ─────────────────────────────────────────────
# 2. ItemCopy — tracks one physical copy
# ─────────────────────────────────────────────

class TestItemCopy:

    def test_copy_class_exists(self):
        from item_copy import ItemCopy
        assert ItemCopy is not None

    def test_copy_is_available_when_created(self):
        from item_copy import ItemCopy
        from items import Book
        book = Book("B1", "Clean Code")
        copy = ItemCopy(copy_id=1, item=book)
        assert copy.is_available() is True

    def test_copy_not_available_after_checkout(self):
        from item_copy import ItemCopy
        from items import Book
        book = Book("B1", "Clean Code")
        copy = ItemCopy(copy_id=1, item=book)
        copy.checkout(member_id="alice")
        assert copy.is_available() is False

    def test_copy_available_after_return(self):
        from item_copy import ItemCopy
        from items import Book
        book = Book("B1", "Clean Code")
        copy = ItemCopy(copy_id=1, item=book)
        copy.checkout(member_id="alice")
        copy.return_item()
        assert copy.is_available() is True

    def test_copy_tracks_due_date(self):
        from item_copy import ItemCopy
        from items import Book
        book = Book("B1", "Clean Code")
        copy = ItemCopy(copy_id=1, item=book)
        copy.checkout(member_id="alice")
        expected = datetime.date.today() + datetime.timedelta(days=14)
        assert copy.due_date == expected

    def test_copy_tracks_member(self):
        from item_copy import ItemCopy
        from items import Magazine
        mag = Magazine("M1", "Nature")
        copy = ItemCopy(copy_id=1, item=mag)
        copy.checkout(member_id="bob")
        assert copy.checked_out_by == "bob"

    def test_copy_cannot_double_checkout(self):
        from item_copy import ItemCopy
        from items import DVD
        dvd = DVD("D1", "Inception")
        copy = ItemCopy(copy_id=1, item=dvd)
        copy.checkout(member_id="alice")
        with pytest.raises(ValueError):
            copy.checkout(member_id="bob")

    def test_copy_cannot_return_when_available(self):
        from item_copy import ItemCopy
        from items import Book
        book = Book("B1", "Clean Code")
        copy = ItemCopy(copy_id=1, item=book)
        with pytest.raises(ValueError):
            copy.return_item()


# ─────────────────────────────────────────────
# 3. LateFeeStrategy
# ─────────────────────────────────────────────

class TestLateFeeStrategies:

    def test_strategy_is_abstract(self):
        from fee_strategy import LateFeeStrategy
        with pytest.raises(TypeError):
            LateFeeStrategy()

    def test_flat_daily_fee(self):
        from fee_strategy import FlatDailyFee
        strategy = FlatDailyFee(rate_per_day=0.50)
        fee = strategy.calculate_fee(days_late=4, item_type="book")
        assert fee == 2.0

    def test_flat_daily_fee_zero_days(self):
        from fee_strategy import FlatDailyFee
        strategy = FlatDailyFee(rate_per_day=0.50)
        fee = strategy.calculate_fee(days_late=0, item_type="book")
        assert fee == 0.0

    def test_tiered_fee(self):
        """First N days at base rate, remaining at higher rate."""
        from fee_strategy import TieredFee
        strategy = TieredFee(base_rate=0.25, base_days=3, overflow_rate=1.0)
        # 5 days late: 3 * 0.25 + 2 * 1.0 = 0.75 + 2.0 = 2.75
        fee = strategy.calculate_fee(days_late=5, item_type="book")
        assert fee == 2.75

    def test_tiered_fee_within_base(self):
        from fee_strategy import TieredFee
        strategy = TieredFee(base_rate=0.25, base_days=3, overflow_rate=1.0)
        fee = strategy.calculate_fee(days_late=2, item_type="book")
        assert fee == 0.50

    def test_no_fee_strategy(self):
        """Some libraries have no late fees."""
        from fee_strategy import NoFee
        strategy = NoFee()
        fee = strategy.calculate_fee(days_late=100, item_type="dvd")
        assert fee == 0.0


# ─────────────────────────────────────────────
# 4. Library (orchestrator)
# ─────────────────────────────────────────────

class TestLibrary:

    def test_library_creation(self):
        from library import Library
        lib = Library()
        assert lib is not None

    def test_add_and_checkout_book(self):
        from library import Library
        from items import Book
        lib = Library()
        book = Book("B1", "Clean Code")
        lib.add_item(book)
        due_date = lib.checkout(member_id="alice", item_id="B1")
        assert due_date == datetime.date.today() + datetime.timedelta(days=14)

    def test_checkout_unavailable_item(self):
        from library import Library
        from items import Book
        lib = Library()
        book = Book("B1", "Clean Code")
        lib.add_item(book)
        lib.checkout(member_id="alice", item_id="B1")
        result = lib.checkout(member_id="bob", item_id="B1")
        assert result is None

    def test_checkout_nonexistent_item(self):
        from library import Library
        lib = Library()
        result = lib.checkout(member_id="alice", item_id="NOPE")
        assert result is None

    def test_return_item_on_time(self):
        from library import Library
        from items import DVD
        lib = Library()
        dvd = DVD("D1", "Inception")
        lib.add_item(dvd)
        lib.checkout(member_id="alice", item_id="D1")
        fee = lib.return_item(item_id="D1")
        assert fee == 0.0

    def test_item_available_after_return(self):
        from library import Library
        from items import Magazine
        lib = Library()
        mag = Magazine("M1", "Nature")
        lib.add_item(mag)
        lib.checkout(member_id="alice", item_id="M1")
        lib.return_item(item_id="M1")
        result = lib.checkout(member_id="bob", item_id="M1")
        assert result is not None

    def test_get_available_items(self):
        from library import Library
        from items import Book, DVD
        lib = Library()
        lib.add_item(Book("B1", "Clean Code"))
        lib.add_item(DVD("D1", "Inception"))
        lib.checkout(member_id="alice", item_id="B1")
        available = lib.get_available_items()
        assert "D1" in available
        assert "B1" not in available

    def test_get_member_checkouts(self):
        from library import Library
        from items import Book, Magazine
        lib = Library()
        lib.add_item(Book("B1", "Clean Code"))
        lib.add_item(Magazine("M1", "Nature"))
        lib.checkout(member_id="alice", item_id="B1")
        lib.checkout(member_id="alice", item_id="M1")
        checkouts = lib.get_member_checkouts("alice")
        assert "B1" in checkouts
        assert "M1" in checkouts

    def test_library_uses_fee_strategy(self):
        from library import Library
        from items import Book
        from fee_strategy import FlatDailyFee
        lib = Library(fee_strategy=FlatDailyFee(rate_per_day=1.0))
        assert lib is not None

    def test_swap_fee_strategy(self):
        from library import Library
        from fee_strategy import FlatDailyFee, NoFee
        lib = Library(fee_strategy=FlatDailyFee(rate_per_day=1.0))
        lib.set_fee_strategy(NoFee())
        assert lib is not None
