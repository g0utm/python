import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class EventPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Planner")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.centralWidget())

        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)
        self.calendar.clicked.connect(self.date_selected)

        self.date_label = QLabel("Date:", self)
        layout.addWidget(self.date_label)

        self.date_entry = QLineEdit(self)
        layout.addWidget(self.date_entry)

        self.event_label = QLabel("Event:", self)
        layout.addWidget(self.event_label)

        self.event_entry = QLineEdit(self)
        layout.addWidget(self.event_entry)

        self.add_button = QPushButton("Add Event", self)
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_event)

        self.save_button = QPushButton("Save as PDF", self)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_as_pdf)

        self.events = {}

    def date_selected(self, date):
        self.selected_date = date
        self.date_entry.setText(date.toString("yyyy-MM-dd"))

    def add_event(self):
        event_date = self.date_entry.text()
        event_text = self.event_entry.text()

        if event_date and event_text:
            if event_date not in self.events:
                self.events[event_date] = []
            self.events[event_date].append(event_text)
            self.calendar.setDateTextFormat(self.selected_date, self.calendar.dateTextFormat(self.selected_date) + f"\n{event_text}")
        else:
            print("Please select a date and provide an event.")

    def save_as_pdf(self):
        c = canvas.Canvas("event_calendar.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)
        for date, events in self.events.items():
            c.drawString(100, 750, date)
            for i, event in enumerate(events):
                c.drawString(120, 750 - (i + 1) * 20, f"- {event}")
            c.showPage()
        c.save()
        print("PDF saved successfully.")

def main():
    app = QApplication(sys.argv)
    planner = EventPlanner()
    planner.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
