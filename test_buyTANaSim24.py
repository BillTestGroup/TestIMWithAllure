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

@allure.title("Покупка телефона клиентом ФЛ в рассрочку на 24 месяца")
def test_buyTANaSim24(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    HB.cut_pop_up(br)
    installment_price = HB.buyTANaSim24(br, test_dude)
    HB.wait_for_order_in_work(br)
    time.sleep(20)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_installment(br, test_dude, installment_price)