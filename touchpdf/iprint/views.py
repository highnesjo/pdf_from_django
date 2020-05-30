from django.shortcuts import render,redirect
from django.http import HttpResponse

from docxtpl import DocxTemplate
from pdf417 import encode, render_image
import subprocess
from django.http import FileResponse

import datetime
import barcode
from barcode.writer import ImageWriter
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



def age_calc(dob):
    # Figure out your age

    currentDate = datetime.datetime.now()
    dob = dob.split('-')
    print(dob[0])
    x = datetime.datetime(int(dob[0]),int(dob[1]),int(dob[2]))
    deadlineDate = x
    # deadline = datetime.datetime.strptime(deadline, '%y-%m-%d')
    print (deadlineDate)
    daysLeft = currentDate -deadlineDate
    print(daysLeft)

    years = ((daysLeft.total_seconds())/(365.242*24*3600))
    yearsInt=int(years)

    months=(years-yearsInt)*12
    monthsInt=int(months)
    return str(yearsInt)+" Years ,"+str(monthsInt)+" months "

def convertpdf(document_name):
    output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,document_name])


@csrf_exempt
def application_form(request):

    if request.method == 'POST':

        def pr(name):
            return request.POST.get(name)
        
        doc = DocxTemplate("admission_form.docx")
        aadhar = None
        sclass = None
        if request.POST.get('aadhar') != '0':
            aadhar = request.POST.get('aadhar')
        if request.POST.get('coa') == '1':
            sclass = 'First'
        elif request.POST.get('coa') == '2':
            sclass = 'Second'
        elif request.POST.get('coa') == '3':
            sclass = 'Third'
        elif request.POST.get('coa') == '4':
            sclass = 'Fourth'

        p = request.POST.get('application_no')
        age = age_calc(pr('dob'))

        text = "Application no: " + request.POST.get('application_no') + "-Name: "+ request.POST.get('name') + "-Gender :" + request.POST.get('gender') + "-Date of birth :"+ str(request.POST.get('dob'))+ "-Class on admission: "+ str(request.POST.get('coa')) + "-Aadhar: "+ str(request.POST.get('aadhar'))+"-Name of father: "+ request.POST.get('father')+"-Name of mother: "+ request.POST.get('mother') +"-Mobile: "+str(request.POST.get('mob'))+"-Address: "+request.POST.get('address')
        # Convert to code words
        codes = encode(text)
        # Generate barcode as image
        image = render_image(codes)  # Pillow Image object
        image.save('barcode.png')

        context = {'p1':p[:5] ,'p2':p[5:7] ,'p3': p[7:12] , 'name' : pr('name').upper(),'gender':pr('gender'),'a':aadhar,'father':pr('father'),'address':pr('address'),'mobile':pr('mob'),'mother':pr('mother'),'dob':pr('dob'),'age':age,'class':sclass}
        doc.render(context)
        doc.replace_media('dummy.png','barcode.png')
        doc.save("admission_form_print.docx")

        convertpdf("admission_form_print.docx")

        return redirect(report)

def report(request):
    pdf = open('admission_form_print.pdf', 'rb')
    return HttpResponse(pdf, content_type='application/pdf')
    # response = FileResponse(pdf)
    # return response
