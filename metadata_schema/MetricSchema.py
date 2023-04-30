from pydantic import BaseModel
from typing import Optional

class BaseMetric(BaseModel):
    """Base metric model
    Base information about URS table/metrics
    
    Fields
    ------
    state_name: str
        Name of state
        Ex., Alabama
    year: int
        Year of data submission
        Ex., 2009
    domain: str
        SAMHSA domain that a URS table is a part of
        Ex., "ACCESS"
    table_name: str
        Name of a URS aggregate table
        Ex., "Utilization Rates/Number of Consumers Served"
    metric_name: str
        Name of a metric in a URS aggregate table
        Ex., "Penetration Rate per 1000 population"
    metric_result: float
        Metric result represented as a float
        Ex., 15.0
    """
    state_name: str
    year: int
    domain: str
    table_name: str
    metric_name: str
    metric_result: float

class ClientMetricExt(BaseMetric):
    """Client metric extended
    Extended information for client-based metrics
    
    Fields
    ------
    age: [Optional]str
        Age categories used for demographic metrics
        Ex., 0-12
    adult_or_child: [Optional]str
        Aggregate categories to define adult vs. child metric
        Ex., "Adult"
    gender: [Optional]str
        Gender categories used for demographic metrics
        Ex., "Female"
    race: [Optional]str
        Race categories used for demographic metrics
        Ex., "Asian"
    ethnicity: [Optional]str
        Ethnicity categories used for demographic metrics
        Ex., "Hispanic or Latino Ethnicity"
    living_situation: [Optional]str
        Living situation categories used for demographic metrics
        Ex., "Private Residence"
    employment_status: [Optional]str
        Employment status categories used for demographic metrics
        Ex., "Employed"
    SMI_SED: [Optional]bool
        Indicator to specify if a metric is specific to SMI/SED clients
        Ex., 0 = not SMI/SED, 1 = SMI/SED
    ESMI: [Optional]bool
        Indicator to specify if a metric is specific to ESMI clients
        Ex., 0 = not ESMI, 1 = ESMI
    """
    age: Optional[str]
    adult_or_child: Optional[str]
    gender: Optional[str]
    race: Optional[str]
    ethnicity: Optional[str]
    living_situation: Optional[str]
    employment_status: Optional[str]
    SMI_SED: Optional[bool]
    ESMI: Optional[bool]

class ServiceMetricExt(BaseMetric):
    """Service metric extended
    Extended information for service-based metrics
    
    Fields
    ------
    service_type: [Optional]str
        Service type categories used for service metrics
        Ex., "Assertive Community Treatment"
    service_location: [Optional]str
        Service location categories used for service metrics
        Ex., "State Hospitals"
    """
    service_type: Optional[str]
    service_location: Optional[str]