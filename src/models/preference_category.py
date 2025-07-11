class PreferenceCategory:
    id: int
    category: str
    description: str

    def __init__(self, id: int, category: str, description: str):
        self.id = id
        self.category = category
        self.description = description