from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
#from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from random import randrange
import allure



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



@allure.step("Открытие стариницы интернет-магазина А1")
def open_browser(site_to_open):
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=ru')
    #options.add_argument('--headless')
    options.add_argument("window-size=1920,1080")
    br = webdriver.Chrome(options=options)
    br.maximize_window()
    br.get(site_to_open)
    return br


@allure.step("Ввод личных данных для входа в магазин")
def login_step(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "dropdownMenuUser"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Войти')]]"))).click()

@allure.step("Выбор типа авторизации")
def pick_authorization_type(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pwd_choose"]/../span[@class="radiobtn"]')))
    WebDriverWait(br, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pwd_choose"]/../span[@class="radiobtn"]'))).click()

@allure.step("Ввести логин")
def set_login(br, login):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='tel' and @name='UserID']")))
    br.find_element_by_xpath("//input[@type='tel' and @name='UserID']").send_keys(login)  # set login

@allure.step("Ввести код\пароль")
def set_password(br, passw):
    br.find_element_by_xpath("//input[@type='password' and @id='ipassword']").send_keys(passw)

@allure.step("Нажать кнопку 'Войти в аккаунт'")
def press_login_button(br):
    br.find_element_by_xpath('//*[@id="butt1"]').click()
    WebDriverWait(br, 30).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id=\"mr\"]/div/div/section/h1")))

def login_site(br, login, passw):
    login_step(br)
    pick_authorization_type(br)
    set_login(br, login)
    set_password(br, passw)
    press_login_button(br)

