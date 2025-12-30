import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from HomePage import HomePage


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'SM J530G'
    options.app_package = 'com.ubercab'
    options.app_activity = 'com.ubercab.presidio.app.core.root.RootActivity'

    # Mantém o login e aceita permissões
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:autoAcceptAlerts", True)

    # --- CORREÇÃO: Conecta APENAS UMA VEZ ---
    driver_appium = webdriver.Remote('http://127.0.0.1:4723', options=options)

    # Ajusta GPS
    print("Ajustando GPS para Rua Paulista, 280 - Peixinhos (Olinda/PE)...")
    driver_appium.set_location(-8.016620, -34.872510, 10)

    # Reinicia o App para garantir estado limpo
    driver_appium.terminate_app('com.ubercab')
    driver_appium.activate_app('com.ubercab')

    yield driver_appium

    driver_appium.quit()


def test_buscar_destino_com_sucesso(driver):
    import time
    time.sleep(5)
    home = HomePage(driver)
    home.tocar_para_onde()
    home.digitar_destino("Av. Paulista, 1000")
    home.selecionar_primeira_opcao()