from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium
import time
from selenium.webdriver import ActionChains
from selenium import webdriver
import traceback
from random import randrange
from selenium.webdriver.common.keys import Keys


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



def open_browser(site_to_open):
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=ru')
    br = webdriver.Chrome(executable_path=r'C:\tools\chromedriver.exe', options=options)
    br.maximize_window()
    br.get(site_to_open)
    return br


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


def logout_site(br):
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.ID, "dropdownMenuUser"))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Выход')]]"))).click()
    time.sleep(3)
    cut_pop_up(br)


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
        cart_delete_list = br.find_elements_by_xpath("//div[contains(@class, 'review-item-fixed-block review-item-fixed-block--with-expandable-body')]")
            #br.find_elements_by_xpath("//span[contains(@class, 'icon icon--remove')]")
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


def buy_accessory(br, test_dude):
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()[contains(.,'Аксессуары')]]/.."))).click()
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


    WebDriverWait(br, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Шаг 2')]]")))
    cut_pop_up(br)
    WebDriverWait(br, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Продолжить')]]/..")))
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
    #корзина
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Корзина')]]")))
    assert br.find_element_by_xpath("//span[contains(@class, 'price-value')]").text == "0,00", "Неверная сумма заказа"
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Купить')]]/..").click()
    #личные данные
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Личные данные')]]")))
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()
    #Способ доставки
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Способ доставки')]]")))
    delivery_method = ""
    try:
        assert br.find_element_by_xpath("//h2[text()[contains(.,' Способ доставки')]]").text == "Способ доставки"
        delivery_method = br.find_element_by_xpath("//h2[text()[contains(.,' Способ доставки')]]").text
    except:
        pass
    if (delivery_method):
        cut_pop_up(br)
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Доставка курьером')]]")))
        time.sleep(1)
        br.find_element_by_xpath("//*[text()[contains(.,'Доставка курьером')]]").click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Данные о доставке')]]")))
        assert br.find_element_by_xpath("//*[text()[contains(.,'Адрес')]]/following::*").text == test_dude.adres
        WebDriverWait(br, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()
    else:
        pass
    #Способ оплаты
    time.sleep(5)
    payment_method = ""
    time.sleep(5)
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
        pass

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

    #Способ оплаты (временное решение вставить сюда этот кусок кода из-за дефекта https://jira.a1.by/browse/HBRS-2348 при котором меняется очередность шагов
    time.sleep(5)
    payment_method = ""
    time.sleep(5)
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
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
        cut_pop_up(br)
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()

        br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    else:
        pass
    ##########################################
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)
    return external_id, device_price, monthly_payment, full_price


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


def check_order_in_wso(br, accessory, test_dude):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(accessory[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    time.sleep(2)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(2)
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == accessory[1]

    monthly_pay_IM = accessory[2]
    monthly_pay_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM == monthly_pay_WSO

    full_price_IM = accessory[3]
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


def buy_device_with_kasko(br, test_dude):
    cut_pop_up(br)
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//*[@id=\"facet-collapse-brand\"]/div/div/div/div[1]/div/div[2]/div/ul/li[2]/form/div/label").click()
    WebDriverWait(br, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
    product_list_block = br.find_element_by_xpath("//div[contains(@class, 'product-listing-content')]")
    product_list = product_list_block.find_elements_by_xpath(
        "//span[text()[contains(.,'Перейти к покупке')]]/../../../a")
    cut_pop_up(br)
    prod_num = randrange(len(product_list))
    WebDriverWait(br, 30).until(EC.visibility_of(product_list[prod_num]))
    time.sleep(3)
    cut_pop_up(br)
    product_list[prod_num].click()
    # карточка оборудования
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'live-filter-content-item active')]")))
    offer_block = br.find_element_by_xpath("//div[contains(@class, 'live-filter-content-item active')]")
    cut_pop_up(br)
    # нажимаем купить
    offer_block.find_element_by_xpath("//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']").click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Просмотр и выбор тарифа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
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
    time.sleep(20)
    cut_pop_up(br)
    # нажать Перейти в корзину
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]"))).click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
    # Окно Корзина
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
    # окно Личные данные
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/..")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    # окно Способ доставки
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

    payment_method = ""
    time.sleep(3)
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
        pass

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
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)
    return external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price


def check_wso_kasko(br, test_dude, device_with_kasko):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(device_with_kasko[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")
    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_with_kasko[1]
    wso_kasko_price = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'СМАРТ гарантия')]]/../../following::div[1]/div[2]/div[4]/div[2]/div[2]/span").text).replace(
        ",", "."))
    assert wso_kasko_price == device_with_kasko[1]
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


