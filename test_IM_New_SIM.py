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

@allure.title("Покупка новой сим с подключением и оборудованием")
# IM_Accessories
def test_IM_New_SIM(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    # - перейти в тарифы
    br.get("https://www.a1.by/ru/plans/c/b2ctariffs")
    HB.cut_pop_up(br)
    external_id, rate_plan, product_price = HB.buy_new_sim(br, test_dude)
    HB.wait_for_order_in_work(br)
    time.sleep(20)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_new_sim(br, test_dude, external_id, rate_plan, product_price)
