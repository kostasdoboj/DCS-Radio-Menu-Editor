# DCS-Radio-Menu-Editor

Create Radio Menus for your DCS missions without having to code in Lua or to get into complicated triggers in the Mission Editor.

This program was initially created for the members of Lock-On Greece, hence the logo and title. If you are interested in a custom version for your Squadron, contact me.

![image](https://github.com/user-attachments/assets/dee87984-99f2-4368-8034-0762433da162)

**Menu Builder**

![image](https://github.com/user-attachments/assets/24493fb3-d01c-4daf-94d0-24f2720e9804)

Enter your Menu ID, its name, choose its parent menu from the drop down menu (leave nil to make this a parent menu) and also the Coalition this menu belongs to.
Click Add Menu. The menu will appear on the right on the nested view and underneath the Lua code will be generated.

![image](https://github.com/user-attachments/assets/b8e8ad46-0f1a-4fad-9007-2fdf05996435)

**Command Builder**

Select the menu this command will belong to. Add its name. Select Action Type, this can be either setting a flag value or running your custom code.

Flag Example:

![image](https://github.com/user-attachments/assets/5c569b5c-1e47-48bd-bf57-4ddc23b42717)

Custom Code Example:

![image](https://github.com/user-attachments/assets/edf19bd5-2537-4add-82ba-e623750ac51a)

Please note that if you choose the flag method, you do NOT need to set a trigger in the Mission Editor to reset the flag's value. The programm will handle it itself.

Click Add Command and your commands and Lua code will be auto-generated:

![image](https://github.com/user-attachments/assets/bb3d6708-5477-494c-87a8-762e63e2c613)

When your menu is ready you can copy the Lua code and insert it as a DO SCRIPT in the Mission Editor or export the code to a Lua file which you can load as a DO SCRIPT FILE in the Mission Editor.

You can also Save/Load your work in a JSON file for future use. 
