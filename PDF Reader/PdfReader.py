import pyttsx3
import pdfplumber
import PyPDF2

file = 'PdfReader.pdf'

pdfObj = open(file,'rb')

pdfReader = PyPDF2.PdfFileReader(pdfObj,strict=False)  #use PyPDF2 as version lower than 2.5

pages = pdfReader.numPages

with pdfplumber.open(file) as pdf:
    #for all the pages traversing
    for i in range(0,pages):
        page = pdf.pages[i]
        text = page.extract_text()
        #print(text)
        speaker = pyttsx3.init()
        speaker.say(text)
        speaker.runAndWait()
