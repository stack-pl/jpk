
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass
class jpk_v7m_declaration_data:
    '''JPK_V7M(2)_v1-0 declaration section'''
    P_10 = 0
    P_11 = 0
    P_12 = 0
    P_13 = 0
    P_14 = 0
    P_15 = 0
    P_16 = 0
    P_17 = 0
    P_18 = 0
    P_19 = 0
    P_20 = 0
    P_21 = 0
    P_22 = 0
    P_23 = 0
    P_24 = 0
    P_25 = 0
    P_26 = 0
    P_27 = 0
    P_28 = 0
    P_29 = 0
    P_30 = 0
    P_31 = 0
    P_32 = 0
    P_33 = 0
    P_34 = 0
    P_35 = 0
    P_36 = 0
    P_37 = 0
    P_38 = 0
    P_39 = 0
    P_40 = 0
    P_41 = 0
    P_42 = 0
    P_43 = 0
    P_44 = 0
    P_45 = 0
    P_46 = 0
    P_47 = 0
    P_48 = 0
    P_49 = 0
    P_50 = 0
    P_51 = 0
    P_52 = 0
    P_53 = 0
    P_54 = 0
    P_540 = 0
    P_55 = 0
    P_56 = 0
    P_560 = 0
    P_57 = 0
    P_58 = 0
    P_59 = 0
    P_60 = 0
    P_61 = ""
    P_62 = 0
    P_63 = 0
    P_64 = 0
    P_65 = 0
    P_66 = 0
    P_660 = 0
    P_67 = 0
    P_68 = 0
    P_69 = 0
    P_ORDZU = ""


class jpk_v7m_sale_data:
    '''JPK_V7M(2)_v1-0 single sale section'''
    KodKrajuNadaniaTIN = ""
    NrKontrahenta = ""
    NazwaKontrahenta = ""
    DowodSprzedazy = ""    
    DataWystawienia = ""   
    DataSprzedazy = ""
    TypDokumentu = ""
    GTU_01 = 0
    GTU_02 = 0
    GTU_03 = 0
    GTU_04 = 0
    GTU_05 = 0
    GTU_06 = 0
    GTU_07 = 0
    GTU_08 = 0
    GTU_09 = 0
    GTU_10 = 0
    GTU_11 = 0
    GTU_12 = 0
    GTU_13 = 0
    WSTO_EE = 0
    IED = 0
    TP = 0
    TT_WNT = 0
    TT_D = 0
    MR_T = 0
    MR_UZ = 0
    I_42 = 0
    I_63 = 0
    B_SPV = 0
    B_SPV_DOSTAWA = 0
    B_MPV_PROWIZJA = 0
    KorektaPodstawyOpodt = ""
    TerminPlatnosci = ""
    DataZaplaty = ""
    K_10 = 0.0
    K_11 = 0.0
    K_12 = 0.0
    K_13 = 0.0
    K_14 = 0.0
    K_15 = 0.0
    K_16 = 0.0
    K_17 = 0.0
    K_18 = 0.0
    K_19 = 0.0
    K_20 = 0.0
    K_21 = 0.0
    K_22 = 0.0
    K_23 = 0.0
    K_24 = 0.0
    K_25 = 0.0
    K_26 = 0.0
    K_27 = 0.0
    K_28 = 0.0
    K_29 = 0.0
    K_30 = 0.0
    K_31 = 0.0
    K_32 = 0.0
    K_33 = 0.0
    K_34 = 0.0
    K_35 = 0.0
    K_36 = 0.0
    SprzedazVAT_Marza = 0


@dataclass
class jpk_v7m_purchase_data:
    '''JPK_V7M(2)_v1-0 single purchase section'''
    KodKrajuNadaniaTIN = ""
    NrDostawcy = "BRAK"
    NazwaDostawcy = "BRAK"  
    DowodZakupu = ""
    DataZakupu = ""
    DataWplywu = ""
    DokumentZakupu = ""
    IMP = 0
    K_40 = 0.0
    K_41 = 0.0
    K_42 = 0.0
    K_43 = 0.0
    K_44 = 0.0
    K_45 = 0.0
    K_46 = 0.0
    K_47 = 0.0
    ZakupVAT_Marza = 0


def xml_field(dataclass, value_name, ommit_if_equal=None):
    value = dataclass.__getattribute__(value_name)
    if value == ommit_if_equal or value == None:
        return ""
    if isinstance(value, float):
        return f'      <{value_name}>{value:.02f}</{value_name}>\n'
    else:
        return f'      <{value_name}>{value}</{value_name}>\n'