def buy_new_sim(br, test_dude):
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
    # Окно Корзина
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//*[@class='col-sm-12']// *[@ class ='description-list description-list--review review-item-table-dl']//span[@class='price ']/span[@class='price-value ']")))
    cut_pop_up(br)
    br.find_element_by_xpath("//button[@class='button button--tertiary with-icon collapsed']").click()
    time.sleep(2)
    assert br.find_element_by_xpath("//div[@id='bundle-collapse-block-0']/div[2]/div[@class='review-item-main']/div[@class='review-item-main-info']/p").text == "SIM-карта"
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
    # окно Личные данные
    br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    # окно Способ доставки
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
    payment_method = ""
    time.sleep(3)
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
        pass

    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Подтверждаю, что я ознакомлен и согласен с условиями ')]]/..").click()
    time.sleep(1)
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)


    return external_id, rate_plan, product_price


def check_wso_new_sim(br, test_dude, new_sim_order):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(new_sim_order[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")
    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == new_sim_order[2]

    assert br.find_element_by_xpath("//*[text()[contains(.,'Тарифный план')]]/../div[2]/div/label").text == \
           new_sim_order[1], f"ТП не совпадают"
    assert br.find_element_by_xpath(
        "//*[text()[contains(.,'Тип SIM-карты')]]/../div[2]/div/label").text == "Universal", "Тип сим не совпадает"

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


# новый клиент - покупка в рассрочку на 6 месяцев
def buy_in_installment_device(br, test_dude):
    cut_pop_up(br)
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//*[@id=\"facet-collapse-brand\"]/div/div/div/div[1]/div/div[2]/div/ul/li[2]/form/div/label").click()
    WebDriverWait(br, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
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
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Новый номер')]]/.."))).click()
    time.sleep(2)
    combobox = br.find_element_by_xpath(
        "//*[@id='NEW_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    ac = ActionChains(br)
    ac.move_to_element(br.find_element_by_xpath("//li/div[text()[contains(., '6 мес по ')]]/..")).perform()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//li/div[text()[contains(., '6 мес по ')]]/.."))).click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='NEW_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='price-block-button']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Просмотр и выбор тарифа')]]")))
    cut_pop_up(br)
    #разворачивание полного списка ТП
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button/span[text()[contains(.,'Показать еще')]]/.."))).click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button/span[text()[contains(.,'Показать еще')]]/.."))).click()
    # подсчет количества предложений с ТП
    tarif_list = br.find_elements_by_xpath("//button/span[text()[contains(.,'Выбрать')]]/..")
    prod_num = randrange(len(tarif_list))
    tarif_list[prod_num].click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button/span[text()[contains(.,'Продолжить')]]/.."))).click()
    # Окно "Добавить к заказу"
    WebDriverWait(br, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//*[text()[contains(.,'Перейти в корзину')]]").click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
    #Окно Корзина
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

    #выбор Я гость\Я абонент А1
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Я гость')]]/..")))
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath("//*[text()[contains(.,'Я гость')]]/..").click()
    time.sleep(3)
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Я гость')]]/..")))
    # переходим в окно Продолжить как гость
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Продолжить как гость')]]/..")))
    fio = test_dude.FIO.split()
    br.find_element_by_xpath("//*[@id='guestLoginForm']/div[1]/label/input").send_keys(fio[1])
    br.find_element_by_xpath("//*[@id='guestLoginForm']/div[2]/label/input").click()
    br.find_element_by_xpath("//*[@id='guestLoginForm']/div[2]/label/input").send_keys(test_dude.login)
    br.find_element_by_xpath("//*[@id='guestLoginForm']/div[3]/button[1]").click()
    # переходим в окно Оформление заказа
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Личные данные')]]/..")))
    cut_pop_up(br)
    br.find_element_by_xpath("//*[@id='lastName']").click()
    fio = test_dude.FIO.split()
    br.find_element_by_xpath("//*[@id='lastName']").send_keys(fio[0])
    br.find_element_by_xpath("//*[@id='firstName']").click()
    br.find_element_by_xpath("//*[@id='firstName']").send_keys(fio[1])
    br.find_element_by_xpath("//*[@name='passportInfo.middleName']").click()
    br.find_element_by_xpath("//*[@name='passportInfo.middleName']").send_keys(fio[2])
    br.find_element_by_xpath("//*[@id='dateOfBirth']").click()
    br.find_element_by_xpath("//*[@id='dateOfBirth']").send_keys(test_dude.dateOfBirth)
    br.find_element_by_xpath("//*[@id='passportSeries']").click()
    br.find_element_by_xpath("//*[@id='passportSeries']").send_keys(test_dude.serialPasport)
    br.find_element_by_xpath("//*[@id='passportNumber']").click()
    br.find_element_by_xpath("//*[@id='passportNumber']").send_keys(test_dude.numberPassport)
    br.find_element_by_xpath("//*[@id='personalNumber']").click()
    br.find_element_by_xpath("//*[@id='personalNumber']").send_keys(test_dude.identifirePassport)
    br.find_element_by_xpath("//*[@id='passportIssuedBy']").click()
    br.find_element_by_xpath("//*[@id='passportIssuedBy']").send_keys(test_dude.whoGivePassport)
    br.find_element_by_xpath("//*[@id='passportIssuedDate']").click()
    br.find_element_by_xpath("//*[@id='passportIssuedDate']").send_keys(test_dude.dateOfIssue)
    # город
    br.find_element_by_xpath("//*[@aria-labelledby='select2-i-city_0-container']").click()
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Населенный пункт')]]/../following-sibling::span//input").send_keys(test_dude.city)
    time.sleep(1)
    br.find_element_by_xpath("//*[@id='select2-i-city_0-results']/li[1]").click()
    time.sleep(1)
    # улица
    br.find_element_by_xpath("//*[@aria-labelledby='select2-i-street_1-container']").click()
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Улица (если есть)')]]/../following-sibling::span//input").send_keys(test_dude.street)
    time.sleep(1)
    br.find_element_by_xpath("//*[@id='select2-i-street_1-results']/li").click()
    time.sleep(1)
    br.find_element_by_tag_name('body').send_keys(u'\ue010')
    time.sleep(1)
    # дом
    br.find_element_by_xpath("//label[@for='i-house_2']").click()
    time.sleep(1)
    br.find_element_by_xpath("//span[text()[contains(.,'Дом')]]/../following-sibling::span//input").send_keys(
        test_dude.house)
    time.sleep(1)
    br.find_element_by_xpath("//*[@id='select2-i-house_2-results']/li").click()
    time.sleep(1)
    # корпус
    br.find_element_by_xpath("//label[@for='i-corp_3']").click()
    time.sleep(1)
    br.find_element_by_xpath("//span[text()[contains(.,'Корп.')]]/../following-sibling::span//input").send_keys(
        test_dude.building)
    time.sleep(1)
    br.find_element_by_xpath("//*[@id='select2-i-corp_3-results']/li").click()
    time.sleep(1)
    # кв.\офис
    br.find_element_by_xpath("//input[@id='i-room_4']").click()
    br.find_element_by_xpath("//input[@id='i-room_4']").send_keys(test_dude.appartment)
    # email
    br.find_element_by_xpath("//*[@id='i-email-input']").click()
    br.find_element_by_xpath("//*[@id='i-email-input']").send_keys(test_dude.email)
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()
    WebDriverWait(br, 30).until(EC.invisibility_of_element((By.XPATH, "//*[text()[contains(.,' Личные данные')]]/..")))
    time.sleep(5)
    # Способ доставки
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Способ доставки')]]/..")))

    try:
        delivery_method = br.find_element_by_xpath("//*[text()[contains(.,'Способ доставки')]]")
    except:
        pass
    if (delivery_method):
        cut_pop_up(br)
        br.find_element_by_xpath("//*[text()[contains(.,'Доставка курьером')]]").click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Создать новый адрес')]]")))
        br.find_element_by_xpath("//*[text()[contains(.,' Создать новый адрес')]]").click()
        # Новый адрес
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,' Новый адрес')]]/..")))
        cut_pop_up(br)
        # город
        br.find_element_by_xpath("//*[@aria-labelledby='select2-i-city_0-container']").click()
        time.sleep(1)
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Населенный пункт')]]/../following-sibling::span//input").send_keys(
            test_dude.city)
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='select2-i-city_0-results']/li[1]").click()
        time.sleep(1)
        # улица
        br.find_element_by_xpath("//*[@aria-labelledby='select2-i-street_1-container']").click()
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Улица (если есть)')]]/../following-sibling::span//input").send_keys(
            test_dude.street)
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='select2-i-street_1-results']/li").click()
        time.sleep(1)
        # дом
        br.find_element_by_xpath("//label[@for='i-house_2']").click()
        time.sleep(1)
        br.find_element_by_xpath("//span[text()[contains(.,'Дом')]]/../following-sibling::span//input").send_keys(
            test_dude.house)
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='select2-i-house_2-results']/li").click()
        time.sleep(1)
        # корпус
        br.find_element_by_xpath("//label[@for='i-corp_3']").click()
        time.sleep(1)
        br.find_element_by_xpath("//span[text()[contains(.,'Корп.')]]/../following-sibling::span//input").send_keys(
            test_dude.building)
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='select2-i-corp_3-results']/li").click()
        time.sleep(1)
        # кв.\офис
        br.find_element_by_xpath("//input[@id='i-room_4']").click()
        br.find_element_by_xpath("//input[@id='i-room_4']").send_keys(test_dude.appartment)
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Сохранить')]]/..")))
        br.find_element_by_xpath("//span[text()[contains(.,'Сохранить')]]/..").click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Данные о доставке')]]/..")))
        cut_pop_up(br)
        WebDriverWait(br, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'Далее')]]/.."))).click()
    else:
        pass
    # Способ оплаты
    payment_method = ""
    time.sleep(5)
    try:
        WebDriverWait(br, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Способ оплаты')]]")))
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
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Состав заказа')]]")))
        cut_pop_up(br)
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Подтверждаю, что я ознакомлен и согласен с условиями ')]]/..").click()
        br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()[contains(.,'Банковской картой при получении')]]"))).click()
        cut_pop_up(br)
        br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    #Состав заказа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Состав заказа')]]")))
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

    br.find_element_by_xpath(
        "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
    time.sleep(1)
    br.find_element_by_xpath(
        "//span[text()[contains(.,'Подтверждаю, что я ознакомлен и согласен с условиями ')]]/..").click()
    time.sleep(1)
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    cut_pop_up(br)
    time.sleep(1)
    return device_price, monthly_payment, full_price


def check_wso_installment_for_new(br, test_dude, buy_in_installment):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    br.find_element_by_id("webShopOrderSearchForm:nameCustomer").send_keys(test_dude.FIO)
    time.sleep(3)
    today = time.strftime("%d.%m.%Y")
    br.find_element_by_id("webShopOrderSearchForm:fromDate_input").clear()
    br.find_element_by_id("webShopOrderSearchForm:fromDate_input").send_keys(today)
    time.sleep(3)
    br.find_element_by_id("webShopOrderSearchForm:status").click()
    time.sleep(3)
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:status_2']").click()
    time.sleep(3)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']")))
    time.sleep(2)
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    time.sleep(1)
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")
    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == buy_in_installment[0]
    monthly_pay_IM = buy_in_installment[1]
    # monthly_pay_WSO = float(str(br.find_element_by_xpath(
    #     "//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    monthly_pay_WSO = float(str(br.find_element_by_xpath(
         "//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM == monthly_pay_WSO

    full_price_IM = buy_in_installment[2]
    full_price_WSO = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(",", "."))
    assert full_price_IM == full_price_WSO

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


