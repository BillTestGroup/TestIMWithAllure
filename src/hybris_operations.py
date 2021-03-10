from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from random import randrange
import allure

@allure.step("блокировка всплывающего окна")
def cut_pop_up(br):
    br.execute_script("""
    var element = document.querySelector(".osr-overlay");
    if (element)
        element.parentNode.removeChild(element);
    """)
    br.execute_script("""
        var element = document.querySelector(".sticky-panels-bottom");
        if (element)
            element.parentNode.removeChild(element);
        """)
    br.execute_script("""
           var element = document.querySelector(".v-cookies.cookies");
           if (element)
               element.parentNode.removeChild(element);
           """)


@allure.description("Проверка возможности загрузки браузера")
@allure.step("Открытие стариницы интернет-магазина А1")
def open_browser(site_to_open):
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=ru')
    br = webdriver.Chrome(executable_path=r'C:\tools\chromedriver\chromedriver.exe', options=options)
    br.maximize_window()
    br.get(site_to_open)
    return br

@allure.description("Проверка возможности входа в магазин")
@allure.step("Ввод личных данных для входа в магазин")
def login_site(br, login, passw):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "dropdownMenuUser"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Войти')]]"))).click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pwd_choose"]/../span[@class="radiobtn"]')))
    WebDriverWait(br, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pwd_choose"]/../span[@class="radiobtn"]'))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='tel' and @name='UserID']")))
    br.find_element_by_xpath("//input[@type='tel' and @name='UserID']").send_keys(login)  # set login
    br.find_element_by_xpath("//input[@type='password' and @id='ipassword']").send_keys(passw)
    br.find_element_by_xpath('//*[@id="butt1"]').click()
    WebDriverWait(br, 30).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id=\"mr\"]/div/div/section/h1")))

@allure.description("Проверка корректности выхода из кабинета")
@allure.step("Выход из личного кабинета")
def logout_site(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "dropdownMenuUser"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Выход')]]"))).click()
    time.sleep(3)
    cut_pop_up(br)

@allure.description("Проверка корзины на предмет наличия в ней некупленного оборудования")
@allure.step("Очистка корзины от оставленного в ней оборудования")
def check_cart(br):
    WebDriverWait(br, 60).until(EC.element_to_be_clickable((By.ID, "miniCart"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[1]/div/div/div/div/h1")))
    time.sleep(5)
    try:
        cut_pop_up(br)
        if br.find_element_by_xpath(
                "//*[text()[contains(.,'Корзина пуста. Перейдите в интернет-магазин, чтобы начать покупки.')]]"):
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Перейти в интернет-магазин')]]/..")))
            br.find_element_by_xpath("//span[text()[contains(.,'Перейти в интернет-магазин')]]/..").click()
        else:
            pass
    except:
        cart_delete_list = br.find_elements_by_xpath(
            "//div[contains(@class, 'review-item-fixed-block review-item-fixed-block--with-expandable-body')]")
        for i in cart_delete_list:
            cut_pop_up(br)
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'icon icon--remove')]/.."))).click()
            WebDriverWait(br, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Удалить?')]]")))
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'form-cta')]/button[1]"))).click()
            WebDriverWait(br, 30).until(
                EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'form-cta')]/button[1]")))
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Перейти в интернет-магазин')]]"))).click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
        time.sleep(4)
        cut_pop_up(br)

