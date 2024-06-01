import copy
import logging
from typing import Union, Tuple, Callable

"""
{
  will-be-replaced-from-environment: ${APP_NAME} 
  # `self` is a special variable that refers to this hierarchy.
  reference-to-author-greeting: $self.author.greeting
  author:
    greeting: "Hello World!"
    hobbies: 
      - creating
      - hiking
      # `me` is a special variable that refers to the current path within this hierarchy.
      # In this case, `me` refers to `author.hobbies`
      - "${self.me[0]} software"  # creating software  
}
"""
SELF_KEY = 'self'
VARIABLE_ANCHOR = '$'

logger = logging.getLogger(__name__)


def contains_variable(value: any) -> bool:
    if not isinstance(value, str):
        return False
    if VARIABLE_ANCHOR in value:
        return True
    s = VARIABLE_ANCHOR + '{'
    if s in value:
        return True if '}' in value[value.index(s) + len(s):] else False
    return False


def _check_replaced(text: str) -> str:
    if contains_variable(text):
        raise ValueError(f'Failed to replace variables in: {text}')
    return text


def replace_all_variables(target: dict[str, any],
                          source: dict[str, any],
                          check_replaced: Callable[[str], str] = _check_replaced,
                          nodes_to_skip: Union[list[str], None] = None) -> dict[str, any]:
    target = copy.deepcopy(target)

    def replace_unscoped_variables(text: str, context: dict[str, any]) -> str:
        def replace(name: str) -> Union[str, None]:
            return context.get(name, None)

        return replace_variables(text, replace)

    # We first replace all variables in the target, using values from the source
    __visit_all_variables(
        target, lambda variable, curr_path: replace_unscoped_variables(variable, source))

    # We then replace all variables in the target, using values from the target
    __visit_all_variables(
        target, lambda variable, curr_path: replace_scoped_variables(
            variable, target, curr_path, nodes_to_skip))

    __visit_all_variables(
        target, lambda variable, curr_path: check_replaced(variable))

    return target


def __visit_all_variables(target: dict[str, any],
                          visit: Callable[[str, [str]], str],
                          path: [str] = None):
    # TODO - Implement 'me' expansion for $self related variables, test it too
    #  To achieve the above you need to implement the correct curr_path argument
    def iter_dict(d: dict[str, any], _, curr_path: [str]):
        for k, v in d.items():
            d[k] = iter_value(v, d, curr_path)
        return d

    def iter_list(e_list: list[any], _, curr_path: [str]):
        for i, e in enumerate(e_list):
            e_list[i] = iter_value(e, e_list, curr_path)
        return e_list

    def iter_value(e: any, parent: any, curr_path: [str]):
        if isinstance(e, dict):
            return iter_dict(e, parent, curr_path)
        elif isinstance(e, list):
            return iter_list(e, parent, curr_path)
        elif isinstance(e, str):
            return visit(e, curr_path)
        else:
            return e

    iter_dict(target, None, [] if path is None else path)


def replace_scoped_variables(text: str,
                             context: dict[str, any],
                             curr_path: [str] = None,
                             nodes_to_skip: Union[list[str], None] = None) -> str:
    def replace(name: str) -> Union[str, None]:
        replacement = context.get(name)
        if replacement is None:
            replacement = get_scoped_value_for_name_having_prefix(
                curr_path, name, SELF_KEY, lambda k: context.get(k, None), nodes_to_skip)
        return replacement

    return replace_variables(text, replace)


def replace_variables(target: str, replace: Callable[[str], any]) -> any:
    if not contains_variable(target):
        return target
    result = target
    pos = 0
    while pos < len(result):
        t: [str, int, int] = __extract_first_variable(result, pos, None)
        if t is None:
            break
        name = t[0]
        start = t[1]
        end = t[2]
        replacement = replace(name)
        # logger.debug(f'{name}, replacement: {replacement}')
        if replacement is None:
            pos = end
            continue
        if start == 0 and end == len(result):
            return replacement
        replacement_str = str(replacement)
        result = result[0:start] + replacement_str + result[end:]
        pos = start + len(replacement_str)
    return result


def get_scoped_value_for_name_having_prefix(
        curr_path: [str],
        name: str,
        prefix: str,
        get: Callable[[str], any] = None,
        nodes_to_skip: Union[list[str], None] = None) -> Union[any, None]:
    def get_value(values_scope: any, key: str) -> any:
        if values_scope is None:
            return None if get is None else get(key)
        else:
            return values_scope.get(key, None)

    return get_scoped_value(curr_path, name, prefix, get_value, nodes_to_skip)


def get_scoped_value(curr_path: [str],
                     name: str,
                     prefix: str,
                     get_value: Callable[[any, str], any],
                     nodes_to_skip: Union[list[str], None] = None) -> Union[str, None]:
    if not name.startswith(prefix):
        return None
    parts_including_prefix, index = __parse_index_part(name)
    parts = parts_including_prefix[1:]

    parts = __expand_me(curr_path, parts)

    extras = [] if nodes_to_skip is None else [e for e in nodes_to_skip]

    scope = None
    for k in parts:
        try:

            v = get_value(scope, k)

            if v is None and len(extras) > 0:
                extra = extras[0]
                v = get_value(scope, extra)
                if v is not None:
                    extras.pop(0)
                    v = get_value(v, k)

        except Exception as ex:
            raise ValueError(f'Value not found for: {k} of {name} in {scope}') from ex
        if v is None:
            raise ValueError(f'Value not found for: {k} of {name} in {scope}')

        scope = v

    try:
        return scope[index] if index > -1 and isinstance(scope, list) else scope
    except IndexError as ex:
        raise IndexError(
            f'Invalid index: {index}, for variable: {name}, in scope: {scope}') from ex


def __expand_me(curr_path: [str], parts: [str]) -> [str]:
    if curr_path is None:
        return parts
    updated_parts: [str] = []
    for part in parts:
        if part == 'me':
            updated_parts.extend(curr_path)
        else:
            updated_parts.append(part)
    return updated_parts


def __parse_index_part(value: str) -> tuple[[str], int]:
    """
    highlight:: python
    code-block:: python
     Input: 'a.b.c[23]'
    Output: ([a, b, c], 23)
    """
    parts: [str] = value.split('.')
    last = parts[len(parts) - 1] if '.' in value else value
    if not last.endswith(']'):
        return parts, -1
    try:
        start: int = last.index('[')
        index_str: str = last[start + 1:len(last) - 1]
        index = int(index_str)
        parts[len(parts) - 1] = last[0:start]
        return parts, index
    except Exception as ex:
        raise ValueError(f'Invalid variable: {value}') from ex


def __extract_first_variable(
        text: str,
        offset: int = 0,
        result_if_none: Union[Tuple[str, int, int], None] = None) -> Tuple[str, int, int]:
    """
    highlight:: python
    code-block:: python
     Input: '${var} ${abc}'
    Output: ('var', 0, 6)
    """

    prefix = VARIABLE_ANCHOR

    try:
        start_idx: int = text.index(prefix, offset) + len(prefix)
        if text[start_idx] == '{':
            prefix = prefix + '{'
            start_idx += 1
    except ValueError:
        return result_if_none

    part: str = text[start_idx:]
    if '}' not in part:
        if ' ' not in part:
            return text[start_idx:], start_idx - len(prefix), len(text)
        else:
            last_char_is_space = True
            end_idx: int = text.index(' ', start_idx)
    else:
        last_char_is_space = False
        end_idx: int = text.index('}', start_idx)

    return (text[start_idx:end_idx],
            start_idx - len(prefix),
            end_idx if last_char_is_space else end_idx + 1)