# ПОКУПКА ПО ПОЛНОЙ СТОИМОСТИ
def buy_full_price_device(br, test_dude):
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
    offer_block = br.find_element_by_xpath("//div[contains(@class, 'live-filter-content-item active')]")
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Полная цена')]]/.."))).click()
    # купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='WITHOUT_CONTRACT']//*[@class='price-block-pane-content']//*[@class='price-block-button']//*[@class='button button--primary button--large']")))
    br.find_element_by_xpath(
        "//*[@id='WITHOUT_CONTRACT']//*[@class='price-block-pane-content']//*[@class='price-block-button']//*[@class='button button--primary button--large']").click()
    # Корзина
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//*[text()[contains(.,'Перейти в корзину')]]").click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]/..")))
    #Корзина
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
    #выбор опции Я абонент А1 или Я гость
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Я абонент A1')]]/..")))
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath("//*[text()[contains(.,'Я абонент A1')]]/..").click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Я абонент A1')]]/..")))

    WebDriverWait(br, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="pwd_choose"]/../span[@class="radiobtn"]'))).click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='tel' and @name='UserID']")))
    br.find_element_by_xpath("//input[@type='tel' and @name='UserID']").send_keys(test_dude.login)  # set login
    br.find_element_by_xpath("//input[@type='password' and @id='ipassword']").send_keys(test_dude.password)
    br.find_element_by_xpath('//*[@id="butt1"]').click()
    WebDriverWait(br, 30).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id=\"mr\"]/div/div/section/h1")))
    cut_pop_up(br)
    fio = test_dude.FIO.split()
    br.find_element_by_xpath("//*[contains(@name, 'lastName')]").send_keys(fio[0])
    br.find_element_by_xpath("//*[contains(@name, 'firstName')]").send_keys(fio[1])
    br.find_element_by_xpath("//*[contains(@name, 'middleName')]").send_keys(fio[2])
    br.find_element_by_xpath("//*[@id='i-email-input']").send_keys(test_dude.email)
    br.find_element_by_id("saveShortInfo").click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Способ доставки')]]")))
    cut_pop_up(br)
    time.sleep(5)
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
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
        cut_pop_up(br)
        br.find_element_by_xpath(
            "//span[text()[contains(.,'Личные данные могут быть использованы для дополнительной проверки.')]]/..").click()
        br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()[contains(.,'Банковской картой при получении')]]"))).click()
        cut_pop_up(br)
        br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    #Состав заказа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Состав заказа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Подтвердить')]]/..").click()
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Мы приступили к обработке Вашего заказа.')]]")))
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(.,'статуса')]]/../span"))).click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Дата размещения')]]")))
    external_id = br.find_element_by_xpath("//h1[text()[contains(.,'Заказ ')]]").text
    time.sleep(3)
    return external_id, device_price


