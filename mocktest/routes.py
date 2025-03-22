from ninja import Router, UploadedFile, File
import pdfplumber


router: Router = Router()


@router.post("/upload")
def upload(request, file: UploadedFile = File(...)) -> dict[str, str]:
    with pdfplumber.open(file) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )
        return {"extracted_text": text}