@allure.step("Выход из личного кабинета")
def logout_site(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "dropdownMenuUser"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Выход')]]"))).click()
    time.sleep(3)
    cut_pop_up(br)

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


@allure.step("Выбор бренда оборудования для покупки")
def select_brand(br):
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    brand_list = br.find_elements_by_xpath("//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
    brand_num = randrange(len(brand_list))
    brand_list[brand_num].click()
    time.sleep(3)
    cut_pop_up(br)

@allure.step("Выбор бренда оборудования для покупки совместо с Каско")
def select_brand_with_kasko(br):
    cut_pop_up(br)
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//*[@id=\"facet-collapse-brand\"]/div/div/div/div[1]/div/div[2]/div/ul/li[2]/form/div/label").click()

@allure.step("Выбор модели оборудования для покупки")
def select_product(br):
    WebDriverWait(br, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
    product_list_block = br.find_element_by_xpath("//div[contains(@class, 'product-listing-content')]")
    product_list = product_list_block.find_elements_by_xpath("//span[text()[contains(.,'Перейти к покупке')]]/../../../a")
    cut_pop_up(br)
    prod_num = randrange(len(product_list))
    WebDriverWait(br, 30).until(EC.visibility_of(product_list[prod_num]))
    time.sleep(3)
    cut_pop_up(br)
    product_list[prod_num].click()


@allure.step("Выбор бренда оборудования для покупки совместо с Каско")
def select_model_for_new_sim(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='facet-collapse-category']/div/div/div/div[2]/button")))
    br.find_element_by_xpath("//*[@id='facet-collapse-category']/div/div/div/div[2]/button").click()
    WebDriverWait(br, 30).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='facet-collapse-category']/div/div/div/div[1]/div/div[2]/div/ul")))
    product_list = br.find_elements_by_xpath(
        "//*[@id='facet-collapse-category']/div/div/div/div[1]/div/div[2]/div/ul/li")
    prod_num = randrange(len(product_list))
    WebDriverWait(br, 30).until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[@id='facet-collapse-category']/div/div/div/div[1]/div/div[2]/div/ul/li[{prod_num + 1}]")))
    # product_list[prod_num].click()
    product_list[5].click()

@allure.step("Выбор тарифного плана для подключения")
def select_rate_plan_for_new_sim(br):
# - вырбрать рандомный тариф из выбранной категории
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button/span[text()[contains(.,'Подробнее')]]/..")))
    tarif_list = br.find_elements_by_xpath("//button/span[text()[contains(.,'Подробнее')]]/..")
    prod_num = randrange(len(tarif_list))
    cut_pop_up(br)
    tarif_list[prod_num].click()
    # - тыкнуть подключиться
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button/span[text()[contains(.,'Подключить')]]/.."))).click()
    cut_pop_up(br)


@allure.step("Выбор типа продажи Рассрочка 6 месяцев")
def select_type_of_sale_rassrochka_6(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    cut_pop_up(br)
    combobox = br.find_element_by_xpath(
        "//*[@id='CURRENT_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    time.sleep(1)
    ac = ActionChains(br)
    ac.move_to_element(br.find_element_by_xpath("//li/div[text()[contains(., '6 мес по ')]]/..")).perform()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//li/div[text()[contains(., '6 мес по ')]]/.."))).click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()

@allure.step("Выбор типа продажи Рассрочка 11 месяцев")
def select_type_of_sale_rassrochka_11(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    cut_pop_up(br)
    combobox = br.find_element_by_xpath(
        "//*[@id='CURRENT_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    time.sleep(1)
    br.find_element_by_xpath("//li/div[text()[contains(., '11 мес по ')]]/..").click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()


@allure.step("Выбор типа продажи Рассрочка 24 месяца")
def select_type_of_sale_rassrochka_24(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    cut_pop_up(br)
    combobox = br.find_element_by_xpath(
        "//*[@id='CURRENT_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    time.sleep(1)
    br.find_element_by_xpath(
        "//li/div[text()[contains(., '24 мес по ')]]/following-sibling::div[text()[contains(.,'С обслуживанием не менее 12')]]/..").click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()


@allure.step("Окно 'Просмотр и выбор тарифа'")
def view_and_select_rate_plan(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Просмотр и выбор тарифа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
    cut_pop_up(br)

@allure.step("Переход в корзину")
def go_to_cart(br):
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]"))).click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]/..")))

@allure.step("Корзина")
def take_price_values_for_equipment(br):
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']")))
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
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Купить')]]/.."))).click()
    cut_pop_up(br)
    return device_price, monthly_payment, full_price


@allure.step("Переход в корзину")
def take_data_from_cart(br):
    # Окно Корзина
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']")))
    cut_pop_up(br)
    br.find_element_by_xpath("//button[@class='button button--tertiary with-icon collapsed']").click()
    time.sleep(2)
    assert br.find_element_by_xpath(
        "//div[@id='bundle-collapse-block-0']/div[2]/div[@class='review-item-main']/div[@class='review-item-main-info']/p").text == "SIM-карта"
    assert br.find_element_by_xpath(
        "//div[@id='bundle-collapse-block-0']/div[2]/div[@class='review-item-main']/div[@class='review-item-main-info']/a/span[@class='link-label']").text == "Universal"
    rate_plan = br.find_element_by_xpath("//div[@id='bundle-collapse-block-0']/div[1]/div/div[2]/a/span").text

    product_price = float(
        str(br.find_element_by_xpath(
            "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    # НАЖИМАЕМ КУПИТЬ
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@class='form review-item-table-price']//*[@class='form-cta']//span[text()[contains(.,'Купить')]]/.."))).click()
    cut_pop_up(br)
    return rate_plan, product_price

@allure.step("Переход на окно 'Личные данные'")
def personal_data_view(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Личные данные')]]/..")))
    time.sleep(1)
    br.find_element_by_id("submitButton").click()
    cut_pop_up(br)

@allure.step("Переход на окно 'Способ доставки', выбор способа доставки")
def select_delivery_method(br, test_dude):
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

@allure.step("Переход на окно 'Способ оплаты', выбор способа оплаты")
def select_payment_method(br):
    payment_method = ""
    time.sleep(3)
    try:
        WebDriverWait(br, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Способ оплаты')]]")))
        payment_method = br.find_element_by_xpath("//h2[text()[contains(.,'Способ оплаты')]]")
    except:
        pass

    if (payment_method):
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()[contains(.,'Банковской картой при получении')]]"))).click()
        cut_pop_up(br)
        br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    else:
        pass

@allure.step("Проверка состава заказа")
def check_order_details(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()

@allure.step("Подтверждение заказа")
def order_confirmation(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)
    return external_id

###########################################################################
@allure.description("Оформление покупки смартфона в рассрочку на 6 месяцев")
@allure.step("Выбор оборудования, выбор типа продажи в рассрочку на 6 месяцев, переход в корзину и оформление покупки")
def buyTANaSimSix(br, test_dude):
    select_brand(br)
    select_product(br)
    select_type_of_sale_rassrochka_6(br)
    view_and_select_rate_plan(br)
    go_to_cart(br)
    device_price, monthly_payment, full_price = take_price_values_for_equipment(br)
    personal_data_view(br)
    select_delivery_method(br, test_dude)
    select_payment_method(br)
    check_order_details(br)
    external_id = order_confirmation(br)
    return external_id, device_price, monthly_payment, full_price
###########################################################################

@allure.description("Оформление покупки смартфона в рассрочку на 24 месяца")
@allure.step("Выбор оборудования, выбор типа продажи в рассрочку на 24 месяца, переход в корзину и оформление покупки")
def buyTANaSim24(br, test_dude):
    select_brand(br)
    select_product(br)
    select_type_of_sale_rassrochka_24(br)
    view_and_select_rate_plan(br)
    go_to_cart(br)
    device_price, monthly_payment, full_price = take_price_values_for_equipment(br)
    personal_data_view(br)
    select_delivery_method(br, test_dude)
    select_payment_method(br)
    check_order_details(br)
    external_id = order_confirmation(br)
    return external_id, device_price, monthly_payment, full_price


###########################################################################

@allure.description("Оформление покупки смартфона в рассрочку на 11 месяцев")
@allure.step("Выбор оборудования, выбор типа продажи в рассрочку на 11 месяцев, переход в корзину и оформление покупки")
def buyTANaSimEleven(br, test_dude):
    select_brand(br)
    select_product(br)
    select_type_of_sale_rassrochka_11(br)
    view_and_select_rate_plan(br)
    go_to_cart(br)
    device_price, monthly_payment, full_price = take_price_values_for_equipment(br)
    personal_data_view(br)
    select_delivery_method(br, test_dude)
    select_payment_method(br)
    check_order_details(br)
    external_id = order_confirmation(br)
    return external_id, device_price, monthly_payment, full_price

###########################################################################

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
###########################################################################

@allure.step("Загрузка модуля WSO")
def open_wso(br, wso_link):
    br.get(wso_link)
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='loginSection']")))

@allure.step("Ввод логина в модуль WSO")
def enter_login(br, vix_creds):
    br.find_element_by_xpath("//input[@name='username']").send_keys(vix_creds.prod_login)

@allure.step("Ввод пароля в модуль WSO")
def enter_password(br, vix_creds):
    br.find_element_by_xpath("//input[@name='password']").send_keys(vix_creds.prod_password)

@allure.step("Вход в модуль WSO")
def click_enter(br):
    br.find_element_by_xpath("//input[@type='submit']").click()

@allure.step("Выбор точки продаж")
def select_point_of_sale(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выбор точки продажи')]]")))
    br.find_element_by_xpath("//input[@id='stchooseOfficeForm:officeAutocomplete_input']").send_keys("-2833")
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'-2833')]]"))).click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='stchooseOfficeForm:chooseOffice']"))).click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@id='stchooseOfficeForm:chooseOffice']")))


@allure.step("Загрузка модуля WSO для проверки корректности передачи заявки и ее данных из ИМ в WSO")
def log_in_wso(br, wso_link, vix_creds):
    open_wso(br, wso_link)
    enter_login(br, vix_creds)
    enter_password(br, vix_creds)
    click_enter(br)
    select_point_of_sale(br)



@allure.step("Выбор меню-интернет-магазин-поиск заявок")
def select_menu_internet_shop(br):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))

