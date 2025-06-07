

// remove the TOC for jupyter notebook pages (examples) to widen the page for readability
// See https://github.com/danielfrg/mkdocs-jupyter/issues/99#issuecomment-2455307893
// See https://github.com/danielfrg/mkdocs-jupyter/issues/220
// Using the document$ observable from mkdocs-material to get notified of page "reload" also if using `navigation.instant` (SSA)
document$.subscribe(function() {
    // First check if the page contains a notebook-related class
    if (document.querySelector('.jp-Notebook')) {
      // "div.md-sidebar.md-sidebar--primary" is the navigation
      // "div.md-sidebar.md-sidebar--secondary is the table of contents
      //document.querySelector("div.md-sidebar.md-sidebar--primary").remove();
      document.querySelector("div.md-sidebar.md-sidebar--secondary").remove();
    }
  });