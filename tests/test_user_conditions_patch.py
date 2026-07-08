import unittest
from datetime import date

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi import HTTPException

from app.db.base import Base
from app.models.condition import ConditionCatalog
from app.models.enums import ConditionCategory, ConditionStatus
from app.models.user import User
from app.models.user_condition import UserCondition
from app.routers.user_conditions import update as update_user_condition_route
from app.schemas.user_condition import UserConditionUpdate


class TestUserConditionPatch(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        Base.metadata.create_all(bind=self.engine)

        session = self.SessionLocal()
        try:
            user = User(email="user@test.com", hashed_password="x")
            other_user = User(email="other@test.com", hashed_password="x")
            condition = ConditionCatalog(
                name="Diabetes",
                category=ConditionCategory.ENDOCRINE_METABOLIC,
                is_custom=False,
            )
            session.add_all([user, other_user, condition])
            session.commit()
            session.refresh(user)
            session.refresh(other_user)
            session.refresh(condition)

            user_condition = UserCondition(
                user_id=user.id,
                condition_id=condition.id,
                status=ConditionStatus.ACTIVE,
                start_date=date(1991, 12, 23),
                notes="initial",
            )
            other_condition = UserCondition(
                user_id=other_user.id,
                condition_id=condition.id,
                status=ConditionStatus.ACTIVE,
            )
            session.add_all([user_condition, other_condition])
            session.commit()
            session.refresh(user_condition)
            session.refresh(other_condition)

            self.user_id = user.id
            self.user_email = user.email
            self.user_hashed_password = user.hashed_password
            self.user_condition_id = user_condition.id
            self.other_user_condition_id = other_condition.id
        finally:
            session.close()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_patch_user_condition_success(self):
        db = self.SessionLocal()
        try:
            result = update_user_condition_route(
                self.user_condition_id,
                UserConditionUpdate(
                    status=ConditionStatus.CHRONIC,
                    start_date=date(1992, 1, 1),
                    end_date=date(1992, 2, 1),
                    notes="updated",
                ),
                current_user=User(
                    id=self.user_id,
                    email=self.user_email,
                    hashed_password=self.user_hashed_password,
                ),
                db=db,
            )
        finally:
            db.close()

        self.assertEqual(result.id, self.user_condition_id)
        self.assertEqual(result.status, ConditionStatus.CHRONIC)
        self.assertEqual(str(result.start_date), "1992-01-01")
        self.assertEqual(str(result.end_date), "1992-02-01")
        self.assertEqual(result.notes, "updated")

    def test_patch_user_condition_returns_404_for_other_user(self):
        db = self.SessionLocal()
        try:
            with self.assertRaises(HTTPException) as exc:
                update_user_condition_route(
                    self.other_user_condition_id,
                    UserConditionUpdate(notes="nope"),
                    current_user=User(
                        id=self.user_id,
                        email=self.user_email,
                        hashed_password=self.user_hashed_password,
                    ),
                    db=db,
                )
        finally:
            db.close()

        self.assertEqual(exc.exception.status_code, 404)
        self.assertEqual(exc.exception.detail, "UserCondition not found")
