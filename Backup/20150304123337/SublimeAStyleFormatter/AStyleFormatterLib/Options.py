"""
Copyright (c) 2012-2015 Timon Wong

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = ["build_astyle_mode_option", "build_astyle_options"]


class RangeError(Exception):
    pass


def ensure_value_range(option_name, value, minval=None, maxval=None):
    new_value = value
    # Clamp value when out of range
    if value < minval:
        new_value = minval
    elif value > maxval:
        new_value = maxval
    # Good
    if new_value == value:
        return

    minval_str = "-Inf" if minval is None else str(minval)
    maxval_str = "+Inf" if maxval is None else str(maxval)
    raise RangeError("{0} should between {1} and {2}".format(
        option_name, minval_str, maxval_str))


def process_option_generic(options, option_name, value):
    if value and len(option_name) > 0:
        options.append("--{0}".format(option_name))
    return options

STYLE_OPTIONS = set([
    "allman", "bsd", "break", "java", "attach", "kr", "k&r", "k/r",
    "stroustrup", "whitesmith", "banner", "gnu", "linux", "horstmann", "1tbs",
    "otbs", "google", "pico", "lisp", "python", "vtk"])


def process_option_style(options, option_name, value):
    assert option_name == "style"
    if not value:
        return options
    assert value in STYLE_OPTIONS
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_min_conditional_indent(options, option_name, value):
    assert option_name == "min-conditional-indent"
    if value is None:
        return options
    ensure_value_range(option_name, value, minval=0, maxval=3)
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_max_instatement_indent(options, option_name, value):
    assert option_name == "max-instatement-indent"
    if value is None:
        return options
    ensure_value_range(option_name, value, minval=40, maxval=120)
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_max_code_length(options, option_name, value):
    assert option_name == "max-code-length"
    if value is None or value == -1:
        return options
    ensure_value_range(option_name, value, minval=50, maxval=200)
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_break_blocks(options, option_name, value):
    assert option_name == "break-blocks"
    if not value:
        return options
    assert value in ("default", "all")
    if value == "default":
        options.append("--break-blocks")
    elif value == "all":
        options.append("--break-blocks=all")
    return options


def process_option_align_pointer(options, option_name, value):
    assert option_name == "align-pointer"
    if not value:
        return options
    assert value in ("type", "middle", "name")
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_align_reference(options, option_name, value):
    assert option_name == "align-reference"
    if not value:
        return options
    assert value in ("none", "type", "middle", "name")
    options.append("--{0}={1}".format(option_name, value))
    return options


def process_option_pad_method_colon(options, option_name, value):
    assert option_name == "pad-method-colon"
    if not value:
        return options
    assert value in ("none", "all", "after", "before")
    options.append("--{0}={1}".format(option_name, value))
    return options


OPTION_PROCESSOR_MAP = {
    "style":                    process_option_style,
    "indent-classes":           process_option_generic,
    "indent-modifiers":         process_option_generic,
    "indent-switches":          process_option_generic,
    "indent-cases":             process_option_generic,
    "indent-namespaces":        process_option_generic,
    "indent-labels":            process_option_generic,
    "indent-preproc-block":     process_option_generic,
    "indent-preproc-define":    process_option_generic,
    "indent-preproc-cond":      process_option_generic,
    "indent-col1-comments":     process_option_generic,
    "attach-namespaces":        process_option_generic,
    "attach-classes":           process_option_generic,
    "attach-inlines":           process_option_generic,
    "attach-extern-c":          process_option_generic,
    "min-conditional-indent":   process_option_min_conditional_indent,
    "max-instatement-indent":   process_option_max_instatement_indent,
    "break-blocks":             process_option_break_blocks,
    "pad-oper":                 process_option_generic,
    "pad-paren":                process_option_generic,
    "pad-paren-out":            process_option_generic,
    "pad-first-paren-out":      process_option_generic,
    "pad-paren-in":             process_option_generic,
    "pad-header":               process_option_generic,
    "unpad-paren":              process_option_generic,
    "delete-empty-lines":       process_option_generic,
    "fill-empty-lines":         process_option_generic,
    "break-closing-brackets":   process_option_generic,
    "break-elseifs":            process_option_generic,
    "add-brackets":             process_option_generic,
    "remove-brackets":          process_option_generic,
    "add-one-line-brackets":    process_option_generic,
    "keep-one-line-blocks":     process_option_generic,
    "keep-one-line-statements": process_option_generic,
    "convert-tabs":             process_option_generic,
    "close-templates":          process_option_generic,
    "remove-comment-prefix":    process_option_generic,
    "max-code-length":          process_option_max_code_length,
    "break-after-logical":      process_option_generic,
    "align-pointer":            process_option_align_pointer,
    "align-reference":          process_option_align_reference,
    "align-method-colon":       process_option_generic,
    "pad-method-prefix":        process_option_generic,
    "unpad-method-prefix":      process_option_generic,
    "pad-method-colon":         process_option_pad_method_colon,
}


def build_astyle_mode_option(mode):
    if not mode:
        return ''
    return '--mode=' + mode


def special_process_option_indent(options, indent_method, spaces):
    if not indent_method:
        return options
    assert indent_method in ("spaces", "tab", "force-tab", "force-tab-x")
    option = '--indent={0}'.format(indent_method)
    if spaces is not None:
        ensure_value_range("indent=%s" % indent_method, spaces, 2, 20)
        option += '={0}'.format(spaces)
    options.append(option)
    return options


def build_astyle_options(settings, indent_options):
    options = []
    # Special indent option handling
    if not settings['indent'] and not settings['indent-spaces']:
        settings['indent'] = indent_options['indent']
        settings['indent-spaces'] = indent_options['spaces']
    options = special_process_option_indent(
        options, settings["indent"], settings.get("indent-spaces"))
    for option_name, function in OPTION_PROCESSOR_MAP.items():
        if option_name not in settings:
            continue
        value = settings[option_name]
        options = function(options, option_name, value)
    return options
