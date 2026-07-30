function parseCSV(text) {
  const rows = [];
  let row = [], cell = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i], next = text[i + 1];
    if (c === '"' && quoted && next === '"') { cell += '"'; i++; }
    else if (c === '"') quoted = !quoted;
    else if (c === "," && !quoted) { row.push(cell); cell = ""; }
    else if ((c === "\n" || c === "\r") && !quoted) {
      if (c === "\r" && next === "\n") i++;
      row.push(cell); if (row.some(Boolean)) rows.push(row); row = []; cell = "";
    } else cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const headers = rows.shift();
  return rows.map(values => Object.fromEntries(headers.map((h, i) => [h, values[i]])));
}

function render(events, threshold = -10) {
  const filtered = events.filter(d => Number(d.magnitude) >= threshold);
  const mags = filtered.map(d => Number(d.magnitude)).filter(Number.isFinite);
  const depths = filtered.map(d => Number(d.depth_km)).filter(Number.isFinite);
  const largest = [...filtered].sort((a, b) => Number(b.magnitude) - Number(a.magnitude))[0];
  document.querySelector("#event-count").textContent = filtered.length.toLocaleString();
  document.querySelector("#max-mag").textContent = largest ? Number(largest.magnitude).toFixed(1) : "—";
  document.querySelector("#max-place").textContent = largest?.place || "No matching events";
  document.querySelector("#avg-depth").textContent = depths.length ? (depths.reduce((a,b)=>a+b,0)/depths.length).toFixed(1) : "—";
  document.querySelector("#large-count").textContent = mags.filter(m => m >= 4).length;
  document.querySelector("#filter-count").textContent = `${filtered.length} events match`;

  const bins = [
    {label:"Below 1", min:-10, max:1}, {label:"1–1.9", min:1, max:2},
    {label:"2–2.9", min:2, max:3}, {label:"3–3.9", min:3, max:4},
    {label:"4–4.9", min:4, max:5}, {label:"5+", min:5, max:100}
  ].map(b => ({...b, count:mags.filter(m => m >= b.min && m < b.max).length}));
  const max = Math.max(...bins.map(b => b.count), 1);
  document.querySelector("#magnitude-chart").innerHTML = bins.map(b =>
    `<div class="bar-row"><span>${b.label}</span><div><i style="width:${b.count/max*100}%"></i></div><b>${b.count}</b></div>`
  ).join("");

  document.querySelector("#event-table").innerHTML = [...filtered]
    .sort((a,b)=>Number(b.magnitude)-Number(a.magnitude)).slice(0,12).map(d =>
      `<tr><td><b class="mag">${Number(d.magnitude).toFixed(1)}</b></td><td>${d.place}</td><td>${new Date(d.time_utc).toLocaleString("en-US",{timeZone:"UTC",dateStyle:"medium",timeStyle:"short"})}</td><td>${Number(d.depth_km).toFixed(1)} km</td></tr>`
    ).join("") || `<tr><td colspan="4">No events match this filter.</td></tr>`;
}

Promise.all([
  fetch("data/earthquakes.csv").then(r => { if(!r.ok) throw Error("CSV unavailable"); return r.text(); }),
  fetch("data/metadata.json").then(r => r.json())
]).then(([csv, metadata]) => {
  const events = parseCSV(csv);
  document.querySelector("#updated-at").textContent = `Updated ${new Date(metadata.generated_at_utc).toLocaleString()} · ${metadata.record_count} records`;
  render(events);
  document.querySelector("#magnitude-filter").addEventListener("change", e => render(events, Number(e.target.value)));
}).catch(error => {
  document.querySelector("#updated-at").textContent = "Data could not be loaded";
  document.querySelector("#event-table").innerHTML = `<tr><td colspan="4">${error.message}</td></tr>`;
});

