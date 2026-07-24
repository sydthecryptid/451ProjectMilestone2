#sydnee boothby, cpts 451, milestone 2, business search app
# need to work through naming conventions and commenting, but it works

# business search app prototype, connects to .ui file
# run with: python business_search_App.py

# edit ui with command: QT_QPA_PLATFORM=xcb .venv/lib/python3.12/site-packages/qt6_applications/Qt/bin/designer business_search.ui
# use command to find designer: find .venv -iname "*designer*" -type f -executable


import sys
import psycopg2
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem

DB_PARAMS = dict( #databaseparameters to allow query
    dbname="yelpdb",
    user="sydnee",
    host="localhost",
    password="password",
)

def run_query(query, params=None): 
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


class BusinessSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("business_search.ui", self)
 
        self.selected_category = None
        self._configure_tables()
 
        # connect ui elements to query functions
        self.stateCombo.currentTextChanged.connect(self.on_state_selected)
        self.cityList.currentTextChanged.connect(self.on_city_selected)
        self.zipcodeList.currentTextChanged.connect(self.on_zip_selected)
        self.categoryList.currentTextChanged.connect(self.on_category_selected)
        self.searchButton.clicked.connect(self.search_businesses)
        self.clearCategoryButton.clicked.connect(self.clear_category_filter)
        self.pushButton.clicked.connect(self.refresh_results)
    
        self.load_states()

    def _configure_tables(self):
        self.resultsTable.setColumnCount(6)
        self.resultsTable.setHorizontalHeaderLabels(
            ["Business Name", "Address", "City", "Stars", "Review Count", "Checkins"]
        )

        self.zipcodeResults.setColumnCount(2)
        self.zipcodeResults.setHorizontalHeaderLabels(["Metric", "Value"])

        self.popularResults.setColumnCount(3)
        self.popularResults.setHorizontalHeaderLabels(
            ["Business Name", "Total Check-Ins", "Review Count"]
        )

        self.successfulResults.setColumnCount(2)
        self.successfulResults.setHorizontalHeaderLabels(["Business Name", "Rating"])

    def _clear_results(self, table):
        table.setRowCount(0)

    def _populate_table(self, table, rows):
        table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()

    def _selected_zipcode(self):
        zipcode_item = self.zipcodeList.currentItem()
        return zipcode_item.text() if zipcode_item else None

    def set_status(self, text): #for debugging, set status label or print to console

        if hasattr(self, "statusLabel"):
            self.statusLabel.setText(text)
        else:
            print(text)

    #below are functions to populate each part of the ui
     
    # populate states
    def load_states(self):
        rows = run_query("SELECT DISTINCT state FROM address ORDER BY state;")
        self.stateCombo.clear()
        self.stateCombo.addItem("")
        for (state,) in rows:
            self.stateCombo.addItem(state)
 
    # populate each city 
    def on_state_selected(self, state):
        self.cityList.clear() #clear previous selections before new
        self.zipcodeList.clear()
        self.categoryList.clear()
        self._clear_results(self.resultsTable)
        self._clear_results(self.popularResults)
        self._clear_results(self.successfulResults)
        self._clear_results(self.zipcodeResults)
 
        if not state:
            return
 
        rows = run_query(
            "SELECT DISTINCT city FROM address WHERE state = %s ORDER BY city;",
            (state,),
        )
        for (city,) in rows:
            self.cityList.addItem(city)
        self.set_status(f"Loaded {len(rows)} cities for {state}.")
 
    # zipcodes depend on city selection
    def on_city_selected(self, city):
        self.zipcodeList.clear()
        self.categoryList.clear()
        self._clear_results(self.resultsTable)
        self._clear_results(self.popularResults)
        self._clear_results(self.successfulResults)
        self._clear_results(self.zipcodeResults)
 
        if not city:
            return
 
        state = self.stateCombo.currentText()
        rows = run_query(
            "SELECT DISTINCT zipcode FROM address WHERE city = %s AND state = %s ORDER BY zipcode;",
            (city, state),
        )
        for (zipcode,) in rows:
            self.zipcodeList.addItem(zipcode)
        self.set_status(f"Loaded {len(rows)} zipcodes for {city}, {state}.")
 
    # get all business categories for zipcode chosen
    def on_zip_selected(self, zipcode):
        self.categoryList.clear()
        self._clear_results(self.resultsTable)
        self._clear_results(self.popularResults)
        self._clear_results(self.successfulResults)
        self._clear_results(self.zipcodeResults)
        self.selected_category = None
 
        if not zipcode:
            return
 
        rows = run_query(
            """
            SELECT DISTINCT bc.categoryTitle
            FROM BusinessCategory bc
            JOIN Business b ON bc.businessID = b.businessID
            JOIN Address a ON b.addressID = a.addressID
            WHERE a.zipcode = %s
            ORDER BY bc.categoryTitle;
            """,
            (zipcode,),
        )
        for (cat,) in rows:
            self.categoryList.addItem(cat)
        self.set_status(f"Loaded {len(rows)} categories for zipcode {zipcode}.")
        self.refresh_results()
 
    def on_category_selected(self, category):
        self.selected_category = category if category else None
 
    def clear_category_filter(self):
        self.categoryList.clearSelection()
        self.selected_category = None
        self.set_status("Category filter cleared.")
 
    # search businesses based on zipcode and category (opt)
    def search_businesses(self):
        zipcode = self._selected_zipcode()
        if not zipcode:
            self.set_status("Please select a zipcode first.")
            return
    
        if self.selected_category:
            rows = run_query(
                """
                SELECT b.name, a.street, a.city, b.stars, b.reviewCount, b.totalCheckins
                FROM Business b
                JOIN Address a ON b.addressID = a.addressID
                JOIN BusinessCategory bc ON b.businessID = bc.businessID
                WHERE a.zipcode = %s AND bc.categoryTitle = %s
                ORDER BY b.name;
                """,
                (zipcode, self.selected_category),
            )
        else:
            rows = run_query(
                """
                SELECT b.name, a.street, a.city, b.stars, b.reviewCount, b.totalCheckins
                FROM Business b
                JOIN Address a ON b.addressID = a.addressID
                WHERE a.zipcode = %s
                ORDER BY b.name;
                """,
                (zipcode,),
            )
    
        self._populate_table(self.resultsTable, rows)
 
        self.set_status(f"Found {len(rows)} businesses.") #change status after search 

    def popular_businesses(self):
        zipcode = self._selected_zipcode()


        if not zipcode:
            self.set_status("No zipcode selected...")
            return

        rows = run_query( #query to find popular businesses within given zip 
            """
            SELECT b.name, b.totalCheckins, b.reviewCount
            FROM Business b
            JOIN Address a ON b.addressID = a.addressID
            WHERE a.zipcode = %s AND b.popularityStatus = TRUE
            ORDER BY b.name;
            """,
            (zipcode,),
        )

        self._populate_table(self.popularResults, rows)
        self.set_status(f"Found {len(rows)} popular businesses.")

    def successful_businesses(self):
        zipcode = self._selected_zipcode()

        if not zipcode:
            self.set_status("No zipcode selected...")
            return

        rows = run_query(
            """
            SELECT b.name, b.averageReviewRating
            FROM Business b
            JOIN Address a ON b.addressID = a.addressID
            WHERE a.zipcode = %s AND b.successStatus = TRUE
            ORDER BY b.name;
            """,
            (zipcode,),
        )
        self._populate_table(self.successfulResults, rows)
        self.set_status(f"Found {len(rows)} successful businesses.")

    def refresh_results(self):
        zipcode = self._selected_zipcode()
        if not zipcode:
            self.set_status("No zipcode selected...")
            return

        self.search_businesses()
        self.popular_businesses()
        self.successful_businesses()

        stats_rows = run_query(
            """
            SELECT 'Businesses in zipcode', COALESCE(MAX(z.businessCount)::text, 'N/A')
            FROM Zipcode z
            WHERE z.zipcode = %s
            UNION ALL
            SELECT 'Population', COALESCE(MAX(z.population)::text, 'N/A')
            FROM Zipcode z
            WHERE z.zipcode = %s
            UNION ALL
            SELECT 'Average Income', COALESCE(MAX(z.averageIncome)::text, 'N/A')
            FROM Zipcode z
            WHERE z.zipcode = %s;
            """,
            (zipcode, zipcode, zipcode),
        )
        self._populate_table(self.zipcodeResults, stats_rows)


if __name__ == "__main__": 
    app = QApplication([])
    window = BusinessSearchApp()
    window.show()
    app.exec()