import os

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
    # Placeholder for registry checking logic
    # This should return a list of software names found in the registry
    return ["Visual Studio", "Microsoft Office", "Google Chrome"]

def get_installed_software():
    registry_software = get_installed_software_registry()
    directory_software = check_common_directories()
    return registry_software + directory_software

def categorize_software(software_list):
    categories = {
        "Games": ["Steam", "Epic Games", "Ubisoft", "Riot Games", "Battle.net", "GOG Galaxy", "Rockstar Games Launcher", "PlayStation Now"],
        "Programming Tools": ["Visual Studio", "PyCharm", "Sublime", "Eclipse", "IntelliJ", "NetBeans"],
        "Office Use Tools": ["Microsoft Office", "LibreOffice", "Google Docs", "Slack", "Zoom"],
        "Other": []
    }

    category_counts = {category: 0 for category in categories}

    for software in software_list:
        categorized = False
        for category, keywords in categories.items():
            if any(keyword in software for keyword in keywords):
                category_counts[category] += 1
                categorized = True
                break
        if not categorized:
            category_counts["Other"] += 1

    return category_counts

# Example usage:
software = get_installed_software()
print("Installed Software:")
for s in software:
    print(s)

software_categories_count = categorize_software(software)
print("\nSoftware Categories Count:")
for category, count in software_categories_count.items():
    print(f"{category}: {count}")