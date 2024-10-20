from publix_db import getCollection
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Function to load all items by clicking the "Load More" button until it disappears
def load_all_items(driver):
    while True:
        try:
            # Wait for the Load More button to be clickable
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Load more']"))
            )
            
            # If the button is visible, click it
            if load_more_button.is_displayed():
                print("Load More button found. Clicking...")
                load_more_button.click()
                time.sleep(2)  # Wait for new items to load
            else:
                print("Load More button is not visible.")
                break  # Exit the loop if the button is not visible anymore
        except Exception as e:
            print("No more items to load or error occurred:", e)
            break  # Exit the loop if there is no "Load More" button or another issue occurs


def get_bogo_items():
    bogo_collection = getCollection()
    bogo_collection.delete_many({})
    print("Deleted contents of bogo collection...")

    driver = webdriver.Chrome()
    driver.get("https://www.publix.com/savings/weekly-ad/bogo")
    # Wait until the page loads
    wait = WebDriverWait(driver, 10)

    try:
        print("Loading all bogo items...")
        load_all_items(driver)  # First, load all available items by clicking "Load More"
    
        # Wait for the BOGO items container to be present
        bogo_container = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "p-grid.grid--spacing-default.grid--bordered.grid--col-1.grid--xxxxs-col-1.grid--xxxs-col-1.grid--xxs-col-2.grid--xs-col-2.grid--sm-col-4.grid--md-col-3.grid--lg-col-4.grid--xl-col-4.grid--xxl-col-4.grid--xxxl-col-4")
        ))

        # Find all individual BOGO items within the container
        bogo_items = bogo_container.find_elements(By.CLASS_NAME, "p-grid-item")

        print("Adding bogo items into bogo collection...")

        # Loop through each item to extract the text
        for item in bogo_items:
            item_name_span = item.find_element(By.CLASS_NAME, "p-text.paragraph-md.normal.context--default.color--null.line-clamp.title")
            item_name = item_name_span.text.strip()
            bogo_collection.insert_one({ "item_name": item_name })  # Add item name to the bogo collection

        print("Finished!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the driver
        driver.quit()

if __name__ == "__main__":
    get_bogo_items()