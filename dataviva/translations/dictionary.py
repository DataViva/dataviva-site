# -*- coding: utf-8 -*-
from flask.ext.babel import gettext, ngettext

def dictionary():

    return {

        # App Titles
        "compare": gettext("Compare"),
        "occugrid": gettext("Occugrid"),
        "geo_map": gettext("Geo Map"),
        "network": gettext("Network"),
        "rings": gettext("Rings"),
        "scatter": gettext("Scatter"),
        "stacked": gettext("Stacked"),
        "tree_map": gettext("Tree Map"),

        # Time Resolution Toggle
        "time": gettext("Time Resolution"),
        "time_desc_stacked": gettext("Changes the time resolution between yearly and monthly."),
        "time_desc_line": gettext("Changes the time resolution between yearly and monthly."),

        # Axes
        "axes": gettext("Axes"),
        "axes_desc_compare": gettext("Changes the X and Y variables used in the chart."),
        "x": gettext("X Axis"),
        "x_desc_scatter": gettext("Changes the X axis variable."),
        "y": gettext("Y Axis"),
        "y_desc_stacked": gettext("Changes the Y axis variable."),
        "y_desc_scatter": gettext("Changes the Y axis variable."),
        "y_desc_line": gettext("Changes the Y axis variable."),
        "y_desc_box": gettext("Changes the Y axis variable."),

        # Stacked Area Sorting/Order
        "order": gettext("Order"),
        "sort_desc_stacked": gettext("Changes the ordering of the visible areas based on the selected sorting."),
        "asc": gettext("Ascending"),
        "desc": gettext("Descending"),

        # Stacked Area Layout Type
        "layout": gettext("Layout"),
        "layout_desc_stacked": gettext("Changes the X axis between value and market share."),
        "value": gettext("Value"),
        "share": gettext("Market Share"),

        # RCA Scope Toggle
        "rca_scope": gettext("RCA Scope"),
        "rca_scope_desc_network": gettext("Changes which RCA variable is used when highlighting products in the visualization."),
        "rca_scope_desc_rings": gettext("Changes which RCA variable is used when highlighting products in the visualization."),
        "rca_scope_desc_scatter": gettext("Changes which RCA variable is used when highlighting products in the visualization."),
        "bra_rca": gettext("Domestic"),
        "wld_rca": gettext("International"),

        # Scale Toggle
        "scale": gettext("Scale"),
        "scale_desc_compare": gettext("Changes the mathematical scale used on both axes."),
        "scale_desc_line": gettext("Changes the mathematical scale used on both axes."),
        "scale_desc_box": gettext("Changes the mathematical scale used on both axes."),
        "log": gettext("Log"),
        "linear": gettext("Linear"),

        # Spotlight Toggle
        "spotlight": gettext("Highlight RCA"),
        "spotlight_desc_network": gettext("Removes coloring from nodes which do not have RCA."),
        "spotlight_scatter": gettext("Hide RCA"),
        "spotlight_scatter_desc_scatter": gettext("Hides nodes that have RCA."),
        "true": gettext("On"),
        "false": gettext("Off"),

        # Sorting Toggle
        "sorting": gettext("Sort"),
        "sort": gettext("Sort"),
        "order_desc_stacked": gettext("Changes the variable used to order the areas."),
        "order_desc_occugrid": gettext("Changes the variable used to order the donut charts."),

        # Sizing Labels
        "sizing": gettext("Size"),
        "sizing_desc_tree_map": gettext("Changes the variable used to size the rectangles."),
        "sizing_desc_network": gettext("Changes the variable used to size the circles."),
        "sizing_desc_compare": gettext("Changes the variable used to size the circles."),
        "sizing_desc_occugrid": gettext("Changes the variable used to size the circles."),
        "sizing_desc_scatter": gettext("Changes the variable used to size the circles."),

        # Color Labels
        "color_toggle": gettext("Color"),
        "color_desc_tree_map": gettext("Changes the variable used to color the rectangles."),
        "color_desc_stacked": gettext("Changes the variable used to color the areas."),
        "color_desc_geo_map": gettext("Changes the variable used to color the locations."),
        "color_desc_network": gettext("Changes the variable used to color the circles."),
        "color_desc_rings": gettext("Changes the variable used to color the circles."),
        "color_desc_compare": gettext("Changes the variable used to color the circles."),
        "color_desc_occugrid": gettext("Changes the variable used to color the circles."),
        "color_desc_scatter": gettext("Changes the variable used to color the circles."),

        # Other Control Labels
        "active": gettext("Available"),
        "available": gettext("Available"),
        "not_available": gettext("Not available"),
        "grouping": gettext("Grouping"),
        "grouping_desc_occugrid": gettext("Groups the donut charts into different categorizations."),
        "none": gettext("None"),
        "year": gettext("Year"),
        "month_1": gettext("Jan"),
        "month_2": gettext("Feb"),
        "month_3": gettext("Mar"),
        "month_4": gettext("Apr"),
        "month_5": gettext("May"),
        "month_6": gettext("Jun"),
        "month_7": gettext("Jul"),
        "month_8": gettext("Aug"),
        "month_9": gettext("Sep"),
        "month_10": gettext("Oct"),
        "month_11": gettext("Nov"),
        "month_12": gettext("Dec"),

        # Filter Depths
        "depth": gettext("Depth"),
        "depth_desc_tree_map": gettext("Changes the level of aggregation."),
        "depth_desc_stacked": gettext("Changes the level of aggregation."),
        "depth_desc_geo_map": gettext("Changes the level of aggregation."),
        "depth_desc_network": gettext("Changes the level of aggregation."),
        "depth_desc_rings": gettext("Changes the level of aggregation."),
        "depth_desc_compare": gettext("Changes the level of aggregation."),
        "depth_desc_occugrid": gettext("Changes the level of aggregation."),
        "depth_desc_scatter": gettext("Changes the level of aggregation."),
        "depth_desc_line": gettext("Changes the level of aggregation."),
        "bra_1": gettext("Region"),
        "bra_3": gettext("State"),
        "bra_5": gettext("Mesoregion"),
        "bra_7": gettext("Microregion"),
        "bra_8": gettext("Planning Region"),
        "bra_9": gettext("Municipality"),
        "cbo_1": gettext("Main Group"),
        "cbo_2": gettext("Principal Subgroup"),
        "cbo_3": gettext("Subgroup"),
        "cbo_4": gettext("Family"),
        "cbo_6": gettext("Occupation"),
        "cnae_1": gettext("Section"),
        "cnae_3": gettext("Division"),
        "cnae_4": gettext("Group"),
        "cnae_6": gettext("Class"),
        "hs_2": gettext("Section"),
        "hs_4": gettext("Chapter"),
        "hs_6": gettext("Position"),
        "hs_8": gettext("Sub-Position"),
        "wld_2": gettext("Continent"),
        "wld_5": gettext("Country"),
        "bra_1_plural": gettext("Regions"),
        "bra_3_plural": gettext("States"),
        "bra_5_plural": gettext("Mesoregions"),
        "bra_7_plural": gettext("Microregions"),
        "bra_8_plural": gettext("Planning Regions"),
        "bra_9_plural": gettext("Municipalities"),
        "cbo_1_plural": gettext("Main Groups"),
        "cbo_2_plural": gettext("Principal Subgroups"),
        "cbo_3_plural": gettext("Subgroups"),
        "cbo_4_plural": gettext("Families"),
        "cbo_6_plural": gettext("Occupations"),
        "cnae_1_plural": gettext("Sections"),
        "cnae_3_plural": gettext("Divisions"),
        "cnae_4_plural": gettext("Groups"),
        "cnae_6_plural": gettext("Classes"),
        "hs_2_plural": gettext("Sections"),
        "hs_4_plural": gettext("Chapters"),
        "hs_6_plural": gettext("Positions"),
        "hs_8_plural": gettext("Sub-Positions"),
        "wld_2_plural": gettext("Continents"),
        "wld_5_plural": gettext("Countries"),
        "course_hedu": gettext("Major"),
        "course_hedu_2": gettext("Field"),
        "course_hedu_6": gettext("Major"),
        "course_hedu_plural": gettext("Majors"),
        "course_hedu_2_plural": gettext("Fields"),
        "course_hedu_6_plural": gettext("Majors"),
        "course_sc": gettext("Course"),
        "course_sc_2": gettext("Field"),
        "course_sc_5": gettext("Course"),
        "course_sc_plural": gettext("Courses"),
        "course_sc_2_plural": gettext("Fields"),
        "course_sc_5_plural": gettext("Courses"),
        "university": gettext("University"),
        "university_5": gettext("University"),
        "university_plural": gettext("Universities"),
        "university_5_plural": gettext("Universities"),
        "school_8": gettext("Vocational School"),
        "school_8_plural": gettext("Vocational Schools"),

        # Calculation Labels
        "eci": gettext("Economic Complexity"),
        "eci_desc": gettext("Economic Complexity measures how diversified and complex a location's export production is."),
        "pci": gettext("Product Complexity"),
        "pci_desc": gettext("Product Complexity is a measure of how complex a product is, based on how many countries export the product and how diversified those exporters are."),

        "bra_diversity": gettext("Location Diversity"),
        "bra_diversity_desc": gettext("The number of unique municipalities where a given variable is present."),
        "bra_diversity_eff": gettext("Effective Location Diversity"),
        "bra_diversity_eff_desc": gettext("The diversity of a given variable corrected for the share that each unit represents."),

        "cnae_diversity": gettext("Industry Diversity"),
        "cnae_diversity_desc": gettext("The number of unique 6-digit CNAE industries that are present for a given variable."),
        "cnae_diversity_eff": gettext("Effective Industry Diversity"),
        "cnae_diversity_eff_desc": gettext("The diversity of a given variable corrected for the share that each unit represents."),

        "cbo_diversity": gettext("Occupation Diversity"),
        "cbo_diversity_desc": gettext("The number of unique 4-digit CBO occupations that are present for a given variable."),
        "cbo_diversity_eff": gettext("Effective Occupation Diversity"),
        "cbo_diversity_eff_desc": gettext("The diversity of a given variable corrected for the share that each unit represents."),

        "hs_diversity": gettext("Product Diversity"),
        "hs_diversity_desc": gettext("The number of unique HS4 products that are present for a given variable."),
        "hs_diversity_eff": gettext("Effective Product Diversity"),
        "hs_diversity_eff_desc": gettext("The diversity of a given variable corrected for the share that each unit represents."),

        "wld_diversity": gettext("Export Destination Diversity"),
        "wld_diversity_desc": gettext("The number of unique import countries that are present for a given variable."),
        "wld_diversity_eff": gettext("Effective Export Destination Diversity"),
        "wld_diversity_eff_desc": gettext("The diversity of a given variable corrected for the share that each unit represents."),

        "distance": gettext("Distance"),
        "distance_desc": gettext('Distance is a measure used to indicate how "far away" any given location is from a particular industry, occupation or product.'),
        "distance_wld": gettext("International Distance"),
        "employed": gettext("Employed"),
        "importance": gettext("Importance"),
        "importance_desc": gettext("Importance measures the ubiquity of a given occupation in a particular industry. Occupations with a high importance in an industry are commonly employed in said industry."),
        "elsewhere": gettext("Employees Available In Other Industries"),
        "required": gettext("Estimated Employees"),
        "required_desc": gettext("The number of employees needed in order to have RCA in an industry in a particular location, based on the averages of locations with similar industrial composition and RCA in the specific industry."),
        "required_bras": gettext("Similar Locations"),
        "required_bras_desc": gettext("These are the locations that were used to calculate the number of Estimated Employees for this location:"),
        "growth_val": gettext("Wage Growth"),
        "growth_val_total": gettext("Cumulative Wage Growth"),
        "proximity": gettext("Proximity"),
        "rca": gettext("Domestic RCA"),
        "rca_desc": gettext("Revealed Comparative Advantage is a numeric value used to connote whether a particular product or industry is especially prominent in a location."),
        "rca_wld": gettext("International RCA"),

        "opp_gain": gettext("Opportunity Gain"),
        "opp_gain_desc": gettext("Opportunity gain is a measure that indicates how much diversity is offered by an industry or product should the given location develop it."),
        "opp_gain_wld": gettext("International Opportunity Gain"),

        "export_val_growth": gettext("Nominal Export Growth (1 year)"),
        "export_val_growth_5": gettext("Nominal Export Growth (5 year)"),
        "import_val_growth": gettext("Nominal Import Growth (1 year)"),
        "import_val_growth_5": gettext("Nominal Import Growth (5 year)"),

        "wage_growth": gettext("Nominal Wage Growth (1 year)"),
        "wage_growth_5": gettext("Nominal Wage Growth (5 year)"),
        "num_emp_growth": gettext("Nominal Employee Growth (1 year)"),
        "num_emp_growth_5": gettext("Nominal Employee Growth (5 year)"),

        "enrolled_growth": gettext("Nominal Enrollment Growth (1 year)"),
        "enrolled_growth_5": gettext("Nominal Enrollment Growth (5 years)"),
        "graduates_growth": gettext("Nominal Graduation Growth (1 year)"),

        # RAIS Labels
        "rais": gettext("Wages and Employment (RAIS)"),
        "rais_footer": gettext("Data provided by RAIS"),
        "num_emp": gettext("Total Employees"),
        "num_est": gettext("Total Establishments"),
        "num_emp_est": gettext("Employees per Establishment"),
        "wage": gettext("Total Monthly Wages"),
        "total_wage": gettext("Total Monthly Wage"),
        "wage_avg": gettext("Average Monthly Wage"),
        "wage_avg_bra": gettext("Brazilian Average Wage"),

        # SECEX Labels
        "secex": gettext("International Trade (SECEX)"),
        "secex_footer": gettext("Data provided by SECEX"),
        "val_usd": gettext("Trade Value"),
        "export_val": gettext("Exports"),
        "export_kg": gettext("Export Weight"),
        "export_val_kg": gettext("Exports per kg"),
        "total_export_val": gettext("Total Exports"),
        "import_val": gettext("Imports"),
        "import_kg": gettext("Import Weight"),
        "import_val_kg": gettext("Imports per kg"),
        "total_import_val": gettext("Total Imports"),
        "trade_balance": gettext("Trade Balance"),
        "direction": gettext("Exports/Imports"),
        "exports": gettext("Exports"),
        "imports": gettext("Imports"),
        "origin": gettext("Origin"),
        "destination": gettext("Destination"),
        "origins": gettext("Import Origins"),
        "destinations": gettext("Export Destinations"),
        "to": gettext("to"),
        "from": gettext("from"),

        # HEDU Labels
        "hedu": gettext("Higher Education"),
        "hedu_footer": gettext("Data provided by INEP/MEC"),
        "enrolled": gettext("Enrolled"),
        "school_type": gettext("Funding"),

        # SC Labels
        "sc": gettext("School Census"),
        "sc_footer": gettext("Data provided by INEP/MEC"),
        "classes": gettext("Classes"),
        "enrolled_classes": gettext("Average Class Size"),
        "age": gettext("Average Age"),

        # EI Labels
        "ei": gettext("Electronic Invoices (EI)"),
        "ei_footer": gettext("Data provided by SEF/MG"),
        "purchase_value": gettext("Purchase Value"),
        "purchase": gettext("Purchase"),
        "transfer_value": gettext("Transfer Value"),
        "transfer": gettext("Transfer"),

        # Key Labels
        "brazil": gettext("Brazil"),
        "bra_id": gettext("BRA ID"),
        "category": gettext("Sector"),
        "cbo_id": gettext("CBO ID"),
        "color": gettext("Sector"),
        "display_id": gettext("ID"),
        "hs_id": gettext("HS ID"),
        "id_ibge": gettext("IBGE ID"),
        "id": gettext("ID"),
        "cnae_id": gettext("CNAE ID"),
        "name": gettext("Name"),
        "name_en": gettext("Name (English)"),
        "name_pt": gettext("Name (Portuguese)"),
        "population": gettext("Population"),
        "top": gettext("Top"),
        "wld_id": gettext("WLD ID"),
        "id_mdic": gettext("MDIC ID"),
        "rank": " ",
        "university_id": gettext("ID"),
        "course_hedu_id": gettext("ID"),
        "course_sc_id": gettext("ID"),
        "course_id": gettext("ID"),

        # Filter Titles
        "bra": gettext("Location"),
        "bra_plural": gettext("Locations"),
        "cbo": gettext("Occupation"),
        "cbo_plural": gettext("Occupations"),
        "hs": gettext("Product"),
        "hs_plural": gettext("Products"),
        "cnae": gettext("Industry"),
        "cnae_plural": gettext("Industries"),
        "wld": gettext("Trade Partner"),
        "wld_plural": gettext("Trade Partners"),
        "university": gettext("University"),
        "university_plural": gettext("Universities"),
        "course_hedu": gettext("Major"),
        "course_hedu_plural": gettext("Majors"),
        "school": gettext("Vocational School"),
        "school_plural": gettext("Vocational Schools"),
        "course_sc": gettext("Vocational Course"),
        "course_sc_plural": gettext("Vocational Courses"),
        "bra_s": gettext("Sending Location"),
        "bra_s_plural": gettext("Sending Locations"),
        "bra_r": gettext("Receiving Location"),
        "bra_r_plural": gettext("Receiving Locations"),
        "icon": gettext("Icon"),

        # File Types
        "download": gettext("Download"),
        "download_desc": gettext("Choose from the following file types:"),
        "csv": gettext("Save as CSV"),
        "csv_desc": gettext("A table format that can be imported into a database or opened with Microsoft Excel."),
        "pdf": gettext("Save as PDF"),
        "pdf_desc": gettext("Similar to SVG files, PDF files are vector-based and can be dynamically scaled."),
        "png": gettext("Save as PNG"),
        "png_desc": gettext("A standard image file, similar to JPG or BMP."),
        "svg": gettext("Save as SVG"),
        "svg_desc": gettext("A vector-based file that can be resized without worrying about pixel resolution."),

        # App Builder
        "basics": gettext("Basic Values"),
        "growth": gettext("Growth"),
        "calculations": gettext("Strategic Indicators"),
        "Data Provided by": gettext("Data Provided by"),
        "View more visualizations on the full DataViva.info website.": gettext("View more visualizations on the full DataViva.info website."),
        "related_apps": gettext("Related Visualizations"),
        "other_apps": gettext("Other Visualizations"),
        "crosswalk_hs": gettext("Common Industries"),
        "crosswalk_cnae": gettext("Common Products"),
        "crosswalk_cbo": gettext("Common Majors"),
        "crosswalk_course_hedu": gettext("Common Occupations"),
        "Show All Years": gettext("Show Historical Data"),
        "Build Not Available": gettext("Build Not Available"),
        "Building Visualization": gettext("Building Visualization"),
        "Downloading Additional Years": gettext("Downloading Historical Data"),
        "all_years": gettext("Click to download all available historical data. This may take a long time depending on your internet connection."),
        "and": gettext("and"),
        "showing": gettext("Showing only"),
        "excluding": gettext("Excluding"),
        "of": gettext("of"),
        "with": gettext("with"),
        "and": gettext("and"),
        "fill": gettext("Fill"),
        "embed_url": gettext("Embed URL"),
        "share_url": gettext("Shortened URL"),
        "social_media": gettext("Social Networks"),
        "secex_3": gettext("Based on State Production"),
        "secex_9": gettext("Based on the Exporting Municipality"),
        "embed_footer": gettext("View more visualizations on the full DataViva.info website."),

        "no_brazil": gettext("This visualization is not available when selecting the entirity of Brazil. Please select a more grainular location."),
        "no_deepest": gettext("This visualization is only available at the deepest nesting. Please select a more grainular filter."),

        # D3plus Text
        "Click for More Info": gettext("Click for more data and related visualizations."),
        "Click to Zoom": gettext("Click to Zoom"),
        "filter": gettext("Hide Group"),
        "solo": gettext("Solo Group"),
        "reset": gettext("Click to Reset all Filters"),
        "Primary Connections": gettext("Primary Connections"),
        "No Data Available": gettext("No Data Available"),
        "No Connections Available": gettext("No Connections Available"),

        # Ask Sabrina
        "Asked": gettext("Asked"),
        "by": gettext("by"),
        "point": gettext("Point"),
        "points": gettext("Points"),
        "reply": gettext("Reply"),
        "replies": gettext("Replies"),
        "votes": gettext("Most Active"),
        "newest": gettext("Most Recent"),
        "questions": gettext("Questions"),
        "learnmore": gettext("User Question"),
        "learnmore_plural": gettext("Learn more"),
        "flagged": gettext("This reply has been flagged."),
        "unflagged": gettext("This flag on this reply has been removed."),
        "voted": gettext("Your vote has been added."),
        "unvoted": gettext("Your vote was removed."),
        "classifications": gettext("Classifications"),

        # Admin
        "edit": gettext("Edit"),
        "visible": gettext("Visible"),
        "hidden": gettext("Hidden"),
        "user": gettext("User"),
        "admin": gettext("Admin"),
        "remove": gettext("Remove"),
        "remove_confirmation": gettext("Are you sure to delete this item?"),

        # Selector & Search
        "search": gettext("Search"),
        "search_results": gettext("Search Results"),
        "other": gettext("Other"),
        "select": gettext("Select"),
        "show": gettext("Show"),
        "loading_attrs": gettext("Loading Attribute List"),
        "loading_items": gettext("Loading More Items"),
        "wait": gettext("Please Wait"),
        "back": gettext("Back"),
        "remove_filter": gettext("Remove this Filter"),
        "Municipalities within": gettext("Municipalities within"),
        "No municipalities within that distance.": gettext("No municipalities within that distance."),
        "Including": gettext("Including"),
        "in": gettext("in"),
        "no_items": gettext("No Data Available")

    }

def plurals(key=None, n=1):

    plurals = {

        # Number Formatting
        "T": ngettext("Trillion", "Trillions", n),
        "B": ngettext("Billion", "Billions", n),
        "M": ngettext("Million", "Millions", n),
        "k": ngettext("Thousand", "Thousands", n),

    }

    if key:
        return unicode(plurals[key]) if key in plurals else None
    return plurals
