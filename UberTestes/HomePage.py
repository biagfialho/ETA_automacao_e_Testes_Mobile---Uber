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

    # Procura por campos de texto (EditText). O índice 0 é Partida, o 1 é Destino.
    _CAMPO_DIGITAR = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    # Botão que aparece na lista sugerindo "Minha localização"
    _OPCAO_MINHA_LOCALIZACAO = (AppiumBy.XPATH,
                                "//*[@text='Minha localização' or contains(@text, 'Localização atual')]")

    # --- Ações ---

    def tocar_para_onde(self):
        print("Tentando encontrar o botão 'Para onde'...")
        try:
            elem = self.wait.until(EC.element_to_be_clickable(self._CAMPO_PARA_ONDE))
            elem.click()
        except:
            print("Botão não encontrado pelo texto, clicando no centro...")
            self.clicar_coordenada_relativa(0.5, 0.4)

    def digitar_destino(self, endereco):
        # Espera aparecerem os campos de texto (Partida e Destino)
        campos = self.wait.until(EC.visibility_of_all_elements_located(self._CAMPO_DIGITAR))

        # --- PASSO 1: CONFIGURAR PARTIDA (Primeiro Campo) ---
        if len(campos) >= 1:
            print("Configurando partida para 'Minha localização'...")
            campo_partida = campos[0]
            campo_partida.click()
            time.sleep(2)

            try:
                # Tenta clicar na opção "Minha localização" na lista
                gps_btn = self.wait.until(EC.element_to_be_clickable(self._OPCAO_MINHA_LOCALIZACAO))
                gps_btn.click()
                print("Partida definida como GPS atual.")
            except:
                print("Não apareceu a opção 'Minha localização' (pode já estar selecionada).")

            time.sleep(2)
            # Atualiza a lista de campos, pois a tela pode ter mudado
            campos = self.wait.until(EC.visibility_of_all_elements_located(self._CAMPO_DIGITAR))

        # --- PASSO 2: CONFIGURAR DESTINO (Segundo Campo) ---
        print(f"Digitando destino: {endereco}...")
        # Pega o último campo disponível (garante que é o de destino)
        campo_destino = campos[-1]
        campo_destino.click()

        # Limpa se tiver texto anterior (exceto se for o placeholder)
        if campo_destino.text and "Para onde" not in campo_destino.text:
            campo_destino.clear()

        campo_destino.send_keys(endereco)

        try:
            self.driver.hide_keyboard()
        except:
            pass
        time.sleep(3)

    def selecionar_primeira_opcao(self):
        print("Selecionando primeira opção...")
        # Tenta clicar no resultado da busca
        try:
            xpath_resultado = "//android.widget.TextView[contains(@text, 'Paulista') or contains(@text, 'Peixinhos')]"
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath_resultado))).click()
            return
        except:
            print("Não achei pelo texto, tentando coordenada...")

        # Coordenada fixa (Plano B)
        self.clicar_coordenada_relativa(0.5, 0.35)

    def clicar_coordenada_relativa(self, x_ratio, y_ratio):
        size = self.driver.get_window_size()
        x = int(size['width'] * x_ratio)
        y = int(size['height'] * y_ratio)
        self.driver.tap([(x, y)])