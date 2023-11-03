import dash_bootstrap_components as dbc
import dash_html_components as html
import data_cleanup


# supplier dropdown
def create_dropdown_supplier_selector(list_of_suppliers_d):
    children_list = []
    for i in list_of_suppliers_d:
        children_list.append(dbc.DropdownMenuItem(i))

    dropdown = dbc.DropdownMenu(
        label="Suppliers",
        menu_variant="dark",
        children=children_list,
        className="d-grid gap-2 d-md-flex justify-content-md-end",
        align_end=True
    )

    return dropdown


# CARDS
def create_display_cards(current_stocks_d, period_sales_d, stock_ratio_d, unique_stock_refs_d, unique_sales_refs_d, stockout_ref_count_d):
    current_stocks_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(current_stocks_d, className="card-title"),
                    html.H6("Current stocks", className="card-subtitle"),
                ]
            ),
        )

    period_sales_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(period_sales_d, className="card-title"),
                    html.H6("Period sales", className="card-subtitle"),
                ]
            ),
        )

    stock_ratio_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(stock_ratio_d, className="card-title"),
                    html.H6("Stock Ratio", className="card-subtitle"),
                ]
            ),
        )

    unique_stock_refs_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(unique_stock_refs_d, className="card-title"),
                    html.H6("Number of SKUs", className="card-subtitle"),
                ]
            ),
        )

    unique_sales_refs_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(unique_sales_refs_d, className="card-title"),
                    html.H6("Unique Products Sold", className="card-subtitle"),
                ]
            ),
        )

    stockout_ref_count_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(stockout_ref_count_d, className="card-title"),
                    html.H6("Stockout Risk Count", className="card-subtitle"),
                ]
            ),
        )

    return current_stocks_card, period_sales_card, stock_ratio_card, unique_stock_refs_card, unique_sales_refs_card, stockout_ref_count_card
