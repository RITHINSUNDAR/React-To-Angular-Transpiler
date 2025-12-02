
import re

react_file = 'react/TodoList.jsx'
angular_ts_file = 'angular_reference/TodoList.component.ts'
angular_html_file = 'angular_reference/TodoList.component.html'

# Read React file
with open(react_file, 'r') as f:
    react_code = f.read()

def extract_comp_name(jsx_code):
    component_name = re.search(r'function\s+(\w+)', jsx_code)
    if component_name:
        return component_name.group(1)
    return"Converted Component"   

def extract_ts_part(component_name, jsx_code):
    # Extract only the inside of the function
    pattern = rf'function\s+{component_name}\s*\([^)]*\)\s*\{{([\s\S]*?)\}}'
    match = re.search(pattern, jsx_code)

    if not match:
        return "TS logic not found"

    ts_body = match.group(1).strip()

    # Remove return(...) HTML section
    ts_body = re.sub(r'return\s*\(([\s\S]*?)\);', '', ts_body).strip()

    return ts_body

def extract_html(c):
    html_portion = re.search(r"return\s*\(([\s\S]*?)\);",c)
    return html_portion.group(1)
   

def convert_to_ts(jsx_ts_part):
    modf = jsx_ts_part
    # Convert React functional component → Angular class
    modf = re.sub(
        r'function\s+(\w+)\s*\([^)]*\)\s*\{',
        r'export class \1Component {',
        modf
    )

    # Convert useState → Angular property
    modf = re.sub(
        r'const\s*\[\s*(\w+)\s*,\s*\w+\s*\]\s*=\s*useState\((.*?)\);',
        r'\1: any = \2;',
        modf,
        flags=re.DOTALL
    )

    # Arrow function → method
    modf = re.sub(
        r'const\s+(\w+)\s*=\s*\((.*?)\)\s*=>\s*\{',
        r'\1(\2) {',
        modf,
        flags=re.DOTALL
    )

    # setState pattern: setTodos([...todos, newTodo])
    modf = re.sub(
        r'set(\w+)\s*\(\s*\[\s*\.\.\.(\w+)\s*,\s*(\w+)\s*\]\s*\);',
        r'this.\2.push(this.\3);',
        modf
    )

    # setState("") → variable = ""
    modf = re.sub(
        r'set(\w+)\s*\(\s*\'\'\s*\);',
        r'this.\1 = \'\';',
        modf
    )

    return modf

def convert_to_html(jsx_code):
    modf=jsx_code
    modf = re.sub(r'onClick=\{(\w+)\}', r'(click)="\1()"', modf)
    modf = re.sub(r'onChange=\{[^}]*\}',"",modf)
    modf = re.sub(r'\{(\w+)\}', r'{{ \1 }}', modf)
    modf = re.sub(
    r'\{(\w+)\.map\(\((\w+),\s*(\w+)\)\s*=>\s*\(',
    r'<li *ngFor="let \2 of \1">',
    modf
    )
    
    modf = modf.replace("key={{ index }}", "")
    modf = re.sub(r'value=\{\{?\s*(\w+)\s*\}?\}', r'[(ngModel)]="\1"', modf)
    modf = modf.replace('))}', '') 
    modf = modf.replace(">)", ">").replace(") <", "<")
    return modf

def generate_ts(react_code):
    Jsx_code=react_code
    compdecor_code = """@Component({selector:'app-todo-list',
        templateUrl:'./TodoList.component.html',
        styleUrls: ['./TodoList.component.css']})"""
    
    state_import_code="import { Component } from '@angular/core';\n"

    component_name=extract_comp_name(Jsx_code)
    tspart=extract_ts_part(component_name, Jsx_code)

    substituted_code=convert_to_ts(tspart)

    with open("angular_reference/TodoList.component.ts", 'w') as ang_ts:
        ang_ts.write(state_import_code)
        ang_ts.write('\n')
        ang_ts.write(compdecor_code)
        ang_ts.write('\n')
        ang_ts.write(substituted_code)

def generate_html(react_code):
    modf=react_code
    jsx_code=extract_html(modf)
    converted_html=convert_to_html(jsx_code)
    with open("angular_reference/TodoList.component.html", 'w') as ang_html:
        ang_html.write(converted_html)        


generate_ts(react_code)
generate_html(react_code)
print("files generated successfully.")   






