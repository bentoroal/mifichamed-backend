from datetime import datetime
from enum import Enum
from html import escape
from io import BytesIO

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import ReportOut
from app.services.report_service import get_report
from app.core.translations import translate_value, get_label

router = APIRouter(prefix="/reports", tags=["Report"])


def _parse_sections(sections: str | None) -> list[str] | None:
    if not sections:
        return None

    return [
        section.strip()
        for section in sections.split(",")
        if section.strip()
    ]


def _filters_to_sections(filters: dict) -> list[str] | None:
    """Convert frontend filters dict to backend sections format."""
    sections = []
    if filters.get("includeProfile", False):
        sections.append("profile")
    if filters.get("includeConditions", False):
        sections.append("conditions")
    if filters.get("includeTreatments", False):
        sections.append("treatments")
    if filters.get("includeSymptoms", False):
        sections.append("symptoms")
    if filters.get("includeAllergies", False):
        sections.append("allergies")
    if filters.get("includeSurgeries", False):
        sections.append("surgeries")

    return sections or None


def _normalize_report_value(value):
    if isinstance(value, Enum):
        return value.value

    return value

def _translated(field_name: str, value):
    return translate_value(field_name, _normalize_report_value(value))


def _map_report_for_frontend(report: dict) -> dict:
    """Map backend report format to frontend expected shape."""
    out = {}
    generated = report.get("generated_at")
    if isinstance(generated, datetime):
        out["generatedAt"] = generated.isoformat()
    else:
        out["generatedAt"] = str(generated)

    profile = report.get("profile")
    if profile:
        out["profile"] = {
            "full_name": _normalize_report_value(getattr(profile, "full_name", None)),
            "birth_date": _normalize_report_value(getattr(profile, "birth_date", None)),
            "age": _normalize_report_value(getattr(profile, "age", None)),
            "sex": _translated("sex", getattr(profile, "sex", None)),
            "weight": _normalize_report_value(getattr(profile, "weight", None)),
            "height": _normalize_report_value(getattr(profile, "height", None)),
            "alcohol_consumption": _translated(
                "alcohol_consumption", getattr(profile, "alcohol_consumption", None)
            ),
            "smoking_habits": _translated(
                "smoking_habits", getattr(profile, "smoking_habits", None)
            ),
            "physical_activity": _translated(
                "physical_activity", getattr(profile, "physical_activity", None)
            ),
        }
    else:
        out["profile"] = None

    conditions = []
    treatments = []
    for user_condition in report.get("active_conditions", []):
        condition_data = user_condition.copy()
        condition_treatments = condition_data.pop("treatments", [])
        conditions.append(
            {
                "id": condition_data.get("id"),
                "status": _translated("status", condition_data.get("status")),
                "start_date": condition_data.get("start_date"),
                "end_date": condition_data.get("end_date"),
                "notes": condition_data.get("notes"),
                "condition": condition_data.get("condition"),
            }
        )

        for treatment in condition_treatments:
            treatments.append(
                {
                    "id": treatment.get("id"),
                    "dosage": treatment.get("dosage"),
                    "frequency": treatment.get("frequency"),
                    "start_date": treatment.get("start_date"),
                    "end_date": treatment.get("end_date"),
                    "notes": treatment.get("notes"),
                    "medication": treatment.get("medication"),
                }
            )

    out["conditions"] = conditions
    out["treatments"] = treatments
    out["symptoms"] = report.get("active_symptoms", [])
    allergies = []
    for allergy in report.get("active_allergies", []):
        allergy_data = allergy.copy()
        allergy_data["status"] = _translated("status", allergy_data.get("status"))
        allergies.append(allergy_data)
    out["allergies"] = allergies
    out["surgeries"] = report.get("surgeries", [])

    return out


def _display(value) -> str:
    if value is None:
        return "-"

    return str(value)


def _item_name(item: dict) -> str:
    for key in ("condition", "medication", "symptom", "allergy", "surgery"):
        catalog_item = item.get(key)
        if catalog_item and catalog_item.get("name"):
            return catalog_item["name"]

    return f"Registro {item.get('id') or ''}".strip()


