import base64
import os
import random
import tempfile
import time

import allure
import requests
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from generator.generator import generated_person, generated_file
from locators.elements_page_locators import (TextBoxPageLocators, CheckBoxPageLocators, RadioButtonPageLocators,
                                             WebTablePageLocators, ButtonPageLocators, LinksPageLocators,
                                             UploadAndDownloadPageLocators, DynamicPropertiesPageLocators)
from pages.base_page import BasePage


class TextBoxPage(BasePage):
    locators = TextBoxPageLocators()

    @allure.step('Fill in all fields')
    def fill_all_fields(self):
        person_info = next(generated_person())
        full_name = person_info.full_name
        email = person_info.email
        current_address = person_info.current_address
        permanent_address = person_info.permanent_address
        with allure.step('filling fields'):
            self.element_is_visible(self.locators.FULL_NAME).send_keys(full_name)
            self.element_is_visible(self.locators.EMAIL).send_keys(email)
            self.element_is_visible(self.locators.CURRENT_ADDRESS).send_keys(current_address)
            self.element_is_visible(self.locators.PERMANENT_ADDRESS).send_keys(permanent_address)
        with allure.step('click submit button'):
            self.go_to_element(self.element_is_present(self.locators.SUBMIT))
            self.element_is_visible(self.locators.SUBMIT).click()
        return full_name, email, current_address, permanent_address

    @allure.step('Check filled form')
    def check_filled_form(self):
        full_name = self.element_is_present(self.locators.CREATED_FULL_NAME).text.split(":")[1]
        email = self.element_is_present(self.locators.CREATED_EMAIL).text.split(":")[1]
        current_address = self.element_is_present(self.locators.CREATED_CURRENT_ADDRESS).text.split(":")[1]
        permanent_address = self.element_is_present(self.locators.CREATED_PERMANENT_ADDRESS).text.split(":")[1]
        return full_name, email, current_address, permanent_address


class CheckBoxPage(BasePage):
    locators = CheckBoxPageLocators()

    @allure.step('open full list')
    def open_full_list(self):
        with allure.step('click expand all button'):
            self.element_is_visible(self.locators.EXPAND_ALL_BUTTON).click()

    @allure.step('click random checkbox')
    def click_random_checkbox(self):
        item_list = self.elements_are_visible(self.locators.ITEM_LIST)
        count = 21
        while count != 0:
            item = item_list[random.randint(1, 15)]
            if count > 0:
                self.go_to_element(item)
                item.click()
                count -= 1
            else:
                break

    @allure.step('get checked checkboxes')
    def get_checked_checkboxes(self):
        checked_list = self.elements_are_present(self.locators.CHECKED_ITEMS)
        data = []
        for box in checked_list:
            title_item = box.find_element("xpath", self.locators.TITLE_ITEM)
            data.append(title_item.text)
        return str(data).replace(' ', '').replace('doc', '').replace('.', '').lower()

    @allure.step('Get output result')
    def get_output_result(self):
        result_list = self.elements_are_present(self.locators.OUTPUT_RESULT)
        data = []
        for item in result_list:
            data.append(item.text)
        return str(data).replace(' ', '').lower()


class RadioButtonPage(BasePage):
    locators = RadioButtonPageLocators()

    @allure.step('Click on the radio button')
    def click_on_the_radio(self, choise):
        choises = {'yes': self.locators.YES_RADIO_BUTTON,
                   'impressive': self.locators.IMPRESSIVE_RADIO_BUTTON,
                   'no': self.locators.NO_RADIO_BUTTON}
        self.element_is_visible(choises[choise]).click()

    @allure.step('get result')
    def output_result(self):
        return self.element_is_present(self.locators.OUTPUT_RESULT).text


class WebTablePage(BasePage):
    locators = WebTablePageLocators()

    @allure.step('adding new person in webtable')
    def add_new_person(self, count=1):
        while count != 0:
            person_info = next(generated_person())
            firstname = person_info.firstname
            lastname = person_info.lastname
            email = person_info.email
            age = person_info.age
            salary = person_info.salary
            department = person_info.department
            with allure.step('click add button'):
                self.element_is_visible(self.locators.ADD_BUTTON).click()
            with allure.step('filled fields'):
                self.element_is_visible(self.locators.FIRSTNAME_INPUT).send_keys(firstname)
                self.element_is_visible(self.locators.LASTNAME_INPUT).send_keys(lastname)
                self.element_is_visible(self.locators.EMAIL_INPUT).send_keys(email)
                self.element_is_visible(self.locators.AGE_INPUT).send_keys(age)
                self.element_is_visible(self.locators.SALARY_INPUT).send_keys(salary)
                self.element_is_visible(self.locators.DEPARTMENT_INPUT).send_keys(department)
            with allure.step('click submit button'):
                self.element_is_visible(self.locators.SUBMIT_BUTTON).click()
            count -= 1
            return [firstname, lastname, str(age), email, str(salary), department]

    @allure.step('checked new person')
    def check_new_added_person(self):
        people_list = self.elements_are_present(self.locators.FULL_PEOPLE_LIST)
        data = []
        for item in people_list:
            data.append(item.text.splitlines())
        return data

    @allure.step('search person in webtable')
    def search_some_person(self, key_word):
        self.element_is_visible(self.locators.SEARCH_INPUT).send_keys(key_word)

    @allure.step('check searched person')
    def check_search_person(self):
        delete_button = self.element_is_present(self.locators.DELETE_BUTTON)
        row = delete_button.find_element("xpath", self.locators.ROW_PARENT)
        return row.text.splitlines()

    @allure.step('update person in webtable')
    def update_person_info(self):
        person_info = next(generated_person())
        age = person_info.age
        with allure.step('click update button'):
            self.element_is_visible(self.locators.UPDATE_BUTTON).click()
        with allure.step('clear age input'):
            self.element_is_visible(self.locators.UPDATE_AGE_INPUT).clear()
        with allure.step('filled age field'):
            self.element_is_visible(self.locators.UPDATE_AGE_INPUT).send_keys(age)
        with allure.step('click submit button'):
            self.element_is_visible(self.locators.UPDATE_SUBMIT_BUTTON).click()
        return str(age)

    @allure.step('delete person in webtable')
    def delete_person(self):
        self.element_is_visible(self.locators.DELETE_BUTTON).click()

    @allure.step('check deleted person in webtable')
    def check_deleted(self):
        return self.element_is_present(self.locators.NO_ROWS_FOUND).text

    @allure.step('select up some rows in webtable')
    def select_up_to_some_rows(self):
        count = [5, 10, 20, 25, 50, 100]
        data = []
        for x in count:
            count_row_button = self.element_is_visible(self.locators.COUNT_ROW_LIST)
            self.go_to_element(count_row_button)
            with allure.step('click random row button'):
                count_row_button.click()
            self.element_is_visible((By.CSS_SELECTOR, f'option[value="{x}"]')).click()
            data.append(self.check_count_rows())
        return data

    @allure.step('check count rows in webtable')
    def check_count_rows(self):
        list_rows = self.elements_are_present(self.locators.FULL_PEOPLE_LIST)
        return len(list_rows)


