import time
import pytest
from src import hybris_operations as HB, ma_dudes as dudes
import allure

test_dude = dudes.Private_dude
vix_creds = dudes.VIX_credentials
wso = dudes.WSO_prod
login = test_dude.login
passw = test_dude.password
dateOfBirth = test_dude.dateOfBirth
serialPasport = test_dude.serialPasport
numberPassport = test_dude.numberPassport
identifirePassport = test_dude.identifirePassport
dateOfIssue = test_dude.dateOfIssue
whoGivePassport = test_dude.whoGivePassport
phoneNumber = test_dude.phoneNumber
city = test_dude.city
street = test_dude.street
house = test_dude.house
building = test_dude.building
appartment = test_dude.appartment


#fixture
@pytest.fixture
def br():
    site = 'https://www.a1.by/ru/'
    br = HB.open_browser(site)
    yield br
    br.save_screenshot("./screenshots/"+(str(time.strftime('%Y-%m-%d-%H-%M'))) + ".png")
    br.quit()

@allure.title("Покупка оборудования в рассрочку новым клиентом")
def test_pokupka_TA_s_novoy_SIM(br):
    HB.check_cart(br)
    device_price, monthly_payment, full_price = HB.buy_ta_s_novoy_sim(br, test_dude)
    time.sleep(80)
    HB.log_in_wso(br, wso, vix_creds)
    HB.check_wso_installment_for_new(br, test_dude, device_price, monthly_payment, full_price)