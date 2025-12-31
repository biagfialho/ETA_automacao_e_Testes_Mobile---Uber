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
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:autoAcceptAlerts", True)
    options.set_capability("appium:settings", {"enforceXPath1": True, "waitForIdleTimeout": 0})
    
    driver_appium = webdriver.Remote('http://127.0.0.1:4723', options=options)
    
    # Set Location para uma área que sabemos que funciona (ou não)
    driver_appium.set_location(-8.016620, -34.872510, 10) # Olinda
    
    driver_appium.terminate_app('com.ubercab')
    driver_appium.activate_app('com.ubercab')
    time.sleep(7)
    
    yield driver_appium
    driver_appium.quit()

def test_fluxo_solicitacao_corrida(driver):
    """
    Cobre Funcionalidade 2:
    - Cenário 1: Solicitar com sucesso (Verifica mensagem 'Procurando')
    - Cenário 2: Falha ao solicitar (Verifica mensagem 'Indisponível')
    """
    home = HomePage(driver)
    ride_page = RideRequestPage(driver)

    # 1. Faz a busca (Pré-requisito)
    home.tocar_para_onde()
    home.digitar_destino("Rua da Aurora, Recife")
    home.selecionar_primeira_opcao()

    # 2. Tenta selecionar UberX
    ride_page.selecionar_uber_x()
    
    # 3. Confirma
    ride_page.confirmar_solicitacao()

    # --- VALIDAÇÕES DOS CENÁRIOS ---
    
    # Verifica Cenário 1: Sucesso
    esta_buscando = ride_page.verificar_status_buscando()
    
    # Verifica Cenário 2: Indisponibilidade
    esta_indisponivel = ride_page.verificar_mensagem_indisponibilidade()

    if esta_buscando:
        print("CENÁRIO 1 PASSOU: Corrida solicitada, app está procurando motorista.")
        assert True
    elif esta_indisponivel:
        print("CENÁRIO 2 PASSOU: Não há motoristas, app informou indisponibilidade corretamente.")
        assert True
    else:
        # Se não apareceu nem "Procurando" nem "Indisponível", o teste falhou
        pytest.fail("ERRO: O app não entrou em estado de busca nem mostrou erro de indisponibilidade.")