import random
import time
import re

import allure

from pages.base_page import BasePage
from locators.interactions_page_locators import (SortablePageLocators, SelectablePageLocators, ResizablePageLocators,
                                                 DroppablePageLocators, DraggablePageLocators)


class SortablePage(BasePage):
    locators = SortablePageLocators()

    @allure.step('Get sortable items')
    def get_sortable_items(self, elements):
        item_list = self.elements_are_visible(elements)
        return [item.text for item in item_list]

    @allure.step('Change list order')
    def change_list_order(self):
        self.element_is_visible(self.locators.TAB_LIST).click()
        order_before = self.get_sortable_items(self.locators.LIST_ITEM)
        item_list = random.sample(self.elements_are_visible(self.locators.LIST_ITEM), k=2)
        item_what = item_list[0]
        item_where = item_list[1]
        self.action_drag_and_drop_to_element(item_what, item_where)
        order_after = self.get_sortable_items(self.locators.LIST_ITEM)
        return order_before, order_after

    @allure.step('Change grid order')
    def change_grid_order(self):
        self.element_is_visible(self.locators.TAB_GRID).click()
        order_before = self.get_sortable_items(self.locators.GRID_ITEM)
        item_list = random.sample(self.elements_are_visible(self.locators.GRID_ITEM), k=2)
        item_what = item_list[0]
        item_where = item_list[1]
        self.action_drag_and_drop_to_element(item_what, item_where)
        order_after = self.get_sortable_items(self.locators.GRID_ITEM)
        return order_before, order_after


class SelectablePage(BasePage):
    locators = SelectablePageLocators()

    @allure.step('Click selectable items')
    def click_selectable_items(self, elements):
        item_list = self.elements_are_visible(elements)
        random.sample(item_list, k=1)[0].click()

    @allure.step('Select list items')
    def select_list_items(self):
        self.element_is_visible(self.locators.TAB_LIST).click()
        self.click_selectable_items(self.locators.LIST_ITEM)
        active_element = self.element_is_visible(self.locators.LIST_ITEM_ACTIVE)
        return active_element.text

    @allure.step('Select grid items')
    def select_grid_items(self):
        self.element_is_visible(self.locators.TAB_GRID).click()
        self.click_selectable_items(self.locators.GRID_ITEM)
        active_element = self.element_is_visible(self.locators.GRID_ITEM_ACTIVE)
        return active_element.text


class ResizablePage(BasePage):
    locators = ResizablePageLocators()

    @allure.step('Get px from width and height')
    def get_px_from_width_height(self, value_of_size):
        width = value_of_size.split(';')[0].split(':')[1].replace(' ', '')
        height = value_of_size.split(';')[1].split(':')[1].replace(' ', '')
        return width, height

    @allure.step('Get max and min size')
    def get_max_min_size(self, element):
        size = self.element_is_present(element)
        size_value = size.get_attribute('style')
        assert size_value
        return size_value

    @allure.step('Change size resizable box')
    def change_size_resizable_box(self):
        resizable_handle = self.element_is_present(self.locators.RESIZABLE_BOX_HANDLE)
        self.go_to_element(resizable_handle)
        self.action_drag_and_drop_by_offset(resizable_handle, 400, 200)
        max_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE_BOX))
        self.action_drag_and_drop_by_offset(resizable_handle, -400, -200)
        min_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE_BOX))
        return max_size, min_size

    @allure.step('Change size resizable')
    def change_size_resizable(self):
        resizable_handle = self.element_is_present(self.locators.RESIZABLE_HANDLE)
        self.go_to_element(resizable_handle)
        random_max_width = random.randint(1, 150)
        random_max_height = random.randint(1, 100)
        self.action_drag_and_drop_by_offset(resizable_handle, random_max_width, random_max_height)
        max_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE))

        random_min_width = random.randint(-200, -1)
        random_min_height = random.randint(-200, -1)
        self.action_drag_and_drop_by_offset(resizable_handle, random_min_width, random_min_height)
        min_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE))
        return max_size, min_size


