# React-to-Angular Transpiler (Regex-Based Prototype)

This project is a simple Python-based **React → Angular transpiler** designed as a proof-of-concept for converting React functional components into Angular component files.

The goal of this project is to demonstrate how JSX, and event handlers can be transformed into Angular TypeScript and HTML templates using a lightweight **regex-driven approach**.
## Approach (Regex)

1. **Read the JSX file as a raw string**  
   This makes regex pattern matching easier.

2. **Split the component into two parts**  
   - TypeScript logic (everything except `return(...)`)  
   - JSX template (`return(...)` block)

3. **Convert the logic (TS part)**  
   - Convert `useState` → Angular properties  
   - Convert arrow functions → Angular methods  
   - Convert state updates like  
     `setTodos([...todos, newTodo])`

4. **Convert the template (HTML part)**  
   - Convert events: `onClick` → `(click)`  
   - Convert bindings: `{value}` → `{{ value }}`  
   - Convert list rendering: `.map()` → `*ngFor`  
   - Convert inputs: `value={x}` → `[(ngModel)]="x"`

5. **Generate final Angular files**  
   - `TodoList.component.ts`  
   - `TodoList.component.html`

 # Limitations

The current transpiler uses a regex-based approach, which is suitable only for small projects or simple assessments.

Regex cannot reliably handle complex React components, deeply nested JSX, or advanced expressions.

# Future Enhancements

Integrate a proper JSX parser (Babel/Esprima) to generate a robust AST and accurately convert all JSX features.

Add unit tests to automatically verify that each React-to-Angular conversion works correctly.
