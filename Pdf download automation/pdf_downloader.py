from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException

download_path = "I:\\DOWNLOAD"


def download_pdf(download_path, start, end, i):
    
    global status 
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.automatic_downloads": 1,
            "download.default_directory": download_path,
            "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("http://mscs.dac.gov.in/MSCS/FiledAR_Old.aspx")

    table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME , "mGrid")))
    table = driver.find_element(By.CLASS_NAME, "mGrid")

    rows = table.find_elements(By.XPATH, ".//tr")[1:]

    file_names = {} 

    try:

        for idx in range(start, end):
            row = rows[idx]
            name = row.find_element(By.XPATH, ".//td[2]").text
            year = row.find_element(By.XPATH, ".//td[4]").text
            updated = row.find_element(By.XPATH, ".//td[5]").text

            # For annual activity
            activity_link = row.find_element(By.XPATH, ".//td[6]")

            before = os.listdir(download_path)

            driver.execute_script(activity_link.find_element(By.TAG_NAME, "a").get_attribute("href"))

            time.sleep(5)

            while True:
                if not any(filename.endswith(".crdownload") for filename in os.listdir(download_path)):
                    break

            after = os.listdir(download_path)

            change = set(after) - set(before)
            if len(change) == 1:
                file_path = f"{download_path}/{change.pop()}"
                file_root, file_ext = os.path.splitext(file_path)
                
                n_file = f"{name} {year} {updated} AnnualActivity"
                n_file = n_file.replace(':', '-').replace('/', '_').replace('"', '_').replace("'", "_").replace('&', ',')
                
                file_names[file_path] = f"{download_path}/{n_file}{file_ext}"
            elif len(change) == 0:
                print("No file downloaded")
            else:
                print("More than one file downloaded")

            # For annual statement
            statement_link = row.find_element(By.XPATH, ".//td[7]")

            before2 = os.listdir(download_path)

            driver.execute_script(statement_link.find_element(By.TAG_NAME, "a").get_attribute("href"))

            time.sleep(5)

            while True:
                if not any(filename.endswith(".crdownload") for filename in os.listdir(download_path)):
                    break

            after2 = os.listdir(download_path)

            change2 = set(after2) - set(before2)
            if len(change2) == 1:
                file_path = f"{download_path}/{change2.pop()}"
                file_root, file_ext = os.path.splitext(file_path)
                
                n_file = f"{name} {year} {updated} ActivityStatement"
                n_file = n_file.replace(':', '-').replace('/', '_').replace('"', '_').replace("'", "_").replace('&', ',')
                file_names[file_path] = f"{download_path}/{n_file}{file_ext}"
            elif len(change2) == 0:
                print("No file downloaded")
                
                raise Exception
            else:
                print("More than one file downloaded")
                
            i = i + 1


    except StaleElementReferenceException:
        
        driver.quit()
        print('website crashed at row ' +str(i+1))
    
        status = "crashed"
    except NoSuchWindowException:
        
        print('Window closed')
        driver.quit()
            
        status = "closed"
    
    except Exception:
        
        driver.quit()
            
        status = "other"
    else:            
        status = "okay"
        
    for key, value in file_names.items():
        os.rename(key, value)
        
    return i


start = 4
end = 6
filename = "output.txt"
j = start-1

while j <end:
    
    j = download_pdf(download_path, j, end, j)
    
    if status == "crashed":
        with open(filename, 'a') as f:
            f.write("row number "+ str(j+1)+" website keeps crashing so skipped\n")
        j=j+1
        print('Restarting...')
        
        status = ""
        continue;
    elif status == "closed":
        status = ""
        break;
    elif status == "other":
        
        status = ""
        with open(filename, 'a') as f:
            f.write("Problem in row number "+ str(j+1)+"\n")
        j=j+1
        continue;
            