import time
import pytest
from src import hybris_operations as HB, ma_dudes as dudes
import allure

test_dude = dudes.Private_dude
vix_creds = dudes.VIX_credentials
wso = dudes.WSO_prod
login = test_dude.login
passw = test_dude.password
UNN = test_dude.TRN
company_name = test_dude.company_name
contact_person = test_dude.contact_person
contact_phone = test_dude.contact_phone
email = test_dude.email
city = test_dude.city
street = test_dude.street
house = test_dude.house
building = test_dude.building
appartment = test_dude.appartment



#fixture
@pytest.fixture
def br():
    site = 'https://corporate.a1.by/shop/'
    br = HB.open_browser(site)
    yield br
    br.save_screenshot("./screenshots/"+(str(time.strftime('%Y-%m-%d-%H-%M'))) + ".png")
    br.quit()

@allure.title("Покупка оборудования со скидкой клиентом Юридическим лицом")
def test_buy_TA_legal(br):
    HB.check_cart_legal(br)
    device_price, external_id = HB.buy_for_legal(br, test_dude)
    time.sleep(60)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_legal(br, test_dude, device_price, external_id)