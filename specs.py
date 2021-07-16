class RequestVerb:
    """Verbs specified in RKSOK specs for requests."""

    GET = "ОТДОВАЙ"
    WRITE = "ЗОПИШИ"
    DELETE = "УДОЛИ"


class ResponseStatus:
    """Response statuses specified in RKSOK specs for responses."""

    OK = "НОРМАЛДЫКС"
    INCORRECT = "НИПОНЯЛ"
    NOT_FOUND = "НИНАШОЛ"
    NOT_APPROVED = "НИЛЬЗЯ"


class ValidationStatus:
    """Validation statuses specified in RKSOK specs for requests."""

    CHECK = "АМОЖНА?"
    ACCEPT = "МОЖНА"
    REJECT = "НИЛЬЗЯ"
