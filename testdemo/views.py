from django.shortcuts import render, HttpResponse
from .models import fact,factmulti
from django.core.files.storage import FileSystemStorage
import csv
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os
# Create your views here.
def factorial (request):
    if request.method == 'POST':
        # image= request.FILES.get('images')
        images = request.FILES.getlist('images')
        num = int(request.POST.get('num'))
        fact_string=" "
        fact_initial = 1
        for i in range(1, num+1):
            fact_initial *= i
            if i == num:
                new_val=(num+1)-i
                fact_string+=str(new_val)
                print(new_val,"!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                new_val=(num+1)-i
                fact_string+=str(new_val)+"*"
                print(fact_string,"______________________________")
        result = fact(factorial=num , value=fact_initial)
        print("result",result)
        result.save()
        # result1 = factmulti(multifactorial=fact_string, factorial_id=result,photo=image)
        # result1.save()
        for image in images:
            result1 = factmulti(multifactorial=fact_string, factorial_id=result,photo=image)
            print("result",result1)
            result1.save()
        # final=factmulti.objects.all()
        facts = fact.objects.all().order_by('-id').prefetch_related('items')
        print(facts,"_________________________________________________********")
        context={
            'facts':facts
        }
        return render(request, 'home.html',context)
        # return render(request, 'home.html', {'result': result,'result1':result1,})
    return render(request, 'home.html')


def export_all_data(request):
    facts = fact.objects.all().order_by('-id').prefetch_related('items')
    df = pd.DataFrame(list(facts.values('id','value', 'factorial', 'items__multifactorial','items__photo')))
    df.columns = ['ID','Value', 'Factorial', 'Multifactorial','Image']

    # df['Image'] = df.groupby('ID')['Image'].transform(lambda x: '; '.join(x.dropna().astype(str)))
    df['Image'] = df.groupby('ID')['Image'].transform(lambda x: ', '.join(x.astype(str)))
    df = df.drop_duplicates(subset=['ID'])  # Remove duplicate rows for the same ID

    csv1 = HttpResponse(content_type='text/csv')
    csv1['Content-Disposition'] = 'attachment; filename="data.csv"'
    df.to_csv(path_or_buf=csv1,index=False)
    return csv1



def export_pdf(request):
    facts = fact.objects.all().order_by('-id').prefetch_related('items')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="data.pdf"'
    
    pdf = canvas.Canvas(response, pagesize=letter)

    # pdf.drawString(100, 750, "Data")
    pdf.drawString(100, 700, "ID")
    pdf.drawString(200, 700, "Value")
    pdf.drawString(300, 700, "Factorial")
    pdf.drawString(400, 700, "Fact_Expression")
    pdf.drawString(500, 700, "Image")

    header_y = 750
    # pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(letter[0] / 2, header_y, "ALL DATA")
    
    y = 670
    page = 1
    for obj in facts:
        pdf.drawString(100, y, str(obj.id))
        pdf.drawString(200, y, str(obj.value))
        pdf.drawString(300, y, str(obj.factorial))
          
        multi=1
        for item in obj.items.all():
            if multi == 1:
                pdf.drawString(400, y, str(item.multifactorial))
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, str(item.photo))):
                pdf.drawImage(os.path.join(settings.MEDIA_ROOT, str(item.photo)), x=500, y=y-50, width=70, height=70, mask='auto')
                y -= 150
                if y < 50:
                        y = 750
                        pdf.showPage()
                        # pdf.drawString(100, 750, "Data")
                        # pdf.drawString(100, 700, "ID")
                        # pdf.drawString(200, 700, "Value")
                        # pdf.drawString(300, 700, "Factorial")
                        # pdf.drawString(400, 700, "Fact_Expression")
                        # pdf.drawString(500, 700, "Image")
                        page += 1

            else:
                pdf.drawString(200, y, "No image available")
                y -= 20
            multi=0
        multi=1









    # for obj in facts:
    #     pdf.drawString(100, y, str(obj.id))
    #     print(obj.id,"_________________________iiidddd")
    #     for item in obj.items.all():

    #         pdf.drawString(100, y, str(obj.id))
    #         pdf.drawString(200, y, str(obj.value))
    #         pdf.drawString(300, y, str(obj.factorial))
    #         pdf.drawString(400, y, str(item.multifactorial))
    #         # images=pdf.drawString(30, y, str(item.photo))
    #         images=item.photo
    #         # print(obj.id,"_________________________iiidddd")

    #         if images:
    #         # Display each image separately
    #             # for image in images:
    #                 if os.path.exists(os.path.join(settings.MEDIA_ROOT, str(images))):
    #                     pdf.drawImage(os.path.join(settings.MEDIA_ROOT, str(images)), x=500, y=y-20, width=100, height=100, mask='auto')
    #                     y -= 120  # Add vertical offset for each image
    #                 else:
    #                     pdf.drawString(500, y, "No image available")
    #                     y -= 20
    #         else:
    #             pdf.drawString(500, y, "No image available")
    #             y -= 20

    #         y -= 20  # Add vertical offset between IDs
        




    #         if os.path.exists(os.path.join(settings.MEDIA_ROOT, str(item.photo))):
    #             pdf.drawImage(os.path.join(settings.MEDIA_ROOT, str(item.photo)), x=500, y=y-20, width=100, height=100, mask='auto')
    #         else:
    #             pdf.drawString(500, y, "No image available")

    #         # pdf.drawString(30, y, str(item.photo))
    # y-= 20  # Move to the next row

    # y -= 20 # Add some space between groups of items

    # if y <= 50:
    #             pdf.showPage()
    #             y = 750
    
    pdf.showPage()
    pdf.save()
    
    return response