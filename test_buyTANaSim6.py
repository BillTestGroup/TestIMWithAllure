import time
import pytest
from src import hybris_operations as HB, ma_dudes as dudes
import allure

test_dude = dudes.Private_dude
vix_creds = dudes.VIX_credentials
wso = dudes.WSO_prod
login = test_dude.login
passw = test_dude.password

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

@allure.title("Покупка телефона клиентом ФЛ в рассрочку на 6 месяцев")
def test_buyTANaSimSix(br):
    HB.login_site(br, login, passw)
    HB.check_cart(br)
    HB.cut_pop_up(br)
    external_id, device_price, monthly_payment, full_price = HB.buyTANaSimSix(br, test_dude)
    HB.wait_for_order_in_work(br)
    time.sleep(30)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_installment(br, test_dude, external_id, device_price, monthly_payment, full_price)


