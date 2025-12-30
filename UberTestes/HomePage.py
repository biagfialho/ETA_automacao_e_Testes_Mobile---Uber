from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        # Aumentei para 30s só por segurança neste início, pois o emulador pode ser lento
        self.wait = WebDriverWait(self.driver, 30)

    # --- Locators ---

    # CORREÇÃO PRINCIPAL: Usamos XPATH para encontrar o texto "Para onde?"
    # O * significa "qualquer elemento" (botão, texto, input) que tenha esse texto.
    _BOTAO_PARA_ONDE = (AppiumBy.XPATH, "//*[contains(@text, 'Pesquisar') or contains(@content-desc, 'Pesquisar')]")

    # Na segunda tela, geralmente o primeiro EditText é o de destino
    _CAMPO_ENDERECO = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    # Tenta pegar o primeiro resultado da lista (ajustado para ser mais genérico)
    _PRIMEIRO_RESULTADO = (AppiumBy.XPATH, "(//android.widget.TextView)[1]")

    # --- Ações ---

    def tocar_para_onde(self):
        print("Tentando encontrar o botão 'PESQUISAR'...")
        self.wait.until(EC.visibility_of_element_located(self._BOTAO_PARA_ONDE)).click()

    def digitar_destino(self, endereco):
        print(f"Digitando endereço: {endereco}...")
        # Aqui usamos element_to_be_clickable que as vezes é melhor para campos de texto
        campo = self.wait.until(EC.element_to_be_clickable(self._CAMPO_ENDERECO))
        campo.click()  # Garante o foco
        campo.send_keys(endereco)

    def selecionar_primeira_opcao(self):
        print("Selecionando primeira opção...")
        self.wait.until(EC.element_to_be_clickable(self._PRIMEIRO_RESULTADO)).click()