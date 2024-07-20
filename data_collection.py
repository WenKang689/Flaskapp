
import os
import winreg

def check_common_directories():
    common_paths = [
        r"C:\Program Files (x86)\Steam",
        r"C:\Program Files (x86)\Ubisoft",
        r"C:\Riot Games",
        r"C:\Program Files (x86)\Epic Games",
        r"C:\Program Files\Electronic Arts",
        r"C:\Program Files (x86)\Origin",
        r"C:\Program Files\GOG Galaxy",
        r"C:\Program Files (x86)\Battle.net",
        r"C:\Program Files\Ubisoft Connect",
        r"C:\Program Files\Xbox App",
        r"C:\Program Files\Bethesda.net Launcher",
        r"C:\Program Files\Rockstar Games Launcher",
        r"C:\Program Files\PlayStation Now",
    ]
    
    detected_software = []
    for path in common_paths:
        if os.path.exists(path):
            detected_software.append(os.path.basename(path))
    return detected_software

def get_installed_software_registry():
    software_list = []
    # Paths to the registry keys
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for path in registry_paths:
        try:
            # Open the registry key
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    # Enumerate through subkeys
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    # Try to read the DisplayName value
                    name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    software_list.append(name)
                    i += 1
                except FileNotFoundError:
                    # If the DisplayName doesn't exist, skip this subkey
                    i += 1
                except OSError:
                    # No more subkeys, break the loop
                    break
        except PermissionError:
            # Skip this path if we don't have permission to access it
            continue
    return software_list

def get_installed_software():
    registry_software = get_installed_software_registry()
    directory_software = check_common_directories()
    return registry_software + directory_software

def categorize_software(software_list):
    categories = {
        "Games": ["Steam", "Epic Games", "Ubisoft", "Riot Games", "Battle.net", "GOG Galaxy", "Rockstar Games Launcher", "PlayStation Now","Genshin Impact"],
        "Programming Tools": ["Visual Studio", "PyCharm", "Sublime", "Eclipse", "IntelliJ", "NetBeans"],
        "Office Use Tools": ["Microsoft Office", "LibreOffice", "Google Docs", "Slack", "Zoom"],
        "Other": []
    }

    # Initialize a dictionary to hold lists of software names for each category
    categorized_software = {category: [] for category in categories}

    for software in software_list:
        categorized = False
        for category, keywords in categories.items():
            if any(keyword in software for keyword in keywords):
                categorized_software[category].append(software)
                categorized = True
                break
        if not categorized:
            categorized_software["Other"].append(software)

    return categorized_software

# Example usage:
software = get_installed_software()
print("Installed Software:")
for s in software:
    print(s)

categorized_software = categorize_software(software)
print("\nSoftware Categories and Their Software:")
for category, software_names in categorized_software.items():
    print(f"{category}:")
    for name in software_names:
        print(f"  - {name}")
