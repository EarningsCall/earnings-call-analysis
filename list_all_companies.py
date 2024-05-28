import earningscall
from earningscall import get_all_companies
from earningscall.utils import enable_debug_logs


with open(".earnings-call-api-key", "r") as fd:
    earningscall.api_key = fd.read().strip()
enable_debug_logs()

for company in get_all_companies():
    print(f"{company.company_info} -- {company.company_info.sector} -- {company.company_info.industry}")
