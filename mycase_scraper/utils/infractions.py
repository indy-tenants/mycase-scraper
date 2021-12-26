from enum import Enum


class Codes(Enum):

    AD = "Adoption (confidential case type)"
    CC = "Civil Collection (new CC case numbers shall not be used for residential and commercial evictions after 12/31/2020)"
    CP = "Civil Plenary (New CP case numbers shall not be issued after 12/31/2001. CP cases filed before 1/1/2020 shall continue to bear the CP case type.)"
    CT = "Civil Tort"
    DC = "Domestic Relations With Children (to be used for cases filed on or after 1/1/2017)"
    DN = "Domestic Relations No Children (to be used for cases filed on or after 1 / 1 / 2017)"
    DR = "Domestic Relation (includes Dissolution of Marriage, Annulment, and Legal Separation) (New DR case numbers shall not be issued after 12 / 31 / 2016. DR cases filed before 1 / 1 / 2017 shall continue to bear the DR case type.)"
    EV = "Petition for Eviction (to be used for residential and commercial evictions filed on or after 1 / 1 / 2021--including claims for related damages; however other landlord / tenant disputes such as damages without request for eviction, suits regarding habitability, and other contract breaches, shall, depending on the amount in controversy, continue to be filed using the small claims (SC) or civil collections (CC) case types.)"
    MF = "Mortgage Foreclosure"
    MH = "Mental Health (confidential case type)"
    MI = "Miscellaneous (Civil cases other than those specifically identified--i.e.change of name, appointment of appraisers, marriage waivers, etc.)"
    PC = "Post Conviction Relief Petition"
    PL = "Civil Plenary (Civil Plenary cases filed after 1 / 1 / 2002--All Civil cases except those otherwise specifically designated)"
    PO = "Order of Protection (confidential case type)"
    RS = "Reciprocal Support"
    SC = "Small Claims (new SC case numbers shall not be used for residential and commercial evictions after 12 / 31 / 2020)"
    TP = "Verified Petition for Issuance of a Tax Deed"
    TS = "Application for Judgment in a Tax Sale"
    XP = "Expungement Petition ( for petitions filed under I.C.35-38-9) (confidential after granted)"

    def __str__(self):
        return self.name
