import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, 
    QTextEdit, QFrame, QTreeView, QSplitter, QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap

class StyleSheet:
    MAIN_STYLE = """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QFrame {
            background-color: white;
            border-radius: 8px;
            margin: 5px;
        }
        
        QPushButton {
            background-color: #2c3e50;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background-color: #34495e;
        }
        
        QLineEdit, QComboBox {
            padding: 6px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
        }
        
        QTextEdit {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
        }
        
        QLabel[heading="true"] {
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px;
        }
        
        #titleFrame {
            background-color: white;
            border-radius: 8px;
            margin: 10px;
            padding: 20px;
        }
    """

class CustomFrame(QFrame):
    def __init__(self, title=None):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setProperty("frameStyle", "panel")
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        if title:
            label = QLabel(title)
            label.setProperty("heading", True)
            self.layout.addWidget(label)

class RadioMenuBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCS Radio Menu Builder")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        # Initialize data
        self.menus = []
        self.commands = []

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        
         # Add Title and Logo Section
        title_frame = QFrame()
        title_frame.setFixedHeight(180)  # Reduced height since we're going horizontal
        title_frame.setObjectName("titleFrame")
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 10, 20, 10)  # Add some padding
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            title_layout.addWidget(logo_label)

        # Title Label
        title_label = QLabel("LOCK-ON GREECE RADIO MENU BUILDER")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        title_layout.addWidget(title_label)
        
        # Add stretch at the end to push everything to the left
        title_layout.addStretch()
        
        main_layout.addWidget(title_frame)

        # Content Layout
        content_layout = QHBoxLayout()

        # Left Panel Content
        left_panel = QVBoxLayout()
        menu_frame = CustomFrame("Menu Builder")
        menu_frame.layout.addLayout(self.create_menu_form())
        left_panel.addWidget(menu_frame)

        command_frame = CustomFrame("Command Builder")
        command_frame.layout.addLayout(self.create_command_form())
        left_panel.addWidget(command_frame)

        # Right Panel Content
        right_panel = QVBoxLayout()
        preview_frame = CustomFrame("Menu Structure Preview")
        self.structure_preview = QTreeView()
        self.structure_preview.setHeaderHidden(True)
        self.structure_preview.setSelectionMode(QTreeView.SingleSelection)  
        # Disable right-click context menu
        self.structure_preview.setContextMenuPolicy(Qt.NoContextMenu)
        # Override mouse double click event to do nothing
        self.structure_preview.mouseDoubleClickEvent = lambda event: None
        preview_frame.layout.addWidget(self.structure_preview)
        right_panel.addWidget(preview_frame)

        lua_frame = CustomFrame("Generated Lua Code")
        self.lua_code_output = QTextEdit()
        self.lua_code_output.setReadOnly(True)
        lua_frame.layout.addWidget(self.lua_code_output)

        # Add Copy Button
        copy_button = QPushButton("Copy Lua Code")
        copy_button.clicked.connect(self.copy_lua_code)
        lua_frame.layout.addWidget(copy_button)

        right_panel.addWidget(lua_frame)

        # Action Buttons
        button_frame = CustomFrame()
        button_layout = QHBoxLayout()
        
        buttons = [
            ("Save Menu", self.save_project),
            ("Load Menu", self.load_project),
            ("Export Lua Code", self.export_lua_code)
        ]
        
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            button_layout.addWidget(btn)
        
        button_frame.layout.addLayout(button_layout)
        right_panel.addWidget(button_frame)

                # Add Reset and Delete buttons to button_layout
        reset_button = QPushButton("Reset Menu")
        reset_button.clicked.connect(self.reset_everything)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        button_layout.addWidget(reset_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected_item)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        button_layout.addWidget(delete_button)

        # Add panels to content layout
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])

        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)

    def create_menu_form(self):
        form_layout = QFormLayout()
        
        # Menu ID input
        self.menu_id_input = QLineEdit()
        form_layout.addRow("Menu ID:", self.menu_id_input)
        self.menu_id_input.setToolTip("Enter a unique non-numerical ID for the menu")
        self.menu_id_input.setPlaceholderText("Enter menu ID...")
        
        # Menu Name input
        self.menu_name_input = QLineEdit()
        form_layout.addRow("Menu Name:", self.menu_name_input)
        self.menu_name_input.setToolTip("Enter a name for your menu")
        self.menu_name_input.setPlaceholderText("Enter menu name...")
        
        # Submenu dropdown
        self.submenu_dropdown = QComboBox()
        self.submenu_dropdown.addItem("nil")
        form_layout.addRow("Parent Menu:", self.submenu_dropdown)
        
        # Coalition dropdown
        self.coalition_dropdown = QComboBox()
        self.coalition_dropdown.addItems(["blue", "red"])
        form_layout.addRow("Coalition:", self.coalition_dropdown)
        
        # Add Menu button
        add_menu_button = QPushButton("Add Menu")
        add_menu_button.clicked.connect(self.add_menu)
        form_layout.addRow(add_menu_button)
        
        return form_layout

    def create_command_form(self):
        form_layout = QFormLayout()
        
        # Menu dropdown
        self.menu_dropdown = QComboBox()
        form_layout.addRow("Menu:", self.menu_dropdown)
        
        # Command Name input
        self.command_name_input = QLineEdit()
        form_layout.addRow("Command Name:", self.command_name_input)
        self.command_name_input.setToolTip("Enter a name for your command")
        self.command_name_input.setPlaceholderText("Enter command name...")
        
        # Action Type Selection
        self.action_type = QComboBox()
        self.action_type.addItems(["Set Flag", "Custom Code"])
        self.action_type.currentTextChanged.connect(self.on_action_type_changed)
        form_layout.addRow("Action Type:", self.action_type)
        
        # Flag inputs widget
        self.flag_widget = QWidget()
        flag_layout = QFormLayout(self.flag_widget)
        self.flag_input = QLineEdit()
        self.value_input = QLineEdit()
        self.flag_input.setToolTip("Enter a flag name")
        self.value_input.setToolTip("Enter a flag value")
        self.flag_input.setPlaceholderText("Enter flag name...")
        self.value_input.setPlaceholderText("Enter flag value...")
        flag_layout.addRow("Flag:", self.flag_input)
        flag_layout.addRow("Value:", self.value_input)
        
        # Custom code widget
        self.custom_widget = QWidget()
        custom_layout = QFormLayout(self.custom_widget)
        self.custom_code_input = QTextEdit()
        self.custom_code_input.setPlaceholderText("Enter Lua code here...")
        custom_layout.addRow("Custom Code:", self.custom_code_input)
        
        # Add widgets to form
        form_layout.addRow(self.flag_widget)
        form_layout.addRow(self.custom_widget)
        
        # Initially show only flag inputs
        self.custom_widget.hide()
        
        # Add Command button
        add_command_button = QPushButton("Add Command")
        add_command_button.clicked.connect(self.add_command)
        form_layout.addRow(add_command_button)
        
        return form_layout

    def on_action_type_changed(self, action_type):
        self.flag_widget.hide()
        self.custom_widget.hide()
        
        if action_type == "Set Flag":
            self.flag_widget.show()
        else:  # Custom Code
            self.custom_widget.show()

    def add_menu(self):
        menu_id = self.menu_id_input.text()
        menu_name = self.menu_name_input.text()
        submenu = self.submenu_dropdown.currentText()
        coalition = self.coalition_dropdown.currentText()
        
        if not menu_id or not menu_name:
            QMessageBox.warning(self, "Input Error", "Menu ID and Name are required!")
            return
        
        self.menus.append((menu_id, menu_name, submenu, coalition))
        self.menu_dropdown.addItem(menu_id)
        self.submenu_dropdown.addItem(menu_id)
        
        self.update_tree_view()
        self.update_lua_code()
        
        # Clear inputs
        self.menu_id_input.clear()
        self.menu_name_input.clear()

    def add_command(self):
        menu_id = self.menu_dropdown.currentText()
        command_name = self.command_name_input.text()
        action_type = self.action_type.currentText()
        
        if not menu_id or not command_name:
            QMessageBox.warning(self, "Input Error", "Menu ID and Command Name are required!")
            return
        
        command_data = {
            'menu_id': menu_id,
            'name': command_name,
            'type': action_type
        }
        
        if action_type == "Set Flag":
            flag = self.flag_input.text()
            value = self.value_input.text()
            
            if not flag or not value:
                QMessageBox.warning(self, "Input Error", "Flag and Value are required!")
                return
                
            try:
                value = int(value)
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Value must be a number!")
                return
                
            command_data['flag'] = flag
            command_data['value'] = value
            
        else:  # Custom Code
            custom_code = self.custom_code_input.toPlainText()
            
            if not custom_code:
                QMessageBox.warning(self, "Input Error", "Custom code is required!")
                return
                
            command_data['code'] = custom_code
        
        self.commands.append(command_data)
        self.update_tree_view()
        self.update_lua_code()
        self.clear_command_inputs()


    def update_tree_view(self):
        print("Updating tree view")
        print("Current menus:", self.menus)
        print("Current commands:", self.commands)
        
        model = QStandardItemModel()
        root = model.invisibleRootItem()
        
        # Create a dictionary to store menu items
        menu_items = {}
        
        # First pass: create all menu items
        for menu_id, menu_name, submenu, coalition in self.menus:
            item = QStandardItem(f"{menu_id}: {menu_name} ({coalition})")
            menu_items[menu_id] = item
        
        # Second pass: build the hierarchy
        for menu_id, menu_name, submenu, coalition in self.menus:
            item = menu_items[menu_id]
            if submenu == "nil":
                root.appendRow(item)
            else:
                if submenu in menu_items:
                    menu_items[submenu].appendRow(item)
        
        # Add commands to their respective menus
        for command in self.commands:
            menu_id = command['menu_id']
            if menu_id in menu_items:
                if command['type'] == "Set Flag":
                    display_text = f"{command['name']} (Flag: {command['flag']}, Value: {command['value']})"
                else:
                    display_text = f"{command['name']} (Custom Code)"
                command_item = QStandardItem(display_text)
                menu_items[menu_id].appendRow(command_item)
        
        self.structure_preview.setModel(model)
        self.structure_preview.expandAll()

    def update_lua_code(self):
        lua_code = "-- Radio Menu Structure\n\n"
        
        # Helper function to get all commands for a specific menu
        def get_menu_commands(menu_id):
            return [cmd for cmd in self.commands if cmd['menu_id'] == menu_id]

        # Helper function to get direct submenus of a menu
        def get_direct_submenus(parent_id):
            return [menu for menu in self.menus if menu[2] == parent_id]

        # Helper function to generate menu and its commands recursively
        def generate_menu_code(menu_data, processed_menus=None):
            if processed_menus is None:
                processed_menus = set()

            menu_id, menu_name, submenu, coalition = menu_data
            
            # Skip if already processed
            if menu_id in processed_menus:
                return ""
            
            processed_menus.add(menu_id)
            code = ""
            
            # Add the menu definition
            coalition_str = f"coalition.side.{coalition.upper()}"
            code += f"local {menu_id} = missionCommands.addSubMenuForCoalition({coalition_str}, \"{menu_name}\", {submenu})\n"
            
            # Add commands for this menu
            menu_commands = get_menu_commands(menu_id)
            for command in menu_commands:
                if command['type'] == "Set Flag":
                    flag = command['flag']
                    # If flag can be converted to int, use it as is, otherwise keep as string
                    try:
                        flag = int(flag)
                        flag_str = str(flag)  # No quotes for numbers
                    except ValueError:
                        flag_str = f"\"{flag}\""  # Quotes for strings
                    
                    code += (f"missionCommands.addCommandForCoalition({coalition_str}, "
                            f"\"{command['name']}\", {menu_id}, function() "
                            f"trigger.action.setUserFlag({flag_str}, {command['value']}); "
                            f"timer.scheduleFunction(function() trigger.action.setUserFlag({flag_str}, 0) end, nil, timer.getTime() + 1) end)\n")
                else:  # Custom Code
                    code += (f"missionCommands.addCommandForCoalition({coalition_str}, "
                            f"\"{command['name']}\", {menu_id}, function() {command['code']} end)\n")
            
            # Process submenus
            submenus = get_direct_submenus(menu_id)
            for submenu in submenus:
                code += generate_menu_code(submenu, processed_menus)
            
            return code

        # Start with top-level menus (those with submenu="nil")
        top_level_menus = [menu for menu in self.menus if menu[2] == "nil"]
        
        # Add menus section
        lua_code += "-- Menus\n"
        for menu in top_level_menus:
            lua_code += generate_menu_code(menu)
        
        # Update the text area
        self.lua_code_output.setText(lua_code)

    def copy_lua_code(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lua_code_output.toPlainText())
        QMessageBox.information(self, "Success", "Lua code copied to clipboard!")

    def save_project(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Menu",
            "",
            "JSON files (*.json);;All Files (*)"
        )
        
        if file_name:
            data = {
                'menus': self.menus,
                'commands': self.commands
            }
            
            try:
                with open(file_name, 'w') as f:
                    json.dump(data, f, indent=4)
                QMessageBox.information(self, "Success", "Menu saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving menu: {str(e)}")

    def load_project(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Menu",
            "",
            "JSON files (*.json);;All Files (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    data = json.load(f)
                
                # Validate the loaded data structure
                if not isinstance(data, dict) or 'menus' not in data or 'commands' not in data:
                    raise ValueError("Invalid menu file format")
                
                self.menus = data['menus']
                self.commands = data['commands']
                
                # Update UI
                self.menu_dropdown.clear()
                self.submenu_dropdown.clear()
                self.submenu_dropdown.addItem("nil")
                
                for menu_id, _, _, _ in self.menus:
                    self.menu_dropdown.addItem(menu_id)
                    self.submenu_dropdown.addItem(menu_id)
                
                self.update_tree_view()
                self.update_lua_code()
                
                QMessageBox.information(self, "Success", "Menu loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading menu: {str(e)}")

    def export_lua_code(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export Lua Code",
            "",
            "Lua Files (*.lua);;All Files (*)"
        )
        
        if file_name:
            if not file_name.endswith('.lua'):
                file_name += '.lua'
                
            try:
                with open(file_name, 'w') as f:
                    f.write(self.lua_code_output.toPlainText())
                QMessageBox.information(self, "Success", "Lua code exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export Lua code: {str(e)}")

    def reset_everything(self):
        # Ask for confirmation
        reply = QMessageBox.question(self, 'Confirmation',
                                'This will reset all your inputs. Are you sure?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Clear all data structures
            self.menus = []
            self.commands = []
            
            # Reset all input fields
            self.menu_id_input.clear()
            self.menu_name_input.clear()
            self.clear_command_inputs()
            
            # Reset dropdowns
            self.menu_dropdown.clear()
            self.submenu_dropdown.clear()
            self.submenu_dropdown.addItem("nil")
            
            # Clear the tree view and lua code
            self.update_tree_view()
            self.update_lua_code()
            
            QMessageBox.information(self, "Success", "Inputs have been reset!")

    def delete_selected_item(self):
        index = self.structure_preview.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Warning", "Please select an item to delete!")
            return

        model = self.structure_preview.model()
        item = model.itemFromIndex(index)
        item_text = item.text()

        reply = QMessageBox.question(self, 'Confirmation',
                                f'Are you sure you want to delete "{item_text}"?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            parent_index = index.parent()
            
            # If it has a parent, it's a command
            if parent_index.isValid():
                parent_text = model.itemFromIndex(parent_index).text()
                parent_menu_id = parent_text.split(":")[0].strip()
                command_name = item_text.split(" (")[0].strip()
                
                # Check if this is actually a submenu in our menus array
                is_submenu = False
                for menu in self.menus:
                    if menu[0] == command_name.split(":")[0].strip() and menu[2] != 'nil':
                        is_submenu = True
                        menu_id = menu[0]
                        break

                if is_submenu:
                    # Delete submenu and its commands
                    self.menus = [menu for menu in self.menus if menu[0] != menu_id]
                    self.commands = [cmd for cmd in self.commands if cmd['menu_id'] != menu_id]
                    
                    # Update dropdowns
                    self.menu_dropdown.clear()
                    self.submenu_dropdown.clear()
                    self.submenu_dropdown.addItem("nil")
                    for menu_id, _, _, _ in self.menus:
                        self.menu_dropdown.addItem(menu_id)
                        self.submenu_dropdown.addItem(menu_id)
                else:
                    # Delete command
                    print(f"Deleting command: {command_name} from menu {parent_menu_id}")
                    print(f"Before deletion - Commands count: {len(self.commands)}")
                    
                    self.commands = [cmd for cmd in self.commands 
                                if not (cmd['menu_id'] == parent_menu_id and cmd['name'] == command_name)]
                    
                    print(f"After deletion - Commands count: {len(self.commands)}")
            
            # If it has no parent, it's a menu
            else:
                menu_id = item_text.split(":")[0].strip()
                print(f"Deleting menu: {menu_id}")
                
                # Remove menu and its commands
                self.menus = [menu for menu in self.menus if menu[0] != menu_id]
                # Also remove any submenus that have this menu as parent
                self.menus = [menu for menu in self.menus if menu[2] != menu_id]
                self.commands = [cmd for cmd in self.commands if cmd['menu_id'] != menu_id]
                
                # Update dropdowns
                self.menu_dropdown.clear()
                self.submenu_dropdown.clear()
                self.submenu_dropdown.addItem("nil")
                for menu_id, _, _, _ in self.menus:
                    self.menu_dropdown.addItem(menu_id)
                    self.submenu_dropdown.addItem(menu_id)

            # Update views
            self.update_tree_view()
            self.update_lua_code()
            
            QMessageBox.information(self, "Success", "Item deleted successfully!")

    def clear_command_inputs(self):
        """Clear all command input fields"""
        self.command_name_input.clear()
        self.flag_input.clear()
        self.value_input.clear()
        self.custom_code_input.clear()
        self.action_type.setCurrentIndex(0)

    def get_menu_coalition(self, menu_id):
        """Get the coalition for a given menu ID"""
        for m_id, _, _, coalition in self.menus:
            if m_id == menu_id:
                return coalition
        return None

def main():
    app = QApplication(sys.argv)
    window = RadioMenuBuilder()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()