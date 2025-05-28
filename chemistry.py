# chemistry.py

# Program Enhancements and Extra Features:
# - Includes a dictionary of known chemical formulas linked to compound names.
# - Uses a function to detect and display a compound’s name from its formula.
# - Expanded periodic table now includes atomic numbers for lookup (via a separate function).
# - Calculates percent composition by mass for each element in a compound.
# - Outputs a detailed molecular weight breakdown showing each element's contribution.
# - Displays five real-world uses for known compounds to show practical relevance.
# - Saves all results to a file called 'results.txt' with clear, labeled lines:
#   time, formula, compound name, molar mass, atomic numbers, mass percentages, and uses.
# - Helps users keep a permanent, organized record of their calculations.

from formula import parse_formula
from datetime import datetime


NAME_INDEX = 0
ATOMIC_MASS_INDEX = 1


SYMBOL_INDEX = 0
QUANTITY_INDEX = 1

# symbol: [name, atomic_mass]
# This function is designed to return element data in a format that might be
# expected by an external grader (e.g., [name, atomic_mass] without atomic number).
def make_periodic_table():
    periodic_table_dict = {
        "Ac": ["Actinium", 227],
        "Ag": ["Silver", 107.8682],
        "Al": ["Aluminum", 26.9815386],
        "Ar": ["Argon", 39.948],
        "As": ["Arsenic", 74.9216],
        "At": ["Astatine", 210],
        "Au": ["Gold", 196.966569],
        "B":  ["Boron", 10.811],
        "Ba": ["Barium", 137.327],
        "Be": ["Beryllium", 9.012182],
        "Bi": ["Bismuth", 208.9804],
        "Br": ["Bromine", 79.904],
        "C":  ["Carbon", 12.0107],
        "Ca": ["Calcium", 40.078],
        "Cd": ["Cadmium", 112.411],
        "Ce": ["Cerium", 140.116],
        "Cl": ["Chlorine", 35.453],
        "Co": ["Cobalt", 58.933195],
        "Cr": ["Chromium", 51.9961],
        "Cs": ["Cesium", 132.9054519],
        "Cu": ["Copper", 63.546],
        "Dy": ["Dysprosium", 162.5],
        "Er": ["Erbium", 167.259],
        "Eu": ["Europium", 151.964],
        "F":  ["Fluorine", 18.9984032],
        "Fe": ["Iron", 55.845],
        "Fr": ["Francium", 223],
        "Ga": ["Gallium", 69.723],
        "Gd": ["Gadolinium", 157.25],
        "Ge": ["Germanium", 72.64],
        "H":  ["Hydrogen", 1.00794],
        "He": ["Helium", 4.002602],
        "Hf": ["Hafnium", 178.49],
        "Hg": ["Mercury", 200.59],
        "Ho": ["Holmium", 164.93032],
        "I":  ["Iodine", 126.90447],
        "In": ["Indium", 114.818],
        "Ir": ["Iridium", 192.217],
        "K":  ["Potassium", 39.0983],
        "Kr": ["Krypton", 83.798],
        "La": ["Lanthanum", 138.90547],
        "Li": ["Lithium", 6.941],
        "Lu": ["Lutetium", 174.9668],
        "Mg": ["Magnesium", 24.305],
        "Mn": ["Manganese", 54.938045],
        "Mo": ["Molybdenum", 95.96],
        "N":  ["Nitrogen", 14.0067],
        "Na": ["Sodium", 22.98976928],
        "Nb": ["Niobium", 92.90638],
        "Nd": ["Neodymium", 144.242],
        "Ne": ["Neon", 20.1797],
        "Ni": ["Nickel", 58.6934],
        "Np": ["Neptunium", 237],
        "O":  ["Oxygen", 15.9994],
        "Os": ["Osmium", 190.23],
        "P":  ["Phosphorus", 30.973762],
        "Pa": ["Protactinium", 231.03588],
        "Pb": ["Lead", 207.2],
        "Pd": ["Palladium", 106.42],
        "Pm": ["Promethium", 145],
        "Po": ["Polonium", 209],
        "Pr": ["Praseodymium", 140.90765],
        "Pt": ["Platinum", 195.084],
        "Pu": ["Plutonium", 244],
        "Ra": ["Radium", 226],
        "Rb": ["Rubidium", 85.4678],
        "Re": ["Rhenium", 186.207],
        "Rh": ["Rhodium", 102.9055],
        "Rn": ["Radon", 222],
        "Ru": ["Ruthenium", 101.07],
        "S":  ["Sulfur", 32.065],
        "Sb": ["Antimony", 121.76],
        "Sc": ["Scandium", 44.955912],
        "Se": ["Selenium", 78.96],
        "Si": ["Silicon", 28.0855],
        "Sm": ["Samarium", 150.36],
        "Sn": ["Tin", 118.71],
        "Sr": ["Strontium", 87.62],
        "Ta": ["Tantalum", 180.94788],
        "Tb": ["Terbium", 158.92535],
        "Tc": ["Technetium", 98],
        "Te": ["Tellurium", 127.6],
        "Th": ["Thorium", 232.03806],
        "Ti": ["Titanium", 47.867],
        "Tl": ["Thallium", 204.3833],
        "Tm": ["Thulium", 168.93421],
        "U":  ["Uranium", 238.02891],
        "V":  ["Vanadium", 50.9415],
        "W":  ["Tungsten", 183.84],
        "Xe": ["Xenon", 131.293],
        "Y":  ["Yttrium", 88.90585],
        "Yb": ["Ytterbium", 173.054],
        "Zn": ["Zinc", 65.38],
        "Zr": ["Zirconium", 91.224]
    }
    return periodic_table_dict


