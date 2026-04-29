from pydantic import BaseModel, FieldValidationInfo, field_validator, conint, constr


class Address(BaseModel):
    id: int
    street: str
    city: str

    @field_validator("id")
    def id_must_be_positive(cls, v, info: FieldValidationInfo):
        if v <= 0:
            raise ValueError("id must be positive")
        return v

    @field_validator("street")
    def street_between_2_50(cls, v, info: FieldValidationInfo):
        if len(v) < 2 or len(v) > 50:
            raise ValueError("Street must be between 2 and 50")
        return v


try:
    user = Address(id=1, street="Hasi", city="Prishtina")
except ValueError as e:
    print(e)