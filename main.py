from src.jpk.jpk_v7m_2_v1_0 import (
    jpk_v7m,
    jpk_v7m_declaration_data,
    jpk_v7m_sale_data, jpk_v7m_purchase_data
)

def main():
    declaration = jpk_v7m_declaration_data()
    # nadwyzka z poprzedniej deklaracji
    declaration.P_39 = 12
    # oczekiwany zwrot z US
    declaration.P_54 = 10

    sales = [jpk_v7m_sale_data()]
    sales[0].KodKrajuNadaniaTIN = "CH"
    sales[0].NrKontrahenta = "CHE347337122"
    sales[0].NazwaKontrahenta = "Matix Inh.Koval Ginter"
    sales[0].DowodSprzedazy = "2307/0135"
    sales[0].DataSprzedazy = "2023-07-14"
    sales[0].DataWystawienia = "2023-07-19"
    sales[0].GTU_12 = 1
    sales[0].K_11 = 1050.00

    purchases = [jpk_v7m_purchase_data()]
    purchases[0].KodKrajuNadaniaTIN = "PL"
    purchases[0].NrDostawcy = "1111111111"
    purchases[0].NazwaDostawcy = "testerek sp. z o.o."
    purchases[0].DowodZakupu = "test_FV48/295/3322"
    purchases[0].DataZakupu = "2023-07-31"
    purchases[0].K_42 = 100.00
    purchases[0].K_43 = 23.00

    with jpk_v7m("jpk.xml", declaration=declaration, sales=sales, purchases=purchases) as jpk:

        jpk.set_header(
            fiscal_year=2023,
            fiscal_month=7,
            tax_office_identifier=1412,
            statement_type=1
        )

        jpk.set_subject_natural_person(
            tax_id="2222222222",
            firstname="Testiusz",
            surname="Testoliński",
            birthdate="1970-01-01",
            email="testiusz@example.com"
        )

if __name__ == '__main__':
    main()