def _build_report_pdf(mapped: dict, requested_sections: list[str] | None = None) -> BytesIO:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail=(
                "PDF generator not available. "
                "Install reportlab: pip install reportlab"
            ),
        )

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="Informe medico",
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("MiFichaMed - Informe medico", styles["Title"]),
        Paragraph(
            f"Generado: {escape(_display(mapped.get('generatedAt')))}",
            styles["Normal"],
        ),
        Spacer(1, 12),
    ]

    def cell(value):
        return Paragraph(escape(_display(value)), styles["BodyText"])

    def add_heading(title: str):
        story.append(Spacer(1, 8))
        story.append(Paragraph(escape(title), styles["Heading2"]))

    def add_table(rows: list[list], widths: list[float]):
        table = Table(rows, colWidths=widths, hAlign="LEFT", repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F1F8")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17324D")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(table)

    def add_section(title: str, items: list, columns: list[tuple[str, str]]):
        add_heading(title)
        if not items:
            story.append(Paragraph("Sin registros", styles["BodyText"]))
            return

        rows = [[cell(label) for label, _ in columns]]
        for item in items:
            rows.append(
                [
                    cell(_item_name(item) if key == "__name__" else item.get(key))
                    for _, key in columns
                ]
            )

        add_table(rows, [16 * cm / len(columns)] * len(columns))

    # Define all available sections
    sections_config = [
        ("profile", None, None, None),  # Special case: profile is handled separately
        (
            "conditions",
            "Enfermedades",
            "conditions",
            [
                ("Nombre", "__name__"),
                ("Estado", "status"),
                ("Inicio", "start_date"),
                ("Fin", "end_date"),
                ("Notas", "notes"),
            ],
        ),
        (
            "treatments",
            "Tratamientos",
            "treatments",
            [
                ("Medicamento", "__name__"),
                ("Dosis", "dosage"),
                ("Frecuencia", "frequency"),
                ("Notas", "notes"),
            ],
        ),
        (
            "symptoms",
            "Sintomas",
            "symptoms",
            [
                ("Nombre", "__name__"),
                ("Inicio", "start_date"),
                ("Fin", "end_date"),
                ("Notas", "notes"),
            ],
        ),
        (
            "allergies",
            "Alergias",
            "allergies",
            [
                ("Nombre", "__name__"),
                ("Estado", "status"),
                ("Inicio", "start_date"),
                ("Notas", "notes"),
            ],
        ),
        (
            "surgeries",
            "Cirugias",
            "surgeries",
            [
                ("Nombre", "__name__"),
                ("Fecha", "surgery_date"),
                ("Notas", "notes"),
            ],
        ),
    ]

    # If requested_sections is None, include all sections (backwards compatibility)
    # Otherwise, only include requested sections
    should_include_all = requested_sections is None

    for section_key, title, data_key, columns in sections_config:
        if section_key == "profile":
            # Handle profile specially
            if should_include_all or (requested_sections and "profile" in requested_sections):
                profile = mapped.get("profile")
                if profile:
                    add_heading("Perfil")
                    
                    # Formatear fecha de nacimiento con edad
                    birth_date = profile.get("birth_date")
                    age = profile.get("age")
                    if birth_date:
                        # Convertir a date si es string
                        if isinstance(birth_date, str):
                            from datetime import datetime as dt
                            birth_date = dt.strptime(birth_date, "%Y-%m-%d").date()
                        birth_date_display = f"{birth_date.strftime('%d/%m/%Y')} ({age} años)" if age else birth_date.strftime('%d/%m/%Y')
                    else:
                        birth_date_display = "No especificado"
                    
                    add_table(
                        [
                            [cell("Nombre"), cell(profile.get("full_name"))],
                            [
                                cell("Fecha de Nacimiento"),
                                cell(birth_date_display),
                            ],
                            [
                                cell("Peso"),
                                cell(f"{profile.get('weight')} kg" if profile.get("weight") else None),
                            ],
                            [
                                cell("Altura"),
                                cell(f"{profile.get('height')} cm" if profile.get("height") else None),
                            ],
                            [
                                cell("Consumo de Alcohol"),
                                cell(profile.get("alcohol_consumption") or "No especificado"),
                            ],
                            [
                                cell("Consumo de Cigarrillo"),
                                cell(profile.get("smoking_habits") or "No especificado"),
                            ],
                            [
                                cell("Actividad Física"),
                                cell(profile.get("physical_activity") or "No especificado")
                            ]
                        ],
                        [4 * cm, 12 * cm],
                    )
        else:
            # Handle other sections
            if should_include_all or (requested_sections and section_key in requested_sections):
                add_section(
                    title,
                    mapped.get(data_key, []),
                    columns,
                )

    doc.build(story)
    buffer.seek(0)
    return buffer


@router.get("/", response_model=ReportOut)
def report(
    sections: str | None = Query(
        None,
        description=(
            "Comma-separated report sections: "
            "profile,conditions,treatments,symptoms,allergies,surgeries"
        ),
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_report(
        db,
        current_user.id,
        sections=_parse_sections(sections),
    )


@router.post("/preview/")
def reports_preview(
    filters: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate report preview with frontend filter format."""
    try:
        sections = _filters_to_sections(filters)
        report_data = get_report(db, current_user.id, sections=sections)
        mapped = _map_report_for_frontend(report_data)
        return JSONResponse(content=jsonable_encoder(mapped))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/pdf/")
def reports_pdf(
    filters: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate and download report as PDF."""
    try:
        sections = _filters_to_sections(filters)
        report_data = get_report(db, current_user.id, sections=sections)
        mapped = jsonable_encoder(_map_report_for_frontend(report_data))
        buffer = _build_report_pdf(mapped, requested_sections=sections)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=informe-medico.pdf"
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
