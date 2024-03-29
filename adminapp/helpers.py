from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa 
import uuid
from django.conf import settings
def save_pdf(params:dict):
    template=get_template("invoice2.html")
    html = template.render(params)
    response=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name=uuid.uuid4()

    try:
        with open(str(settings.BASE_DIR)+ f"/adminapp/static/{file_name}.pdf",'wb+') as output:
            output.write(response.getvalue())
    except Exception as e:
        print(f"An error occurred: {e}")
        return '', False

    if pdf.err:
        return '',False
    
    return file_name,True

