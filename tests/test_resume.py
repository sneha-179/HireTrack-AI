import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def get_token():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "resumetest@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "resumetest@test.com",
        "password": "test1234"
    })
    return response.json()["access_token"]


def get_dummy_pdf():
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((100, 100), "Sneha Patidar - Python Developer - FastAPI MySQL Docker")
    pdf_bytes = doc.tobytes()
    return io.BytesIO(pdf_bytes)


def test_upload_resume():
    token = get_token()
    pdf = get_dummy_pdf()
    response = client.post("/resumes/upload",
        files={"file": ("test_resume.pdf", pdf, "application/pdf")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert "resume_id" in response.json()


def test_get_resume():
    token = get_token()
    pdf = get_dummy_pdf()
    client.post("/resumes/upload",
        files={"file": ("test_resume.pdf", pdf, "application/pdf")},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get("/resumes/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "resume_id" in response.json()


def test_delete_resume():
    token = get_token()
    pdf = get_dummy_pdf()
    upload = client.post("/resumes/upload",
        files={"file": ("test_resume.pdf", pdf, "application/pdf")},
        headers={"Authorization": f"Bearer {token}"}
    )
    resume_id = upload.json()["resume_id"]
    response = client.delete(f"/resumes/{resume_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Resume deleted successfully"


def test_upload_non_pdf():
    token = get_token()
    response = client.post("/resumes/upload",
        files={"file": ("test.txt", io.BytesIO(b"not a pdf"), "text/plain")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"