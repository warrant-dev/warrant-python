from warrant.api_resource import APIResource, WarrantException
from warrant.list_result import ListResult
from warrant.object import Object
from warrant.warrant import Warrant, Subject, QueryResult
from warrant.authz import Authz, CheckOp

from warrant.feature import Feature
from warrant.permission import Permission
from warrant.pricing_tier import PricingTier
from warrant.role import Role

from warrant.user import User
from warrant.tenant import Tenant

__version__ = "3.1.0"

api_key = ""
api_endpoint = "https://api.warrant.dev"
self_service_dashboard_base_url = "https://self-serve.warrant.dev"
user_agent = "warrant-python/" + __version__
