from items import LibraryItem   
import datetime

class ItemCopy:
    # Physicalcopy of a library item, tracks its state - Uses Library Item
    def __init__(self, copy_id: str, item: LibraryItem):
        self.copy_id = copy_id
        self.item = item
        self._checked_out_by = None
        self._due_date = None

    def is_available(self) -> bool:
        return self._checked_out_by is None
    
    def checkout(self, member_id: str):
        if self._checked_out_by:
            raise ValueError("Already Checked Out !")
        
        self._checked_out_by = member_id
        # Accessing LibraryItem @property -> load_period_days
        self._due_date = datetime.date.today() + datetime.timedelta(days=self.item.loan_period_days)


    def return_item(self):
        if self._checked_out_by is None:
            raise ValueError('Item Already Returned/Available')
        
        self._checked_out_by = None
        self._due_date = None

    @property
    def due_date(self):
        return self._due_date
    
    @property
    def checked_out_by(self):
        return self._checked_out_by