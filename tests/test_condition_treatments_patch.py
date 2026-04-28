import unittest
from datetime import date

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models
from fastapi import HTTPException
from app.db.base import Base
from app.models.condition import ConditionCatalog
from app.models.condition_treatment import ConditionTreatment
from app.models.enums import ConditionCategory, ConditionStatus
from app.models.medication import MedicationCatalog
from app.models.user import User
from app.models.user_condition import UserCondition
from app.routers.condition_treatments import update as update_condition_treatment_route
from app.schemas.condition_treatment import ConditionTreatmentUpdate


class TestConditionTreatmentPatch(unittest.TestCase):
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

        seed_db = self.SessionLocal()

        user_1 = User(email="user1@test.com", hashed_password="x")
        user_2 = User(email="user2@test.com", hashed_password="x")
        seed_db.add_all([user_1, user_2])
        seed_db.commit()
        seed_db.refresh(user_1)
        seed_db.refresh(user_2)

        condition = ConditionCatalog(
            name="Hipertension",
            category=ConditionCategory.CARDIOVASCULAR,
            is_custom=False,
        )
        seed_db.add(condition)
        seed_db.commit()
        seed_db.refresh(condition)

        user_condition_1 = UserCondition(
            user_id=user_1.id,
            condition_id=condition.id,
            status=ConditionStatus.ACTIVE,
        )
        user_condition_2 = UserCondition(
            user_id=user_2.id,
            condition_id=condition.id,
            status=ConditionStatus.ACTIVE,
        )
        seed_db.add_all([user_condition_1, user_condition_2])
        seed_db.commit()
        seed_db.refresh(user_condition_1)
        seed_db.refresh(user_condition_2)

        medication_1 = MedicationCatalog(name="Aspirina", is_custom=False)
        medication_2 = MedicationCatalog(name="Ibuprofeno", is_custom=False)
        medication_other_user = MedicationCatalog(
            name="Custom ajeno",
            is_custom=True,
            created_by_user_id=user_2.id,
        )
        seed_db.add_all([medication_1, medication_2, medication_other_user])
        seed_db.commit()
        seed_db.refresh(medication_1)
        seed_db.refresh(medication_2)
        seed_db.refresh(medication_other_user)

        own_treatment = ConditionTreatment(
            user_condition_id=user_condition_1.id,
            medication_id=medication_1.id,
            dosage="10mg",
            frequency="daily",
            start_date=date(2026, 1, 10),
            notes="initial note",
        )
        other_treatment = ConditionTreatment(
            user_condition_id=user_condition_2.id,
            medication_id=medication_1.id,
            dosage="20mg",
            frequency="daily",
        )
        seed_db.add_all([own_treatment, other_treatment])
        seed_db.commit()
        seed_db.refresh(own_treatment)
        seed_db.refresh(other_treatment)

        self.user_1_id = user_1.id
        self.user_1_email = user_1.email
        self.user_1_hashed_password = user_1.hashed_password
        self.own_treatment_id = own_treatment.id
        self.other_treatment_id = other_treatment.id
        self.own_user_condition_id = user_condition_1.id
        self.other_user_condition_id = user_condition_2.id
        self.medication_1_id = medication_1.id
        self.medication_2_id = medication_2.id
        self.medication_other_user_id = medication_other_user.id
        seed_db.close()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_patch_condition_treatment_success(self):
        db = self.SessionLocal()
        try:
            result = update_condition_treatment_route(
                self.own_treatment_id,
                ConditionTreatmentUpdate(
                    medication_id=self.medication_2_id,
                    dosage="25mg",
                    frequency="twice daily",
                    start_date=date(2026, 2, 1),
                    end_date=date(2026, 3, 1),
                    notes="updated note",
                ),
                current_user=User(
                    id=self.user_1_id,
                    email=self.user_1_email,
                    hashed_password=self.user_1_hashed_password,
                ),
                db=db,
            )
        finally:
            db.close()

        self.assertEqual(result.id, self.own_treatment_id)
        self.assertEqual(result.user_condition_id, self.own_user_condition_id)
        self.assertEqual(result.medication_id, self.medication_2_id)
        self.assertEqual(result.dosage, "25mg")
        self.assertEqual(result.frequency, "twice daily")
        self.assertEqual(str(result.start_date), "2026-02-01")
        self.assertEqual(str(result.end_date), "2026-03-01")
        self.assertEqual(result.notes, "updated note")

    def test_patch_condition_treatment_returns_404_for_other_user(self):
        db = self.SessionLocal()
        try:
            with self.assertRaises(HTTPException) as exc:
                update_condition_treatment_route(
                    self.other_treatment_id,
                    ConditionTreatmentUpdate(notes="should not work"),
                    current_user=User(
                        id=self.user_1_id,
                        email=self.user_1_email,
                        hashed_password=self.user_1_hashed_password,
                    ),
                    db=db,
                )
        finally:
            db.close()

        self.assertEqual(exc.exception.status_code, 404)
        self.assertEqual(
            exc.exception.detail,
            "ConditionTreatment not found or not owned",
        )

    def test_patch_condition_treatment_ignores_user_condition_id(self):
        db = self.SessionLocal()
        try:
            result = update_condition_treatment_route(
                self.own_treatment_id,
                ConditionTreatmentUpdate.model_validate(
                    {
                        "user_condition_id": self.other_user_condition_id,
                        "notes": "keeps ownership",
                    }
                ),
                current_user=User(
                    id=self.user_1_id,
                    email=self.user_1_email,
                    hashed_password=self.user_1_hashed_password,
                ),
                db=db,
            )
        finally:
            db.close()

        self.assertEqual(result.user_condition_id, self.own_user_condition_id)
        self.assertEqual(result.notes, "keeps ownership")

        session = self.SessionLocal()
        try:
            db_obj = session.get(ConditionTreatment, self.own_treatment_id)
            self.assertEqual(db_obj.user_condition_id, self.own_user_condition_id)
        finally:
            session.close()

    def test_patch_condition_treatment_partial_payload_updates_only_sent_fields(self):
        db = self.SessionLocal()
        try:
            result = update_condition_treatment_route(
                self.own_treatment_id,
                ConditionTreatmentUpdate(notes="partial update only"),
                current_user=User(
                    id=self.user_1_id,
                    email=self.user_1_email,
                    hashed_password=self.user_1_hashed_password,
                ),
                db=db,
            )
        finally:
            db.close()

        self.assertEqual(result.notes, "partial update only")
        self.assertEqual(result.dosage, "10mg")
        self.assertEqual(result.frequency, "daily")
        self.assertEqual(result.medication_id, self.medication_1_id)
        self.assertEqual(str(result.start_date), "2026-01-10")
        self.assertIsNone(result.end_date)

    def test_patch_condition_treatment_rejects_inaccessible_medication(self):
        db = self.SessionLocal()
        try:
            with self.assertRaises(HTTPException) as exc:
                update_condition_treatment_route(
                    self.own_treatment_id,
                    ConditionTreatmentUpdate(
                        medication_id=self.medication_other_user_id
                    ),
                    current_user=User(
                        id=self.user_1_id,
                        email=self.user_1_email,
                        hashed_password=self.user_1_hashed_password,
                    ),
                    db=db,
                )
        finally:
            db.close()

        self.assertEqual(exc.exception.status_code, 404)
        self.assertEqual(
            exc.exception.detail,
            "Medication not found or not accessible",
        )


if __name__ == "__main__":
    unittest.main()