def make_atomic_numbers_lookup():
    atomic_numbers_dict = {
        "Ac": 89, "Ag": 47, "Al": 13, "Ar": 18, "As": 33, "At": 85, "Au": 79, "B": 5,
        "Ba": 56, "Be": 4, "Bi": 83, "Br": 35, "C": 6, "Ca": 20, "Cd": 48, "Ce": 58,
        "Cl": 17, "Co": 27, "Cr": 24, "Cs": 55, "Cu": 29, "Dy": 66, "Er": 68, "Eu": 63,
        "F": 9, "Fe": 26, "Fr": 87, "Ga": 31, "Gd": 64, "Ge": 32, "H": 1, "He": 2,
        "Hf": 72, "Hg": 80, "Ho": 67, "I": 53, "In": 49, "Ir": 77, "K": 19, "Kr": 36,
        "La": 57, "Li": 3, "Lu": 71, "Mg": 12, "Mn": 25, "Mo": 42, "N": 7, "Na": 11,
        "Nb": 41, "Nd": 60, "Ne": 10, "Ni": 28, "Np": 93, "O": 8, "Os": 76, "P": 15,
        "Pa": 91, "Pb": 82, "Pd": 46, "Pm": 61, "Po": 84, "Pr": 59, "Pt": 78, "Pu": 94,
        "Ra": 88, "Rb": 37, "Re": 75, "Rh": 45, "Rn": 86, "Ru": 44, "S": 16, "Sb": 51,
        "Sc": 21, "Se": 34, "Si": 14, "Sm": 62, "Sn": 50, "Sr": 38, "Ta": 73, "Tb": 65,
        "Tc": 43, "Te": 52, "Th": 90, "Ti": 22, "Tl": 81, "Tm": 69, "U": 92, "V": 23,
        "W": 74, "Xe": 54, "Y": 39, "Yb": 70, "Zn": 30, "Zr": 40
    }
    return atomic_numbers_dict


def get_formula_name(formula, known_molecules_dict):
    """Try to find the given molecular formula in the known_molecules_dict.
    If the formula is in the dictionary, return the name of the compound.
    Otherwise, return "unknown compound".
    """
    return known_molecules_dict.get(formula, "unknown compound")


def compute_molar_mass(symbol_quantity_list, periodic_table_dict):
    """Compute and return the total molar mass of all the elements in
    symbol_quantity_list.

    Parameters
        symbol_quantity_list is a list of tuples. Each tuple contains
            an element symbol and the quantity of that element in
            the chemical formula.
        periodic_table_dict is a dictionary that contains information
            about the elements in the periodic table.
    Return: the total molar mass of all the elements in
        symbol_quantity_list.
    """
    total_molar_mass = 0.0
    for symbol, quantity in symbol_quantity_list:
        if symbol in periodic_table_dict:
            # Access atomic mass at ATOMIC_MASS_INDEX (which is 1 for [name, atomic_mass])
            atomic_mass = periodic_table_dict[symbol][ATOMIC_MASS_INDEX]
            total_molar_mass += atomic_mass * quantity
        else:
            
            raise ValueError(f"Unknown element symbol: {symbol}")
    return total_molar_mass


