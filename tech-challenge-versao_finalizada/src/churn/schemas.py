from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
YesNo = Literal["Yes", "No"]
InternetOption = Literal["Yes", "No", "No internet service"]

class Customer(BaseModel):
    # Campos extras costumam indicar erro de integração (ou envio do alvo Churn).
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    gender: Literal["Female", "Male"]
    SeniorCitizen: Literal[0, 1]
    Partner: YesNo
    Dependents: YesNo
    tenure: int = Field(ge=0, le=1200)
    PhoneService: YesNo
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: InternetOption
    OnlineBackup: InternetOption
    DeviceProtection: InternetOption
    TechSupport: InternetOption
    StreamingTV: InternetOption
    StreamingMovies: InternetOption
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: YesNo
    PaymentMethod: Literal["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    MonthlyCharges: float = Field(ge=0, le=10000)
    TotalCharges: float | None = Field(default=None, ge=0, le=10000000)

    @model_validator(mode="after")
    def consistent_services(self):
        # "No phone service" descreve ausência de serviço; não é igual a "No".
        if (self.PhoneService == "No") != (self.MultipleLines == "No phone service"):
            raise ValueError("MultipleLines incompatível com PhoneService")
        for field in ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]:
            if (self.InternetService == "No") != (getattr(self, field) == "No internet service"):
                raise ValueError(f"{field} incompatível com InternetService")
        return self

class Prediction(BaseModel):
    churn_probability: float = Field(ge=0, le=1)
    churn_prediction: int
    threshold: float
    model_name: str
