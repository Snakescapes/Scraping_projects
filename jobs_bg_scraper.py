import requests
import xlsxwriter as xl
import time
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.now()
year, month, day = today.year, today.month, today.day
hour, minutes = today.hour, today.minute


row = 0
col = 0
job_index = 0

pages_to_search = int(input('How many pages should I search? '))
print('Searching...')

# Output file specs:
workbook = xl.Workbook(f'{year}-{month}-{day} Job_Search_{pages_to_search}p_{hour}h{minutes}.xlsx')
worksheet = workbook.add_worksheet('Results')

for page in range(0, (pages_to_search * 15), 15):
    # The url has filters applied. For more options need to update it from jobs.bg accordingly.
    url = f'https://www.jobs.bg/front_job_search.php?frompage={page}&add_sh=1&location_sid=1&distance=0&categories%5B0%5D=56&type_all=0&position_level_all=0&company_type%5B0%5D=0&keyword=&job_languages_all=0&salary_from=0&last=0#paging'
    # Filters /
    # url = f'https://www.jobs.bg/front_job_search.php?frompage={page}&add_sh=1&location_sid=1&distance=0&categories%5B0%5D=38&categories%5B1%5D=13&categories%5B2%5D=11&categories%5B3%5D=22&categories%5B4%5D=19&categories%5B5%5D=24&categories%5B6%5D=25&categories%5B7%5D=17&categories%5B8%5D=51&type_all=0&position_level_all=0&company_type%5B0%5D=0&keyword=&job_languages_all=0&salary_from=0&last=0#paging'
    current_page = requests.get(url)
    current_page.raise_for_status()
    soup = BeautifulSoup(current_page.text, 'html.parser')
    jobs_on_page = soup.select('a.joblink')



    for current_job in jobs_on_page:
        job = current_job.get('href')
        job_url = 'http://www.jobs.bg/' + job
        open_job = requests.get(job_url)
        open_job.raise_for_status()
        job_soup = BeautifulSoup(open_job.text, 'html.parser')

        job_date = job_soup.find('td', class_='explainGray').text
        job_title = job_soup.title.string
        job_text = job_soup.text.lower()
        # print(job_text)

        # What to look for in the job opportunities:
        keywords_to_check = ['python', 'django', 'flask']

        # keywords_to_check = ['психолог', 'психология', 'психоанализа', 'терапия']

        if any(word in job_text for word in keywords_to_check):
            job_index += 1
            result = [job_index, job_url, job_date, job_title]
            worksheet.write(row, col, job_index)
            worksheet.write(row, col+1, job_url)
            worksheet.write(row, col+2, job_date)
            worksheet.write(row, col+3, job_title)
            row += 1
    time.sleep(1)

workbook.close()
print('Search finished! You can find the results in the newly created Excel worksheet.')



