import time
import pytest
from src import hybris_operations as HB, ma_dudes as dudes
import allure

test_dude = dudes.Private_dude
vix_creds = dudes.VIX_credentials
wso = dudes.WSO_prod
login = test_dude.login
passw = test_dude.password

#fixture
@pytest.fixture
def br():
    site = 'https://www.a1.by/ru/'
    br = HB.open_browser(site)
    yield br
    print(f"\nSCREENSHOT: " + (str(time.strftime('%Y-%m-%d-%H-%M'))))
    s = br.get_window_size()
    # obtain browser height and width
    w = br.execute_script('return document.body.parentNode.scrollWidth')
    h = br.execute_script('return document.body.parentNode.scrollHeight')
    # set to new window size
    br.set_window_size(w, h)
    # obtain screenshot of page within body tag
    br.save_screenshot("./screenshots/" + (str(time.strftime('%Y-%m-%d-%H-%M'))) + ".png")
    br.set_window_size(s['width'], s['height'])
    br.quit()


# IM_KASKO
@allure.suite("Покупка оборудования в интернет-магазине А1.")
@allure.title("Покупка ТА в рассрочку на 24 месяца  + КАСКО по полной стоимости")
def test_IM_KASKO(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price = HB.buy_device_with_kasko(br, test_dude)
    HB.wait_for_order_in_work(br)
    time.sleep(20)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_kasko_full(br, test_dude, external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price)
