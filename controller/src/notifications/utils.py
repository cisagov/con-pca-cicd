def get_notification(message_type: str) -> str:
    if message_type == "monthly_report":
        subject = "Con-PCA Monthly Report"
        path = "monthly_report"
    elif message_type == "quarterly_report":
        subject = "Con-PCA Monthly Report"
        path = "quarterly_report"
    elif message_type == "yearly_report":
        subject = "Con-PCA Monthly Report"
        path = "yearly_report"
    else:
        subject = ""
        path = ""
    return subject, path
