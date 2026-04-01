import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Maintenance Schedule",
            "fieldname": "maintenance_schedule",
            "fieldtype": "Link",
            "options": "Maintenance Schedule",
            "width": 180,
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140,
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 240,
        },
        {
            "label": "Scheduled Date",
            "fieldname": "scheduled_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Sales Order",
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150,
        },
        {
            "label": "Job Card No",
            "fieldname": "job_card_no",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Quotation Ref",
            "fieldname": "quotation_ref",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Building No/Name",
            "fieldname": "building",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Maintenance Visit",
            "fieldname": "maintenance_visit",
            "fieldtype": "Link",
            "options": "Maintenance Visit",
            "width": 180,
        },
        {
            "label": "Visit Date",
            "fieldname": "visit_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Completion Status",
            "fieldname": "completion_status",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": "Technician",
            "fieldname": "technician",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Work Done / Remarks",
            "fieldname": "remarks",
            "fieldtype": "Small Text",
            "width": 260,
        },
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters.get("from_date"):
        conditions.append("msd.scheduled_date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("msd.scheduled_date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    if filters.get("customer"):
        conditions.append("ms.customer = %(customer)s")
        values["customer"] = filters.get("customer")

    if filters.get("sales_order"):
        conditions.append("msi.sales_order = %(sales_order)s")
        values["sales_order"] = filters.get("sales_order")

    if filters.get("item_code"):
        conditions.append("msi.item_code = %(item_code)s")
        values["item_code"] = filters.get("item_code")

    where_clause = ""
    if conditions:
        where_clause = " AND " + " AND ".join(conditions)

    return frappe.db.sql(
        f"""
        SELECT
            ms.name AS maintenance_schedule,
            ms.customer_name AS customer,
            msi.item_code,
            msi.item_name,
            msd.scheduled_date,
            msi.sales_order,

            so.custom_job_card_no AS job_card_no,
            so.custom_quotation_ref AS quotation_ref,
            so.custom_building_nameno AS building,

            mv.name AS maintenance_visit,
            mv.mntc_date AS visit_date,
            mv.completion_status AS completion_status,

            mvp.service_person AS technician,
            mvp.work_done AS remarks

        FROM `tabMaintenance Schedule` ms

        LEFT JOIN `tabMaintenance Schedule Item` msi
            ON msi.parent = ms.name
            AND msi.parenttype = 'Maintenance Schedule'

        LEFT JOIN `tabMaintenance Schedule Detail` msd
            ON msd.parent = ms.name
            AND msd.parenttype = 'Maintenance Schedule'
            AND msd.item_code = msi.item_code

        LEFT JOIN `tabSales Order` so
            ON so.name = msi.sales_order

        LEFT JOIN `tabMaintenance Visit` mv
            ON mv.maintenance_schedule = ms.name
            AND mv.mntc_date = msd.scheduled_date

        LEFT JOIN `tabMaintenance Visit Purpose` mvp
            ON mvp.parent = mv.name
            AND mvp.parenttype = 'Maintenance Visit'

        WHERE ms.docstatus < 2
        {where_clause}

        ORDER BY ms.name, msd.scheduled_date, mv.name
        """,
        values,
        as_dict=1,
    )