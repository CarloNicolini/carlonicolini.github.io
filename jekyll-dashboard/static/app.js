"use strict";

let POSTS = [];      // server state
let TAGS = [];       // tag universe
const DIRTY = {};    // id -> {field: value} pending changes
let sortKey = "date";
let sortDir = -1;

const $ = (sel) => document.querySelector(sel);
const rowsEl = $("#rows");

async function load() {
  const res = await fetch("/api/posts");
  const data = await res.json();
  POSTS = data.posts;
  TAGS = data.tags;
  populateSectionFilter();
  renderTagDatalist();
  render();
}

function populateSectionFilter() {
  const sel = $("#sectionFilter");
  const sections = [...new Set(POSTS.map((p) => p.section))].sort();
  for (const s of sections) {
    const o = document.createElement("option");
    o.value = s; o.textContent = s;
    sel.appendChild(o);
  }
}

function renderTagDatalist() {
  $("#allTags").innerHTML = TAGS.map((t) => `<option value="${esc(t)}">`).join("");
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

function current(p) {
  // merge server record with pending edits
  return { ...p, ...(DIRTY[p.id] || {}) };
}

function filtered() {
  const q = $("#filter").value.toLowerCase();
  const sec = $("#sectionFilter").value;
  const st = $("#statusFilter").value;
  let list = POSTS.map(current).filter((p) => {
    if (sec && p.section !== sec) return false;
    if (st === "published" && !p.published) return false;
    if (st === "draft" && p.published) return false;
    if (st === "invalid" && (!p.issues || p.issues.length === 0)) return false;
    if (q && !(p.title.toLowerCase().includes(q) || p.filename.toLowerCase().includes(q))) return false;
    return true;
  });
  list.sort((a, b) => {
    let av = a[sortKey], bv = b[sortKey];
    if (sortKey === "issues") { av = (a.issues || []).length; bv = (b.issues || []).length; }
    if (av < bv) return -1 * sortDir;
    if (av > bv) return 1 * sortDir;
    return 0;
  });
  return list;
}

function render() {
  const list = filtered();
  rowsEl.innerHTML = "";
  for (const p of list) rowsEl.appendChild(renderRow(p));
  $("#stats").textContent = `${POSTS.length} post · ${POSTS.filter((x) => x.published).length} pubblicati · ${POSTS.filter((x) => (x.issues || []).length).length} con errori`;
  updateDirty();
}

function setField(id, field, value) {
  const orig = POSTS.find((p) => p.id === id);
  if (!DIRTY[id]) DIRTY[id] = {};
  DIRTY[id][field] = value;
  // if value reverts to original, drop it
  if (JSON.stringify(orig[field]) === JSON.stringify(value)) {
    delete DIRTY[id][field];
    if (Object.keys(DIRTY[id]).length === 0) delete DIRTY[id];
  }
  updateDirty();
}

function updateDirty() {
  const n = Object.keys(DIRTY).length;
  $("#saveBtn").disabled = n === 0;
  $("#dirtyCount").textContent = n ? `${n} post modificati` : "";
  // mark dirty rows
  document.querySelectorAll("tr[data-id]").forEach((tr) => {
    tr.classList.toggle("dirty", !!DIRTY[tr.dataset.id]);
  });
}

function renderRow(p) {
  const tr = document.createElement("tr");
  tr.dataset.id = p.id;
  if ((p.issues || []).length) tr.classList.add("invalid");

  const tdSection = el("td", "section-tag", esc(p.section));
  const tdFile = el("td", "", esc(p.filename));

  // title
  const tdTitle = document.createElement("td");
  tdTitle.className = "col-title";
  const titleInput = document.createElement("input");
  titleInput.type = "text"; titleInput.value = p.title;
  titleInput.oninput = () => setField(p.id, "title", titleInput.value);
  tdTitle.appendChild(titleInput);

  // description
  const tdDesc = document.createElement("td");
  tdDesc.className = "col-desc";
  const descInput = document.createElement("textarea");
  descInput.value = p.description;
  descInput.oninput = () => setField(p.id, "description", descInput.value);
  tdDesc.appendChild(descInput);

  // date
  const tdDate = document.createElement("td");
  const dateInput = document.createElement("input");
  dateInput.type = "date";
  dateInput.value = /^\d{4}-\d{2}-\d{2}$/.test(p.date) ? p.date : "";
  dateInput.onchange = () => setField(p.id, "date", dateInput.value);
  tdDate.appendChild(dateInput);

  // published
  const tdPub = document.createElement("td");
  tdPub.className = "col-pub";
  const cb = document.createElement("input");
  cb.type = "checkbox"; cb.checked = !!p.published;
  cb.onchange = () => setField(p.id, "published", cb.checked);
  tdPub.appendChild(cb);

  // tags
  const tdTags = document.createElement("td");
  tdTags.appendChild(renderTags(p));

  // issues
  const tdIssues = document.createElement("td");
  if ((p.issues || []).length) {
    tdIssues.innerHTML = `<span class="issues">${esc(p.issues.join("; "))}</span>`;
  } else {
    tdIssues.innerHTML = `<span class="ok-badge">ok</span>`;
  }

  [tdSection, tdFile, tdTitle, tdDesc, tdDate, tdPub, tdTags, tdIssues].forEach((td) => tr.appendChild(td));
  return tr;
}

function renderTags(p) {
  const box = document.createElement("div");
  box.className = "tagbox";
  const tags = [...(p.tags || [])];

  function refresh() {
    box.innerHTML = "";
    tags.forEach((t, i) => {
      const span = document.createElement("span");
      span.className = "tag";
      span.appendChild(document.createTextNode(t));
      const x = document.createElement("button");
      x.textContent = "×";
      x.onclick = () => { tags.splice(i, 1); setField(p.id, "tags", [...tags]); refresh(); };
      span.appendChild(x);
      box.appendChild(span);
    });
    const add = document.createElement("button");
    add.className = "addtag"; add.textContent = "+ tag";
    add.onclick = () => {
      const inp = document.createElement("input");
      inp.setAttribute("list", "allTags");
      inp.style.width = "90px"; inp.style.fontSize = "11px";
      add.replaceWith(inp);
      inp.focus();
      const commit = () => {
        const v = inp.value.trim();
        if (v && !tags.includes(v)) {
          tags.push(v);
          if (!TAGS.includes(v)) { TAGS.push(v); TAGS.sort(); renderTagDatalist(); }
          setField(p.id, "tags", [...tags]);
        }
        refresh();
      };
      inp.onblur = commit;
      inp.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); commit(); } if (e.key === "Escape") refresh(); };
    };
    box.appendChild(add);
  }
  refresh();
  return box;
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

