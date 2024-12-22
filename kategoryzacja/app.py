import argparse
from kategoryzacja import all_grouped_verbs

def perform_operation(set1, set2, operation):
    if operation == 'OR':
        return set1 | set2
    elif operation == 'AND':
        return set1 & set2
    elif operation == 'XOR':
        return set1 ^ set2
    else:
        raise ValueError("Niedozwolona operacja. Wybierz OR, AND lub XOR.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Wykonaj operacje na zbiorach rzeczowników z lexemów.")
    parser.add_argument("lexem1", type=str, help="Pierwszy lexem")
    parser.add_argument("lexem2", type=str, help="Drugi lexem")
    parser.add_argument("operation", type=str, choices=["OR", "AND", "XOR"], help="Operacja do wykonania na zbiorach")
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.lexem1 not in all_grouped_verbs or args.lexem2 not in all_grouped_verbs:
        print("Błąd: Podany lexem nie istnieje w słowniku.")
        return
    
    set1 = all_grouped_verbs[args.lexem1]
    set2 = all_grouped_verbs[args.lexem2]

    result = perform_operation(set1, set2, args.operation)

    print(f"Wynik operacji {args.operation} na zbiorach lexemów '{args.lexem1}' i '{args.lexem2}':")
    print(result)

if __name__ == "__main__":
    main()
