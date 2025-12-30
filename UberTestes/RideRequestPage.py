from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class RideRequestPage:
    def __init__(self, driver):
        self.driver = driver
        # Paciência de 30 segundos, pois calcular rota demora
        self.wait = WebDriverWait(self.driver, 30)

    # --- Localizadores ---

    # Busca UberX pelo nome (Texto ou Descrição)
    _OPCAO_UBER_X = (AppiumBy.XPATH, "//*[contains(@text, 'UberX') or contains(@content-desc, 'UberX')]")

    # SELEÇÃO GENÉRICA MELHORADA: Procura 'R$' no texto OU na descrição (content-desc)
    _QUALQUER_CARRO = (AppiumBy.XPATH, "(//*[contains(@text, 'R$') or contains(@content-desc, 'R$')])[1]")

    # Botão de Confirmar Corrida
    _BOTAO_CONFIRMAR = (AppiumBy.XPATH, "//*[contains(@text, 'Confirmar') or contains(@content-desc, 'Confirmar')]")

    # Botão Intermediário (Confirmar local de partida antes de ver carros)
    _CONFIRMAR_LOCAL_PARTIDA = (AppiumBy.XPATH,
                                "//*[contains(@text, 'Confirmar local') or contains(@text, 'Confirmar partida')]")

    # Botão do Pino (Aparece depois de confirmar o carro)
    _CONFIRMAR_PINO = (AppiumBy.XPATH,
                       "//*[contains(@text, 'Confirmar local') or contains(@text, 'Confirmar partida')]")

    # --- Ações ---

    def selecionar_uber_x(self):
        print("Verificando se precisa confirmar local de partida antes...")
        try:
            # Espera rápida de 5s para ver se apareceu "Confirmar local"
            wait_curto = WebDriverWait(self.driver, 5)
            wait_curto.until(EC.element_to_be_clickable(self._CONFIRMAR_LOCAL_PARTIDA)).click()
            print("Confirmei o local de partida. Agora esperando os carros...")
        except TimeoutException:
            print("Não precisou confirmar partida. Seguindo para carros.")

        print("Aguardando opções de carro aparecerem...")
        try:
            # Tenta achar o UberX especificamente
            self.wait.until(EC.element_to_be_clickable(self._OPCAO_UBER_X)).click()
            print("Selecionei o UberX!")
        except TimeoutException:
            print("Não achei 'UberX' pelo nome. Tentando clicar na primeira opção com preço (R$)...")
            # Clica no primeiro preço que aparecer
            self.wait.until(EC.element_to_be_clickable(self._QUALQUER_CARRO)).click()
            print("Selecionei a primeira opção da lista.")

    def confirmar_solicitacao(self):
        print("Tentando confirmar a corrida...")
        time.sleep(2)  # Pequena pausa para animação

        # 1. Clica no botão principal "Confirmar UberX"
        self.wait.until(EC.element_to_be_clickable(self._BOTAO_CONFIRMAR)).click()

        # 2. Verifica se apareceu o pino de confirmação no mapa (comum em endereços novos)
        try:
            espera_curta = WebDriverWait(self.driver, 5)
            espera_curta.until(EC.element_to_be_clickable(self._CONFIRMAR_PINO)).click()
            print("Confirmei o pino no mapa.")
        except TimeoutException:
            print("Nenhuma confirmação de pino extra foi necessária.")

    # --- Validações ---

    def verificar_status_buscando(self):
        _MSG_BUSCANDO = (AppiumBy.XPATH, "//*[contains(@text, 'Procurando') or contains(@text, 'Conectando')]")
        try:
            return self.wait.until(EC.visibility_of_element_located(_MSG_BUSCANDO)).is_displayed()
        except TimeoutException:
            return False

    def verificar_mensagem_indisponibilidade(self):
        _MSG_SEM_CARRO = (AppiumBy.XPATH, "//*[contains(@text, 'indisponível') or contains(@text, 'Ocupado')]")
        try:
            return self.wait.until(EC.visibility_of_element_located(_MSG_SEM_CARRO)).is_displayed()
        except TimeoutException:
            return False