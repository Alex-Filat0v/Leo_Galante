class KarnoMap:
    @staticmethod
    def simplify(variables, cell_values, simplification_type):
        if not variables:
            return "Введите переменные"

        num_vars = len(variables)

        # Формируем минтермы из значений ячеек
        minterms = []
        for row in range(len(cell_values)):
            for col in range(len(cell_values[row])):
                if cell_values[row][col] == 1:
                    minterms.append((row, col))

        if not minterms:
            return "0"

        # Простое упрощение для демонстрации
        if num_vars == 3:
            if (1, 1) in minterms:
                return f"{variables[0]} {variables[1]}′ {variables[2]}"

        # Более сложная логика упрощения должна быть здесь
        terms = []
        for row, col in minterms:
            term = []
            if num_vars >= 1:
                term.append(f"{variables[0]}{'' if row else '′'}")
            if num_vars >= 2:
                term.append(f"{variables[1]}{'' if col >= 2 else '′'}")
            if num_vars >= 3:
                term.append(f"{variables[2]}{'' if col % 2 else '′'}")
            terms.append(" ".join(term))

        return " + ".join(terms) if simplification_type == "sop" else "(" + ") (".join(terms) + ")"
