(() => {
  function textOf(el) {
    if (!el) return "";
    // prefer label-like children
    const label = el.querySelector(
      '.ui-treenode-label, .node-label, .label, span.caret, a, span'
    );
    if (label && label.textContent) return label.textContent.trim();

    // else try anchor
    const a = el.querySelector("a");
    if (a && a.textContent) return a.textContent.trim();

    // fallback: direct text content
    const own = Array.from(el.childNodes)
      .filter((n) => n.nodeType === Node.TEXT_NODE)
      .map((n) => n.textContent.trim())
      .join(" ")
      .trim();
    if (own) return own.split("\n")[0].trim();

    // last resort
    return (el.textContent || "").trim().split("\n")[0].trim();
  }

  function childrenOf(el) {
    const containers = [];
    const c1 = el.querySelector(":scope > .ui-treenode-children");
    if (c1) containers.push(c1);
    const c2 = el.querySelector(":scope > ul, :scope > ol");
    if (c2) containers.push(c2);

    // fallback: any nested ul
    if (containers.length === 0) {
      const fallback = el.querySelector("ul");
      if (fallback) containers.push(fallback);
    }

    const items = [];
    containers.forEach((cont) => {
      const found = cont.querySelectorAll(
        ":scope > .ui-treenode, :scope > li, :scope > div"
      );
      found.forEach((n) => items.push(n));
    });
    return items;
  }

  function nodeToObj(el) {
    const obj = { label: textOf(el) || "" };

    // add href if present
    const a = el.querySelector("a[href]");
    if (a && a.href) obj.href = a.href;

    const kids = childrenOf(el);
    if (kids && kids.length > 0) {
      obj.children = Array.from(kids).map((k) => nodeToObj(k));
    } else {
      obj.children = [];
    }
    return obj;
  }

  // root candidates
  const rootCandidates = [
    document.querySelector(".ui-tree"),
    document.querySelector("#myUL"),
    document.querySelector(".tree"),
    document.querySelector(".treelist"),
    document.querySelector("body"),
  ];
  let root = rootCandidates.find((r) => r !== null);
  if (!root) root = document.body;

  // if root is body, get top-level items
  if (root === document.body) {
    const top = document.querySelectorAll(
      ".ui-treenode, #myUL > li, .tree > li, .tree > div"
    );
    if (top.length === 0) {
      const basic = document.querySelectorAll("body > ul > li, body > div > ul > li");
      return Array.from(basic)
        .slice(0, 200)
        .map((el) => nodeToObj(el));
    }
    return Array.from(top)
      .slice(0, 200)
      .map((el) => nodeToObj(el));
  } else {
    return nodeToObj(root);
  }
})();
