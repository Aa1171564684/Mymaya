for i in range(self.layout.count()):
	self.layout.itemAt(i).widget().deleteLater()