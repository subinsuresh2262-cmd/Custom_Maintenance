import frappe
from frappe.utils import add_days, add_months, cint, getdate
from erpnext.maintenance.doctype.maintenance_schedule.maintenance_schedule import (
    MaintenanceSchedule,
)


class CustomMaintenanceSchedule(MaintenanceSchedule):
    def validate(self):
        # keep validations only; do not auto-generate schedules on save
        self.validate_end_date_visits()

    def get_next_schedule_date(self, current_date, periodicity):
        if periodicity == "Weekly":
            return add_days(current_date, 7)
        elif periodicity == "Monthly":
            return add_months(current_date, 1)
        elif periodicity == "Quarterly":
            return add_months(current_date, 3)
        elif periodicity == "Half Yearly":
            return add_months(current_date, 6)
        elif periodicity == "Yearly":
            return add_months(current_date, 12)
        else:
            return current_date

    @frappe.whitelist()
    def generate_schedule(self):
        if self.docstatus != 0:
            return

        self.set("schedules", [])
        count = 1

        for d in self.get("items"):
            start_date = getdate(d.start_date)
            no_of_visits = cint(d.no_of_visits)
            periodicity = d.periodicity

            current_date = start_date

            for i in range(no_of_visits):
                child = self.append("schedules")
                child.item_code = d.item_code
                child.item_name = d.item_name
                child.scheduled_date = current_date

                if getattr(d, "serial_no", None):
                    child.serial_no = d.serial_no

                child.idx = count
                count += 1
                child.sales_person = d.sales_person
                child.completion_status = "Pending"
                child.item_reference = d.name

                current_date = self.get_next_schedule_date(current_date, periodicity)
