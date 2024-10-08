from selenium.webdriver.common.by import By


class BrowserWindowsPageLocators:
    NEW_TAB_BUTTON = (By.CSS_SELECTOR, 'button[id="tabButton"]')
    TITLE_NEW_TAB = (By.CSS_SELECTOR, 'h1[id="sampleHeading"]')
    NEW_WINDOW_BUTTON = (By.CSS_SELECTOR, 'button[id="windowButton"]')


class AlertsPageLocators:
    SEE_ALERT_BUTTON = (By.CSS_SELECTOR, 'button[id="alertButton"]')

    APPEAR_AFTER_5_SEC_BUTTON = (By.CSS_SELECTOR, 'button[id="timerAlertButton"]')

    CONFIRM_BOX_ALERT_BUTTON = (By.CSS_SELECTOR, 'button[id="confirmButton"]')
    RESULT_CONFIRM_BOX = (By.CSS_SELECTOR, 'span[id="confirmResult"]')

    PROMPT_BOX_ALERT_BUTTON = (By.CSS_SELECTOR, 'button[id="promtButton"]')
    RESULT_PROMPT_BOX = (By.CSS_SELECTOR, 'span[id="promptResult"]')


class FramesPageLocators:
    FIRST_FRAME = (By.CSS_SELECTOR, 'iframe[id="frame1"]')
    SECOND_FRAME = (By.CSS_SELECTOR, 'iframe[id="frame2"]')
    TITLE_FRAME = (By.CSS_SELECTOR, 'h1[id="sampleHeading"]')


class NestedFramesPageLocators:
    PARENT_FRAME = (By.CSS_SELECTOR, 'iframe[id="frame1"]')
    TEXT_PARENT_FRAME = (By.CSS_SELECTOR, 'body')
    CHILD_FRAME = (By.CSS_SELECTOR, 'iframe[srcdoc="<p>Child Iframe</p>"]')
    TEXT_CHILD_FRAME = (By.CSS_SELECTOR, 'p')


class ModalDialogsPageLocators:
    SMALL_MODAL_BUTTON = (By.CSS_SELECTOR, 'button[id="showSmallModal"]')
    TITLE_SMALL_MODAL = (By.CSS_SELECTOR, 'div[id="example-modal-sizes-title-sm"]')
    TEXT_SMALL_DIALOG = (By.CSS_SELECTOR, 'div[class="modal-body"]')
    CLOSE_SMALL_MODAL_BUTTON = (By.CSS_SELECTOR, 'button[id="closeSmallModal"]')

    LARGE_MODAL_BUTTON = (By.CSS_SELECTOR, 'button[id="showLargeModal"]')
    TITLE_LARGE_MODAL = (By.CSS_SELECTOR, 'div[id="example-modal-sizes-title-lg"]')
    TEXT_LARGE_DIALOG = (By.CSS_SELECTOR, 'div[class="modal-body"] p')
    CLOSE_LARGE_MODAL_BUTTON = (By.CSS_SELECTOR, 'button[id="closeLargeModal"]')