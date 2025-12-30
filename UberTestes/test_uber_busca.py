import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from HomePage import HomePage

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'emulator-5554'
    options.app_package = 'com.ubercab'
    options.app_activity = 'com.ubercab.presidio.app.core.root.RootActivity'

    # Mantém o login (não apaga os dados)
    options.set_capability("appium:noReset", True)

    # Permissões
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:autoAcceptAlerts", True)

    # Conecta ao servidor
    driver_appium = webdriver.Remote('http://127.0.0.1:4723', options=options)

    # --- O TRUQUE DE MESTRE ---
    # Isso garante que o app feche e abra do zero antes de cada teste
    # Assim ele volta para a Home, mas logado.
    driver_appium.terminate_app('com.ubercab')
    driver_appium.activate_app('com.ubercab')
    # --------------------------

    yield driver_appium

    driver_appium.quit()

def test_buscar_destino_com_sucesso(driver):
    # O resto continua igual, pois agora ele JÁ VAI ABRIR na Home!
    import time
    time.sleep(5)  # Só para garantir que carregou o mapa

    home = HomePage(driver)
    home.tocar_para_onde()
    home.digitar_destino("Av. Paulista, 1000")
    home.selecionar_primeira_opcao()

