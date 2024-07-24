from src.db.entity import PlaneTokenDB

from sqlalchemy.orm import Session


class PlaneTokensListRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_token_by_workspace(self, workspace: str) -> str:
        query = self.session.query(PlaneTokenDB).filter(PlaneTokenDB.workspace == workspace)

        row = query.one()

        return row.token