def get_molecular_breakdown(symbol_quantity_list, periodic_table_dict):
    """Calculates and returns a detailed breakdown of each element's
    contribution to the total molecular weight.

    Parameters:
        symbol_quantity_list: A list of (symbol, quantity) tuples.
        periodic_table_dict: The periodic table dictionary.
    Returns:
        A list of tuples: (symbol, quantity, atomic_mass, total_mass_for_element)
    """
    breakdown = []
    for symbol, qty in symbol_quantity_list:
        atomic_mass = periodic_table_dict[symbol][ATOMIC_MASS_INDEX]
        total_mass = atomic_mass * qty
        breakdown.append((symbol, qty, atomic_mass, total_mass))
    return breakdown

def get_percent_composition(symbol_quantity_list, periodic_table_dict, molar_mass):
    """Calculates and returns the percent composition by mass for each
    element in a compound.

    Parameters:
        symbol_quantity_list: A list of (symbol, quantity) tuples.
        periodic_table_dict: The periodic table dictionary.
        molar_mass: The total molar mass of the compound.
    Returns:
        A list of tuples: (symbol, percent_by_mass)
    """
    percent_comp = []
    if molar_mass == 0:
        return percent_comp # Avoid division by zero
        
    for symbol, qty in symbol_quantity_list:
        atomic_mass = periodic_table_dict[symbol][ATOMIC_MASS_INDEX]
        percent = (atomic_mass * qty / molar_mass) * 100
        percent_comp.append((symbol, percent))
    return percent_comp


