from app.core.translations import translate_value


def test_translate_exam_type_values():
    assert translate_value("exam_type", "blood") == "Análisis de sangre"
    assert translate_value("exam_type", "urine") == "Orina"
    assert translate_value("exam_type", "stool") == "Heces"
    assert translate_value("exam_type", "imaging") == "Imágenes"
    assert translate_value("exam_type", "procedure") == "Procedimiento"
    assert translate_value("exam_type", "pathology") == "Patología"
    assert translate_value("exam_type", "other") == "Otro"