def check_wso_full_price_device(br, test_dude, full_price_device):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(full_price_device[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")
    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == full_price_device[1]

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




#РАССРОЧКА НА 6 МЕСЯЦЕВ
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
    product_list = product_list_block.find_elements_by_xpath("//span[text()[contains(.,'Перейти к покупке')]]/../../../a")
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
    ac = ActionChains(br)
    ac.move_to_element(br.find_element_by_xpath("//li/div[text()[contains(., '6 мес по ')]]/..")).perform()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//li/div[text()[contains(., '6 мес по ')]]/.."))).click()
    # нажимаем купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Просмотр и выбор тарифа')]]")))
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
    #окно Способ доставки
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


#РАССРОЧКА НА 11 МЕСЯЦЕВ
def buyTANaSimEleven(br, test_dude):
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    brand_list = br.find_elements_by_xpath("//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
    brand_list = br.find_elements_by_xpath(
        "//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
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
    br.find_element_by_xpath("//li/div[text()[contains(., '11 мес по ')]]/..").click()
    # нажимаем купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Просмотр и выбор тарифа')]]")))
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
    br.find_element_by_id("submitButton").click()
    cut_pop_up(br)
    #окно Способ доставки
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


#РАССРОЧКА НА 24 МЕСЯЦЕВ
def buyTANaSim24(br, test_dude):
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    brand_list = br.find_elements_by_xpath("//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
    brand_list = br.find_elements_by_xpath(
        "//*[@id='facet-collapse-brand']/div/div/div/div[1]/div/div[2]/div/ul/li")
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
    br.find_element_by_xpath("//li/div[text()[contains(., '24 мес по ')]]/following-sibling::div[text()[contains(.,'С обслуживанием не менее 12')]]/..").click()
    # нажимаем купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,' Просмотр и выбор тарифа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]"))).click()
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
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
    #окно Способ доставки
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



#КАСКО в рассрочку
def buy_device_with_kasko_installment(br, test_dude):
    cut_pop_up(br)
    brand_pannel = br.find_element_by_id("facet-collapse-brand")
    brand_pannel.find_element_by_xpath("//div[@id='facet-collapse-brand']/div[1]/div/div/div[2]/button").click()
    time.sleep(3)
    cut_pop_up(br)
    br.find_element_by_xpath(
        "//*[@id=\"facet-collapse-brand\"]/div/div/div/div[1]/div/div[2]/div/ul/li[2]/form/div/label").click()
    WebDriverWait(br, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product-listing-content')]")))
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
    offer_block = br.find_element_by_xpath("//div[contains(@class, 'live-filter-content-item active')]")
    cut_pop_up(br)
    # карточка оборудования
    combobox = br.find_element_by_xpath(
        "//*[@id='CURRENT_CONTRACT']//span[contains(@class, 'select2-selection select2-selection--single')]")
    combobox.click()
    time.sleep(1)
    ac = ActionChains(br)
    ac.move_to_element(br.find_element_by_xpath("//li/div[text()[contains(., '6 мес по ')]]/..")).perform()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//li/div[text()[contains(., '6 мес по ')]]/.."))).click()
    # нажимаем купить
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//*[@id='CURRENT_CONTRACT']//*[@class='live-filter-content-item active']//*[@class='button button--primary button--large']"))).click()
    # переход на окно Просмотр и выбор тарифа
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Просмотр и выбор тарифа')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Продолжить')]]/..").click()
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
    add_to_basket = br.find_element_by_xpath("//*[@id='20.Kasko.1000']//div[@class='tabs-content']/div[@id='addon-map-view']/div/div[3]/div[2]/div[@class='product-listing-item-btn']/form[@id='command']/button[@type='submit']")
    cut_pop_up(br)
    time.sleep(10)
    add_to_basket.click()
    time.sleep(20)
    cut_pop_up(br)
    #нажать Перейти в корзину
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]"))).click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Перейти в корзину')]]")))
    # Окно Корзина
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
    #окно Личные данные
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH,"//span[text()[contains(.,'Далее')]]/..")))
    cut_pop_up(br)
    br.find_element_by_xpath("//span[text()[contains(.,'Далее')]]/..").click()
    #окно Способ доставки
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

    payment_method = ""
    time.sleep(3)
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
        pass

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
    kasko_monthly_payment = float(
        str(br.find_element_by_xpath(
            "//div[@id='bundle-collapse-block-0']/div[2]//p[text()[contains(.,'Регулярный платеж')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))
    kasko_full_price = float(
        str(br.find_element_by_xpath(
            "//div[@id='bundle-collapse-block-0']/div[2]//p[text()[contains(.,'Итоговая стоимость')]]/following-sibling::p//span[@class='price-value ']").text).replace(
            " ", "").replace(",", "."))

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
    return external_id, device_price, phone_monthly_payment, phone_full_price, kasko_monthly_payment, kasko_full_price




def check_wso_kasko(br, test_dude, device_with_kasko):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(device_with_kasko[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(2)
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_with_kasko[1]

    monthly_pay_IM_TA = device_with_kasko[2]
    monthly_pay_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM_TA == monthly_pay_WSO_TA

    full_price_IM_TA = device_with_kasko[3]
    full_price_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(",", "."))
    assert full_price_IM_TA == full_price_WSO_TA

    monthly_pay_IM_KASKO = device_with_kasko[4]
    monthly_pay_WSO_KASKO = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'СМАРТ гарантия')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert monthly_pay_IM_KASKO == monthly_pay_WSO_KASKO

    full_price_IM_KASKO = device_with_kasko[5]
    full_price_WSO_KASKO = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'СМАРТ гарантия')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert full_price_IM_KASKO == full_price_WSO_KASKO

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

def check_wso_kasko_full(br, test_dude, device_with_kasko):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(device_with_kasko[0]).replace("Заказ ", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(2)
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[6]").text).strip() == test_dude.FIO, "Отобразилось неверное ФИО абонента"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id
    assert br.find_element_by_xpath("//span[text()[contains(.,'ФИО')]]/../following::div[1]/span").text == test_dude.FIO

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_with_kasko[1]

    monthly_pay_IM_TA = device_with_kasko[2]
    monthly_pay_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Ежемесячно:')]]/../following::div[1]/span").text).replace(",", "."))
    assert monthly_pay_IM_TA == monthly_pay_WSO_TA

    full_price_IM_TA = device_with_kasko[3]
    full_price_WSO_TA = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'Продажа оборудования')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(",", "."))
    assert full_price_IM_TA == full_price_WSO_TA

    full_price_IM_KASKO = device_with_kasko[4]
    full_price_WSO_KASKO = float(str(br.find_element_by_xpath(
        "//*[text()[contains(.,'СМАРТ гарантия')]]/../../..//div[text()[contains(.,'Данные по оборудованию')]]/..//span[text()[contains(.,'Полная стоимость:')]]/../following::div[1]/span").text).replace(
        ",", "."))
    assert full_price_IM_KASKO == full_price_WSO_KASKO

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

##########LEGAL
def check_cart_legal(br):
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Продолжить как юридическое лицо')]]")))
    cut_pop_up(br)
    br.find_element_by_xpath("//*[text()[contains(.,'Продолжить как юридическое лицо')]]").click()
    WebDriverWait(br, 60).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Продолжить как юридическое лицо')]]")))
    WebDriverWait(br, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'basket-small__widget')]")))
    br.find_element_by_xpath("//a[contains(@class, 'basket-small__widget')]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Корзина')]]/..")))
    time.sleep(5)
    try:
        cut_pop_up(br)
        if br.find_element_by_xpath(
                "//*[text()[contains(.,'Корзина пуста. Перейдите в интернет-магазин, чтобы продолжить покупки.')]]"):
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()[contains(.,'Перейти в интернет-магазин')]]")))
            br.find_element_by_xpath("//a[text()[contains(.,'Перейти в интернет-магазин')]]").click()
        else:
            pass
    except:
        cart_delete_list = br.find_elements_by_xpath("//button[contains(@class, 'basket-item__remove')]")
        for i in cart_delete_list:
            cut_pop_up(br)
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'basket-item__remove')]"))).click()
            WebDriverWait(br, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//button[text()[contains(.,'Да')]]")))
            WebDriverWait(br, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()[contains(.,'Да')]]"))).click()
            WebDriverWait(br, 30).until(
                EC.invisibility_of_element_located((By.XPATH, "//button[text()[contains(.,'Да')]]")))
        WebDriverWait(br, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()[contains(.,'Перейти в интернет-магазин')]]"))).click()
        WebDriverWait(br, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'v-product-grid product-grid')]")))
        time.sleep(4)
        cut_pop_up(br)



