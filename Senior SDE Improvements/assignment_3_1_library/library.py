"""
Library Checkout System — Starter Code

This is a WORKING but poorly designed library system.
Everything is crammed into one class. Your job is to refactor it.

Current features:
- Add items (book, magazine, dvd)
- Check out items to members
- Return items with late fee calculation
- Track member checkouts

Sample Flow User:

from items import Book, Magazine, DVD
from fee_strategy import FlatDailyFee
from library import Library

# Create the library with a fee strategy
lib = Library(fee_strategy=FlatDailyFee(rate_per_day=0.50))

# Create item objects
book = Book("B1", "Clean Code")
dvd = DVD("D1", "Inception")

# Add them to the library
lib.add_item(book)
lib.add_item(dvd)

# Member checks out a book
due_date = lib.checkout("member_001", "B1")

# Member returns it (maybe late)
fee = lib.return_item("B1")
print(f"Late fee: ${fee}")

"""
import datetime
from item_copy import ItemCopy
from items import LibraryItem
from fee_strategy import LateFeeStrategy, FlatDailyFee

class Library:
    """
    A library that handles everything in one class.
    Works, but adding new item types or fee rules is painful.
    """

    # OLD --> Initialised Lists
    # def __init__(self):
    #     self.items = {}        # item_id -> dict with all info
    #     self.checkouts = {}    # member_id -> list of item_ids
    #     self.late_fee_rate = 0.50  # flat rate per day overdue



    # NEW --> We store ItemCopy objects (item_id -> ItemCopy)
    # Fee calculation is delegated to a swappable LateFeeStrategy
    def __init__(self, fee_strategy = None):
        self.items = {}
        self.fee_strategy = fee_strategy or FlatDailyFee(0.5)
        self.checkouts = {}

    def add_item(self, item: LibraryItem) -> None:
        """
        Add an item to the library.
        item_type: 'book', 'magazine', 'dvd'
        """

        # OLD --> 15 lines of code assigning a dict with all details of the item to self.items{}
        # if item_type == "book":
        #     loan_days = 14
        # elif item_type == "magazine":
        #     loan_days = 7
        # elif item_type == "dvd":
        #     loan_days = 3
        # else:
        #     return None  # Unknown type
        
        # self.items[item.item_id] = {
        #     "title": item.title,
        #     "type": item_type,
        #     "loan_days": loan_days,
        #     "available": True,
        #     "due_date": None,
        #     "checked_out_by": None,
        # }

        # NEW --> 
        # User calls:
        # lib.add_item(Book("B1", "Clean Code"))
        #                     ↓
        # Library.add_item receives a Book object
        #                     ↓
        # Creates: ItemCopy(copy_id="B1", item=<Book object>)
        #                     ↓
        # Stores: self.items["B1"] = <ItemCopy object>

        self.items[item.item_id] = ItemCopy(copy_id=item.item_id, item=item)

    def checkout(self, member_id, item_id):
        """
        Check out an item to a member.
        Returns due_date if successful, None otherwise.
        """
        # OLD
        # if item_id not in self.items:
        #     return None

        # item = self.items[item_id]
        # if not item["available"]:
        #     return None  # Already checked out

        # due_date = datetime.date.today() + datetime.timedelta(days=item["loan_days"])
        # item["available"] = False
        # item["due_date"] = due_date
        # item["checked_out_by"] = member_id

        # if member_id not in self.checkouts:
        #     self.checkouts[member_id] = []
        # self.checkouts[member_id].append(item_id)

        # return due_date
    
        # NEW
        if item_id not in self.items:
            return None
        
        item: ItemCopy = self.items[item_id] # Gets the copy object

        if not item.is_available():
            return None
        
        item.checkout(member_id=member_id)
        
        # We add the member first with a list of their checkouts
        if member_id not in self.checkouts:
            self.checkouts[member_id] = []
        # aDding the item_id checkout by memeber by adding to their list.
        self.checkouts[member_id].append(item_id)

        return item.due_date
        

    def return_item(self, item_id):
        """
        Return an item. Calculates late fee if overdue.
        Returns late_fee (0.0 if on time), or None if item not found.
        """
        # if item_id not in self.items:
        #     return None

        # item = self.items[item_id]
        # if item["available"]:
        #     return None  # Not checked out

        # today = datetime.date.today()
        # late_fee = 0.0
        # if today > item["due_date"]:
        #     days_late = (today - item["due_date"]).days
        #     late_fee = days_late * self.late_fee_rate

        # member_id = item["checked_out_by"]
        # self.checkouts[member_id].remove(item_id)
        # item["available"] = True
        # item["due_date"] = None
        # item["checked_out_by"] = None

        # return late_fee

        if item_id not in self.items:
            return None
        
        item: ItemCopy = self.items[item_id]
        
        if item.is_available():
            return None
        
        # If book is to be returned:
        # Calculate fee, remove from member_id checkout list, make the book available again

        today = datetime.date.today()
        days_late = (today - item.due_date).days
        days_late = max(0, days_late)
        late_fee = self.fee_strategy.calculate_fee(days_late=days_late)

        member_id = item.checked_out_by
        item.return_item()
        self.checkouts[member_id].remove(item_id)
        return late_fee

    def get_available_items(self):
        """Returns list of available item_ids."""
        return [item_id for item_id, copy in self.items.items() if copy.is_available()]

    def get_member_checkouts(self, member_id):
        """Returns list of item_ids currently checked out by a member."""
        return self.checkouts.get(member_id, [])
    
    def set_fee_strategy(self, strategy: LateFeeStrategy):
        self.fee_strategy = strategy
    
# This class Library has 5 responsibilities !
# Solution: Make individual classes and file for extracting logic and refactoring the Library class.


# Expected LEarning Outcomes

# Core Learnings from Assignment 3.1:

# Abstraction & Type Hierarchy

# LibraryItem is abstract — you never instantiate it directly
# Subclasses (Book, Magazine, DVD) define their own rules via @property loan_period_days
# The system handles all types uniformly without if item_type == "book" checks
# Composition Over State Duplication

# ItemCopy wraps a LibraryItem — doesn't duplicate its data
# ItemCopy manages its own state (_checked_out_by, _due_date)
# Library stores ItemCopy objects, not raw dicts
# Each layer of abstraction has ONE job
# Strategy Pattern (Swappable Behavior)

# LateFeeStrategy lets you change fee calculation at runtime
# Library accepts a strategy as a parameter, not hardcoded
# You can swap FlatDailyFee ↔ TieredFee ↔ NoFee without touching Library code
# This is Dependency Injection
# Separation of Concerns

# LibraryItem — knows its loan period
# ItemCopy — tracks checkout state
# LateFeeStrategy — calculates fees
# Library — orchestrates everything
# Each class has ONE reason to change
# Polymorphism in Action

# Library.add_item() accepts any LibraryItem subclass
# No type checking needed — polymorphism handles it
# Observers work the same way (next assignment)
# Object Interaction Pattern

# Objects ask each other to do things: copy.checkout(member_id) vs doing it themselves
# Objects don't reach into each other's state: item.checked_out_by (property) vs item._checked_out_by (private)
# This is encapsulation
