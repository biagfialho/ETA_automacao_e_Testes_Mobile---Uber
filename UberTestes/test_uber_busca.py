import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from HomePage import HomePage

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'SM J530G' # Seu device
    options.app_package = 'com.ubercab'
    options.app_activity = 'com.ubercab.presidio.app.core.root.RootActivity'
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:autoAcceptAlerts", True)
    options.set_capability("appium:settings", {"waitForIdleTimeout": 0})
    
    driver_appium = webdriver.Remote('http://127.0.0.1:4723', options=options)
    
    # Reinicia app para estado limpo
    driver_appium.terminate_app('com.ubercab')
    driver_appium.activate_app('com.ubercab')
    time.sleep(5) # Aguarda carga inicial
    
    yield driver_appium
    driver_appium.quit()

# --- CENÁRIO 1: Buscar destino válido ---
# Dado que estou na tela inicial
# Quando eu digito um endereço válido
# Então deve exibir uma lista
def test_buscar_destino_valido_exibe_lista(driver):
    home = HomePage(driver)
    
    home.tocar_para_onde()
    home.digitar_destino("Shopping Recife") # Endereço válido
    
    # Validação (Assert)
    lista_apareceu = home.validar_lista_enderecos_apareceu()
    
    assert lista_apareceu is True, "A lista de endereços sugeridos não apareceu!"
    print("CENÁRIO 1 PASSOU: Lista exibida com sucesso.")

# --- CENÁRIO 2: Reservar destino (Agendamento) ---
# Dado que estou na tela inicial
# Quando escolho uma viagem e seleciono horário
# Então deve exibir calendário
def test_acessar_tela_agendamento(driver):
    home = HomePage(driver)
    
    # Tenta clicar no botão de "Reserve" ou "Agendar" na home
    home.tocar_botao_reserva()
    
    # Validação (Assert)
    calendario_abriu = home.validar_tela_calendario_apareceu()
    
    assert calendario_abriu is True, "O calendário/seletor de data não foi exibido!"
    print("CENÁRIO 2 PASSOU: Tela de agendamento exibida.")
    