import requests

API_KEY = "c0f729ac225ae545358ac0b0dbaea776"
BASE_URL = "https://d2ssns4w4hvcti.cloudfront.net"


def list_components_for_sbom(sbom_id):
    #fetch and print components of an SBOM ID
    try:
        response = requests.get(
            f"{BASE_URL}/sboms/{sbom_id}",
            headers={"X-Api-Key": API_KEY}
        )
        #save the response in a JSON format
        sbom = response.json()
        print("components used in system:")
        #get the name and version of each component thats in the response
        for comp in sbom.get("components", []):
            name = comp.get("name", "Unknown")
            version = comp.get("version", "")
            print(f"- {name} {version}")
    except Exception as e:
        print(f" Error fetching SBOM {sbom_id}: {e}")

def get_system_components(system_id):

    try:
        response = requests.get(
            f"{BASE_URL}/systems/{system_id}",
            headers={"X-Api-Key": API_KEY}
        )
        #save the response in a JSON format
        system = response.json()

        applications = system.get("applications", [])

        if not applications:
            print("⚠️ No applications found for this system.")
            return

        

        # Fetch and print components for each application SBOM
        for app in applications:
            sbom_id = app.get("sbom_id")
            if sbom_id:
                list_components_for_sbom(sbom_id)
            else:
                print(f"No SBOM for application {app.get('application_id', 'Unknown')}")

    except Exception as e:
        print(f"❌ Error fetching system details: {e}")


def get_systems_using_component(component_name):
    #search all systems in a text file for a given component.

    try:
        with open("systems.txt", "r") as f:
            system_ids = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    print(f"\nSearching {len(system_ids)} systems for component '{component_name}'...\n")

    for system_id in system_ids:
        try:
            response = requests.get(
                f"{BASE_URL}/systems/{system_id}",
                headers={"X-Api-Key": API_KEY}
            )
            response.raise_for_status()
            system = response.json()
            applications = system.get("applications", [])

            matched = False
            for app in applications:
                sbom_id = app.get("sbom_id")
                if sbom_id:
                    components = list_components_for_sbom(sbom_id)
                    for comp in components:
                        name = comp.get("name", "").lower()
                        if name == component_name:
                            app_id = app.get("application_id", "Unknown")
                            print(f"  - Application ID: {app_id} → SBOM: {sbom_id}")
                            break  # Stop checking this app after first match

        except Exception as e:
            print(f"❌ Error fetching system {system_id}: {e}")



print("Welcome. Please choose an option. \n 1.Get components for a system \n 2. Get systems using a component")
choice = input("Enter number: ")

if choice == "1":
    system_id = input("Please enter a system id: ")
    get_system_components(system_id)
elif choice == "2":
        component_name = input("Enter component name to search for: ")
        get_systems_using_component(component_name)