@allure.step("Поиск заявки по номеру")
def find_order(br, external_id):
    order_external_id = str(external_id).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(3)
    return order_external_id

@allure.step("Получение таблицы с результатами поиска, сравнение полученных данных")
def view_search_results(br, test_dude, order_external_id):
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"

@allure.step("Нажать на ссылку с номером заявки для просмотра деталей")
def view_order_details(br):
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='hybrisOrderDetailForm:rootOrderDetailPanel_header']")))

@allure.step("Сравнение номера заявки")
def check_order_id(br, order_external_id):
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id

@allure.step("Сравнение ФИО")
def check_fio(br, test_dude):
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

@allure.step("Сравнение адреса")
def check_adress(br, test_dude):
    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

@allure.step("Сравнение стоимости оборудования")
def check_prices(br, device_price, monthly_payment, full_price):
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_price

    monthly_pay_IM = monthly_payment
    monthly_pay_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM == monthly_pay_WSO

    full_price_IM = full_price
    full_price_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(",", "."))
    assert full_price_IM == full_price_WSO

@allure.step("Сравнение стоимости оборудования и Каско")
def check_prices_with_kasko(br, device_price, phone_monthly_payment, phone_full_price, kasko_full_price):
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_price

    monthly_pay_IM_TA = phone_monthly_payment
    monthly_pay_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert monthly_pay_IM_TA == monthly_pay_WSO_TA

    full_price_IM_TA = phone_full_price
    full_price_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert full_price_IM_TA == full_price_WSO_TA

    full_price_IM_KASKO = kasko_full_price
    full_price_WSO_KASKO = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'СМАРТ гарантия')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert full_price_IM_KASKO == full_price_WSO_KASKO


