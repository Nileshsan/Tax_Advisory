import re
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def chatbot_view(request):
    """
    Django view to handle chatbot queries and return structured extracted data.
    """
    user_input = request.GET.get("query", "").strip()

    if not user_input:
        return JsonResponse({"error": "No input provided"}, status=400)

    extracted_info = extract_data(user_input)

    return JsonResponse({"response": extracted_info})

def generate_pdf(data):
    """
    Generates a PDF from extracted data and returns it as an HTTP response.
    """

    # Ensure data is valid
    if not data:
        return HttpResponse("No data provided for PDF generation.", status=400)

    try:
        # Load template and render with data
        template = get_template('users/pdf_template.html')

        html_content = template.render({'data': data})

        # Convert HTML to PDF
        pdf_result = BytesIO()
        pdf = pisa.CreatePDF(html_content, dest=pdf_result)

        if pdf.err:
            return HttpResponse("Failed to generate PDF.", status=500)

        # Prepare response with PDF
        response = HttpResponse(pdf_result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="tax_report.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
