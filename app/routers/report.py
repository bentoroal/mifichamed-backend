from io import BytesIO
from datetime import datetime

from fastapi import APIRouter, Depends, Query, Body, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.report_service import get_report
from app.schemas.report import ReportOut
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Report"])


def _parse_sections(sections: str | None) -> list[str] | None:
    if not sections:
        return None

    return [
        section.strip()
        for section in sections.split(",")
        if section.strip()
    ]


def _filters_to_sections(filters: dict) -> tuple[list[str] | None, str]:
    """Convert frontend filters dict to backend sections format"""
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

    detail = "detailed" if filters.get("detail", "summary") == "detailed" else "summary"
    return (sections or None, detail)


def _map_report_for_frontend(report: dict) -> dict:
    """Map backend report format to frontend expected shape"""
    out = {}
    generated = report.get("generated_at")
    if isinstance(generated, datetime):
        out["generatedAt"] = generated.isoformat()
    else:
        out["generatedAt"] = str(generated)

    profile = report.get("profile")
    if profile:
        out["profile"] = {
            "full_name": getattr(profile, "full_name", None),
            "weight": getattr(profile, "weight", None),
            "height": getattr(profile, "height", None),
        }
    else:
        out["profile"] = None

    # active_conditions contains condition dicts; separate treatments
    conditions = []
    treatments = []
    for cond in report.get("active_conditions", []):
        cond_copy = cond.copy()
        cond_treats = cond_copy.pop("treatments", [])
        conditions.append({
            "id": cond_copy.get("id"),
            "status": cond_copy.get("status"),
            "start_date": cond_copy.get("start_date"),
            "end_date": cond_copy.get("end_date"),
            "notes": cond_copy.get("notes"),
            "condition": cond_copy.get("condition"),
        })

        for t in cond_treats:
            treatments.append({
                "id": t.get("id"),
                "dosage": t.get("dosage"),
                "frequency": t.get("frequency"),
                "start_date": t.get("start_date"),
                "end_date": t.get("end_date"),
                "notes": t.get("notes"),
                "medication": t.get("medication"),
            })

    out["conditions"] = conditions
    out["treatments"] = treatments
    out["symptoms"] = report.get("active_symptoms", [])
    out["allergies"] = report.get("active_allergies", [])
    out["surgeries"] = report.get("surgeries", [])

    return out


@router.get("/", response_model=ReportOut)
def report(
    sections: str | None = Query(
        None,
        description="Comma-separated report sections: profile,conditions,treatments,symptoms,allergies,surgeries",
    ),
    detail: str = Query(
        "summary",
        description="Report detail level: summary or detailed",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_report(
        db,
        current_user.id,
        sections=_parse_sections(sections),
        detail=detail,
    )


@router.post("/preview/")
def reports_preview(
    filters: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate report preview with frontend filter format"""
    try:
        sections, detail = _filters_to_sections(filters)
        report = get_report(db, current_user.id, sections=sections, detail=detail)
        mapped = _map_report_for_frontend(report)
        return JSONResponse(content=mapped)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/pdf/")
def reports_pdf(
    filters: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate and download report as PDF"""
    try:
        sections, detail = _filters_to_sections(filters)
        report = get_report(db, current_user.id, sections=sections, detail=detail)
        mapped = _map_report_for_frontend(report)

        # Generate PDF with reportlab
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            raise HTTPException(status_code=500, detail="PDF generator not available. Install reportlab: pip install reportlab")

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40

        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, "MiFichaMed - Informe Médico")
        y -= 24

        c.setFont("Helvetica", 10)
        c.drawString(40, y, f"Generado: {mapped.get('generatedAt')}")
        y -= 18

        if mapped.get("profile"):
            prof = mapped["profile"]
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, "Perfil")
            y -= 16
            c.setFont("Helvetica", 10)
            c.drawString(50, y, f"Nombre: {prof.get('full_name') or ''}")
            y -= 14
            c.drawString(50, y, f"Peso: {prof.get('weight') or ''} kg")
            y -= 14
            c.drawString(50, y, f"Altura: {prof.get('height') or ''} cm")
            y -= 18

        def _draw_section(title: str, items: list):
            nonlocal y
            if y < 120:
                c.showPage()
                y = height - 40
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y, title)
            y -= 16
            c.setFont("Helvetica", 10)
            if not items:
                c.drawString(50, y, "(Sin registros)")
                y -= 14
            else:
                for it in items:
                    title_line = None
                    if it.get("condition") and it["condition"].get("name"):
                        title_line = it["condition"]["name"]
                    elif it.get("medication") and it["medication"].get("name"):
                        title_line = it["medication"]["name"]
                    elif it.get("symptom") and it["symptom"].get("name"):
                        title_line = it["symptom"]["name"]
                    elif it.get("allergy") and it["allergy"].get("name"):
                        title_line = it["allergy"]["name"]
                    elif it.get("surgery") and it["surgery"].get("name"):
                        title_line = it["surgery"]["name"]
                    else:
                        title_line = f"ID {it.get('id') or ''}"

                    c.drawString(50, y, title_line)
                    y -= 12
                    notes = it.get("notes")
                    if notes:
                        c.drawString(60, y, (notes[:120] + ("..." if len(notes) > 120 else "")))
                        y -= 12

        _draw_section("Condiciones", mapped.get("conditions", []))
        _draw_section("Tratamientos", mapped.get("treatments", []))
        _draw_section("Sintomas", mapped.get("symptoms", []))
        _draw_section("Alergias", mapped.get("allergies", []))
        _draw_section("Cirugias", mapped.get("surgeries", []))

        c.showPage()
        c.save()
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=informe-medico.pdf"})

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
