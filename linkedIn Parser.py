from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import csv

def getstr(stri):
    temp = stri.split()
    main = ""
    for val in temp:
        main += val + " "
    return main

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.linkedin.com/")

driver.find_element_by_id("session_key").send_keys("<email>")
driver.find_element_by_id("session_password").send_keys("<password>")
driver.find_element_by_class_name("sign-in-form__submit-button").click()

# To get all the links of search result in a text file
details = []
for i in range(1, 101):
    path = "https://www.linkedin.com/search/results/companies/?industry=%5B%22109%22%2C%22127%22%5D&origin=FACETED_SEARCH&page=" + str(i)
    driver.get(path)
    data = driver.find_elements_by_class_name("app-aware-link")
    for entry in data:
        if entry.get_attribute('href').startswith("https://www.linkedin.com/company/"):
            if entry.get_attribute('href') not in details:
                details.append(entry.get_attribute('href'))
for a in details:
    print(a)
print("\n", len(details))

with open("links.txt", "w") as file:
    for link in details:
        file.write(link)
        file.write("\n")

with open(r"C:\Users\M Usman\Desktop\RESULT.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Studio Name", "Industry", "Company Size", "Headquarters", "Type", "Founded", "Specialities", "Overview", "Website", "Profile Pic"])
    writer.writeheader()

# To parse company data from those links and write on file
with open("links.txt", "r") as file:
    data = file.read().split()
    for link in data:
        link += "about/"
        print(link)
        driver.get(link)
        Data = driver.page_source
        soup = BeautifulSoup(Data, 'html.parser')
        name = "Not Available"
        industry = "Not Available"
        size = "Not Available"
        headquarters = "Not Available"
        type = "Not Available"
        founded = "Not Available"
        specialities = "Not Available"
        overview = "Not Available"
        web = "Not Available"
        image = "Not Available"

        name = soup.find('h1', attrs={'class': 'org-top-card-summary__title t-24 t-black t-bold truncate'})
        if name != None:
            name = getstr(name.text.encode('utf8').decode('ascii', 'ignore'))
        overview = soup.find('p', attrs={'class': 'break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal'})
        if overview != None:
            overview = overview.text.encode('utf8').decode('ascii', 'ignore')
        size = soup.find('dd', attrs={'class': 'org-about-company-module__company-size-definition-text t-14 t-black--light mb1 fl'})
        yes = False
        if size != None:
            if size.text != None:
                size = size.text.encode('utf8').decode('ascii', 'ignore')
                yes = True
        size2 = soup.find('dd', attrs={'class': 'org-page-details__employees-on-linkedin-count t-14 t-black--light mb5'})
        if size2 != None:
            if size2.text != None:
                size += " " + size2.text.encode('utf8').decode('ascii', 'ignore')
        if yes:
            size = getstr(size)
        Data = soup.find_all('dd', attrs={'class': 'org-page-details__definition-text t-14 t-black--light t-normal'})
        Data2 = soup.find_all('dt', attrs={'class': 'org-page-details__definition-term t-14 t-black t-bold'})
        for item in Data2:
            if getstr(item.text).startswith("Company size"):
                Data2.remove(item)
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Website"):
                web = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Industry"):
                industry = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Headquarters"):
                headquarters = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Type"):
                type = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Founded"):
                founded = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        for i in range(len(Data2)):
            if Data2[i] == None:
                continue
            if getstr(Data2[i].text).startswith("Specialties"):
                specialities = getstr(Data[i].text.encode('utf8').decode('ascii', 'ignore'))
        image = soup.find('img', attrs={'class': 'lazy-image ember-view org-top-card-primary-content__logo'})
        if image != None:
            image = image.get('src')

        data = {"Studio Name": str(name), "Industry": str(industry), "Company Size": str(size), "Headquarters": str(headquarters),
        "Type": str(type), "Founded": str(founded), "Specialities": str(specialities), "Overview": str(overview), "Website": str(web), "Profile Pic": str(image)}

        with open(r"C:\Users\M Usman\Desktop\RESULT.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Studio Name", "Industry", "Company Size", "Headquarters", "Type", "Founded", "Specialities", "Overview", "Website", "Profile Pic"])
            writer.writerow(data)