@allure.step("Сравнение выбранного ТП и стоимости нового подключения")
def check_prices_new_sim(br, product_price, rate_plan):
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == product_price

    assert br.find_element_by_xpath("//*[text()[contains(.,'Тарифный план')]]/../div[2]/div/label").text == rate_plan, f"ТП не совпадают"
    assert br.find_element_by_xpath(
        "//*[text()[contains(.,'Тип SIM-карты')]]/../div[2]/div/label").text == "Universal", "Тип сим не совпадает"



@allure.step("Смена статуса заявки на 'Отклонена ИМ'")
def change_status_for_rejected(br):
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

@allure.step("Смена статуса заявки на 'Завершена/Отказ ИМ'")
def change_status_for_closed(br):
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

@allure.description("Поиск и открытие созданной заявки для сравнения данных и закрытия заявки")
@allure.step("Анализ данных заявки, сравнение данных и закрытие заявки")
def check_wso_installment(br, test_dude, external_id, device_price, monthly_payment, full_price):
    select_menu_internet_shop(br)
    order_external_id = find_order(br, external_id)
    view_search_results(br, test_dude, order_external_id)
    view_order_details(br)
    check_order_id(br, order_external_id)
    check_fio(br, test_dude)
    check_adress(br, test_dude)
    check_prices(br, device_price, monthly_payment, full_price)
    change_status_for_rejected(br)
    change_status_for_closed(br)





############################################################################3
@allure.step("Переход на вкладку 'Аксессуары'")
def go_to_accessory(br):
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()[contains(.,'Аксессуары')]]/.."))).click()
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//a[text()[contains(.,'Аксессуары')]]/../../div[contains(@class, 'tabs-controls-item active is-visible is-selected')]")))
    cut_pop_up(br)


@allure.step("Выбор бренда для покупаемого аксессуара")
def select_brand_for_accessory(br):
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    brand_pannel.find_element_by_xpath("//span[text()[contains(.,'Xiaomi')]]/../input").click()
    WebDriverWait(br, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))


