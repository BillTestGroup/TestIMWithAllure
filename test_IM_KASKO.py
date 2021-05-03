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
    br.save_screenshot("./screenshots/"+(str(time.strftime('%Y-%m-%d-%H-%M'))) + ".png")
    br.quit()


# IM_KASKO
@allure.title("Оформление покупки оборудования вместе с Каско")
def test_IM_KASKO(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price = HB.buy_device_with_kasko(br, test_dude)
    HB.wait_for_order_in_work(br)
    time.sleep(20)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_kasko_full(br, test_dude, external_id, device_price, phone_monthly_payment, phone_full_price, kasko_full_price)
