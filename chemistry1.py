# chemistry.py

from formula import parse_formula
from datetime import datetime

NAME_INDEX = 0
ATOMIC_MASS_INDEX = 2
SYMBOL_INDEX = 0
QUANTITY_INDEX = 1

def make_periodic_table():
    periodic_table_dict = {
        "H": [1, "Hydrogen", 1.00794],
        "O": [8, "Oxygen", 15.9994],
        "C": [6, "Carbon", 12.0107],
        # ...
    }
    return periodic_table_dict

def get_formula_name(formula, known_molecules_dict):
    if formula in known_molecules_dict:
        return known_molecules_dict[formula]
    else:
        return "unknown compound"

def compute_molar_mass(symbol_quantity_list, periodic_table_dict):
    total_molar_mass = 0.0
    for item in symbol_quantity_list:
        symbol = item[SYMBOL_INDEX]
        quantity = item[QUANTITY_INDEX]
        if symbol in periodic_table_dict:
            element_info = periodic_table_dict[symbol]
            atomic_mass = element_info[ATOMIC_MASS_INDEX]
        else:
            raise ValueError(f"Unknown element symbol: {symbol}")
        total_molar_mass += atomic_mass * quantity
    return total_molar_mass

def main():
    known_molecules_dict = {
        "H2O": "water",
        "C2H5OH": "ethanol",
        "C3H8O": "isopropyl alcohol",
        # ...
    }

    known_uses = {
        "H2O": ["Solvent", "Coolant", "Cleaning", "Transport", "Reactions"],
        "C2H5OH": ["Disinfectant", "Fuel", "Solvent", "Beverages", "Antiseptic"],
        "CH3OH": ["Fuel", "Solvent", "Antifreeze", "Washer", "Feedstock"],
        # ...
    }

    formula = input("Enter the molecular formula: ")
    periodic_table_dict = make_periodic_table()

    try:
        symbol_quantity_list = parse_formula(formula, periodic_table_dict)
        molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table_dict)
        compound_name = get_formula_name(formula, known_molecules_dict)
        percent_composition = [
            (symbol, (periodic_table_dict[symbol][ATOMIC_MASS_INDEX] * qty) / molar_mass * 100)
            for symbol, qty in symbol_quantity_list
        ]
        print(f"\nCompound Name: {compound_name}")
        print(f"Molar Mass: {molar_mass:.5f} g/mol")
        print("Percent Composition by Mass:")
        for symbol, percent in percent_composition:
            print(f"  {symbol}: {percent:.2f}%")
        if formula in known_uses:
            print("Common Uses:")
            for use in known_uses[formula]:
                print(f"  - {use}")
        now = datetime.now().strftime("%I:%M%p").lower()
        with open("molar_mass_results.txt", "a") as f:
            f.write(f"\nTime: {now}\n")
            f.write(f"Formula: {formula}\n")
            f.write(f"Name: {compound_name}\n")
            f.write(f"Mass: {molar_mass:.5f} g/mol\n")
            f.write("Percent Composition:\n")
            for symbol, percent in percent_composition:
                f.write(f"  {symbol}: {percent:.2f}%\n")
            if formula in known_uses:
                f.write("Uses:\n")
                for use in known_uses[formula]:
                    f.write(f"  - {use}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
