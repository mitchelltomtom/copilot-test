import requests
import os

urls = [
            'https://aib.ie/content/dam/frontdoor/investorrelations/docs/resultscentre/annualreport/2022/AIB-Group-plc-AFR-dec-2022.pdf',
            'https://investorrelations.bankofireland.com/app/uploads/Bank-of-Ireland-Annual-Report-2022.pdf'
        ]

for url in urls:
    pdf_name = os.path.basename(url)
    print(pdf_name)
    response = requests.get(url, timeout=5)

    with open(pdf_name, 'wb') as f:
        f.write(response.content)
