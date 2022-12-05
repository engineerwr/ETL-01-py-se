from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
servico = Service(ChromeDriverManager().install())


class Type(Enum):
    INDIVIDUAL_FAMILY = 1
    SMALL_BUSS = 2
    MEDICAID_CHIP = 3


class ExtractData:
    def __init__(self):
        self.driver = webdriver.Chrome(service=servico, options=chrome_options)
        self.data = []

    def get_zipcode_items(self, zipcode):
        self.driver.implicitly_wait(5)
        self.driver.get("https://localhelp.healthcare.gov/")
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/form/div[1]/div/input").send_keys(zipcode)
        selector_elements = self.driver.find_elements(By.CLASS_NAME, "ds-c-autocomplete__list-item")
        print()
        for i, element in enumerate(selector_elements):
            if i < len(selector_elements) - 1:
                self.get_zipcode_item(i, zipcode)
        return self.data

    def get_zipcode_item(self, index, zipcode):
        self.driver.execute_script("window.open('arguments[0]');", "")
        self.driver.switch_to.window(self.driver.window_handles[index + 1])
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/form/div[1]/div/input").send_keys(zipcode)
        selector_element = self.driver.find_elements(By.CLASS_NAME, "ds-c-autocomplete__list-item")
        selector_element[index].click()

        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/form/div[2]/button").click()
        self.get_zipcode_item_data(Type.INDIVIDUAL_FAMILY)

        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/button").click()
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Medicaid or CHIP')]").click()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]").click()
        self.get_zipcode_item_data(Type.MEDICAID_CHIP)

        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/button").click()
        self.driver.find_element(By.XPATH, "//span[contains(text(),'Small business')]").click()
        self.driver.find_element(By.ID, "inner-flh-c-filter-pill-coverage_type").click()
        self.get_zipcode_item_data(Type.SMALL_BUSS)

    def get_zipcode_item_data(self, agent_type):
        page_value = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/p")
        count_page = int(page_value.text.split(" ")[-1])

        for i in range(count_page):
            elements_list = self.driver.find_elements(By.XPATH, "//a[contains(text(),'More details')]")
            for j in range(len(elements_list)):
                more_details = self.driver.find_elements(By.XPATH, "//a[contains(text(),'More details')]")
                more_details[j].click()
                data = self.get_zipcode_item_data_detail(agent_type)

                if data["name"] not in [item["name"] for item in self.data]:
                    self.data.append(data)
                else:
                    for item in self.data:
                        if item["name"] == data["name"] and agent_type.name not in item["type"]:
                            item["type"].append(agent_type.name)

                self.driver.back()

            if i < count_page - 1:
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/div/div[3]/a").click()

    def get_zipcode_item_data_detail(self, agent_type):
        data = {}

        def get_phone():
            list_phone = []
            elem_phone = self.driver.find_elements(By.CLASS_NAME, "qa-flh-resource-phone")
            for i in range(len(elem_phone)):
                list_phone.append(elem_phone[i].text)
            return list_phone

        def get_available_times():
            list_times = []
            elem_times = self.driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]").text.replace(
                "\n", " ").replace("\u2009", " ").replace("pm ", "pmDIV")
            elem_times = elem_times.split("DIV")
            for i in range(len(elem_times)):
                list_times.append(elem_times[i])
            return list_times

        data["name"] = self.driver.find_element(By.CLASS_NAME, "qa-flh-resource-name").text
        data["type"] = [agent_type.name]
        body_address = self.driver.find_element(By.XPATH, "//div[contains(text(),'Address')]/..")
        data["address"] = body_address.text.replace("\n", ", ").replace("Address", "")
        data["role"] = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/span").text
        data["years"] = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div").text.replace("\n", " ")
        data["phone"] = get_phone()
        data["email"] = self.driver.find_element(By.XPATH, "//a[contains(@href,'@')]").text
        data["website"] = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/a").text
        data["languages"] = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div/div/div[2]").text
        data["times"] = get_available_times()
        return data
