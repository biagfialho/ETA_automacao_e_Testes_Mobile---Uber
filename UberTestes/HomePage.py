from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    # --- Localizadores ---
    _CAMPO_PARA_ONDE = (AppiumBy.XPATH, "//*[@text='Para onde?' or @content-desc='Para onde?']")
    _CAMPO_DIGITAR = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    _OPCAO_MINHA_LOCALIZACAO = (AppiumBy.XPATH, "//*[@text='Minha localização' or contains(@text, 'Localização atual')]")
    
    # NOVOS LOCALIZADORES (Cenário 1 e 2)
    _LISTA_RESULTADOS = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Rua') or contains(@text, 'Av')]")
    # O botão de reserva costuma ser "Reserve" ou um ícone de relógio/calendário
    _BOTAO_RESERVA = (AppiumBy.XPATH, "//*[contains(@text, 'Reserve') or contains(@content-desc, 'Reserve') or contains(@text, 'Agendar')]")
    _MODAL_DATA_HORA = (AppiumBy.XPATH, "//*[contains(@text, 'Agendar') or contains(@text, 'Escolha') or android.widget.DatePicker]")

    # --- Ações ---

    def tocar_para_onde(self):
        print("Clicando em 'Para onde'...")
        try:
            elem = self.wait.until(EC.element_to_be_clickable(self._CAMPO_PARA_ONDE))
            elem.click()
        except:
            print("Botão texto não achado, tentando coordenada...")
            self.clicar_coordenada_relativa(0.5, 0.4)

    def digitar_destino(self, endereco):
        campos = self.wait.until(EC.visibility_of_all_elements_located(self._CAMPO_DIGITAR))
        
        # Configura Partida (Opcional, mas bom manter)
        if len(campos) >= 1:
            try:
                campos[0].click()
                gps_btn = self.wait.until(EC.element_to_be_clickable(self._OPCAO_MINHA_LOCALIZACAO))
                gps_btn.click()
                time.sleep(2)
                campos = self.wait.until(EC.visibility_of_all_elements_located(self._CAMPO_DIGITAR))
            except:
                pass 

        # Configura Destino
        print(f"Digitando destino: {endereco}...")
        campo_destino = campos[-1]
        campo_destino.click()
        if campo_destino.text and "Para onde" not in campo_destino.text:
            campo_destino.clear()
        campo_destino.send_keys(endereco)
        try:
            self.driver.hide_keyboard()
        except:
            pass

    # --- NOVO MÉTODO PARA O CENÁRIO 1 (Validar Busca) ---
    def validar_lista_enderecos_apareceu(self):
        print("Validando se a lista de endereços apareceu...")
        try:
            self.wait.until(EC.visibility_of_element_located(self._LISTA_RESULTADOS))
            return True
        except:
            return False

    def selecionar_primeira_opcao(self):
        print("Selecionando primeira opção...")
        try:
            self.wait.until(EC.element_to_be_clickable(self._LISTA_RESULTADOS)).click()
        except:
            self.clicar_coordenada_relativa(0.5, 0.35)

    # --- NOVOS MÉTODOS PARA O CENÁRIO 2 (Agendamento) ---
    def tocar_botao_reserva(self):
        print("Tentando clicar no botão de Agendar/Reserve...")
        self.wait.until(EC.element_to_be_clickable(self._BOTAO_RESERVA)).click()

    def validar_tela_calendario_apareceu(self):
        print("Verificando se o calendário abriu...")
        try:
            self.wait.until(EC.visibility_of_element_located(self._MODAL_DATA_HORA))
            return True
        except:
            return False

    def clicar_coordenada_relativa(self, x_ratio, y_ratio):
        size = self.driver.get_window_size()
        x = int(size['width'] * x_ratio)
        y = int(size['height'] * y_ratio)
        self.driver.tap([(x, y)])
        