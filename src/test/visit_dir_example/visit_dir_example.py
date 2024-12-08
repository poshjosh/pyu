from pyu.io.file import read_content, visit_dirs, write_content

operands = [
    'jvm.thread.count',
    'jvm.thread.count.daemon',
    'jvm.thread.count.deadlocked',
    'jvm.thread.count.deadlocked.monitor',
    'jvm.thread.count.peak',
    'jvm.thread.count.started',
    'jvm.thread.current.count.blocked',
    'jvm.thread.current.count.waited',
    'jvm.thread.current.id',
    'jvm.thread.current.state',
    'jvm.thread.current.suspended',
    'jvm.thread.current.time.blocked',
    'jvm.thread.current.time.cpu',
    'jvm.thread.current.time.user',
    'jvm.thread.current.time.waited',
    'sys.environment',
    'jvm.memory.available',
    'jvm.memory.free',
    'jvm.memory.max',
    'jvm.memory.total',
    'jvm.memory.used',
    'sys.property',
    'sys.time',
    'sys.time.elapsed',
    'web.request.attribute',
    'web.request.auth.scheme',
    'web.request.header',
    'web.request.locale',
    'web.request.parameter',
    'web.request.ip',
    'web.request.remote.address',
    'web.request.uri',
    'web.request.cookie',
    'web.request.user.principal',
    'web.request.user.role',
    'web.session.id'
]

# The negations come first: e.g "!>=" comes before ">="
# The compound form comes first: e.g: "<=" comes before "="
operators = [
    '!>=',
    '!<=',
    '!=',
    '!>',
    '!<',
    '!%',
    '!^',
    '!&',
    '<=',
    '>=',
    '=',
    '>',
    '<',
    '%',
    '^',
    '&'
]

if __name__ == '__main__':

    dry_run = True

    def surround_operator_with_space(src: str, _):
        print(src)
        replaced = 0
        content = read_content(src)
        for operator in operators:
            for operand in operands:
                if f"{operand}{operator}" in content:
                    if dry_run is False:
                        content = content.replace(f"{operand}{operator}", f"{operand} {operator} ")
                    replaced += 1
                    print(f'\tReplaced: "{operand}{operator}" with: "{operand} {operator} "')

        if replaced > 0 and dry_run is False:
            write_content(content, src)

    def print_files_with_rhs_expression(src: str, _):
        content = read_content(src)
        for operator in operators:
            to_find = operator + '{'
            if to_find in content:
                print(src)
                break

    def test(src: str, dest: str) -> bool:
        return src.endswith(".md") or src.endswith(".MD") or src.endswith(".java")

    root_src_dir = '/Users/chinomso/dev_looseboxes/rate-limiter-spring'

    visit_dirs(print_files_with_rhs_expression, root_src_dir, test=test)
