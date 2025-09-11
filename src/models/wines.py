import uuid

class Wine:
    wine_id: int
    wine_name: str
    type: str
    elaborate: str
    grapes: str
    harmonize: str
    abv: float
    body: str
    acidity: str
    country: str
    region: str
    winery: str
    vintages: str
    id: uuid.UUID

    def __init__(
        self,
        wine_id: int,
        wine_name: str,
        type: str,
        elaborate: str,
        grapes: str,
        harmonize: str,
        abv: float,
        body: str,
        acidity: str,
        country: str,
        region: str,
        winery: str,
        vintages: str,
        id: uuid.UUID
    ):
        self.wine_id = wine_id
        self.wine_name = wine_name
        self.type = type
        self.elaborate = elaborate
        self.grapes = grapes
        self.harmonize = harmonize
        self.abv = abv
        self.body = body
        self.acidity = acidity
        self.country = country
        self.region = region
        self.winery = winery
        self.vintages = vintages
        self.id = id

    def id_to_str(self):
        return str(self.id)