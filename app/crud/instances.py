"""Pre-built CRUD instances for each model."""

from app.crud.base import CRUDBase
from app.models import (
    AgriDrug,
    AgriDrugApplication,
    CropType,
    Farmer,
    FarmerLandPlot,
    FarmingPeriod,
    LandPlot,
    Report,
    Role,
    User,
    UserRole,
    VisitMedia,
)

user = CRUDBase(User, "user_id")
role = CRUDBase(Role, "role_id")
user_role = CRUDBase(UserRole, "user_role_id")
farmer = CRUDBase(Farmer, "farmer_id")
land_plot = CRUDBase(LandPlot, "land_plot_id")
farmer_land_plot = CRUDBase(FarmerLandPlot, "farmer_land_plot_id")
crop_type = CRUDBase(CropType, "crop_type_id")
agri_drug = CRUDBase(AgriDrug, "agri_drug_id")
farming_period = CRUDBase(FarmingPeriod, "farming_period_id")
report = CRUDBase(Report, "report_id")
visit_media = CRUDBase(VisitMedia, "visit_media_id")
agri_drug_application = CRUDBase(AgriDrugApplication, "drug_application_id")
