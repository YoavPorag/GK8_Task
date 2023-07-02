import json
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_base = "https://www.blockchain.com/btc/tx/"
first_tx = "79ec6ef52c0a2468787a5f671f666cf122f68aaed11a28b15b5da55c851aee75"

driver = webdriver.Chrome() 
wait = WebDriverWait(driver, 10)

def get_tx(tx_id):
    retries = 3
    while retries > 0:
        try:
            driver.get(url_base + tx_id)
            driver.implicitly_wait(10)
            break
        except TimeoutException as e:
            retries -= 1
            print(f"TimeoutException occurred. {retries} attempts left")
            if retries <= 0:
                raise TimeoutException (f"page load failed\n{str(e)}") from e
        except Exception as e:
            raise Exception(f"An error occurred while fetching transaction data:\n{str(e)}") from e

def get_tx_data():
    retries = 3
    while retries > 0:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="sc-fcce043f-5 cprSab"]')))
            time.sleep(5)
            btn.click()

            text = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,'pre[class="sc-6abc7442-1 eIwaHT"]'))
            ).get_attribute("innerHTML")

            return json.loads(text)
        
        except StaleElementReferenceException as e:
            retries -= 1
            print(f"StaleElementReferenceException occurred. {retries} attempts left")
            if retries <= 0:
                raise StaleElementReferenceException(f"Page load failed\n{str(e)}") from e
        except TimeoutException as e:
            retries -= 1
            print(f"TimeoutException occurred. {retries} attempts left")
            if retries <= 0:
                raise TimeoutException(f"Page load failed\n{str(e)}") from e
        except Exception as e:
            raise Exception(f"An error occurred while fetching transaction data\n{str(e)}") from e

    print("cant load data of transaction . skipping...")
    return None

def is_coinbase(json_data):
    return json_data["inputs"][0]["coinbase"]

def get_input_ids(json_data):
    ids = []
    for input in json_data["inputs"]:
        ids.append(input["txid"])
    return ids


def main():
    # queue =[(tx_id,[path_to_tx]),...]
    queue = [(first_tx,[first_tx])]

    while queue:
        print(queue)
        current_tx_id, path = queue.pop(0)
        try:
            get_tx(current_tx_id)
            data = get_tx_data()
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Error occurred while fetching transaction data for transaction {current_tx_id}.\n{str(e)}\Skipping transaction {current_tx_id}...")
            continue
        except Exception as e:
            print(f"an unforseen error as occured: \n{str(e)}\nSkipping transaction {current_tx_id}")
            continue

        if is_coinbase(data):
            print (f"coinbase found!\nThe shortest path length is {len(path)}\nThe shortest path is : {path}")
            driver.quit()
            exit(0)     
        
        inputs = get_input_ids(data)
        for input in inputs:
            queue.append((input,path + [input]))

    print("queue is empty!search failed!")
    driver.quit()
    exit(1)

if (__name__ == "__main__"):
    main()