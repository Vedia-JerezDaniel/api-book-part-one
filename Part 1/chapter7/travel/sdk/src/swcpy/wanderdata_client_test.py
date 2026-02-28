# %%
import httpx
# import swcpy.swc_config as config
# from .schemas import League, Team, Player, Performance, Counts
from typing import List
import backoff
import logging
logger = logging.getLogger(__name__)

# %%
class SWCCLient: 
    def __init__(self, swc_base_url: str): 
        self.swc_base_url = swc_base_url 
    def get_health_check(self): 
        # make the API call 
        with httpx.Client(base_url=self.swc_base_url) as client: 
            return client.get("/")


# %%

# %%


# %%