class ButtonPage(BasePage):
    locators = ButtonPageLocators()

    @allure.step('click on different button')
    def click_on_different_button(self, type_click):
        if type_click == "double":
            self.action_double_click(self.element_is_visible(self.locators.DOUBLE_CLICK_BUTTON))
            return self.check_clicked_on_the_button(self.locators.RESULT_DOUBLE_CLICK)
        if type_click == "right":
            self.action_right_click(self.element_is_visible(self.locators.RIGHT_CLICK_BUTTON))
            return self.check_clicked_on_the_button(self.locators.RESULT_RIGHT_CLICK)
        if type_click == "click":
            self.element_is_visible(self.locators.CLICK_ME_BUTTON).click()
            return self.check_clicked_on_the_button(self.locators.RESULT_CLICK_ME)

    @allure.step('check clicked button')
    def check_clicked_on_the_button(self, element):
        return self.element_is_present(element).text


class LinksPage(BasePage):
    locators = LinksPageLocators()

    @allure.step('check new tab simple link')
    def check_new_tab_simple_link(self):
        simple_link = self.element_is_visible(self.locators.SIMPLE_LINK)
        link_href = simple_link.get_attribute('href')
        request = requests.get(link_href)
        if request.status_code == 200:
            simple_link.click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            url = self.driver.current_url
            return link_href, url
        else:
            return link_href, request.status_code

    @allure.step('check broken link')
    def check_broken_link(self, url):
        request = requests.get(url)
        if request.status_code == 200:
            self.element_is_present(self.locators.BAD_REQUEST).click()
        else:
            return request.status_code

    @allure.step('check unauthorized link')
    def check_unauthorized_link(self, url):
        request = requests.get(url)
        if request.status_code == 200:
            self.element_is_present(self.locators.UNAUTHORIZED_REQUEST).click()
        else:
            return request.status_code

    @allure.step('check forbidden link')
    def check_forbidden_link(self, url):
        request = requests.get(url)
        if request.status_code == 200:
            self.element_is_present(self.locators.FORBIDDEN_REQUEST).click()
        else:
            return request.status_code

    @allure.step('check invalid link')
    def check_invalid_url_link(self, url):
        request = requests.get(url)
        if request.status_code == 200:
            self.element_is_present(self.locators.INVALID_URL_REQUEST).click()
        else:
            return request.status_code


class UploadAndDownloadPage(BasePage):
    locators = UploadAndDownloadPageLocators()

    @allure.step('upload file')
    def upload_file(self):
        file_name, path = generated_file()
        path_str = str(path)
        self.element_is_present(self.locators.UPLOAD_INPUT).send_keys(path_str)
        os.remove(path_str)
        text = self.element_is_visible(self.locators.UPLOADED_FILE_PATH).text
        return file_name.split('\\')[-1], text.split('\\')[-1]

    @allure.step('download file')
    def download_file(self):
        link = self.element_is_present(self.locators.DOWNLOAD_BUTTON).get_attribute('href')
        link_b = base64.b64decode(link)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(link_b)
            temp_file_path = temp_file.name
            check_file = os.path.exists(temp_file_path)
            os.remove(temp_file_path)
        return check_file


class DynamicPropertiesPage(BasePage):
    locators = DynamicPropertiesPageLocators()

    @allure.step('check enable button')
    def check_enable_button(self):

        try:
            self.element_is_clickable(self.locators.ENABLE_BUTTON, 5)
        except TimeoutException:
            return False
        return True

    @allure.step('check changed of color button')
    def check_changed_of_color(self):
        color_button = self.element_is_present(self.locators.COLOR_CHANGE_BUTTON)
        color_button_before = color_button.value_of_css_property('color')
        time.sleep(30)
        color_button_after = color_button.value_of_css_property('color')
        return color_button_before, color_button_after

    @allure.step('check appear button')
    def check_appear_of_button(self):
        try:
            self.element_is_visible(self.locators.VISIBLE_AFTER_5_SEC_BUTTON, 6)
        except TimeoutException:
            return False
        return True