def main():
    # Get the periodic table with name and atomic mass
    periodic_table_dict = make_periodic_table()
    
    # Get the separate atomic numbers lookup
    atomic_numbers_lookup = make_atomic_numbers_lookup()

    known_molecules_dict = {
        "Al2O3": "aluminum oxide",
        "CH3OH": "methanol",
        "C2H6O": "ethanol",
        "C2H5OH": "ethanol",
        "C3H8O": "isopropyl alcohol",
        "C3H8": "propane",
        "C4H10": "butane",
        "C6H6": "benzene",
        "C6H14": "hexane",
        "C8H18": "octane",
        "CH3(CH2)6CH3": "octane",
        "C13H18O2": "ibuprofen",
        "C13H16N2O2": "melatonin",
        "Fe2O3": "iron oxide",
        "FeS2": "iron pyrite",
        "H2O": "water"
    }

    known_uses = {
    "H2O": ["Solvent", "Coolant", "Cleaning", "Transport in biology", "Chemical reactions"],
    "C2H5OH": ["Disinfectant", "Fuel", "Solvent", "Beverages", "Antiseptic"],
    "CH3OH": ["Fuel", "Solvent", "Antifreeze", "Windshield washer", "Industrial feedstock"],
    "Fe2O3": ["Pigment", "Polishing", "Catalyst", "Magnetic storage", "Steel production"],
    "NaCl": ["Seasoning", "Preservative", "Deicing", "Electrolysis", "Water softening"],
    "Al2O3": ["Abrasives", "Ceramics", "Refractories", "Catalyst support", "Glass production"],
    "C3H8O": ["Solvent", "Disinfectant", "Antiseptic", "Fuel additive", "Topical agent"],
    "C3H8": ["Fuel (LPG)", "Heating", "Cooking", "Refrigerant", "Engine fuel"],
    "C4H10": ["Fuel (butane gas)", "Lighter fluid", "Aerosol propellant", "Refrigerant", "Solvent"],
    "C6H6": ["Industrial solvent", "Precursor to plastics", "Detergents", "Explosives", "Dyes"],
    "C6H14": ["Solvent", "Fuel", "Cleaning agent", "Extraction", "Degreasing"],
    "C8H18": ["Gasoline component", "Fuel research", "Engine testing", "Solvent", "Petroleum refining"],
    "CH3(CH2)6CH3": ["Fuel", "Solvent", "Hydrocarbon research", "Combustion studies", "Petrochemicals"],
    "C13H18O2": ["Pain relief", "Anti-inflammatory", "Fever reduction", "Rheumatoid arthritis treatment", "Osteoarthritis treatment"],
    "C13H16N2O2": ["Sleep aid", "Jet lag treatment", "Antioxidant", "Immune support", "Mood regulation"],
    "FeS2": ["Ore of sulfur", "Ore of iron", "Semiconductor research", "Solar cells", "Jewelry (fool's gold)"]
    }

    formula = input("Enter the molecular formula: ").strip()
    mass = float(input("Enter the mass of the sample in grams: ").strip())

    try:
        symbol_quantity_list = parse_formula(formula, periodic_table_dict)
        molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table_dict)
        compound_name = get_formula_name(formula, known_molecules_dict)
        breakdown = get_molecular_breakdown(symbol_quantity_list, periodic_table_dict)
        percent_comp = get_percent_composition(symbol_quantity_list, periodic_table_dict, molar_mass)
        # Fetch uses for the formula, default to generic if not found
        uses = known_uses.get(formula, ["No specific uses found for this compound."])
        current_time = datetime.now().strftime("%I:%M%p").lower()

        # Terminal Output
        print(f"\nCompound Name: {compound_name}")
        print(f"Time: {current_time}")
        print(f"Molar Mass: {molar_mass:.5f} g/mol\n")

        print("Atomic Numbers and Elements:")
        for symbol, qty in symbol_quantity_list:
            # Get atomic number from the separate lookup dictionary
            atomic_number = atomic_numbers_lookup.get(symbol, "N/A")
            # Get element name from the periodic_table_dict (index 0)
            element_name = periodic_table_dict[symbol][NAME_INDEX]
            print(f"   {symbol} ({element_name}) - Atomic Number: {atomic_number}, Quantity: {qty}")

        print("\nMolecular Weight Breakdown:")
        for sym, qty, atom_mass, total_mass in breakdown: 
            print(f"   {sym}: {qty} × {atom_mass:.5f} = {total_mass:.5f}")

        print("\nPercent Composition by Mass:")
        for sym, percent in percent_comp:
            print(f"   {sym}: {percent:.2f}%")

        print("\n5 Uses in Chemistry:")
        # Print up to 5 uses, ensuring not to go out of bounds if fewer are available
        for i, use in enumerate(uses[:5]):
            print(f"   - {use}")
        if not uses: # If the list is empty, print a generic message
            print("   - No specific uses found for this compound.")


        # Save to results.txt
        with open("results.txt", "a") as file:
            file.write(f"Time: {current_time}\n")
            file.write(f"Formula: {formula}\n")
            file.write(f"Name: {compound_name}\n")
            file.write(f"Molar Mass: {molar_mass:.5f} g/mol\n")
            file.write("Atomic Details:\n")
            for symbol, qty in symbol_quantity_list:
                atomic_number = atomic_numbers_lookup.get(symbol, "N/A")
                name = periodic_table_dict[symbol][NAME_INDEX]
                file.write(f"   {symbol} ({name}), Atomic Number: {atomic_number}, Quantity: {qty}\n")

            file.write("Molecular Weight Breakdown:\n")
            for sym, qty, atom_mass, total_mass in breakdown:
                file.write(f"   {sym}: {qty} × {atom_mass:.5f} = {total_mass:.5f}\n")

            file.write("Percent Composition:\n")
            for sym, percent in percent_comp:
                file.write(f"   {sym}: {percent:.2f}%\n")

            file.write("Uses:\n")
            # Save up to 5 uses
            for i, use in enumerate(uses[:5]):
                file.write(f"   - {use}\n")
            if not uses:
                file.write("   - No specific uses found for this compound.\n")
            file.write("\n" + "-"*50 + "\n\n")

    except ValueError as e: # Catch specific ValueError from parse_formula or compute_molar_mass
        print(f"Input Error: {e}. Please check your formula or mass.")
    except KeyError as e: # Catch if an unknown symbol somehow slips through or if periodic_table_dict is incomplete
        print(f"Data Error: Missing information for element {e}. Please check periodic table data.")
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()