def buy_for_legal(br, test_dude):
    cut_pop_up(br)
    br.find_element_by_xpath("//*[@class='filter__tab-list-item']//a[text()[contains(.,'Телефоны')]]/..").click()
    cut_pop_up(br)
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Телефоны')]]")))
    #Показать все
    br.find_element_by_xpath("//a[text()[contains(.,'Бренд')]]/../following-sibling::div//button").click()
    time.sleep(3)
    brand_list = br.find_elements_by_xpath("//a[text()[contains(.,'Бренд')]]/../following-sibling::div//span[@class= 'field-checkbox__visual']")
    brand_num = randrange(len(brand_list))
    brand_list[brand_num].click()
    time.sleep(3)
    try:
        if br.find_elements_by_xpath("//span[text()[contains(.,'Перейти к покупке')]]"):
            pass
        else:
            br.find_element_by_xpath("page-nav__link page-nav__arrow page-nav__arrow--next").click()
            time.sleep(5)
    except:
        pass
    product_list_block = br.find_element_by_xpath("//div[contains(@class, 'product-grid__grid')]")
    product_list = product_list_block.find_elements_by_xpath("//span[text()[contains(.,'Перейти к покупке')]]")
    prod_num = randrange(len(product_list))
    WebDriverWait(br, 30).until(EC.visibility_of(product_list[prod_num]))
    time.sleep(3)
    product_list[prod_num].click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'price-panel__price flc')]")))
    cut_pop_up(br)
    # карточка оборудования
    combobox = br.find_element_by_xpath("//button[contains(@class, 'field-select__btn')]")
    combobox.click()
    time.sleep(3)
    br.find_element_by_tag_name('body').send_keys(u'\ue00f')
    ac = ActionChains(br)
    ac.move_to_element(br.find_element_by_xpath("//div/button[text()[contains(., 'Цена со скидкой')]]")).perform()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div/button[text()[contains(., 'Цена со скидкой')]]"))).click()
    time.sleep(2)
    # нажимаем купить
    br.find_element_by_xpath("//button[text()[contains(.,'Купить')]]/..").click()
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//div[text()[contains(.,'Для добавления товара в корзину необходимо ввести УНП Вашей организации.')]]")))
    #br.find_element_by_xpath("//input[contains(@placeholder, 'Введите УНП')]").click()
    br.find_element_by_xpath("//input[contains(@placeholder, 'Введите УНП')]").send_keys(test_dude.TRN)
    br.find_element_by_xpath("//button[contains(@class, 'btn btn--md btn--center btn--primary form-unp__submit')]").click()
    # продолжить
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH,"//h4[text()[contains(.,'Товар добавлен в корзину')]]")))
    br.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[2]/div/div[2]/a").click()

    # Корзина
    WebDriverWait(br, 30).until(EC.visibility_of_element_located((By.XPATH,"//h1[text()[contains(.,'Корзина')]]")))
    cut_pop_up(br)
    device_price = float(
        str(br.find_element_by_xpath("//*[text()[contains(.,'Итого к оплате (первым взносом):')]]/following-sibling::div/*[text()!=' руб']").text).replace(
            " ", "").replace(",", "."))
    # НАЖИМАЕМ ОФОРМИТЬ
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()[contains(.,'Оформить')]]"))).click()
    cut_pop_up(br)
    WebDriverWait(br, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Оформление заказа')]]")))
    #заполняем раздел Об организации
    br.find_element_by_xpath("//input[@placeholder = 'Название ЮЛ']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Название ЮЛ']").send_keys(test_dude.company_name)
    br.find_element_by_xpath("//input[@placeholder = 'Контактное лицо']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Контактное лицо']").send_keys(test_dude.contact_person)
    br.find_element_by_xpath("//input[@placeholder = 'Номер телефона']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Номер телефона']").send_keys(test_dude.contact_phone)
    br.find_element_by_xpath("//input[@placeholder = 'Email']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Email']").send_keys(test_dude.email)
    #заполняем раздел Данные о доставке
    br.find_element_by_xpath("//*[text()[contains(.,'Курьером')]]").click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder = 'Населенный пункт']")))
    # город
    br.find_element_by_xpath("//input[@placeholder = 'Населенный пункт']").click()
    time.sleep(2)
    br.find_element_by_xpath("//input[@placeholder = 'Населенный пункт']").send_keys(test_dude.city)
    time.sleep(2)
    # br.find_element_by_xpath("//div[text()[contains(.,'г. Минск')]]/..").click()
    br.find_element_by_xpath("//*[@class='field-tooltip__list-container']/button[1]").click()
    time.sleep(2)
    # улица
    br.find_element_by_xpath("//input[@placeholder = 'Улица']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Улица']").send_keys(test_dude.street)
    time.sleep(2)
    br.find_element_by_xpath("//*[@class='field-tooltip__list-container']/button[1]").click()
    time.sleep(2)
    # дом
    br.find_element_by_xpath("//input[@placeholder = 'Дом']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Дом']").send_keys(test_dude.house)
    time.sleep(2)
    br.find_element_by_xpath("//*[@class='field-tooltip__list-container']/button[1]").click()
    time.sleep(2)
    # корпус
    br.find_element_by_xpath("//input[@placeholder = 'Корпус (необяз.)']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Корпус (необяз.)']").send_keys(test_dude.building)
    time.sleep(2)
    # кв.\офис
    br.find_element_by_xpath("//input[@placeholder = 'Кв./Оф.']").click()
    br.find_element_by_xpath("//input[@placeholder = 'Кв./Оф.']").send_keys(test_dude.appartment)
    time.sleep(2)
    #комментарий
    br.find_element_by_xpath("//textarea[@placeholder = 'Комментарий (необязательно)']").click()
    br.find_element_by_xpath("//textarea[@placeholder = 'Комментарий (необязательно)']").send_keys("Тестовая заявка. Просьба не обрабатывать.")
    time.sleep(2)
    #Подтверждаю ознакомление
    br.find_element_by_xpath("//span[text()[contains(.,'Подтверждаю, что ознакомлен с ')]]/..").click()
    WebDriverWait(br, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()[contains(.,'Оформить заказ')]]")))
    br.find_element_by_xpath("//button[text()[contains(.,'Оформить заказ')]]").click()
    #Финальное окно
    WebDriverWait(br, 60).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[text()[contains(.,'Ваша заявка принята. Для подтверждения деталей заказа мы свяжемся с Вами по телефону')]]")))
    cut_pop_up(br)
    external_id = br.find_element_by_xpath("//div[text()[contains(.,'в наличии')]]").text
    time.sleep(3)
    return external_id, device_price



