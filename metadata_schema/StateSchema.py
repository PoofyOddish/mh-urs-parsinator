from pydantic import BaseModel,HttpUrl

class State(BaseModel):
    """State model
    Information about state submissions
    
    Fields
    ------
    id: str
        FIPS code for state
        Ex., "01" = Alabama
    name: str
        State name
        Ex., Alabama
    urs_url: HttpUrl
        Full URL to URS PDF on SAMHSA website
        Ex., https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf
    year: int
        Year of URS submission
        Ex., 2009
    """
     
    id: str
    name: str
    url: HttpUrl
    year: int