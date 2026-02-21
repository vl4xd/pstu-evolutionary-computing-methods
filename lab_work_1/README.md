# pstu-evolutionary-computing-methods

`plotly==6.5.2` & `PyQtWebEngine==5.15.7` & `PyQtWebEngine-Qt5==5.15.2` don't work
```bash
js: Uncaught SyntaxError: Failed to execute 'insertRule' on 'CSSStyleSheet': Failed to parse the rule '.js-plotly-plot .plotly .modebar-btn:focus-visible{outline:1px solid #000;outline-offset:1px;border-radius:3px;}'.
js: Uncaught ReferenceError: Plotly is not defined
```

to fix it, use `plotly==4.14.3`