def check_wso_legal(br, test_dude, device_price):
    ac = ActionChains(br)
    WebDriverWait(br, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='menuForm']")))
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Операции')]]"))).perform()
    ac.move_to_element((br.find_element_by_xpath("//span[text()[contains(.,'Интернет магазин')]]"))).perform()
    br.find_element_by_xpath("//span[text()[contains(.,'Поиск заявок')]]").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='webShopOrderSearchForm:webShopOrderPanel_content']")))
    order_external_id = str(device_price[0]).replace(" в наличии", '')
    br.find_element_by_xpath("//td[text()[contains(.,'ID во внешн. системе')]]/following::td/input").send_keys(
        order_external_id)
    br.find_element_by_id("webShopOrderSearchForm:findWebShopOrderBtn").click()
    time.sleep(3)
    WebDriverWait(br, 60).until(EC.invisibility_of_element_located(
        (By.XPATH, "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr[2]")))  # переделать
    assert str(br.find_element_by_xpath(
        "//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[3]").text).strip() == order_external_id, "Внешний ID заявки в WSO не соответствует отобразившемуся в ИМ"
    br.find_element_by_xpath("//*[@id='webShopOrderSearchForm:WebShopOrdersList_data']/tr/td[2]/a").click()
    WebDriverWait(br, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='hybrisOrderDetailForm:rootOrderDetailPanel_header']")))
    assert br.find_element_by_xpath(
        "//span[text()[contains(.,'ID заявки во внешней системе:')]]/../following::div[1]/span").text == order_external_id

    displayed_adress = str(br.find_element_by_xpath(
        "//div[text()[contains(.,'Адрес доставки')]]/following::div[1]/div/span").text).replace("\n", " ")
    assert displayed_adress == test_dude.adres.replace("кв./оф.", "кв.")

    br.find_element_by_xpath("//*[text()[contains(.,'Сменить статус')]]/..").click()
    final_price = float(str(br.find_element_by_xpath(
        "//span[text()[contains(.,'Итого к оплате')]]/../following::div[1]/span").text).replace(",", "."))
    assert final_price == device_price[1]
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



