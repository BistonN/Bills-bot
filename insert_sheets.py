import os
from datetime import date
import pygsheets
from dotenv import load_dotenv

load_dotenv()

class GerenciadorGastos:
    """
    Classe para inserir gastos no Google Sheets usando pygsheets.
    - Autoriza via service_account_file
    - Abre a planilha por URL (SPREADSHEET_URL no .env)
    - A partir do dia 26, duplica a aba do mês atual para a próxima,
      e mantém apenas as 3 primeiras linhas (com seus cálculos).
    """
    def __init__(self, entidade: dict, service_account_file: str = "./service_account.json"):
        self.entidade = entidade
        self.service_account_file = service_account_file
        self.spreadsheet_url = os.getenv("SPREADSHEET_URL")

        if not self.spreadsheet_url:
            raise ValueError("SPREADSHEET_URL não definido no .env")

        self.client = pygsheets.authorize(service_account_file=self.service_account_file)
        self.sheet = self.client.open_by_url(self.spreadsheet_url)

    @staticmethod
    def nome_aba_atual(data: date) -> str:
        meses = ["jan", "fev", "mar", "abr", "mai", "jun",
                 "jul", "ago", "set", "out", "nov", "dez"]
        return f"{meses[data.month - 1]}/{str(data.year)[2:]}"

    @staticmethod
    def proxima_aba(data: date) -> str:
        ano = data.year
        mes = data.month + 1
        if mes > 12:
            mes = 1
            ano += 1
        meses = ["jan", "fev", "mar", "abr", "mai", "jun",
                 "jul", "ago", "set", "out", "nov", "dez"]
        return f"{meses[mes - 1]}/{str(ano)[2:]}"

    def _worksheet_by_title_safe(self, title: str):
        try:
            return self.sheet.worksheet_by_title(title)
        except pygsheets.WorksheetNotFound:
            return None

    def preparar_nova_aba(self, aba_nome_atual: str, aba_nome_nova: str):
        wks_atual = self._worksheet_by_title_safe(aba_nome_atual)
        if wks_atual is None:
            nova_aba = self.sheet.add_worksheet(aba_nome_nova, rows=3, cols= wks_atual.cols if wks_atual else 20)
            return nova_aba

        nova_aba = wks_atual.duplicate(aba_nome_nova)

        if nova_aba.rows != 3:
            nova_aba.resize(rows=3)

        return nova_aba

    def inserir_gasto(self):
        hoje = date.today()
        aba_nome_atual = self.nome_aba_atual(hoje)

        if hoje.day >= 26:
            aba_nome_destino = self.proxima_aba(hoje)
            wks_destino = self._worksheet_by_title_safe(aba_nome_destino)
            if wks_destino is None:
                wks_destino = self.preparar_nova_aba(aba_nome_atual, aba_nome_destino)
        else:
            aba_nome_destino = aba_nome_atual
            wks_destino = self._worksheet_by_title_safe(aba_nome_destino)
            if wks_destino is None:
                wks_destino = self.sheet.add_worksheet(aba_nome_destino, rows=3, cols=20)

        nova_linha = [
            self.entidade.get("local"),
            self.entidade.get("valor"),
            self.entidade.get("categoria").upper(),
        ]

        wks_destino.append_table(values=nova_linha)

        print(f"Gasto inserido na aba '{aba_nome_destino}': {nova_linha}")
        return nova_linha


if __name__ == "__main__":
    entidade_exemplo = {
        "data": "19/08/2025",
        "local": "Padaria",
        "valor": 15.50,
        "categoria": "COMIDA"
    }

    gestor = GerenciadorGastos(entidade_exemplo, service_account_file="./service_account.json")
    gestor.inserir_gasto()
