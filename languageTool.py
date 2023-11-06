import enchant
d = enchant.Dict('en_US')

frase2 = "enginemotor"


def corrigir_frase(frase1):
    # Verifique a frase em busca de erros gramaticais.
    erros = d.check(frase1)
    print(erros)

    if not erros:
        frase_corrigida1 = d.suggest(frase1)
        print(frase_corrigida1)
        return frase_corrigida1

    else:
        # Se não houver erros, retorne a frase original.
        return frase1


frase_corrigida2 = corrigir_frase(frase2)
print(f"Frase corrigida: {frase_corrigida2}")