async function save() {
  const ids = Object.keys(DIRTY);
  $("#saveBtn").disabled = true;
  let ok = 0, fail = 0;
  for (const id of ids) {
    const encoded = id.split("/").map(encodeURIComponent).join("/");
    try {
      const res = await fetch(`/api/posts/${encoded}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(DIRTY[id]),
      });
      if (!res.ok) throw new Error((await res.json()).detail || res.status);
      const updated = await res.json();
      const idx = POSTS.findIndex((p) => p.id === id);
      POSTS[idx] = updated;
      delete DIRTY[id];
      ok++;
    } catch (e) {
      fail++;
      console.error(id, e);
    }
  }
  const toast = $("#toast");
  toast.className = fail ? "toast err" : "toast";
  toast.textContent = fail ? `${ok} salvati, ${fail} falliti` : `${ok} post salvati`;
  setTimeout(() => (toast.textContent = ""), 4000);
  render();
}

$("#saveBtn").onclick = save;
$("#filter").oninput = render;
$("#sectionFilter").onchange = render;
$("#statusFilter").onchange = render;
document.querySelectorAll("th[data-sort]").forEach((th) => {
  th.onclick = () => {
    const k = th.dataset.sort;
    if (sortKey === k) sortDir *= -1; else { sortKey = k; sortDir = 1; }
    render();
  };
});

load();
