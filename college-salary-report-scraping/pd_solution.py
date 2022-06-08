#################### SOLUTION USING PANDAS #####################

# used libraries
import pandas as pd

# main dataframe to collect all data
table_from_html = pd.read_html(
    "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")  # get table from html
df = table_from_html[0].copy()  # copy the table to df
df.columns = ["Rank", "Major", "Type", "EarlyCareerPay", "MidCareerPay", "HighMeaning"]  # specify headers in the table

# add tables from other pages to main df
for page_no in range(2, 35):
    # get table from html on the specific page
    table_from_html = pd.read_html(
        f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page_no}")

    page_df = table_from_html[0].copy()  # copy the table from the page to main df
    page_df.columns = ["Rank", "Major", "Type", "EarlyCareerPay", "MidCareerPay",
                       "HighMeaning"]  # specify headers in the table
    df = pd.concat(objs=[df, page_df], ignore_index=True)  # append data to main df

df = df[["Major", "EarlyCareerPay", "MidCareerPay"]]  # select necessary columns only

# clean columns
df.replace({"^Major:": "", "^Early Career Pay:\$": "", "^Mid-Career Pay:\$": "", ",": ""}, regex=True, inplace=True)

# change datatype of numeric columns
df[["EarlyCareerPay", "MidCareerPay"]] = df[["EarlyCareerPay", "MidCareerPay"]].apply(pd.to_numeric)

# rename columns
df.rename(columns={"Major": "Undergraduate Major",
                   "EarlyCareerPay": "Starting Median Salary",
                   "MidCareerPay": "Mid-Career Median Salary"},
          inplace=True)

# save data from df to csv
df.to_csv("college_salary_report_2021.csv", index=False)
