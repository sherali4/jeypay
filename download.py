import os
import wget
from datetime import datetime, date
import os
import zipfile

# path = 'json/2023-08-20/'
path = 'json/2023-08-20/'
ziph = 'sher/'
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))

with zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir('json/', zipf)

# python -m pip freeze > requirements.txt
# python -m pip install -r requirements.txt

today = datetime.today()
for_filename = today.strftime('%Y-%m-%d-%H-%M-%S-%f')
foldername = date.today()
folder_path = f"json/{foldername}/"
filerange = range(270, 280)

if not os.path.isdir(folder_path):
     # os.mkdir("logo/images")
    os.makedirs(folder_path)
# print(folder_path)

# URL = "https://api.siat.stat.uz/media/uploads/sdmx/sdmx_data_548.json"
# response = wget.download(URL, f"images/sdmx_data_548.json")
for i in filerange:
    url = f'https://api.siat.stat.uz/media/uploads/sdmx/sdmx_data_{i}.json'
    filename = wget.filename_from_url(url)
    # filename = f'sdmx_data_{for_filename}_{i}.json'
    try:
        response = wget.download(url, f'{folder_path}/{filename}')
        print(filename)
    except:
        print(f"An exception occurred - {filename}")

    # print(url, filename, for_filename)






