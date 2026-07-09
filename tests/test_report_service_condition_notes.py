import unittest
from datetime import date

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.condition import ConditionCatalog
from app.models.enums import ConditionCategory, ConditionStatus
from app.models.user import User
from app.models.user_condition import UserCondition
from app.routers.report import _map_report_for_frontend
from app.services.report_service import get_report


class TestReportServiceConditionNotes(unittest.TestCase):
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
            condition = ConditionCatalog(
                name="Diabetes",
                category=ConditionCategory.ENDOCRINE_METABOLIC,
                is_custom=False,
            )
            session.add_all([user, condition])
            session.commit()
            session.refresh(user)
            session.refresh(condition)

            user_condition = UserCondition(
                user_id=user.id,
                condition_id=condition.id,
                status=ConditionStatus.ACTIVE,
                start_date=date(1991, 12, 23),
                notes="Nota personal de la enfermedad",
            )
            session.add(user_condition)
            session.commit()
            session.refresh(user_condition)
        finally:
            session.close()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_summary_report_keeps_user_condition_notes(self):
        db = self.SessionLocal()
        try:
            user = db.query(User).first()
            report = get_report(db, user.id, sections=["conditions"], detail="summary")
        finally:
            db.close()

        conditions = report["active_conditions"]
        self.assertEqual(len(conditions), 1)
        self.assertEqual(conditions[0]["notes"], "Nota personal de la enfermedad")

    def test_map_report_for_frontend_keeps_user_condition_notes(self):
        db = self.SessionLocal()
        try:
            user = db.query(User).first()
            report = get_report(db, user.id, sections=["conditions"], detail="detailed")
        finally:
            db.close()

        mapped = _map_report_for_frontend(report)
        self.assertEqual(len(mapped["conditions"]), 1)
        self.assertEqual(mapped["conditions"][0]["notes"], "Nota personal de la enfermedad")
