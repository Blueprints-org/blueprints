document$.subscribe(({ body }) => { 
    renderMathInElement(body, {
      delimiters: [
        { left: "$$",  right: "$$",  display: false },
        { left: "$",   right: "$",   display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: false}
      ],
    })
  })