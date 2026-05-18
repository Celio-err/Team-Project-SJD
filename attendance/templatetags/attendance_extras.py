from django import template

register = template.Library()

@register.filter
def por_extenso(value):
    try:
        val = int(float(value))
        # Nama angka khusus dalam Bahasa Portugis
        map_pt = {
            0: 'Zero', 1: 'Um', 2: 'Dois', 3: 'Três', 4: 'Quatro', 5: 'Cinco',
            6: 'Seis', 7: 'Sete', 8: 'Oito', 9: 'Nove', 10: 'Dez',
            11: 'Onze', 12: 'Doze', 13: 'Treze', 14: 'Catorze', 15: 'Quinze',
            16: 'Dezasseis', 17: 'Dezassete', 18: 'Dezoito', 19: 'Dezanove',
            20: 'Vinte', 30: 'Trinta', 40: 'Quarenta', 50: 'Cinquenta',
            60: 'Sessenta', 70: 'Setenta', 80: 'Oitenta', 90: 'Noventa', 100: 'Cem'
        }
        
        if val in map_pt:
            return map_pt[val]
        
        if 21 <= val <= 99:
            dezena = (val // 10) * 10
            unidade = val % 10
            return f"{map_pt[dezena]} e {map_pt[unidade]}"
            
        return str(val)
    except:
        return value

@register.filter
def media_final(total, lista):
    try:
        qtd = len(lista)
        if qtd > 0:
            res = total / qtd
            return "{:.1f}".format(res).replace('.', ',')
        return "0"
    except:
        return "0"

@register.filter
def add_one(value):
    """Filter sederhana untuk menambah 1 pada angka"""
    try:
        return int(value) + 1
    except:
        return value