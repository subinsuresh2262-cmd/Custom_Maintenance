frappe.query_reports["Maintenance Schedule Detailed Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date"
		},
		{
			fieldname: "customer",
			label: "Customer",
			fieldtype: "Link",
			options: "Customer"
		},
		{
			fieldname: "sales_order",
			label: "Sales Order",
			fieldtype: "Link",
			options: "Sales Order"
		},
		{
			fieldname: "item_code",
			label: "Item Code",
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname: "show_all",
			label: "Show All",
			fieldtype: "Check",
			default: 0
		}
	]
};