import PyPDF2

def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as file:
        # Créer un lecteur de PDF
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extraire le texte de chaque page
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

    # Enregistrer le texte extrait dans un fichier txt
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == '__main__':
    pdf_path = 'C:\\Users\\Dominic\\OneDrive\\AI\\context_data\\LoggingLoggingOpenShiftContainerPlatform4.10.pdf'
    txt_path = 'C:\\Users\\Dominic\\OneDrive\\AI\\context_data\\LoggingLoggingOpenShiftContainerPlatform4.10.txt'
    convert_pdf_to_txt(pdf_path, txt_path)
