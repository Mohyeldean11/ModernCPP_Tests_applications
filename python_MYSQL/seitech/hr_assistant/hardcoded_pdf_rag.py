#!/usr/bin/env python3
"""
PDF RAG System - Search Only Version
Hardcoded database - no PDF processing, only search functionality
"""

import os
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import re
from typing import List, Dict, Tuple
import pickle
from pathlib import Path
from collections import Counter

class PDFRagSystem:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        """
        Initialize the PDF RAG system with a sentence transformer model
        Search-only version with hardcoded database
        """
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer(model_name)
        self.vector_db = []
        self.embeddings = None
        self.min_accuracy_threshold = 0.5 # Fixed threshold
        
        # Initialize with hardcoded database
        self.initialize_hardcoded_database()
    
    def initialize_hardcoded_database(self):
        """
        Initialize the system with a hardcoded database
        Replace this with your actual data
        """
        # Example hardcoded database - replace with your actual data
        hardcoded_chunks = [
                                {
                                    "text": "4. VACATION LEAVE POLICY\n4.1 Number of days\nThe number of days for annual leave vacations is as per employment period covered by social insurance and labor law:\n- Employees with less than 5 years get 21 days.\n- Employees who reach 5 years get 23 days.\n- Employees who reach 7 years get 25 days.\n- Employees who reach 10 years get 30 days.\n4.2 Vacation requests\nEmployees are allowed to plan their vacations at the beginning of the year. Each vacation request must be approved by their manager. Should any cancellations happen due to workload, the employee can modify their submitted plans accordingly.\nRequests should be provided within the following timeframes:\n- For 1 day: 1 day before vacation start day.\n- For 2-3 days: 1 week before vacation start day.\n- For 4-10 days: latest 2 weeks before vacation start day.\n- For 11+ days: latest 1 month before vacation start day.\n4.3 Guidelines\nThe following guidelines are applicable when it comes to annual vacations:\n- Employees must consume 75% of their vacation days before the start of Q3.\n- Employees shouldnâ€™t have more than 10% of their annual balance by the end of November.\n- Non-compliant cases will be addressed by the HR BP\n- Approval from N+1 is required to proceed with any vacation requests. Approval is subject to business needs and projectsâ€™ situation.\n- The annual balance should be consumed entirely within the current year.\n- In case the employee couldnâ€™t consume their vacation days due to heavy workload or justified business need, a maximum number of 4 vacation days can be carried over and consumed within the first month of the following year.\n- Carry over days request to be submitted by N+1, reviewed by N+2 and HR business partner, and approved by HR Manager and Department Head.\n- Any exception from the above mentioned guidelines must be approved by the HR Manager and Department Head.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 0,
                                    "chunk_length": 1583,
                                    "word_count": 284,
                                    "keywords": ["vacation policy", "annual leave", "vacation requests", "guidelines", "carry over"]
                                },
                                {
                                    "text": "5. EMERGENCY VACATION\n- Each employee has a maximum of 6 emergency days per year, to be deducted from his annual balance.\n- Employees are allowed emergency vacations with a maximum of 2 consecutive days.\n- In case of Emergency, the employee must inform the N+1 on the same day of the emergency before the start of core working day.\n- Emergencies are to be reported by N+1 to the HR BP\n- In case of more than 6 days emergency, the employee will receive an HR verbal or written warning, and the actual number of emergency leaves will be deducted from the annual balance.\n- Penalties for exceeding emergency days are as follows:\n  - 7th emergency day: Deduction of 1 day from annual balance (one day from salary if annual balance is fully consumed) and HR verbal warning.\n  - 8th emergency day: Deduction of Â¼ day equivalent from salary and 1 day from annual balance (one day from salary if annual balance is fully consumed), including penalties for the previous violated days and HR written warning.\n  - 9th emergency day: Deduction of Â½ day from salary and 1 day from annual balance (one day from salary if annual balance is empty), including penalties for the violated previous days HR written warning.\n  - 10th emergency day or more: Deduction of 2 days from salary and 1 day from annual balance (one day from salary if annual balance is empty), including penalties for the previous violated days HR written warning.\n- After the third Written HR warning, the company has the right to terminate the contract.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 1,
                                    "chunk_length": 1191,
                                    "word_count": 216,
                                    "keywords": ["emergency vacation","vacation","emergency days", "penalties", "HR warning", "contract termination"]
                                },
                                {
                                    "text": "6. SICK LEAVE\nA sick leave request is provided according to the following conditions as per Egyptian labor law:\n- The employee must inform their N+1 on the same day. N+1 will inform HR business partner.\n- All sick leave absences require a medical doctor/hospital note that is signed or stamped.\n- The employee must attach a medical note from the hospital or a doctor, of the sick request and submit it on the companyâ€™s tool.\n- A sick leave request can be rejected if a medical note or proof of illness is not provided and, in that case, the sick days will be considered as an emergency or absence.\n- The Employee must submit the original medical note within one working day of coming back to work.\n- The employee is allowed to self-certify their sick leave for up to 8 separate days per year, with a maximum of 2 consecutive days per instance, without the need for a medical certificate.\n- The employee must inform their direct manager (N+1) on the same day before the start of core working hours. N+1 will then notify the HR Business Partner (HRBP).\n- A medical note is required for any sick leave beyond the 2 consecutive days, covering the whole duration of the sickness.\n- If the employee fails to provide a medical note on the third day, that day and any subsequent days will be considered as emergency leave and will be deducted from the employee's annual leave balance or his/her salary in case of no vacation balance as per labor law will be applied as follows:\n  - Payment of 75% of basic salary during the first 90 days.\n  - Payment of 85% of basic salary during following 90 days.\n- In case an employee submits a medical note for more than 5 days or for a condition exceeding 5 days a signed and stamped medical note must be provided from a doctor or facility within the companyâ€™s approved network.\n- Failure to provide the required documentation may lead to the rejection of the sick leave request.\n- Sick days are counted as calendar days and includes weekends and public holidays.\n- A sick leave balance cannot be transferred from year to year.\n- Abusing sick leaves or repeated instances of not providing a valid medical note or timely notification, may result in disciplinary action that may be salary deductions or HR warning.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 2,
                                    "chunk_length": 1839,
                                    "word_count": 326,
                                    "keywords": ["sick leave", "medical note", "self-certify", "salary payment", "abuse penalties"]
                                },
                                {
                                    "text": "7. VACATION BALANCE FOR RESIGNING EMPLOYEES\nEmployees who choose to leave the company and are not able to finish their balance are entitled to receive payments equivalent non consumed vacation days in relation to the actual employment service within the year of resigning. In the case of the resigning employee who has exceeded their vacation balance, the amount will be deducted from their final statement.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 3,
                                    "chunk_length": 315,
                                    "word_count": 59,
                                    "keywords": ["resigning employees", "vacation balance", "final payment", "deductions"]
                                },
                                {
                                    "text": "8. UNPAID LEAVE\nUnpaid leave is only applicable if the employee has no annual balance left and the request must be approved by N+2 and HR Director in a written format as per business requirements.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 4,
                                    "chunk_length": 170,
                                    "word_count": 32,
                                    "keywords": ["unpaid leave", "approval process", "business requirements"]
                                },
                                {
                                    "text": "9. MATERNITY LEAVE\n9.1 Eligibility\nAll female employees who have completed 10 months or more, across one or more companies are eligible to benefit from the maternity leave.\n- An unpaid maternity leave is allowed 3 times during the employment period of the employee.\n- Medical insurance is resumed during maternity unpaid leave.\n- During the 4 months of paid maternity leave, employees are entitled to any bonus scheme.\n- Both employee and their N+1 must inform HR with the start date and duration of the maternity leave, 5 months before it begins.\n- For further details please refer to the Maternity Leave Policy and Process",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 5,
                                    "chunk_length": 481,
                                    "word_count": 87,
                                    "keywords": ["maternity leave", "eligibility", "unpaid leave", "medical insurance", "notification"]
                                },
                                {
                                    "text": "10. SPECIAL OCCASIONS AND PTO\nThe following guidelines are applicable when it comes to Special occasions. This should help maintain a healthy work-life balance and clearly communicate the requirements to follow to request time off.\n10.1 Marriage Leave\nMarriage Leave is considered as a complimentary company benefit where no specific rules are applicable.\n- The Marriage leave grant is 5 Paid days, can be consumed any day starting from one week before the official marriage (Pre-wedding Preparations) to maximum One-Month after the wedding or the grant expires.\n- N+1 and HRBP must be informed about the marriage leave days beforehand.\n- The 5 days can be taken as a bundle or separate days before and after the wedding day.\n- Any extended days will be deducted from your annual vacation balance.\n- If the Employee has no annual balance left, the request must be approved by N+2 and HRBP in a written format.\n10.2 Bereavement Leave\nBereavement leave is considered as an internal PTO policy where no specific rules are applicable and differs by the relationship degree.\n- 1st Degree (Parents â€“ Siblings â€“ Children - Spouse): 2 days are granted after the loss of a family member.\n- 2nd and 3rd Degree (Grandparents - Uncles â€“ Aunts â€“ Nephews â€“ Nieces â€“ Cousins â€“ Grandchildren): 1 days are granted after the loss of a relative\n- Any extended days N+1 and HR must be informed beforehand.\n10.3 Newborn\nNewborn leave is considered as an internal PTO policy where no specific rules are applicable.\n- The Newborn leave grant is 2 Paid days, can be consumed any day starting from one week to maximum One-Month after the baby is born or the grant expires.\n- Employees must inform N+1 and HRBP beforehand.\n10.5 Relocation\nRelocation leave is considered as an internal PTO policy where no specific rules are applicable.\n- Relocation leave is only granted to an employee who is changing his/her residing location.\n- The Relocation leave grant is 1 Paid day per year.\n- Employees must inform N+1 and HRBP beforehand.\n- Employees must inform the HRBP with the new address as soon as the relocation is done.",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 6,
                                    "chunk_length": 1310,
                                    "word_count": 238,
                                    "keywords": ["special occasions", "marriage leave", "bereavement leave", "newborn leave", "relocation leave"]
                                },
                                {
                                    "text": "11. HOLIDAYS AND COMPENSATION\nCompensation will be provided for employees working during weekends and public holidays.\n11.1 Guidelines\n- A request must be submitted via our tool to N+1 and the HR BP at least one day before the required working day\n- Working on weekend or holiday must be approved by Department Head and HR Manager.\n- Working on weekends or holidays must be with written approval prior to the request and supported by a justified business need\n- Upon approval, employees are eligible for monetary compensation or alternative working days as per labor law\n- Employees working on Weekend (Friday) will be compensated either double payment or one day payment and one day vacation\n- Employees working on public holidays will be compensated either double payment or one day payment and one day vacation\n- Employees working on Saturday will be compensated by one day payment and one day vacation\n- One day vacation compensation must be planned on same customer invoice, within the same calendar month in which the extra day work occurred\n- N+1 and HR BP must ensure that the employee does not work more than 7 consecutive days, in case of high or urgent business need\n- HR Manager and Department Head approval required if the work exceeds more than two consecutive weekends\n- Company will compensate the employees on their extra hours within 2 months after approval based on hourly compensation",
                                    "source": "Vacation & Paid Time Off Policy.pdf",
                                    "chunk_id": 7,
                                    "chunk_length": 1093,
                                    "word_count": 196,
                                    "keywords": ["holiday compensation", "weekend work", "monetary compensation", "approval process", "overtime rules"]
                                },
                                {
                                  "text": "4. ELIGIBILITY\nAll employees who have a direct contract with SEITech Solutions LLC are automatically enrolled in the plan after successfully completing their 3 months' probation period.",
                                  "source": "Retirement and Employee Benefit Policy.pdf",
                                  "chunk_id": 8,
                                  "chunk_length": 181,
                                  "word_count": 31,
                                  "keywords": ["retirement eligibility", "enrollment", "probation","eligibility","enrolled","3 months probation","eligible"]
                                },
                                {
                                  "text": "5. GUIDELINES\n- Starting February 2025, all contributions to the â€œEmployee benefit planâ€ are paid directly by the company to the employee, calculated as a percentage of the employeeâ€™s gross monthly base salary according to their job level.\n- Benefit payments are subject to applicable taxation.\n- Employees may choose either to cash out 100% of the lump sum amount of their current â€œpension planâ€ balance or to continue with their current balance with our third-party provider, GIG.\n- The continuation option is applicable only to the currently enrolled employees.\n- The pension plan investment will continue to be managed by an independent third-party provider, GIG.\n- The minimum number of employees that can be enrolled under the group company policy with GIG is 30 employees.\n- In case the number of employees who opt to continue with the pension plan is less than 30, they will have to enroll individually with the investment company, GIG.\n- Employees who opt to continue with GIG under group policy will receive an annual investment statement at the end of the financial year, detailing their starting and ending balances, along with a comprehensive investment overview.",
                                  "source": "Retirement and Employee Benefit Policy.pdf",
                                  "chunk_id": 9,
                                  "chunk_length": 876,
                                  "word_count": 152,
                                  "keywords": ["contributions", "taxation", "cashout", "continuation", "provider", "minimum", "statements","benefit plan","benefit",""]
                                },
                                {
                                  "text": "6. PROCESS AND PROCEDURES\nStarting February 2025:\n- The company will not pay any further contributions to the third-party company, GIG.\n- Employees who meet the eligibility criteria will be automatically enrolled in the Employee Benefit Plan, which will be reflected in their monthly salary under the band \"Employee Benefit Plan\".\n- Employees who are currently enrolled may opt out of the pension plan by contacting their HRBP.\n- A table detailing job levels and corresponding percentages is provided on page 3 of this policy appendix.\n- Resigned employees can cash out the full amount of their pension plan based on their effective exit date and, within three months of leaving the company.\n- In the event of an employeeâ€™s death, if the pension plan has not been cashed out, a lump sum payment will be made to the designated beneficiary. The HR department will oversee the processing of this payment.\n- The HR department is responsible for maintaining records and communicating with employees regarding the plan.\n\nAppendix 1\nJob level and the Contributions Amount\n| Job Level | Company Contribution |\n|---|---|\n| Assistant/Specialist/Junior/Staff/Senior | 5% |\n| Expert/Senior Expert/Leader/senior Leader/ Manager/Chief | 6% |\n| Associate/Senior Associate/Senior Chief /Senior Manager/Director/Senior Director/Executive | 7% |",
                                  "source": "Retirement and Employee Benefit Policy.pdf",
                                  "chunk_id": 10,
                                  "chunk_length": 915,
                                  "word_count": 159,
                                  "keywords": ["procedures", "enrollment", "optout", "resignation", "beneficiary", "records", "contributions"]
                                },
                                {
                                  "text": "4. OVERTIME COMPENSATION\nCompensation will be provided for employees working overtime.\n4.1Guidelines\nThe following guidelines must be fulfilled:\n- Employees can work overtime to a maximum of 16 hours on working week, ensuring not to exceed 40 approved extra hours a month.\n- Any exceptions must be approved by Department Head and HR Manager.\n- N+1 and HR BP must monitor overtime and communicate to the employee to avoid having high extra hours in consecutive months.\n- Company will compensate the employees on their extra hours within 2 months after approval based on hourly compensation.\n4.2 Criteria\n- Employees who exceed 10 extra hours per month are to be compensated on their full logged hours.\n- Extra hours must be based on a justified business need.\n- Extra hours must be in alignment and approved by N+1.\n- Extra hours must be approved by Department Head and HR Manager.",
                                  "source": "Compensation Policy.pdf",
                                  "chunk_id": 11,
                                  "chunk_length": 690,
                                  "word_count": 124,
                                  "keywords": ["overtime", "compensation", "guidelines", "criteria", "approval", "limits"]
                                },
                                {
                                  "text": "5. HOLIDAYS AND COMPENSATION\nCompensation will be provided for employees working during weekends and public holidays.\n5.1 Guidelines\n- A request must be submitted via our tool to N+1 and the HR BP at least one day before the required working day\n- Working on weekend or holiday must be approved by Department Head and HR Manager.\n- Working on weekends or holidays must be with written approval prior to the request and supported by a justified business need\n- Upon approval, employees are eligible for monetary compensation or alternative working days as per labor law\n- Employees working on Weekend (Friday) will be compensated either double payment or one day payment and one day vacation\n- Employees working on public holidays will be compensated either double payment or one day payment and one day vacation\n- Employees working on Saturday will be compensated by one day payment and one day vacation\n- One day vacation compensation must be planned on same customer invoice, within the same calendar month in which the extra day work occurred\n- N+1 and HR BP must ensure that the employee does not work more than 7 consecutive days, in case of high or urgent business need\n- HR Manager and Department Head approval required if the work exceeds more than two consecutive weekends\n- Company will compensate the employees on their extra hours within 2 months after approval based on hourly compensation",
                                  "source": "Compensation Policy.pdf",
                                  "chunk_id": 12,
                                  "chunk_length": 1002,
                                  "word_count": 178,
                                  "keywords": ["holidays", "weekends", "compensation", "guidelines", "approval", "payment", "limits"]
                                },
                                {
                                  "text": "3. EGYPTIAN VISA PROCESS\nSEITech Foreigner Visitors can issue Egyptian VISA via one of the following options:\nI. Option one:\nThe travel agency service will assist in Cairo Airport to get the visa upon arrival.\n- Meeting and assistance service costs 100 Euros (paid in cash).\n- VISA costs 25 USD or 25 EUR (paid in cash).\nII. Option two:\n- VISA can be issued by visitor directly without prior request upon arrival at Cairo Airport.\n- VISA cost is 25 USD or 25 EUR (paid in cash)\nIII. Option three:\n- Apply online at least seven days prior to the travel date to allow processing time.\n- Website: Egypt e-Visa Portal\nNote: If you enter the country by ID card instead of the passport, you should bring a personal photo.",
                                  "source": "Visitors Guideline.pdf",
                                  "chunk_id": 13,
                                  "chunk_length": 650,
                                  "word_count": 120,
                                  "keywords": ["visa", "arrival", "online", "options", "costs"]
                                },
                                {
                                  "text": "4. TRANSPORTATION GUIDELINES:\nThe below instructions aim to ease your transportation from the airport to the hotel and vice versa.\nI. Option one:\nThe travel agency will arrange someone to meet the visitor at the airport and pick him/ her up by a limousine from the airport to the hotel and it will cost 100 Euro.\nII. Option two:\n- Arrangement can be made for a London cab to pick up the visitor from the airport to the hotel.\n- It costs approximately 900 EGP.\nIII. Option three:\n- Visitors use Uber transportation by ordering a pickup from the airport to the hotel via the uber app.\n- It costs up to 600 EGP.",
                                  "source": "Visitors Guideline.pdf",
                                  "chunk_id": 14,
                                  "chunk_length": 519,
                                  "word_count": 95,
                                  "keywords": ["transportation", "airport", "limousine", "cab", "uber"]
                                },
                                {
                                  "text": "5. HOTEL GUIDELINES\nThe following options are hotels, which have a corporate rate for SEITech solutions employees and visitors.\n|    | Crowne Plaza    | Helnan Dream    | Hilton pyramids golf |\n|---|---|---|---|\n| Hotel Website Link    | https://www.ihg.com/crown eplaza/hotels/us/en/cairo/c aisz/hoteldetail    | Microsoft Bing Travel - Helnan Dreamland Hotel    | Hilton Hotel Pyramids Golf | Hilton    |\n| Price per night (Single Room)    | 155 USD/ night    | 110 USD/ night.    | 120 USD/ night    |\n|    | Including breakfast    | Including breakfast.    | Including breakfast    |\n|    | Excluding the service charge and any taxes charges.    | All-inclusive of service charge and all applicable tax.    | All-inclusive of all service charge and taxes 14% vat tax, 12% service charge and 1% governmental taxes. |\nIf a visitor is willing to benefit from this special rate, He/she shall send a passport copy to SEITech Team, to arrange the reservation. Hotel payment is made by the visitor upon arrival at the hotel.\nOter hotels recommendations near to SEITech office, with no corporate rate benefit:\n- NOVOTEL: http://novotel.accor.com/a/en//middle-east.html\n- Hayat Regency: https://www.hyatt.com/en-US/hotel/egypt/hyatt-regency-cairo-west/hberc",
                                  "source": "Visitors Guideline.pdf",
                                  "chunk_id": 15,
                                  "chunk_length": 1023,
                                  "word_count": 154,
                                  "keywords": ["hotels", "rates", "reservation", "payment", "recommendations"]
                                },
                                {
                                  "text": "6. OFFICE GUIDELINES\n- **SEITech main office location in Egypt**: https://maps.app.goo.gl/M9tifewXhVGycCwq6\n- **Working hours**: From 8:00 AM to 5: 00 PM\n- **Contact numbers**:  \n  - MRS. Nesrin Mohamed (+20)1091195241  \n  - MS. Haidy Mohamed (+20)1022380010\n\n- **SEITech office rules**:  \n  - Visitors shall register his/her presence at SEITech premises front desk and to receive visitor access card.  \n  - Visitors are obligated to always carry the visitor access card during the presence at SEITech Offices.  \n  - Visitors are obliged to read and understand the visitorsâ€™ regulations manual.  \n  - Visitors are not allowed to take any pictures or videos unless approved by SEITech management.",
                                  "source": "Visitors Guideline.pdf",
                                  "chunk_id": 16,
                                  "chunk_length": 627,
                                  "word_count": 110,
                                  "keywords": ["office", "location", "hours", "contacts", "rules"]
                                },
                                {
                                  "text": "4. ELIGIBILITY\nAll employees who have a direct contract with SEITech Solutions LLC are automatically enrolled in the plan after successfully completing their 3 months' probation period.\n\n5. GUIDELINES\n- Starting February 2025, all contributions to the â€œEmployee benefit planâ€ are paid directly by the company to the employee, calculated as a percentage of the employeeâ€™s gross monthly base salary according to their job level.\n- Benefit payments are subject to applicable taxation.\n- Employees may choose either to cash out 100% of the lump sum amount of their current â€œpension planâ€ balance or to continue with their current balance with our third-party provider, GIG.\n- The continuation option is applicable only to the currently enrolled employees.\n- The pension plan investment will continue to be managed by an independent third-party provider, GIG.\n- The minimum number of employees that can be enrolled under the group company policy with GIG is 30 employees.\n- In case the number of employees who opt to continue with the pension plan is less than 30, they will have to enroll individually with the investment company, GIG.\n- Employees who opt to continue with GIG under group policy will receive an annual investment statement at the end of the financial year, detailing their starting and ending balances, along with a comprehensive investment overview.\n\n6. PROCESS AND PROCEDURES\nStarting February 2025:\n- The company will not pay any further contributions to the third-party company, GIG.\n- Employees who meet the eligibility criteria will be automatically enrolled in the Employee Benefit Plan, which will be reflected in their monthly salary under the band \"Employee Benefit Plan\".\n- Employees who are currently enrolled may opt out of the pension plan by contacting their HRBP.\n- A table detailing job levels and corresponding percentages is provided on page 3 of this policy appendix.\n- Resigned employees can cash out the full amount of their pension plan based on their effective exit date and, within three months of leaving the company.\n- In the event of an employeeâ€™s death, if the pension plan has not been cashed out, a lump sum payment will be made to the designated beneficiary. The HR department will oversee the processing of this payment.\n- The HR department is responsible for maintaining records and communicating with employees regarding the plan.\n\nJob level and the Contributions Amount\n| Job Level | Company Contribution |\n|---|---|\n| Assistant/Specialist/Junior/Staff/Senior | 5% |\n| Expert/Senior Expert/Leader/senior Leader/ Manager/Chief | 6% |\n| Associate/Senior Associate/Senior Chief /Senior Manager/Director/Senior Director/Executive | 7% |",
                                  "source": "Retirement and Employee Benefit Policy .pdf",
                                  "chunk_id": 17,
                                  "chunk_length": 1952,
                                  "word_count": 342,
                                  "keywords": ["Retirement", "contributions", "taxation", "cashout", "continuation","statements", "enrollment", "optout", "resignation", "beneficiary"]
                                },
                                {
                                  "text": "4. ELIGIBILITY\nAll employees who have a direct contract with SEITech Solutions LLC are automatically enrolled in the plan after successfully completing their 3 months' probation period.",
                                  "source": "Budget Procedure .pdf",
                                  "chunk_id": 18,
                                  "chunk_length": 181,
                                  "word_count": 31,
                                  "keywords": ["enrollment", "probation period"]
                                },
                                {
                                  "text": "5. GUIDELINES\n- Starting February 2025, all contributions to the â€œEmployee benefit planâ€ are paid directly by the company to the employee, calculated as a percentage of the employeeâ€™s gross monthly base salary according to their job level.\n- Benefit payments are subject to applicable taxation.\n- Employees may choose either to cash out 100% of the lump sum amount of their current â€œpension planâ€ balance or to continue with their current balance with our third-party provider, GIG.\n- The continuation option is applicable only to the currently enrolled employees.\n- The pension plan investment will continue to be managed by an independent third-party provider, GIG.\n- The minimum number of employees that can be enrolled under the group company policy with GIG is 30 employees.\n- In case the number of employees who opt to continue with the pension plan is less than 30, they will have to enroll individually with the investment company, GIG.\n- Employees who opt to continue with GIG under group policy will receive an annual investment statement at the end of the financial year, detailing their starting and ending balances, along with a comprehensive investment overview.",
                                  "source": "Budget Procedure .pdf",
                                  "chunk_id": 19,
                                  "chunk_length": 876,
                                  "word_count": 152,
                                  "keywords": ["contributions", "taxation rules", "cashout option", "continuation policy", "provider management", "minimum enrollment", "investment statements"]
                                },
                                {
                                  "text": "6. PROCESS AND PROCEDURES\nStarting February 2025:\n- The company will not pay any further contributions to the third-party company, GIG.\n- Employees who meet the eligibility criteria will be automatically enrolled in the Employee Benefit Plan, which will be reflected in their monthly salary under the band \"Employee Benefit Plan\".\n- Employees who are currently enrolled may opt out of the pension plan by contacting their HRBP.\n- A table detailing job levels and corresponding percentages is provided on page 3 of this policy appendix.\n- Resigned employees can cash out the full amount of their pension plan based on their effective exit date and, within three months of leaving the company.\n- In the event of an employeeâ€™s death, if the pension plan has not been cashed out, a lump sum payment will be made to the designated beneficiary. The HR department will oversee the processing of this payment.\n- The HR department is responsible for maintaining records and communicating with employees regarding the plan.",
                                  "source": "Budget Procedure .pdf",
                                  "chunk_id": 20,
                                  "chunk_length": 733,
                                  "word_count": 127,
                                  "keywords": ["contribution cessation", "automatic enrollment", "opt-out process", "resignation payout", "death benefits", "records management"]
                                },
                                {
                                  "text": "Job level and the Contributions Amount\n| Job Level | Company Contribution |\n|---|---|\n| Assistant/Specialist/Junior/Staff/Senior | 5% |\n| Expert/Senior Expert/Leader/senior Leader/ Manager/Chief | 6% |\n| Associate/Senior Associate/Senior Chief /Senior Manager/Director/Senior Director/Executive | 7% |",
                                  "source": "Budget Procedure .pdf",
                                  "chunk_id": 21,
                                  "chunk_length": 310,
                                  "word_count": 42,
                                  "keywords": ["contribution percentages", "job levels"]
                                },
                                {
                                  "text": "4. FLEXIBLE WORKING HOURS\n4.1. Eligibility\nAll employees of SEITech solutions are eligible to flexible working hours. This duration can be reduced if approved by the manager.\n4.2. Criteria\n- The main priority is meeting all business goals, so work flexibility is entirely dependent on current business meetings with clients or otherwise as needed. The employeeâ€™s flexible time must be aligned with any staff meetings and client meetings.\n- The normal standard working hours for all employees are from 9 am to 6 pm from Sunday to Thursday in our sites in Egypt.\n- The normal standard working hours for all employees are from 8 am to 5 pm from Monday to Friday in our site in Germany.\n- The core working hours start from 10 am, not to end before 4 pm, even if there are no business needs\n- A request should be sent to N+1 and HR BP in case the employee cannot abide by the core working hours. The request must be approved by the N+1.\n- All employees must abide by their working hours mentioned in their contracts (40 hours per week/8 hours a day).\n- All employees must be available for work during their core working hours.\n- In accordance with our policy, employees are recommended to take a 45-minute break during the workday.",
                                  "source": "Working Hours Policy.pdf",
                                  "chunk_id": 22,
                                  "chunk_length": 1055,
                                  "word_count": 187,
                                  "keywords": ["flexible hours", "eligibility", "core hours", "country differences", "break policy"]
                                },
                                {
                                  "text": "5. WORKING FROM HOME\n5.1. Eligibility\nEmployees who have spent more than 3 months in the company are entitled to work from home based on the guidelines mentioned in this policy.\n5.2. Criteria\n- Employees with 0-5 years of experience are entitled to up to 6 days per month, with maximum 2 days per week.\n- Employees with 5 and more years of experience are entitled to up to 8 days per month with maximum 3 days per week.\n5.3. Guidelines\n- Working from home days can be taken within a normal working week.\n- Working from home days cannot be taken before and then after minimum 2 consecutive non-Working days.\n- Working from home day is allowed to be taken either before or after minimum 2 consecutive non-working days.\n- Non-working days are defined as holidays, vacation, weekend or combination of any.\n- The employee must be available for calls and online meetings throughout the day.\n- It is the employeeâ€™s personal responsibility to maintain proper internet connection; otherwise, they must head immediately to the office.\n- Requests to work from home must be submitted a minimum of 1 day prior to the day requested and latest by 6 pm, and it must be approved by N+1.\n- Non approved request for 24 hours is considered as approved request by default.\n- In case of no show on refused days or non-requested days, the day will be considered as an emergency leave.\n- The employee must inform all stakeholders that they are working from home.\n- Any exceptional cases to the above guidelines will be evaluated accordingly by the N+1 and HR BPs\n- Salaries are not affected by the allowed working from home days.\n- In the case of exceeding the monthly allowed number of \"work from home\" days, employee is subject to relevant compensation deduction.",
                                  "source": "Working Hours Policy.pdf",
                                  "chunk_id": 23,
                                  "chunk_length": 1314,
                                  "word_count": 239,
                                  "keywords": ["remote work", "eligibility criteria", "experience tiers", "request process", "availability requirements", "compensation deduction"]
                                },
                                {
                                  "text": "6. COVID-19 AND OTHER EMERGENCIES\nWorking from home, rules are subject to change if any COVID-related lockdowns or any other state emergency take place. Rules will be communicated by HR if any such incident takes place in the future.",
                                  "source": "Working Hours Policy.pdf",
                                  "chunk_id": 24,
                                  "chunk_length": 224,
                                  "word_count": 41,
                                  "keywords": ["emergency provisions", "policy flexibility"]
                                },
                                {
                                  "text": "7. TIME SHEET SUBMISSION\n7.1. Eligibility\nAll employees who are working in business units or projects require time sheet submission in addition to normal attendance.\n7.2. Guidelines\n- Every employee must submit their attendance in the companyâ€™s system/tool and Time sheet in the project logging tools(internal/external) at latest by the end of the business week.\n- All employees must submit hours of special projects on the companyâ€™s system/tool.\n- In case the employee has no access to the companyâ€™s system/tool because of travel reasons or otherwise, they should send the hours by mail to the N+1.\n- In case of the unavailability of an opened task or project, the employee should report to his N+1, 2 days before end of the week.\n- Any violation of time sheet submission rules will be considered as a non-compliant act, and the reoccurrence will have a direct impact on the performance evaluation, bonuses, and promotions.",
                                  "source": "Working Hours Policy.pdf",
                                  "chunk_id": 25,
                                  "chunk_length": 722,
                                  "word_count": 130,
                                  "keywords": ["timesheet requirements", "submission deadlines", "access exceptions", "compliance consequences"]
                                },
                                {
                                  "text": "8. WORKING HOURS OVERTIME\n8.1. Guidelines\n- In a 40 hours week, employees can work overtime to a maximum of 16 hours on working week, ensuring not to exceed 40 approved extra hours a month.\n- N+1 must review and approve the hours of his N-1s monthly, providing the relevant justification.\n- HR Manager and Department Head will review and approve all extra hours reported monthly by N+1.\n- N+1 and HR BP must monitor overtime and communicate to the employee to avoid having high extra hours in consecutive months\n- Overtime is compensated, as referred to in the companyâ€™s compensation policy.\n8.2 Criteria\nThese criteria are only applicable for employees in Egyptian site.\n- Employees who exceed 10 extra hours per month are to be compensated on their full logged hours.\n- Extra hours must be approved by the HR Manager and Department Head.\n- Extra hours must be based on a justified business need.",
                                  "source": "Working Hours Policy.pdf",
                                  "chunk_id": 26,
                                  "chunk_length": 716,
                                  "word_count": 129,
                                  "keywords": ["overtime limits", "approval process", "monthly monitoring", "Egypt criteria", "business justification"]
                                },
                                {
                                  "text": "4. OPEN SPACE POLICY AND ETIQUETTE\n4.1 Guidelines\nThese guidelines should help set up a respectful environment that allows everyone to remain productive. The following guidelines of open office etiquette will be considered as the normal standard during working hours for all employees from 9 am to 6 pm from Sunday to Thursday for Egypt and from 8 am to 5 pm from Monday to Friday in Germany.\n4.2 Keep noise down and minimize distraction\nAvoid creating things that can lead to noise/distractions for others in the working space.\n- Use headphones for meetings and calls.\n- Use headphones when listening to music and videos.\n- Take personal calls in the common designated areas and not on the work floor.\n- Avoid loud conversation in common working areas.\n4.3 Conduct meetings in designated areas\n- Face to face meetings: make sure you plan and take the meetings in a reserved meeting room.\n- Online meetings: make sure you plan and take the meetings in the designated meeting rooms. In case of room unavailability, please make sure to have your headphones on.\n4.4 Office and desk organization\nUnlike in a traditional office, an open office puts your desk in the line of sight of everyone else.\nPlease apply the Following 4Cs Golden Rules for desk organization:\n- Clear your piles. De-clutter, empty, shred, get rid of everything that you do not need or want. Make sure you file each paper/ document/post it in its designated place, archive it or bin it.\n- Confine the usage of personal decoration items on your workstation, for example, frames, candles, or soft toys, etcâ€¦. Keep it professional.\n- Collect and redistribute every item that does not belong and put it where it does, for example, kitchen utensils.\n- Clean your desktop. Keep your workstation and drawerâ€™s tidy. At the end of the day, do a quick straighten, so you have a clean start the next day.",
                                  "source": "Office Open Workspace Policy.pdf",
                                  "chunk_id": 27,
                                  "chunk_length": 1470,
                                  "word_count": 260,
                                  "keywords": ["open space", "noise reduction", "meeting etiquette", "desk organization", "4Cs rules"]
                                },
                                {
                                  "text": "5. MEETING ROOMS ETIQUITE\n- Book rooms in advance. Be on time and leave on time.\n- Cancel at the earliest possible time in case you do not need the meeting room.\n- Keep it clean and orderly. Do a hard reset for the next group to use the space.\n- Use only intended whiteboard markers for the whiteboards.\n- Do not tape things to the whiteboards as it can ruin the surface.\n- Throw markers away once they have run dry.\n- Erase your work from the white board once you are done with the meeting.\n- Do not erase someone elseâ€™s work without their permission.",
                                  "source": "Office Open Workspace Policy.pdf",
                                  "chunk_id": 28,
                                  "chunk_length": 495,
                                  "word_count": 88,
                                  "keywords": ["room booking", "cleanliness", "whiteboard care", "respect work"]
                                },
                                {
                                  "text": "6. SHARED KITECHEN RULES AND ETIQUETTE\n- Treat the shared office kitchen as your own.\n- Respect others and wait for your turn.\n- Move with care, the office kitchen space is limited, avoid fast and sudden movements as it can risk others dropping or breaking items and hurting yourself or others.\n- Respect the hygiene rules.\n- Clean after you have finished with using the kitchen.\n- Respect food property.\n- Report office kitchen issues and inform the office manager of any issue you cannot solve:\n  - Supplies such as paper towels run low.\n  - Something breaks.\n  - Office kitchen, a surface, or an appliance is very dirty.\n  - Someone always breaks the office kitchen rules.",
                                  "source": "Office Open Workspace Policy.pdf",
                                  "chunk_id": 29,
                                  "chunk_length": 592,
                                  "word_count": 107,
                                  "keywords": ["kitchen etiquette", "respect others", "safety precautions", "hygiene standards", "issue reporting"]
                                },
                                {
                                  "text": "7. SAFETY AND SECURITY\n- Never leave your laptop unattended. Make sure to lock up your laptop either using a dock station or locking it up in your drawer.\n- Make sure you connect your cables in a safe way to avoid any hazardous accidents.\n- Do not leave your personal belongings unattended.\n7.1 Confidentiality\n- Keep all confidential information in a secure place.\n- Do not leave confidential documents lying on your desktop or anywhere it can be easily accessed by unauthorized persons.\n- Use shredders to dispose all sensitive documents.\n7.2 Respect privacy\nIn addition to respecting the space of others in the office, respect their privacy.\n- Do not intentionally eavesdrop on a meeting, phone call or conversation.\n- Do not oversee any document that is not meant for you.\n7.3 Avoid strong smells\nCreate a scent-free work environment in the office and always be hygienic.\n- Avoid Strong smell food in the open workspace. Eating strong smell meals is only allowed in the designated areas.\n- The office is non-smoking area. Cigarettes, E-cigarettes, Iqos and Vapes are banned in the office and building. Smokers can only use and the designated smoking areas.",
                                  "source": "Office Open Workspace Policy.pdf",
                                  "chunk_id": 30,
                                  "chunk_length": 849,
                                  "word_count": 154,
                                  "keywords": ["laptop security", "cable safety", "confidentiality rules", "privacy respect", "scent policy", "smoking ban"]
                                },
                                {
                                  "text": "8. POLICY VIOLATION\nWhile we are working in an open office, setting rules and boundaries are important to keep the environment safe and if any are crossed, you can address the issue with your HR BP.\nBreaking the office rules and policy will subject you to HR warning, which will lead to lower performance grades and salary deductions.",
                                  "source": "Office Open Workspace Policy.pdf",
                                  "chunk_id": 31,
                                  "chunk_length": 311,
                                  "word_count": 55,
                                  "keywords": ["violation consequences", "HR warnings", "performance impact"]
                                },
                                {
                                    "text": "4. INTERNAL MOBILITY POLICY\n4.1 Eligibility\n- All SEITech Solutions employees who successfully completed their probation period and at least 6 months in a designated project are eligible to request internal mobility if an open position is available.\n- Employee must achieve minimum performance rating of â€˜Bâ€™ and no corrective actions for the previous 6-months period.",
                                    "source": "Internal & International Mobility Policy.pdf",
                                    "chunk_id": 32,
                                    "chunk_length": 369,
                                    "word_count": 66,
                                    "keywords": ["internal mobility", "eligibility criteria", "probation completion", "performance rating"]
                                },
                                {
                                    "text": "5. INTERNATIONAL MOBILITY POLICY\n5.1 Eligibility\n- All SEITech Solutions employees who successfully completed their probation period and at least 12 months within the company are eligible to request international mobility if an open position is available.\n- Employee must achieve minimum performance rating of â€˜Bâ€™ and no corrective actions for the previous 12-months period.",
                                    "source": "Internal & International Mobility Policy.pdf",
                                    "chunk_id": 33,
                                    "chunk_length": 376,
                                    "word_count": 67,
                                    "keywords": ["international mobility", "eligibility requirements", "tenure requirement", "performance standards"]
                                },
                                {
                                    "text": "6. GUIDELINES\n- SEITech solutions opt to create a culture that encourages its employees to explore new opportunities.\n- Internal jobs will be published internally.\n- Some open full-time jobs, depending on the job role and need, will be posted internally before publishing externally.\n- Hiring managers having an internal opening will communicate with the HR to publish the positions internally via our tool.\n- Employees who are interested in the open job position and have the needed qualifications, shall apply via our tool, or Email and notify his/her current manager.\n- The approval cycle should be done first by the HR BP then goes to current employee N+1.\n- The hiring manager & HR are responsible for confirming that the internal applicant meets the eligibility requirements for the new position with the final decision of acceptance or rejection.\n- The HR Team will be responsible for confirming that the internal applicant meets the eligibility requirements for company positions as per company policy.\n- Each application will be assessed on an individual basis depending on the business need and/or the available openings and whether the employeeâ€™s skills fit the requirements of the desired job.\n- Qualified internal applicant goes through interview cadence below:\n  - Technical Interview.\n  - Customer Interview if needed.\n  - HR/Management interview.\nIn the case of international mobility, the company covers the travel expenses, in case an interview is needed abroad.\nIf an internal applicant is selected, the current manager must solidify a transition date and timeline that ensures a seamless transition without impacting the current business operations.\nThe start date of the new position will be contingent on backfilling the current role of the applicant.",
                                    "source": "Internal & International Mobility Policy.pdf",
                                    "chunk_id": 34,
                                    "chunk_length": 1374,
                                    "word_count": 246,
                                    "keywords": ["job posting", "application process", "approval cycle", "eligibility confirmation", "interview process", "transition planning", "backfilling requirement"]
                                }
                            ]        
        self.vector_db = hardcoded_chunks
        print(f"Hardcoded database initialized with {len(self.vector_db)} chunks")
        
        # Generate embeddings for the hardcoded data
        self.create_embeddings()
    
    def create_embeddings(self) -> None:
        """
        Generate embeddings for all chunks in the vector database
        """
        if not self.vector_db:
            print("No chunks to embed.")
            return
        
        print("Generating embeddings...")
        texts = [chunk['text'] for chunk in self.vector_db]
        
        # Generate embeddings in batches to avoid memory issues
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embedding_model.encode(batch, convert_to_tensor=True)
            all_embeddings.append(batch_embeddings)
        
        # Concatenate all embeddings
        self.embeddings = torch.cat(all_embeddings, dim=0)
        print(f"Generated embeddings shape: {self.embeddings.shape}")
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text for better search
        """
        # Simple keyword extraction - remove stopwords and get important terms
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'do', 'does', 'did', 'get', 'got', 'go', 'goes', 'went', 'come', 'came', 'take', 'took', 'make', 'made', 'see', 'saw', 'know', 'knew', 'think', 'thought', 'say', 'said', 'tell', 'told', 'ask', 'asked', 'work', 'worked', 'try', 'tried', 'use', 'used', 'want', 'wanted', 'need', 'needed', 'give', 'gave', 'put', 'set', 'find', 'found', 'call', 'called', 'move', 'moved', 'live', 'lived', 'feel', 'felt', 'become', 'became', 'leave', 'left', 'turn', 'turned', 'start', 'started', 'show', 'showed', 'hear', 'heard', 'play', 'played', 'run', 'ran', 'move', 'moved', 'like', 'liked', 'back', 'just', 'now', 'then', 'here', 'there', 'where', 'when', 'why', 'how', 'what', 'who', 'which', 'all', 'any', 'each', 'every', 'some', 'many', 'much', 'more', 'most', 'other', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'well', 'also'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stopwords]
        
        # Get most frequent keywords
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(10)]
    
    def search_similar_chunks(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Search for similar chunks using hybrid search
        """
        return self.hybrid_search(query, top_k)
    
    def hybrid_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Combine semantic search with keyword matching for better accuracy
        """
        if self.embeddings is None:
            return []
        
        # Semantic search
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        
        # Keyword matching
        query_keywords = set(self.extract_keywords(query))
        
        # Combine scores
        combined_scores = []
        for i, chunk in enumerate(self.vector_db):
            semantic_score = cosine_scores[i].item()
            
            # Keyword overlap score
            chunk_keywords = set(chunk.get('keywords', []))
            keyword_overlap = len(query_keywords.intersection(chunk_keywords))
            keyword_score = keyword_overlap / max(len(query_keywords), 1)
            
            # Text similarity score (simple)
            text_score = 0
            query_lower = query.lower()
            chunk_lower = chunk['text'].lower()
            for word in query_lower.split():
                if word in chunk_lower:
                    text_score += 1
            text_score = text_score / len(query.split())
            
            # Combined score (weighted)
            combined_score = (0.6 * semantic_score + 0.3 * keyword_score + 0.1 * text_score)
            
            combined_scores.append({
                'index': i,
                'semantic_score': semantic_score,
                'keyword_score': keyword_score,
                'text_score': text_score,
                'combined_score': combined_score
            })
        
        # Sort by combined score
        combined_scores.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Return top results
        results = []
        for item in combined_scores[:top_k]:
            result = self.vector_db[item['index']].copy()
            result['similarity_score'] = item['combined_score']
            result['semantic_score'] = item['semantic_score']
            result['keyword_score'] = item['keyword_score']
            results.append(result)
        
        return results
    
    def answer_question(self, query: str, top_k: int = 3) -> str:
        """
        Answer a question based on the hardcoded database content - returns only the answer text
        """
        # Search for relevant chunks
        relevant_chunks = self.search_similar_chunks(query, top_k)
        
        if not relevant_chunks:
            return "Sorry, this information is not provided in the documents."
        
        # Check if the best match meets the minimum accuracy threshold
        best_similarity = relevant_chunks[0]['similarity_score']
        
        if best_similarity < self.min_accuracy_threshold:
            return "Sorry, this information is not provided in the documents."
        
        # Filter chunks that meet the threshold
        filtered_chunks = [chunk for chunk in relevant_chunks 
                          if chunk['similarity_score'] >= self.min_accuracy_threshold]
        
        if not filtered_chunks:
            return "Sorry, this information is not provided in the documents."
        
        # Create context from filtered chunks
        context_parts = []
        
        for chunk in filtered_chunks:
            context_parts.append(chunk['text'])
        
        # Return the combined context as the answer
        return "\n\n".join(context_parts)
    
    def get_database_info(self) -> Dict:
        """
        Get information about the current database
        """
        if not self.vector_db:
            return None
        
        info = {
            'total_chunks': len(self.vector_db),
            'sources': list(set(chunk['source'] for chunk in self.vector_db)),
            'threshold': self.min_accuracy_threshold,
            'total_words': sum(chunk['word_count'] for chunk in self.vector_db),
            'avg_chunk_length': sum(chunk['chunk_length'] for chunk in self.vector_db) / len(self.vector_db)
        }
        return info
    