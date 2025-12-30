import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options

from HomePage import HomePage
from RideRequestPage import RideRequestPage


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'SM J530G'
    options.app_package = 'com.ubercab'
    options.app_activity = 'com.ubercab.presidio.app.core.root.RootActivity'

    # --- CORREÇÃO DO ERRO DE TIMEOUT ---
    # 1. enforceXPath1: Usa um método alternativo para achar elementos (recomendado pelo erro)
    # 2. waitForIdleTimeout: 0 diz para o Appium NÃO esperar o app parar de carregar (mapas/animações)
    options.set_capability("appium:settings", {
        "enforceXPath1": True,
        "waitForIdleTimeout": 0
    })
    # -----------------------------------

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:autoAcceptAlerts", True)

    # Aumentando timeouts de conexão
    options.set_capability("appium:uiautomator2ServerInstallTimeout", 60000)
    options.set_capability("appium:adbExecTimeout", 60000)
    options.set_capability("appium:newCommandTimeout", 300)

    driver_appium = webdriver.Remote('http://127.0.0.1:4723', options=options)

    # Ajusta GPS
    print("Ajustando GPS para Rua Paulista, 280 - Peixinhos (Olinda/PE)...")
    driver_appium.set_location(-8.016620, -34.872510, 10)

    # Reinicia o app para garantir estado limpo
    driver_appium.terminate_app('com.ubercab')
    driver_appium.activate_app('com.ubercab')

    yield driver_appium
    driver_appium.quit()


def test_solicitar_corrida_com_sucesso(driver):
    home = HomePage(driver)

    # Aumentei um pouco o tempo inicial para o mapa carregar antes de tentar clicar
    print("Aguardando mapa carregar (8s)...")
    time.sleep(8)

    print("Iniciando busca de destino...")
    home.tocar_para_onde()

    home.digitar_destino("Rua Paulista, 280")

    home.selecionar_primeira_opcao()

    ride_page = RideRequestPage(driver)
    ride_page.selecionar_uber_x()
    ride_page.confirmar_solicitacao()

    sucesso = ride_page.verificar_status_buscando()

    if sucesso:
        print("SUCESSO: O app está procurando motorista!")
        assert True
    else:
        indisponivel = ride_page.verificar_mensagem_indisponibilidade()
        if indisponivel:
            print("SUCESSO (Cenário 2): Sem motoristas disponíveis.")
        else:
            pytest.fail("FALHA: O teste não conseguiu confirmar a corrida.")