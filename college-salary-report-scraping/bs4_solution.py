##################### SOLUTION USING BEAUTIFUL SOUP #####################

# used libraries
import requests
from bs4 import BeautifulSoup

# link to data of Highest Paying Jobs With a Bachelor’s Degree
CSR_LINK = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"

with open("college_salary_report_2021.csv", mode="w") as major_file:  # create file and enable writing
    major_file.write("Undergraduate Major,Starting Median Salary,Mid-Career Median Salary\n")  # write columns names

for page_no in range(34):  # range defined to go thrugh all web pages with data
    response = requests.get(f"{CSR_LINK}/page/{page_no+1}")  # link to single page
    results = response.text
    soup = BeautifulSoup(results, "html.parser")  # get html from the url

    major_list = [major.getText() for major in soup.select(selector="tr")]  # select all table rows on the page

    with open("college_salary_report_2021.csv", mode="a") as major_file:  # open file and enable appending
        for row in major_list[1:]:  # skip 0. row (headers) and go through all other rows

            # get needed data and clean it
            undergraduate_major = row.split(":")[2].replace("Degree Type", "")
            starting_salary = row.split(":")[4].strip("Mid-Career Pay").strip("$").replace(",", "")
            mid_career_salary = row.split(":")[5].strip("% High Meaning").strip("$").replace(",", "")

            # write scraped data to the file
            major_file.write(f"{undergraduate_major},{starting_salary},{mid_career_salary}\n")