class DroppablePage(BasePage):
    locators = DroppablePageLocators()

    @allure.step('Drop simple')
    def drop_simple(self):
        self.element_is_visible(self.locators.SIMPLE_TAB).click()
        drag_div = self.element_is_visible(self.locators.SIMPLE_DRAG_ME)
        drop_div = self.element_is_visible(self.locators.SIMPLE_DROP_HERE)
        self.action_drag_and_drop_to_element(drag_div, drop_div)
        return drop_div.text

    @allure.step('Drop accept')
    def drop_accept(self):
        self.element_is_visible(self.locators.ACCEPT_TAB).click()
        acceptable_div = self.element_is_visible(self.locators.ACCEPTABLE)
        not_acceptable_div = self.element_is_visible(self.locators.NOT_ACCEPTABLE)
        drop_div = self.element_is_visible(self.locators.ACCEPT_DROP_HERE)
        self.action_drag_and_drop_to_element(not_acceptable_div, drop_div)
        drop_text_not_acceptable = drop_div.text
        self.action_drag_and_drop_to_element(acceptable_div, drop_div)
        drop_text_acceptable = drop_div.text
        return drop_text_not_acceptable, drop_text_acceptable

    @allure.step('Drop prevent propogation')
    def drop_prevent_propogation(self):
        self.element_is_visible(self.locators.PREVENT_TAB).click()
        drag_div = self.element_is_visible(self.locators.PREVENT_DRAG_ME)
        not_greedy_inner_box = self.element_is_visible(self.locators.NOT_GREEDY_INNER_DROP_BOX)
        greedy_inner_box = self.element_is_visible(self.locators.GREEDY_INNER_BOX)
        self.action_drag_and_drop_to_element(drag_div, not_greedy_inner_box)
        text_not_greedy_box = self.element_is_visible(self.locators.NOT_GREEDY_DROP_BOX_TEXT).text
        text_not_greedy_inner_box = not_greedy_inner_box.text
        self.go_to_element(self.element_is_present(self.locators.GREEDY_INNER_BOX))
        self.action_drag_and_drop_to_element(drag_div, greedy_inner_box)
        text_greedy_box = self.element_is_visible(self.locators.NOT_GREEDY_DROP_BOX_TEXT).text
        text_greedy_inner_box = not_greedy_inner_box.text
        return text_not_greedy_box, text_not_greedy_inner_box, text_greedy_box, text_greedy_inner_box

    @allure.step('Drop revert draggable')
    def drop_revert_draggable(self, type_drag):
        drags = {'will':
                     {'revert': self.locators.WILL_REVERT},
                 'not_will':
                     {'revert': self.locators.NOT_REVERT}
                 }
        self.element_is_visible(self.locators.REVERT_TAB).click()
        revert = self.element_is_visible(drags[type_drag]['revert'])
        drop_div = self.element_is_visible(self.locators.REVERT_DROP_HERE)
        self.action_drag_and_drop_to_element(revert, drop_div)
        position_after_move = revert.get_attribute('style')
        time.sleep(1)
        position_after_revert = revert.get_attribute('style')
        return position_after_move, position_after_revert


class DraggablePage(BasePage):
    locators = DraggablePageLocators()

    @allure.step('Get before and after positions')
    def get_before_and_after_positions(self, drag_element):
        self.action_drag_and_drop_by_offset(drag_element, random.randint(1, 50), random.randint(1, 50))
        before_position = drag_element.get_attribute('style')
        self.action_drag_and_drop_by_offset(drag_element, random.randint(1, 50), random.randint(1, 50))
        after_position = drag_element.get_attribute('style')
        return before_position, after_position

    @allure.step('Simple drag box')
    def simple_drag_box(self):
        self.element_is_visible(self.locators.TAB_SIMPLE).click()
        drag_div = self.element_is_visible(self.locators.SIMPLE_DRAG_BOX)
        before_position, after_position = self.get_before_and_after_positions(drag_div)
        return before_position, after_position

    @allure.step('Get top positions')
    def get_top_positions(self, positions):
        return re.findall(r'\d[0-9]|\d', positions.split(';')[2])

    @allure.step('Get left positions')
    def get_left_positions(self, positions):
        return re.findall(r'\d[0-9]|\d', positions.split(';')[1])

    @allure.step('Axis restricted X')
    def axis_restricted_x(self):
        self.element_is_visible(self.locators.AXIS_TAB).click()
        only_x = self.element_is_visible(self.locators.ONLY_X)
        position_x = self.get_before_and_after_positions(only_x)
        top_x_before = self.get_top_positions(position_x[0])
        top_x_after = self.get_top_positions(position_x[1])
        left_x_before = self.get_left_positions(position_x[0])
        left_x_after = self.get_left_positions(position_x[1])
        return [top_x_before, top_x_after], [left_x_before, left_x_after]

    @allure.step('Axis restricted Y')
    def axis_restricted_y(self):
        self.element_is_visible(self.locators.AXIS_TAB).click()
        only_y = self.element_is_visible(self.locators.ONLY_Y)
        position_y = self.get_before_and_after_positions(only_y)
        top_y_before = self.get_top_positions(position_y[0])
        top_y_after = self.get_top_positions(position_y[1])
        left_y_before = self.get_left_positions(position_y[0])
        left_y_after = self.get_left_positions(position_y[1])
        return [top_y_before, top_y_after], [left_y_before, left_y_after]





