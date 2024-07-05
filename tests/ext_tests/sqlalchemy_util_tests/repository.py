from __future__ import annotations

import logging

from red_utils.ext import sqlalchemy_utils

log = logging.getLogger("tests.ext_tests.sqlalchemy_util_tests.repository")
from .models import TestUserModel

from sqlalchemy.exc import IntegrityError, NoResultFound
import sqlalchemy.orm as so


class TestUserRepository(sqlalchemy_utils.RepositoryBase):
    def __init__(self, session: so.Session):
        assert session is not None, ValueError("session cannot be None")
        assert isinstance(session, so.Session), TypeError(
            f"session must be of type sqlalchemy.orm.Session. Got type: ({type(session)})"
        )

        self.session: so.Session = session

    def add(self, entity: TestUserModel) -> None:
        """Add new entity to the database."""
        try:
            self.session.add(instance=entity)
            self.session.commit()

            ## Refresh session after committing
            self.session.refresh(entity)
        except IntegrityError as integ:
            msg = Exception(
                f"Integrity error committing entity to database. Details: {integ}"
            )
            log.warning(msg)

            raise integ
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception committing entity to database. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def remove(self, entity: TestUserModel) -> None:
        """Remove existing entity from the database."""
        try:
            self.session.delete(instance=entity)
            self.session.commit()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception removing entity from database. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def update(self, entity: TestUserModel) -> None:
        ## Search for existing entity
        try:
            existing_entity: TestUserModel = self.get_by_id(user_id=entity.user_id)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity from database. Details: {exc}"
            )
            log.error(msg)

            raise exc

        if existing_entity is None:
            ## Entity not found, insert new entity
            log.warning(f"Entity does not exist in database. Inserting")

            try:
                self.add(entity=entity)
            except Exception as exc:
                msg = Exception(
                    f"Entity not found in database, and error while attempting to insert. Details: {exc}"
                )
                log.error(msg)

                raise exc
        else:
            ## Entity found, update values & commit.
            for attr, value in entity.__dict__.items():
                try:
                    setattr(existing_entity, attr, value)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception updating attribute '{attr}' to '{value}'. Details: {exc}"
                    )
                    log.error(msg)

                    raise exc

            ## Commit changes to database
            try:
                self.session.commit()
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception updating entity with ID [{existing_entity.user_id}]. Details: {exc}"
                )
                log.error(msg)

                raise exc

    def get_all(self) -> list[TestUserModel]:
        """Return a list of all entitites found in database."""
        try:
            all_comics: list[TestUserModel] = self.session.query(TestUserModel).all()

            return all_comics
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all comic numbers from database. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def get_by_id(self, user_id: int) -> TestUserModel:
        try:
            return self.session.query(TestUserModel).get(user_id)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by ID '{user_id}'. Details: {exc}"
            )
            log.error(msg)

            raise exc

    def count(self) -> int:
        try:
            return self.session.query(TestUserModel).count()
        except Exception as exc:
            msg = Exception(f"Unhandled exception counting entities. Details: {exc}")
            log.error(msg)

            raise exc