@allure.step("Проверка корректности перехода на страницу аксессуара")
def check_accessory_page(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    #offer_block = br.find_element_by_xpath("//*[@id='WITHOUT_CONTRACT']")
    cut_pop_up(br)
    time.sleep(3)
    try:
        if br.find_element_by_xpath("//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']/span[text()[contains(.,'Оставить заявку')]]"):
            br.find_element_by_xpath("//ol[@class='breadcrumbs']//span[text()[contains(.,'Аксессуары')]]/..").click()
            WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                          "//a[text()[contains(.,'Аксессуары')]]/../../div[contains(@class, 'tabs-controls-item active is-visible is-selected')]")))
            cut_pop_up(br)
            brand_pannel = br.find_element_by_id("facet-collapse-brand")
            brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
            time.sleep(3)
            cut_pop_up(br)
            brand_pannel.find_element_by_xpath("//span[text()[contains(.,'Xiaomi')]]/../input").click()
            WebDriverWait(br, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
            product_list_block = br.find_element_by_xpath("//div[contains(@class, 'product-listing-content')]")
            product_list = product_list_block.find_elements_by_xpath(
                "//span[text()[contains(.,'Перейти к покупке')]]/../../../a")
            cut_pop_up(br)
            prod_num = randrange(len(product_list))
            WebDriverWait(br, 30).until(EC.visibility_of(product_list[prod_num]))
            time.sleep(3)
            product_list[prod_num].click()
            WebDriverWait(br, 60).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
            cut_pop_up(br)
            time.sleep(3)
        else:
            pass
    except:
        pass

@allure.step("Покупка аксессура")
def select_accessory(br):
    WebDriverWait(br, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()


@allure.step("Шаг 2")
def step_2(br):
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Шаг 2')]]")))
    cut_pop_up(br)
    WebDriverWait(br, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Продолжить')]]/..")))
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()


@allure.step("Корзина")
def check_cart_with_accessory(br):
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Корзина')]]")))
    assert br.find_element_by_xpath("//span[contains(@class, 'price-value')]").text == "0,00", "Неверная сумма заказа"
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Купить')]]/..").click()

@allure.step("Переход на окно 'Личные данные'")
def personal_data_window(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Личные данные')]]")))
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()


@allure.step("Переход на окно 'Способ оплаты', выбор способа оплаты")
def select_payment_method_for_order(br):
    time.sleep(6)
    payment_method = ""
    time.sleep(6)
    try:
        payment_method = br.find_element_by_xpath("//h2[text()[contains(.,'Способ оплаты')]]")
    except:
        pass

    if (payment_method):
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()[contains(.,'Банковской картой при получении')]]"))).click()
        cut_pop_up(br)
        br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    else:
        time.sleep(3)
        pass

@allure.step("Переход на окно 'Состав заказа'")
def order_list(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//button[@class='button button--tertiary with-icon collapsed']").click()
    time.sleep(2)
    device_price = float(
        str(br.find_element_by_xpath(
            "//*[@id='orderReviewForm']//dt[text()[contains(.,'Итого к оплате:')]]/following-sibling::dd//span[@class='price-value']").text).replace(
            " ", "").replace(",", "."))
    monthly_payment = float(
        str(br.find_element_by_xpath(
            "//p[text()[contains(.,'Регулярный платеж')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    full_price = float(
        str(br.find_element_by_xpath(
            "//p[text()[contains(.,'Итоговая стоимость')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    return device_price, monthly_payment, full_price


###########################################################################

@allure.description("Оформление покупки аксессуара")
@allure.step("Оформление покупки аксессуара")
def buy_accessory(br, test_dude):
    go_to_accessory(br)
    select_brand_for_accessory(br)
    select_product(br)
    check_accessory_page(br)
    select_accessory(br)
    step_2(br)
    check_cart_with_accessory(br)
    personal_data_window(br)
    select_delivery_method(br, test_dude)
    select_payment_method_for_order(br)
    device_price, monthly_payment, full_price = order_list(br)
    select_payment_method(br)
    external_id = order_confirmation(br)
    return external_id, device_price, monthly_payment, full_price
##############################################################################

@allure.step("Выбор типа продажи для продажи оборудования вместе с Каско")
def select_type_of_sale_for_kasko(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    offer_block = br.find_element_by_xpath("//div[contains(@class, 'live-filter-content-item active')]")
    cut_pop_up(br)
    offer_block.find_element_by_xpath("//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']").click()

@allure.step("Добавление Каско с заказу")
def add_kasko_to_order(br):
    # Окно "Добавить к заказу"
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Добавить к заказу')]]")))
    cut_pop_up(br)
    try:
        WebDriverWait(br, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Мобильное Каско')]]/.."))).click()
        WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                      "//*[contains(@class, 'tabs-controls-item active is-visible is-selected')]/*[text()[contains(.,'Мобильное Каско')]]")))
    except:
        WebDriverWait(br, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Мобильное КАСКО')]]/.."))).click()
        WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                      "//*[contains(@class, 'tabs-controls-item active is-visible is-selected')]/*[text()[contains(.,'Мобильное КАСКО')]]")))
    cut_pop_up(br)
    time.sleep(5)
    br.find_element_by_tag_name('body').send_keys(u'\ue00f')
    add_to_basket = br.find_element_by_xpath(
        "//*[@id='20.Kasko.100']//div[@class='tabs-content-pane active product-listing-item-tabs-content-pane']//form[@id='command']/button[@type='submit']")
    time.sleep(10)
    cut_pop_up(br)
    add_to_basket.click()
    cut_pop_up(br)
    time.sleep(10)
    cut_pop_up(br)

@allure.step("Корзина")
def take_device_price_from_cart(br):
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']")))
    cut_pop_up(br)
    device_price = float(
        str(br.find_element_by_xpath(
            "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    # НАЖИМАЕМ КУПИТЬ
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@class='form review-item-table-price']//*[@class='form-cta']//span[text()[contains(.,'Купить')]]/.."))).click()
    cut_pop_up(br)
    return device_price


@allure.step("Подтверждение покупки оборудования вместе с Каско")
def order_with_prices_confirmation(br):
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//button[@class='button button--tertiary with-icon collapsed']").click()
    time.sleep(2)
    phone_monthly_payment = float(
        str(br.find_element_by_xpath(
            "//div[@id='bundle-collapse-block-0']/div[1]//p[text()[contains(.,'Регулярный платеж')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    phone_full_price = float(
        str(br.find_element_by_xpath(
            "//div[@id='bundle-collapse-block-0']/div[1]//p[text()[contains(.,'Итоговая стоимость')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    kasko_full_price = float(
        str(br.find_element_by_xpath(
            "//div[@id='bundle-collapse-block-0']/div[2]//p[text()[contains(.,'К оплате')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()

    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    return phone_monthly_payment, phone_full_price, kasko_full_price

#########################################################################

@allure.description("Оформление покупки оборудования вместе с Каско")
@allure.step("Оформление покупки оборудования вместе с Каско")
def buy_device_with_kasko(br, test_dude):
    select_brand_with_kasko(br)
    select_product(br)
    select_type_of_sale_for_kasko(br)
    view_and_select_rate_plan(br)
    add_kasko_to_order(br)
    go_to_cart(br)
    device_price = take_device_price_from_cart(br)
    personal_data_window(br)
    select_delivery_method(br, test_dude)
    select_payment_method_for_order(br)
    phone_monthly_payment, phone_full_price, kasko_full_price = order_with_prices_confirmation(br)
    external_id = order_confirmation(br)
    return external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price

@allure.description("Проверка данных заказа в WSO")
@allure.step("Проверка данных заказа в WSO")
def check_wso_kasko_full(br, test_dude, external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price):
    select_menu_internet_shop(br)
    order_external_id = find_order(br, external_id)
    view_search_results(br, test_dude, order_external_id)
    view_order_details(br)
    check_order_id(br, order_external_id)
    check_fio(br, test_dude)
    check_adress(br, test_dude)
    check_prices_with_kasko(br, device_price, phone_monthly_payment, phone_full_price, kasko_full_price)
    change_status_for_rejected(br)
    change_status_for_closed(br)

###############
@allure.description("Покупка новой сим с подключением и оборудованием")
@allure.step("Покупка новой сим с подключением и оборудованием")
def buy_new_sim(br, test_dude):
    select_model_for_new_sim(br)
    select_rate_plan_for_new_sim(br)
    rate_plan, product_price = take_data_from_cart(br)
    personal_data_window(br)
    select_delivery_method(br, test_dude)
    select_payment_method(br)
    check_order_details(br)
    external_id = order_confirmation(br)
    return external_id, rate_plan, product_price


@allure.description("Проверка данных по подключению новой сим с оборудованием в WSO")
@allure.step("Проверка данных по подключению новой сим с оборудованием в WSO")
def check_wso_new_sim(br, test_dude, external_id, rate_plan, product_price):
    select_menu_internet_shop(br)
    order_external_id = find_order(br, external_id)
    view_search_results(br, test_dude, order_external_id)
    view_order_details(br)
    check_order_id(br, order_external_id)
    check_fio(br, test_dude)
    check_adress(br, test_dude)
    check_prices_new_sim(br, product_price, rate_plan)
    change_status_for_rejected(br)
    change_status_for_closed(br)