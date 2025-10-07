async function loadHTMLList(folder, containerId) {
  try {
    const response = await fetch(folder);
    const text = await response.text();

    // Parse the directory listing (works for GitHub Pages / Quarto output)
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, "text/html");
    const links = [...doc.querySelectorAll("a")];

    const container = document.getElementById(containerId);
    if (!container) return;

    links
      .filter(link => link.href.endsWith(".html") && !link.href.endsWith("index.html"))
      .forEach(link => {
        const name = decodeURIComponent(link.href.split("/").pop().replace(".html", ""));
        const item = document.createElement("div");
        item.className = "col-md-12 animate-box";
        item.innerHTML = `
          <div class="blog-card">
            <h3><a href="${folder}/${name}.html">${name.replace(/[-_]/g, " ")}</a></h3>
          </div>
        `;
        container.appendChild(item);
      });
  } catch (err) {
    console.error("Failed to load HTML list:", err);
  }
}