class jpk_v7m:
    '''JPK_V7M(2)_v1-0 file creator (context manager)'''

    def __init__(self,
                 file_name: str,
                 declaration: jpk_v7m_declaration_data,
                 sales: Iterable[jpk_v7m_sale_data] = [],
                 purchases: Iterable[jpk_v7m_purchase_data] = []
        ):
        self.file_name = file_name
        self.declaration = declaration
        self.sales = sales
        self.purchases = purchases
        self.header_fiscal_year = 0
        self.header_fiscal_month = 0
        self.header_tax_office_identifier = 0

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()        

    def set_header(self, *, fiscal_year, fiscal_month, tax_office_identifier, statement_type=1):
        self.header_fiscal_year = fiscal_year
        self.header_fiscal_month = fiscal_month
        self.header_tax_office_identifier = tax_office_identifier
        self.header_statement_type = statement_type

    def _set_subject(self, *, tax_id, email, telephone):
        self.subject_tax_id = tax_id
        self.subject_email = email
        self.subject_telephone = telephone

    def set_subject_natural_person(self, *, tax_id, firstname, surname, birthdate, email, telephone=None):
        self._set_subject(tax_id=tax_id, email=email, telephone=telephone)        
        self.subject_natural_person_firstname = firstname
        self.subject_natural_person_surname = surname
        self.subject_natural_person_birthdate = birthdate
        self._subject_xml_gen = self._subject_xml_gen_natural_person
    
    def set_subject_legal_person(self, *, tax_id, fullname, email, telephone):
        self._set_subject(tax_id=tax_id, email=email, telephone=telephone)        
        self.subject_legal_person_fullname = fullname
        self._subject_xml_gen = self._subject_xml_gen_legal_person

    def begin(self):
        self.file = open(self.file_name, "tw")

    def end(self):
        self.file.writelines(self.content_gen())
        self.file.close()

    def content_gen(self):
        yield '<?xml version="1.0" encoding="UTF-8"?>\n'
        yield '<JPK xmlns:etd="http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2021/06/08/eD/DefinicjeTypy/" '
        yield 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        yield 'xmlns="http://crd.gov.pl/wzor/2021/12/27/11148/">\n'
        yield from self._header_xml_gen()
        yield from self._subject_xml_gen()
        yield from self._declaration_xml_gen()
        yield from self._evidence_xml_gen()
        yield '</JPK>'

    def _header_xml_gen(self):
        yield f'  <Naglowek>\n'
        yield f'    <KodFormularza kodSystemowy="JPK_V7M (2)" wersjaSchemy="1-0E">JPK_VAT</KodFormularza>\n'
        yield f'    <WariantFormularza>2</WariantFormularza>\n'
        yield f'    <DataWytworzeniaJPK>{datetime.utcnow().isoformat()}Z</DataWytworzeniaJPK>\n'
        yield f'    <NazwaSystemu>Python jpk Library</NazwaSystemu>\n'
        yield f'    <CelZlozenia poz="P_7">{int(self.header_statement_type)}</CelZlozenia>\n'
        yield f'    <KodUrzedu>{self.header_tax_office_identifier}</KodUrzedu>\n'
        yield f'    <Rok>{self.header_fiscal_year}</Rok>\n'
        yield f'    <Miesiac>{self.header_fiscal_month}</Miesiac>\n'
        yield f'  </Naglowek>\n'

    def _subject_xml_gen_natural_person(self):
        yield f'  <Podmiot1 rola="Podatnik">\n'
        yield f'    <OsobaFizyczna>\n'
        yield f'      <etd:NIP>{self.subject_tax_id}</etd:NIP>\n'
        yield f'      <etd:ImiePierwsze>{self.subject_natural_person_firstname}</etd:ImiePierwsze>\n'
        yield f'      <etd:Nazwisko>{self.subject_natural_person_surname}</etd:Nazwisko>\n'
        yield f'      <etd:DataUrodzenia>{self.subject_natural_person_birthdate}</etd:DataUrodzenia>\n'
        yield f'      <Email>{self.subject_email}</Email>\n'
        if self.subject_telephone:
            yield f'      <Telefon>{self.subject_telephone}</Telefon>\n'
        yield f'    </OsobaFizyczna>\n'
        yield f'  </Podmiot1>\n'

    def _subject_xml_gen_legal_person(self):
        yield f'  <Podmiot1 rola="Podatnik">\n'
        yield f'    <OsobaNiefizyczna>\n'
        yield f'      <etd:NIP>{self.subject_tax_id}</etd:NIP>\n'
        yield f'      <etd:PelnaNazwa>{self.subject_legal_person_fullname}</etd:PelnaNazwa>\n'
        yield f'      <Email>{self.subject_email}</Email>\n'
        if self.subject_telephone:
            yield f'      <Telefon>{self.subject_telephone}</Telefon>\n'
        yield f'    </OsobaNiefizyczna>\n'
        yield f'  </Podmiot1>\n'

    def sum_key_in_sales(self, key) -> str:
        return self._sum_key_values(key, self.sales)
    
    def sum_key_in_purchases(self, key) -> str:
        return self._sum_key_values(key, self.purchases)

    def _sum_key_values(self, key, list_of_transactions):
        result = 0.0
        for transaction in list_of_transactions:
            result += transaction.get(key, 0.0)
        return f'{result:.02}'

    def calc_declaration(self):
        """
        Calc and overwrite declaration fields
        """
        self.declaration.P_10 = round(sum(sale.K_10 for sale in self.sales))
        self.declaration.P_11 = round(sum(sale.K_11 for sale in self.sales))
        self.declaration.P_12 = round(sum(sale.K_12 for sale in self.sales))
        self.declaration.P_13 = round(sum(sale.K_13 for sale in self.sales))
        self.declaration.P_14 = round(sum(sale.K_14 for sale in self.sales))
        self.declaration.P_15 = round(sum(sale.K_15 for sale in self.sales))
        self.declaration.P_16 = round(sum(sale.K_16 for sale in self.sales))
        self.declaration.P_17 = round(sum(sale.K_17 for sale in self.sales))
        self.declaration.P_18 = round(sum(sale.K_18 for sale in self.sales))
        self.declaration.P_19 = round(sum(sale.K_19 for sale in self.sales))
        self.declaration.P_20 = round(sum(sale.K_20 for sale in self.sales))
        self.declaration.P_21 = round(sum(sale.K_21 for sale in self.sales))
        self.declaration.P_22 = round(sum(sale.K_22 for sale in self.sales))
        self.declaration.P_23 = round(sum(sale.K_23 for sale in self.sales))
        self.declaration.P_24 = round(sum(sale.K_24 for sale in self.sales))
        self.declaration.P_25 = round(sum(sale.K_25 for sale in self.sales))
        self.declaration.P_26 = round(sum(sale.K_26 for sale in self.sales))
        self.declaration.P_27 = round(sum(sale.K_27 for sale in self.sales))
        self.declaration.P_28 = round(sum(sale.K_28 for sale in self.sales))
        self.declaration.P_29 = round(sum(sale.K_29 for sale in self.sales))
        self.declaration.P_30 = round(sum(sale.K_30 for sale in self.sales))
        self.declaration.P_31 = round(sum(sale.K_31 for sale in self.sales))
        self.declaration.P_32 = round(sum(sale.K_32 for sale in self.sales))
        self.declaration.P_33 = round(sum(sale.K_33 for sale in self.sales))
        self.declaration.P_34 = round(sum(sale.K_34 for sale in self.sales))
        self.declaration.P_35 = round(sum(sale.K_35 for sale in self.sales))
        self.declaration.P_36 = round(sum(sale.K_36 for sale in self.sales))
        self.declaration.P_37 = (
            self.declaration.P_10 + self.declaration.P_11 +
            self.declaration.P_13 + self.declaration.P_15 + 
            self.declaration.P_17 + self.declaration.P_19 + 
            self.declaration.P_21 + self.declaration.P_22 + 
            self.declaration.P_23 + self.declaration.P_25 + 
            self.declaration.P_27 + self.declaration.P_29 +
            self.declaration.P_31
        )
        self.declaration.P_38 = (
            self.declaration.P_16 + self.declaration.P_18 +
            self.declaration.P_20 + self.declaration.P_24 + 
            self.declaration.P_26 + self.declaration.P_28 +
            self.declaration.P_30 + self.declaration.P_32 + 
            self.declaration.P_33 + self.declaration.P_34 -
            self.declaration.P_35 - self.declaration.P_36
        )
        # self.declaration.P_39 field remains unchanged
        self.declaration.P_40 = round(sum(purchase.K_40 for purchase in self.purchases))
        self.declaration.P_41 = round(sum(purchase.K_41 for purchase in self.purchases))
        self.declaration.P_42 = round(sum(purchase.K_42 for purchase in self.purchases))
        self.declaration.P_43= round(sum(purchase.K_43 for purchase in self.purchases))
        self.declaration.P_44 = round(sum(purchase.K_44 for purchase in self.purchases))
        self.declaration.P_45 = round(sum(purchase.K_45 for purchase in self.purchases))
        for purchase in self.purchases:
            if purchase.K_46 > 0.0:
                raise ValueError('"in minus" value is required here')
        self.declaration.P_46 = round(sum(purchase.K_46 for purchase in self.purchases))
        for purchase in self.purchases:
            if purchase.K_47 < 0.0:
                raise ValueError('"in plus" value is required here')
        self.declaration.P_47 = round(sum(purchase.K_47 for purchase in self.purchases))
        self.declaration.P_48 = (
            self.declaration.P_39 + self.declaration.P_41 + 
            self.declaration.P_43 + self.declaration.P_44 + 
            self.declaration.P_45 + self.declaration.P_46 +
            self.declaration.P_47
        )
        if self.declaration.P_48 - self.declaration.P_38 >= 0:
            self.declaration.P_53 = (
                self.declaration.P_48 - self.declaration.P_38 +
                self.declaration.P_52
            )
        else:
            self.declaration.P_51 = self.declaration.P_38 - self.declaration.P_48

        if self.declaration.P_53 > 0.0:
            self.declaration.P_62 = self.declaration.P_53 - self.declaration.P_54


    def _decl(self, value_name, empty_if_equal=None):
        value = self.declaration.__getattribute__(value_name)
        if value == empty_if_equal:
            value = ""
        if isinstance(value, float):
            return f'<{value_name}>{int(value)}</{value_name}>'
        else:
            return f'<{value_name}>{value}</{value_name}>'

    def _declaration_xml_gen(self):
        # compute all data before fill this section
        self.calc_declaration()
        decl = self.declaration

        yield f'  <Deklaracja>\n'
        yield f'    <Naglowek>\n'
        yield f'      <KodFormularzaDekl kodSystemowy="VAT-7 (22)" kodPodatku="VAT" rodzajZobowiazania="Z" wersjaSchemy="1-0E">VAT-7</KodFormularzaDekl>\n'
        yield f'      <WariantFormularzaDekl>22</WariantFormularzaDekl>\n'
        yield f'    </Naglowek>\n'
        yield f'    <PozycjeSzczegolowe>\n'
        yield xml_field(decl, "P_10", 0)
        yield xml_field(decl, "P_11", 0)
        yield xml_field(decl, "P_12", 0)
        yield xml_field(decl, "P_13", 0)
        yield xml_field(decl, "P_14", 0)
        yield xml_field(decl, "P_15", 0)
        yield xml_field(decl, "P_16", 0)
        yield xml_field(decl, "P_17", 0)
        yield xml_field(decl, "P_18", 0)
        yield xml_field(decl, "P_19", 0)
        yield xml_field(decl, "P_20", 0)
        yield xml_field(decl, "P_21", 0)
        yield xml_field(decl, "P_22", 0)
        yield xml_field(decl, "P_23", 0)
        yield xml_field(decl, "P_24", 0)
        yield xml_field(decl, "P_25", 0)
        yield xml_field(decl, "P_26", 0)
        yield xml_field(decl, "P_27", 0)
        yield xml_field(decl, "P_28", 0)
        yield xml_field(decl, "P_29", 0)
        yield xml_field(decl, "P_30", 0)
        yield xml_field(decl, "P_31", 0)
        yield xml_field(decl, "P_32", 0)
        yield xml_field(decl, "P_33", 0)
        yield xml_field(decl, "P_34", 0)
        yield xml_field(decl, "P_35", 0)
        yield xml_field(decl, "P_36", 0)
        yield xml_field(decl, "P_37")
        yield xml_field(decl, "P_38")
        yield xml_field(decl, "P_39", 0)
        yield xml_field(decl, "P_40", 0)
        yield xml_field(decl, "P_41", 0)
        yield xml_field(decl, "P_42", 0)
        yield xml_field(decl, "P_43", 0)
        yield xml_field(decl, "P_44", 0)
        yield xml_field(decl, "P_45", 0)
        yield xml_field(decl, "P_46", 0)
        yield xml_field(decl, "P_47", 0)
        yield xml_field(decl, "P_48")
        yield xml_field(decl, "P_49", 0)
        yield xml_field(decl, "P_50", 0)
        yield xml_field(decl, "P_51")
        yield xml_field(decl, "P_52", 0)
        yield xml_field(decl, "P_53")
        yield xml_field(decl, "P_54", 0)
        yield xml_field(decl, "P_540", 0)
        yield xml_field(decl, "P_55", 0.0)
        yield xml_field(decl, "P_56", 0)
        yield xml_field(decl, "P_560", 0)
        yield xml_field(decl, "P_57", 0)
        yield xml_field(decl, "P_58", 0)
        yield xml_field(decl, "P_59", 0)
        yield xml_field(decl, "P_60", 0)
        yield xml_field(decl, "P_61", "")
        yield xml_field(decl, "P_62")
        yield xml_field(decl, "P_63", 0)
        yield xml_field(decl, "P_64", 0)
        yield xml_field(decl, "P_65", 0)
        yield xml_field(decl, "P_66", 0)
        yield xml_field(decl, "P_660", 0)
        yield xml_field(decl, "P_67", 0)
        yield xml_field(decl, "P_68", 0)
        yield xml_field(decl, "P_69", 0)
        yield xml_field(decl, "P_ORDZU", "")
        yield f'    </PozycjeSzczegolowe>\n'
        yield f'    <Pouczenia>1</Pouczenia>\n'
        yield f'  </Deklaracja>\n'

    def _evidence_xml_gen(self):
        yield '  <Ewidencja>\n'
        yield from self._sales_xml_gen()
        yield from self._purchases_xml_gen()
        yield '  </Ewidencja>\n'

    def _sales_xml_gen(self):
        count = 0
        for count, sale in enumerate(self.sales, start=1):
            yield from self._sale_xml_gen(count, sale)
        yield f'    <SprzedazCtrl>\n'
        yield f'      <LiczbaWierszySprzedazy>{count}</LiczbaWierszySprzedazy>\n'
        yield f'      <PodatekNalezny>{self.calc_sales_vat():.2f}</PodatekNalezny>\n'
        yield f'    </SprzedazCtrl>\n'

    def _purchases_xml_gen(self):
        count = 0
        for count, purchase in enumerate(self.purchases, start=1):
            yield from self._purchase_xml_gen(count, purchase)
        yield f'    <ZakupCtrl>\n'
        yield f'      <LiczbaWierszyZakupow>{count}</LiczbaWierszyZakupow>\n'
        yield f'      <PodatekNaliczony>{self.calc_purchases_vat():.2f}</PodatekNaliczony>\n'
        yield f'    </ZakupCtrl>\n'



    def _sale_xml_gen(self, counter, sale: jpk_v7m_sale_data):
        yield f'    <SprzedazWiersz>\n'
        yield f'      <LpSprzedazy>{counter}</LpSprzedazy>\n'
        yield xml_field(sale, "KodKrajuNadaniaTIN")
        yield xml_field(sale, "NrKontrahenta")
        yield xml_field(sale, "NazwaKontrahenta")
        yield xml_field(sale, "DowodSprzedazy")
        yield xml_field(sale, "DataWystawienia")
        yield xml_field(sale, "DataSprzedazy")
        yield xml_field(sale, "TypDokumentu", "")
        yield xml_field(sale, "GTU_01", 0)
        yield xml_field(sale, "GTU_02", 0)
        yield xml_field(sale, "GTU_03", 0)
        yield xml_field(sale, "GTU_04", 0)
        yield xml_field(sale, "GTU_05", 0)
        yield xml_field(sale, "GTU_06", 0)
        yield xml_field(sale, "GTU_07", 0)
        yield xml_field(sale, "GTU_08", 0)
        yield xml_field(sale, "GTU_09", 0)
        yield xml_field(sale, "GTU_10", 0)
        yield xml_field(sale, "GTU_11", 0)
        yield xml_field(sale, "GTU_12", 0)
        yield xml_field(sale, "GTU_13", 0)
        yield xml_field(sale, "WSTO_EE", 0)
        yield xml_field(sale, "IED", 0)
        yield xml_field(sale, "TP", 0)
        yield xml_field(sale, "TT_WNT", 0)
        yield xml_field(sale, "TT_D", 0)
        yield xml_field(sale, "MR_T", 0)
        yield xml_field(sale, "MR_UZ", 0)
        yield xml_field(sale, "I_42", 0)
        yield xml_field(sale, "I_63", 0)
        yield xml_field(sale, "B_SPV", 0)
        yield xml_field(sale, "B_SPV_DOSTAWA", 0)
        yield xml_field(sale, "B_MPV_PROWIZJA", 0)
        yield xml_field(sale, "KorektaPodstawyOpodt", "")
        yield xml_field(sale, "TerminPlatnosci", "")
        yield xml_field(sale, "DataZaplaty", "")
        yield xml_field(sale, "K_10", 0.0)
        yield xml_field(sale, "K_11", 0.0)
        yield xml_field(sale, "K_12", 0.0)
        yield xml_field(sale, "K_13", 0.0)
        yield xml_field(sale, "K_14", 0.0)
        yield xml_field(sale, "K_15", 0.0)
        yield xml_field(sale, "K_16", 0.0)
        yield xml_field(sale, "K_17", 0.0)
        yield xml_field(sale, "K_18", 0.0)
        yield xml_field(sale, "K_19", 0.0)
        yield xml_field(sale, "K_20", 0.0)
        yield xml_field(sale, "K_21", 0.0)
        yield xml_field(sale, "K_22", 0.0)
        # K_23 and K_24 conditions
        yield xml_field(sale, "K_23", 0.0)
        if sale.K_23 > 0.0:
            yield xml_field(sale, "K_24")
        # K_25 and K_26 conditions
        yield xml_field(sale, "K_25", 0.0)
        if sale.K_25 > 0.0:
            yield xml_field(sale, "K_26")
        yield xml_field(sale, "K_27", 0.0)
        yield xml_field(sale, "K_28", 0.0)
        # K_29 and K_30 conditions
        yield xml_field(sale, "K_29", 0.0)
        if sale.K_29 > 0.0:
            yield xml_field(sale, "K_30")
        # K_31 and K_32 conditions
        yield xml_field(sale, "K_31", 0.0)
        if sale.K_31 > 0.0:
            yield xml_field(sale, "K_32")
        yield xml_field(sale, "K_33", 0.0)
        yield xml_field(sale, "K_34", 0.0)
        yield xml_field(sale, "K_35", 0.0)
        yield xml_field(sale, "K_36", 0.0)
        yield xml_field(sale, "SprzedazVAT_Marza", 0)
        yield f'    </SprzedazWiersz>\n'

    def _purchase_xml_gen(self, counter, purchase: jpk_v7m_purchase_data):
        yield f'    <ZakupWiersz>\n'
        yield f'      <LpZakupu>{counter}</LpZakupu>\n'
        yield xml_field(purchase, "KodKrajuNadaniaTIN", "")
        yield xml_field(purchase, "NrDostawcy")
        yield xml_field(purchase, "NazwaDostawcy")
        yield xml_field(purchase, "DowodZakupu")
        yield xml_field(purchase, "DataZakupu")
        yield xml_field(purchase, "DataWplywu", "")
        yield xml_field(purchase, "DokumentZakupu", "")
        yield xml_field(purchase, "IMP", 0)
        yield xml_field(purchase, "K_40", 0.0)
        if purchase.K_40 > 0.0:
            yield xml_field(purchase, "K_41")
        yield xml_field(purchase, "K_42", 0.0)
        if purchase.K_42 > 0.0:
            yield xml_field(purchase, "K_43")
        yield xml_field(purchase, "K_44", 0.0)
        yield xml_field(purchase, "K_45", 0.0)
        yield xml_field(purchase, "K_46", 0.0)
        yield xml_field(purchase, "K_47", 0.0)
        yield f'    </ZakupWiersz>\n'

    def calc_sales_vat(self):
        result = 0.0
        for sale in self.sales:
            if sale.TypDokumentu == "FP":
                # Ommit invoice marked as 'invoice for recipt ('faktura do paragonu' - art. 109 ust. 3d ustawy)'
                continue
            result += (
                sale.K_16 + sale.K_18  + sale.K_20 + sale.K_24 + sale.K_26 +
                sale.K_28 + sale.K_30 + sale.K_32 + sale.K_33 + sale.K_34 -
                sale.K_35 - sale.K_36
            )
        return result

    def calc_purchases_vat(self):
        result = 0.0
        for purchase in self.purchases:
            result += (
                purchase.K_41 + purchase.K_43 +
                purchase.K_44 + purchase.K_45 +
                purchase.K_46 + purchase.K_47
            )
        return result
