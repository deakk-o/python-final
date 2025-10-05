from PyQt5.QtWidgets import  QMainWindow
from phobias_design import Ui_MainWindow
from phobia import Phobia
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import qdarktheme


class MplCanvas(FigureCanvas):      #Canvas კლასის აღწერა დიაგრამების აპლიკაციაში გამოსახვისთვის
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class MyApp(QMainWindow, Ui_MainWindow):   #აპლიკაციის კლასის აღწერა
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.canvas = MplCanvas(self, width=8, height=7, dpi=100)
        self.widget.layout().addWidget(self.canvas)
        self.diagram_button.clicked.connect(self.plots_button)
        self.add_button.clicked.connect(self.add_phobia)
        self.update_button.clicked.connect(self.update_phobia)
        self.delete_button.clicked.connect(self.delete_phobia)
        self.listWidget.itemClicked.connect(self.load_selected_phobia)
        self.canvas_most_common_fears = MplCanvas(self, width=10, height=7, dpi=100)
        self.widget.layout().addWidget(self.canvas_most_common_fears)
        self.checkBox.stateChanged.connect(self.toggle_theme)
        self.checkBox.setChecked(False)


    def load_phobia(self):      #ბაზის ჩანაწერების დამატება list widget-ში
        self.phobia_list = self.db.fetch_phobia()
        self.listWidget.clear()
        for each in self.phobia_list:
            self.listWidget.addItem(str(each))

    def load_selected_phobia(self):     #input ველების შევსება სიიდან არჩეული მონაცემების შესაბამისად
        item = self.listWidget.currentItem()
        if item:
            selected = item.text()
            self.selected_name = selected.split(",")[0]
            phobia = next(p for p in self.phobia_list if p.name == self.selected_name)
        else:
            return

        self.name_line.setText(phobia.name)
        self.age_line.setText(str(phobia.age))
        self.phobia_line.setText(phobia.phobia)


    def add_phobia(self):   #ფობიის დამატება list widget-ში
        if self.ready_box.isChecked():
            if self.radioButton_1.isChecked():
                phobia = Phobia(self.name_line.text(), int(self.age_line.text()), self.programme_combo.currentText(),
                                int(self.radioButton_1.text()),  self.phobia_line.text(),
                                int(self.fear_combo.currentText()))
            elif self.radioButton_2.isChecked():
                phobia = Phobia(self.name_line.text(), int(self.age_line.text()), self.programme_combo.currentText(),
                                int(self.radioButton_2.text()),  self.phobia_line.text(),
                                int(self.fear_combo.currentText()))
            elif self.radioButton_3.isChecked():
                phobia = Phobia(self.name_line.text(), int(self.age_line.text()), self.programme_combo.currentText(),
                                int(self.radioButton_3.text()),  self.phobia_line.text(),
                                int(self.fear_combo.currentText()))
            elif self.radioButton_4.isChecked():
                phobia = Phobia(self.name_line.text(), int(self.age_line.text()), self.programme_combo.currentText(),
                                int(self.radioButton_4.text()),  self.phobia_line.text(), int(self.fear_combo.currentText()))


        self.db.insert_phobia(phobia)
        self.load_phobia()
        self.create_plot()
        self.create_most_common_fears_plot()

    def update_phobia(self):  #ჩანაწერის განახლება
        if hasattr(self, 'selected_name'):
           if self.radioButton_1.isChecked():
                phobia = Phobia(self.name_line.text(),
                        int(self.age_line.text()),
                        self.programme_combo.currentText(),
                        int(self.radioButton_1.text()),
                        self.phobia_line.text(),
                        int(self.fear_combo.currentText()))
           elif self.radioButton_2.isChecked():
                phobia = Phobia(self.name_line.text(),
                            int(self.age_line.text()),
                            self.programme_combo.currentText(),
                            int(self.radioButton_2.text()),
                            self.phobia_line.text(),
                            int(self.fear_combo.currentText()))
           elif self.radioButton_3.isChecked():
                phobia = Phobia(self.name_line.text(),
                            int(self.age_line.text()),
                            self.programme_combo.currentText(),
                            int(self.radioButton_3.text()),
                            self.phobia_line.text(),
                            int(self.fear_combo.currentText()))
           elif self.radioButton_4.isChecked():
                phobia = Phobia(self.name_line.text(),
                            int(self.age_line.text()),
                            self.programme_combo.currentText(),
                            int(self.radioButton_4.text()),
                            self.phobia_line.text(),
                            int(self.fear_combo.currentText()))

           self.db.update_phobia(phobia)
           self.load_phobia()
           self.create_plot()
           self.create_most_common_fears_plot()

    def delete_phobia(self):   #შესაბამისი ჩანაწერის წაშლა
        if hasattr(self, 'selected_name'):
            self.db.delete_phobia(self.selected_name)
            self.load_phobia()
            self.create_plot()
            self.create_most_common_fears_plot()

    def create_plot(self):  #წრიული დიაგრამის შექმნა
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        data = self.db.num_people()
        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Pie plot according to programmes")
        self.canvas.draw()

    def create_most_common_fears_plot(self): #სვეტოვანი დიაგრამა
        self.canvas_most_common_fears.fig.clear()
        ax = self.canvas_most_common_fears.fig.add_subplot(111)
        data = self.db.most_common_fears()
        phobias = [row[0] for row in data]
        counts = [row[1] for row in data]
        if not phobias:
            ax.text(0.5, 0.5, "No phobia data available",
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, color=qdarktheme.get_text_colors()[0])
        else:
            ax.barh(phobias, counts, color='lightcoral')
            ax.set_xlabel('Number of People')
            ax.set_ylabel('Phobia')
            ax.set_title('Most Common Fears')
            ax.invert_yaxis()

        self.canvas_most_common_fears.draw()

    def plots_button(self):   #ფუნქციონალი ღილაკთან დასაკავშირებლად
        self.create_plot()
        self.create_most_common_fears_plot()

    def toggle_theme(self):    #dark mode-ის ფუნქციის აღწერა
        if self.checkBox.isChecked():
            qdarktheme.setup_theme("dark")
        else:
            qdarktheme.setup_theme("light")
