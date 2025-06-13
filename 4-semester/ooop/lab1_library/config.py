class LibraryConfig:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.max_books_per_user = 5
            self.default_search_strategy = "composite"
            self.max_borrow_days = 14
            self.fine_per_day = 0.50
            self.email_notifications_enabled = True
            self.auto_save_enabled = True
            self.backup_interval_minutes = 30
            self._initialized = True

    def get_config(self) -> dict:
        return {
            'max_books_per_user': self.max_books_per_user,
            'default_search_strategy': self.default_search_strategy,
            'max_borrow_days': self.max_borrow_days,
            'fine_per_day': self.fine_per_day,
            'email_notifications_enabled': self.email_notifications_enabled,
            'auto_save_enabled': self.auto_save_enabled,
            'backup_interval_minutes': self.backup_interval_minutes
        }

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

    def reset_to_defaults(self):
        self.max_books_per_user = 5
        self.default_search_strategy = "composite"
        self.max_borrow_days = 14
        self.fine_per_day = 0.50
        self.email_notifications_enabled = True
        self.auto_save_enabled = True
        self.backup_interval_minutes = 30