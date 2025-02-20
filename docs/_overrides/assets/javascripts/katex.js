// this javascript file has to be added according to the mkdocs materials documentation: https://squidfunk.github.io/mkdocs-material/reference/math/#katex
document$.subscribe(({ body }) => { 
    renderMathInElement(body, {
      delimiters: [
        { left: "$$",  right: "$$",  display: true },
        { left: "$",   right: "$",   display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
    })
  })