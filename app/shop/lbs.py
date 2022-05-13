import re

def clean_string(s):
	reg = re.compile('([\W_])+')
	
	s = s.lower().strip('')
	s = s.translate({
		ord('й'): 'j',  ord('ц'): 'c',  ord('у'): 'u', ord('к'): 'k',
		ord('е'): 'e',  ord('н'): 'n',  ord('г'): 'g', ord('ш'): 'sh',
		ord('щ'): 'sh', ord('з'): 'z',  ord('х'): 'h', ord('ъ'): '',
		ord('ф'): 'f',  ord('ы'): 'y',   ord('в'): 'v', ord('а'): 'a',
		ord('п'): 'p',  ord('р'): 'r',  ord('о'): 'o', ord('л'): 'l',
		ord('д'): 'd',  ord('ж'): 'g',  ord('э'): 'e',
		ord('я'): 'ya', ord('ч'): 'ch', ord('с'): 's', ord('м'): 'm',
		ord('и'): 'i',  ord('т'): 't',  ord('ь'): '',  ord('б'): 'b',
		ord('ю'): 'u', ord('ё'): 'jo',
	})
	return reg.sub('-', s).strip('-')