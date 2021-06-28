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
    br.save_screenshot("./screenshots/"+(str(time.strftime('%Y-%m-%d-%H-%M'))) + ".png")
    br.quit()

@allure.title("Покупка оборудования по полной стоимости")
def test_Pokupka_TA_bez_sim_i_skidki(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    HB.cut_pop_up(br)
    HB.logout_site(br)
    external_id, device_price = HB.buy_full_price_device(br, test_dude, login, passw)
    HB.wait_for_order_in_work(br)
    time.sleep(20)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_full_price_device(br, test_dude, external_id, device_price)
