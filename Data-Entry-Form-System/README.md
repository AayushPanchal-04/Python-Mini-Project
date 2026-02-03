# 🧾 User Data Entry System

A simple and beginner-friendly **User Data Entry System** built using **Python**, **Tkinter**, and **Excel**.  
This application allows users to enter personal details through a graphical interface and automatically saves the data into an Excel file.

## 🌟 Features

- 🖥️ **Modern GUI**: Clean and user-friendly interface using Tkinter  
- 📊 **Excel Storage**: Saves user data securely in an `.xlsx` file  
- ✅ **Input Validation**: Prevents submission if any field is empty  
- 🔔 **Popup Alerts**: Success and error messages using message boxes  
- 🧹 **Auto Reset**: Clears all input fields after successful submission  
- 📁 **Auto File Creation**: Creates the Excel file automatically if not found  

## 🛠️ Technology Stack

- **Python**: Core programming language  
- **Tkinter**: GUI framework  
- **openpyxl**: Excel file handling  
- **Excel (.xlsx)**: Persistent data storage  

## 📂 Project Overview

The application collects the following user details:

- Full Name  
- Age  
- Gender  
- Email Address  
- Contact Number  

All entered data is saved row-by-row into an Excel file named **`data.xlsx`**.

## 📁 Excel File Structure

When the application runs for the first time, it creates an Excel file with the following structure:

| Column | Description |
|------|------------|
| A | Name |
| B | Age |
| C | Gender |
| D | Email |
| E | Contact |

Each new user entry is stored on a new row.

## ▶️ How It Works

1. Launch the application  
2. Enter all required user details  
3. Click **SAVE DATA**  
4. Data is stored in `data.xlsx`  
5. A success message is displayed  
6. The form resets automatically for the next entry  

## ⚠️ Validation Rules

- All fields are **mandatory**  
- If any field is empty, an error message is shown  
- Data is saved only when all inputs are valid  

## 🎯 Use Cases

- Student registration systems  
- User information collection tools  
- Small office data entry applications  
- Beginner Python GUI practice  
- College mini-projects  

## 📂 Project Structure

user-data-entry-system/
│
├── data.xlsx # Excel file for stored data
├── main.py # Application file
└── README.md # Project documentation