@allure.description("Оформление покупки смартфона в рассрочку на 6 месяцев")
@allure.step("Выбор оборудования, выбор типа продажи в рассрочку на 6 месяцев, переход в корзину и оформление покупки")
def buyTANaSimSix(br, test_dude):
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    brand_list = br.find_elements_by_xpath("//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
    brand_num = randrange(len(brand_list))
    brand_list[brand_num].click()
    time.sleep(3)
    cut_pop_up(br)
    product_list_block = br.find_element_by_xpath("//div[contains(@class, 'product-listing-content')]")
    product_list = product_list_block.find_elements_by_xpath(
        "//span[text()[contains(.,'Перейти к покупке')]]/../../../a")
    cut_pop_up(br)
    prod_num = randrange(len(product_list))
    WebDriverWait(br, 30).until(EC.visibility_of(product_list[prod_num]))
    time.sleep(3)
    cut_pop_up(br)
    product_list[prod_num].click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    cut_pop_up(br)
    # карточка оборудования
    combobox = br.find_element_by_xpath(
        "//*[@id='CURRENT_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    time.sleep(1)
    br.find_element_by_xpath("//li/div[text()[contains(., '6 мес по ')]]/..").click()
    # нажимаем купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(@class, 'h h--2 text-block-title')]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]"))).click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]/..")))
    # Корзина
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']")))
    cut_pop_up(br)
    br.find_element_by_xpath("//button[@class='button button--tertiary with-icon collapsed']").click()
    time.sleep(2)
    monthly_payment = float(
        str(br.find_element_by_xpath(
            "//p[text()[contains(.,'Регулярный платеж')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    full_price = float(
        str(br.find_element_by_xpath(
            "//p[text()[contains(.,'Итоговая стоимость')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    device_price = float(
        str(br.find_element_by_xpath(
            "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    # НАЖИМАЕМ КУПИТЬ
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Купить')]]/.."))).click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Личные данные')]]/..")))
    time.sleep(1)
    br.find_element_by_id("submitButton").click()
    cut_pop_up(br)
    # окно Способ доставки
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Способ доставки')]]/..")))
    delivery_method = ""
    time.sleep(3)
    try:
        delivery_method = br.find_element_by_xpath("//*[text()[contains(.,'Способ доставки')]]")
    except:
        pass
    if (delivery_method):
        cut_pop_up(br)
        br.find_element_by_xpath("//*[text()[contains(.,'Доставка курьером')]]").click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Данные о доставке')]]")))
        assert br.find_element_by_xpath("//*[text()[contains(.,'Адрес')]]/following::*").text == test_dude.adres
        WebDriverWait(br, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()
    else:
        pass

    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()

    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)
    return external_id, device_price, monthly_payment, full_price

@allure.description("Ожидание перехода статуса заявки из 'Оформлен' в 'В работе'")
@allure.step("Проверка статуса заявки, ожидание перехода статуса заявки из 'Оформлен' в 'В работе'")
def wait_for_order_in_work(br):
    order_status = br.find_element_by_xpath("//dt[text()[contains(.,'Статус')]]/following::dd").text
    loop_counter = 0
    while order_status == "Оформлен" and loop_counter <= 30:
        time.sleep(5)
        loop_counter = loop_counter + 1
        br.refresh()
        cut_pop_up(br)
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//dt[text()[contains(.,'Статус')]]/following::dd")))
        order_status = br.find_element_by_xpath("//dt[text()[contains(.,'Статус')]]/following::dd").text
    assert order_status == "В работе", f"Статус заявки в WSO {order_status}"

@allure.description("Загзузка модуля WSO для проверки корректности передачи заявки и ее данных из ИМ в WSO")
@allure.step("Загрузка модуля WSO для проверки корректности передачи заявки и ее данных из ИМ в WSO")
def log_in_wso(br, wso_link, vix_creds):
    br.get(wso_link)
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='loginSection']")))
    br.find_element_by_xpath("//input[@name='username']").send_keys(vix_creds.prod_login)
    br.find_element_by_xpath("//input[@name='password']").send_keys(vix_creds.prod_password)
    br.find_element_by_xpath("//input[@type='submit']").click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выбор точки продажи')]]")))
    br.find_element_by_xpath("//input[@id='stchooseOfficeForm:officeAutocomplete_input']").send_keys("-2833")
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'-2833')]]"))).click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='stchooseOfficeForm:chooseOffice']"))).click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@id='stchooseOfficeForm:chooseOffice']")))

@allure.description("Поиск и открытие созданной заявки для сравнения данных и закрытия заявки")
@allure.step("Анализ данных заявки, сравнение данных и закрытие заявки")
def check_wso_installment(br, test_dude, installment_price):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(installment_price[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(3)
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()

    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='hybrisOrderDetailForm:rootOrderDetailPanel_header']")))
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == installment_price[1]

    monthly_pay_IM = installment_price[2]
    monthly_pay_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM == monthly_pay_WSO

    full_price_IM = installment_price[3]
    full_price_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(",", "."))
    assert full_price_IM == full_price_WSO

    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    br.find_element_by_xpath("//span[text()[contains(.,'Отклонена ИМ')]]/../..").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:confirmChangeStatusDialog")))
    br.find_element_by_id("hybrisOrderDetailForm:confirmChangeStatus").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:addCommentDialog")))
    br.find_element_by_xpath("//textarea[contains(@data-p-rmsg, 'Комментарий не должен быть пустым!')]").send_keys(
        "test test")
    br.find_element_by_xpath(
        "//textarea[contains(@data-p-rmsg, 'Комментарий не должен быть пустым!')]/../../following::div[1]/button/span[text()[contains(.,'Сохранить')]]/..").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:messages")))
    assert br.find_element_by_id("hybrisOrderDetailForm:messages").text == "Статус заявки успешно изменен"

    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    br.find_element_by_xpath("//span[text()[contains(.,'Завершена/Отказ ИМ')]]/../..").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:confirmChangeStatusDialog")))
    br.find_element_by_id("hybrisOrderDetailForm:confirmChangeStatus").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:addCommentDialog")))
    br.find_element_by_xpath("//textarea[contains(@data-p-rmsg, 'Комментарий не должен быть пустым!')]").send_keys(
        "test test")
    br.find_element_by_xpath(
        "//textarea[contains(@data-p-rmsg, 'Комментарий не должен быть пустым!')]/../../following::div[1]/button/span[text()[contains(.,'Сохранить')]]/..").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "hybrisOrderDetailForm:messages")))
    assert br.find_element_by_id("hybrisOrderDetailForm:messages").text == "Статус заявки успешно изменен"
    assert br.find_element_by_xpath(
        "//div[@id='hybrisOrderDetailForm:rootOrderDetailPanel_header']/span").text == "Текущий статус - Завершена/Отказ ИМ"

