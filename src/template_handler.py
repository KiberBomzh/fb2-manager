# все места в которые нужно подставить переменные берутся в фигурные скобки
# всё что после / - это разделитель который добавляется только если в книге есть такая переменная
# указывать его в самом конце

# для authors нужно указать после названия переменной разделитель для переменных
# то есть если указать {authors&} то выйдет следующее: author1 & author2, если автор только один
# ничего добавляться не будет
# если укзать разделителем '1' то будет использован толькл первый элемент, первый автор, первый язык

# '|' - это если нужно заключать текст в какие-то скобки
# обязательно указаывать слева и справа
# то есть, чтоб заключить в () нужно указать (|)
# можно использовать любые разрешенные символы

# можно привязать одну переменную к другой
# например: нужно указывать номер серии только если есть серия
# {sequence/ <number*/, >}
# дополнительные переменные нужно указывать как конец текущей, то есть после '/'
# сами переменные заключать в < >, после имени переменной указывать '*'
# такие переменные поддерживают всё тоже самое что и обычные
# '|', '/' это всё
# нельзя только привязать ещё переменных к ним
# к основным переменным можно добавлять сколько угодно вложенных


# Значения
# title - название книги
# authors - авторы
# sequence, number - серия, номер в серии
# language - язык


def get_without_forbidden_chars(text):
    forbiddenChars = {'<', '>', ':', '"', '/', '|', '?', '*', '`'}
    
    for char in text:
        if char in forbiddenChars:
            text = text.replace(char, '')
    
    return text

def unwrap_tag(name, tag, the_var):
    index = name.find(tag)
    if index < 0:
        return name
    
    end_i = name[index:].find('}') + index
    the_tag = name[index + len(tag): end_i]
    
    
    # проверка есть ли привязанные знаки
    line_index = the_tag.find('/')
    if line_index >= 0:
        bind_text = the_tag[line_index + 1:]
        the_tag = the_tag[:line_index]
    else:
        bind_text = ''


    # проверка есть ли знаки в которые нужно заключить значение
    # берется по одному символу
    # символ слева от '/' будет левым символом
    # символ справа от '/' будет правым
    embrace_index = the_tag.find('|')
    if embrace_index >= 0:
        embrace_left = the_tag[embrace_index - 1]
        embrace_right = the_tag[embrace_index + 1]
        the_tag = the_tag[:embrace_index - 1] + the_tag[embrace_index + 2:]
    else:
        embrace_left = ''
        embrace_right = ''
    
    
    # если переменная список то нужно проверить есть ли разделитель и развернуть переменную
    if isinstance(the_var, list):
        divider = the_tag
        
        if not divider:
            divider = '&'

        if divider == '1' and len(the_var) > 0:
            var_name = the_var[0]
        else: 
            divider = f' {divider} '
            var_name = divider.join(the_var)
    else:
        var_name = the_var
    
    
    if var_name:
        name = name[:index] + embrace_left + var_name + embrace_right + bind_text + name[end_i + 1:]
    else:
        name = name[:index] + name[end_i + 1:]
    
    return name


def unwrap_secondary_tags(name, meta, number_template):
    counter = 0
    while '*' in name:
        if counter > 100:
            break
        start = name.find('<')
        start_tag = start + 1
        end_tag = name[start_tag:].find('*') + start_tag
        tag = name[start_tag:end_tag]
        end = name[start:].find('>') + start
        name = name[:start] + '{' + tag + name[end_tag + 1:end] + '}' + name[end + 1:]
        
        meta_value = meta[tag]
        if tag == 'number':
            meta_value = number_templ_handl(meta_value, number_template)
        
        
        name = unwrap_tag(name, '{' + tag, meta_value)
        
        counter += 1
    
    return name


def number_templ_handl(number, template):
    if not number:
        return number
    
    try:
        nums_in_start, divider, nums_in_end = template.split('|')
        nums_in_start = int(nums_in_start)
        nums_in_end = int(nums_in_end)
    except ValueError:
        return number
    
    try:
        if '.' not in number:
            number += '.0'
        s_nums_start, s_nums_end = number.split('.')
    except ValueError:
        return number
    
    if s_nums_start.startswith('0'):
        s_nums_start = s_nums_start[1:]
    if s_nums_end == '0':
        s_nums_end = ''
    
    if len(s_nums_start) < nums_in_start:
        how_many_zeros = nums_in_start - len(s_nums_start)
        s_nums_start = '0' * how_many_zeros + s_nums_start
    
    if len(s_nums_end) < nums_in_end:
        how_many_zeros = nums_in_end - len(s_nums_end)
        s_nums_end = '0' * how_many_zeros + s_nums_end
    
    
    number = s_nums_start
    if s_nums_end:
        number += divider + s_nums_end
    
    return number


def get_name(meta, template, number_template):
    name = template
    
    while '{' in name:
        for key, value in meta.items():
            tag = '{' + key
            if tag not in name:
                continue
            
            
            if key == 'number':
                value = number_templ_handl(value, number_template)
            
            name = unwrap_tag(name, tag, value)
        
        if '*' in name:
            name = unwrap_secondary_tags(name, meta, number_template)
    
    name = get_without_forbidden_chars(name)
    return name

def main(meta, template, number_template):
    if isinstance(template, str):
        template = [template]

    names = []
    for templ in template:
        name = get_name(meta, templ, number_template)
        if name:
            names.append(name)
    
    if len(names) == 1:
        return names[0]
    
    return names
