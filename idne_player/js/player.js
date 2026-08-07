/* global IDNE_LIBRARY */
(function () {
  "use strict";

  const SAVE_SLOT_COUNT = 3;
  const STORAGE_PREFIX = "idne_player_v1";

  const screens = {
    library: document.getElementById("screen-library"),
    opening: document.getElementById("screen-opening"),
    play: document.getElementById("screen-play"),
  };

  const state = {
    library: Array.isArray(window.IDNE_LIBRARY) ? window.IDNE_LIBRARY : [],
    adventureMeta: null,
    gamebook: null,
    currentSection: null,
    loadedFromFile: false,
  };

  function saveKey(adventureId, slot) {
    return `${STORAGE_PREFIX}:${adventureId}:slot:${slot}`;
  }

  function autoSaveKey(adventureId) {
    return `${STORAGE_PREFIX}:${adventureId}:autosave`;
  }

  function showScreen(name) {
    Object.entries(screens).forEach(([key, el]) => {
      el.classList.toggle("hidden", key !== name);
    });
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderMarkdownLite(text) {
    const blocks = String(text || "").trim().split(/\n{2,}/);
    return blocks
      .map((block) => {
        const lines = block.split("\n");
        if (lines.every((line) => line.trim().startsWith("- "))) {
          const items = lines
            .map((line) => `<li>${formatInline(line.trim().slice(2))}</li>`)
            .join("");
          return `<ul>${items}</ul>`;
        }
        return `<p>${formatInline(block.replace(/\n/g, " "))}</p>`;
      })
      .join("");
  }

  function formatInline(text) {
    return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  function readSave(adventureId, slot) {
    try {
      const raw = localStorage.getItem(saveKey(adventureId, slot));
      return raw ? JSON.parse(raw) : null;
    } catch (_err) {
      return null;
    }
  }

  function writeSave(adventureId, slot, payload) {
    localStorage.setItem(saveKey(adventureId, slot), JSON.stringify(payload));
  }

  function readAutoSave(adventureId) {
    try {
      const raw = localStorage.getItem(autoSaveKey(adventureId));
      return raw ? JSON.parse(raw) : null;
    } catch (_err) {
      return null;
    }
  }

  function writeAutoSave(adventureId, payload) {
    localStorage.setItem(autoSaveKey(adventureId), JSON.stringify(payload));
  }

  function clearSaves(adventureId) {
    for (let slot = 1; slot <= SAVE_SLOT_COUNT; slot += 1) {
      localStorage.removeItem(saveKey(adventureId, slot));
    }
    localStorage.removeItem(autoSaveKey(adventureId));
  }

  function currentSavePayload() {
    return {
      adventure_id: state.gamebook.adventure_id,
      schema_version: state.gamebook.schema_version,
      section: state.currentSection,
      saved_at: new Date().toISOString(),
    };
  }

  function validateGamebook(data) {
    if (!data || typeof data !== "object") {
      throw new Error("Invalid gamebook file.");
    }
    if (!data.sections || !data.start_section) {
      throw new Error("Gamebook is missing sections or a starting section.");
    }
    const startKey = String(data.start_section);
    if (!data.sections[startKey]) {
      throw new Error("Starting section is not present in this gamebook.");
    }
  }

  function loadBundledGamebook(adventureId) {
    return new Promise((resolve, reject) => {
      const scriptId = `idne-gamebook-${adventureId}`;
      if (document.getElementById(scriptId)) {
        const book = window.IDNE_GAMEBOOKS && window.IDNE_GAMEBOOKS[adventureId];
        if (book) {
          resolve(book);
          return;
        }
      }
      const script = document.createElement("script");
      script.id = scriptId;
      script.src = `library/adventures/${adventureId}.js`;
      script.onload = () => {
        const book = window.IDNE_GAMEBOOKS && window.IDNE_GAMEBOOKS[adventureId];
        if (!book) {
          reject(new Error(`Bundled adventure failed to load: ${adventureId}`));
          return;
        }
        resolve(book);
      };
      script.onerror = () => reject(new Error(`Could not load bundled adventure: ${adventureId}`));
      document.body.appendChild(script);
    });
  }

  function renderLibrary() {
    const list = document.getElementById("adventure-list");
    list.innerHTML = "";
    if (!state.library.length) {
      list.innerHTML = "<p>No bundled adventures found. Load a <code>gamebook.json</code> file to play.</p>";
      return;
    }
    state.library.forEach((entry) => {
      const card = document.createElement("article");
      card.className = "adventure-card";
      card.innerHTML = `
        <h3>${escapeHtml(entry.title)}</h3>
        <p>${escapeHtml(entry.premise || "")}</p>
        <p><strong>Role:</strong> ${escapeHtml(entry.player_role || "Investigator")}</p>
        <p><strong>Playtime:</strong> ${escapeHtml(entry.playtime || "About two hours")}</p>
      `;
      const actions = document.createElement("div");
      actions.className = "actions-row";
      const openBtn = document.createElement("button");
      openBtn.type = "button";
      openBtn.className = "primary";
      openBtn.textContent = "Open";
      openBtn.addEventListener("click", () => openBundledAdventure(entry));
      actions.appendChild(openBtn);
      card.appendChild(actions);
      list.appendChild(card);
    });
  }

  function renderSaveSlots() {
    const list = document.getElementById("save-slot-list");
    list.innerHTML = "";
    const adventureId = state.gamebook.adventure_id;
    for (let slot = 1; slot <= SAVE_SLOT_COUNT; slot += 1) {
      const btn = document.createElement("button");
      btn.type = "button";
      const saved = readSave(adventureId, slot);
      btn.textContent = saved
        ? `Load slot ${slot} (section ${saved.section})`
        : `Slot ${slot} empty`;
      btn.disabled = !saved;
      btn.addEventListener("click", () => {
        if (saved) {
          goToSection(saved.section, false);
          showScreen("play");
        }
      });
      list.appendChild(btn);

      const saveBtn = document.createElement("button");
      saveBtn.type = "button";
      saveBtn.className = "secondary";
      saveBtn.textContent = `Save to slot ${slot}`;
      saveBtn.addEventListener("click", () => {
        writeSave(adventureId, slot, currentSavePayload());
        renderSaveSlots();
      });
      list.appendChild(saveBtn);
    }
  }

  function showOpening() {
    document.getElementById("opening-title").textContent = state.gamebook.title;
    document.getElementById("opening-body").innerHTML = renderMarkdownLite(state.gamebook.opening || "");
    const auto = readAutoSave(state.gamebook.adventure_id);
    document.getElementById("btn-continue").disabled = !auto;
    renderSaveSlots();
    showScreen("opening");
  }

  function renderSection(sectionNumber) {
    const key = String(sectionNumber);
    const section = state.gamebook.sections[key];
    const errorEl = document.getElementById("play-error");
    errorEl.classList.add("hidden");
    errorEl.textContent = "";

    if (!section) {
      errorEl.textContent = `Section ${sectionNumber} is missing from this gamebook.`;
      errorEl.classList.remove("hidden");
      return;
    }

    state.currentSection = section.section;
    document.getElementById("play-adventure-title").textContent = state.gamebook.title;
    document.getElementById("section-heading").textContent = `Section ${section.section}${
      section.title ? ` — ${section.title}` : ""
    }`;

    const metaEl = document.getElementById("section-meta");
    metaEl.innerHTML = (section.meta || []).map((line) => `<p>${formatInline(line)}</p>`).join("");

    document.getElementById("section-body").innerHTML = renderMarkdownLite(section.body || "");

    const choicesEl = document.getElementById("choice-list");
    choicesEl.innerHTML = "";
    const choices = section.choices || [];
    if (!choices.length) {
      const end = document.createElement("p");
      end.textContent = "This section has no further choices.";
      choicesEl.appendChild(end);
      return;
    }

    choices.forEach((choice) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "choice-button";
      btn.textContent = choice.label;
      btn.addEventListener("click", () => {
        goToSection(choice.target_section, true);
      });
      choicesEl.appendChild(btn);
    });
  }

  function goToSection(sectionNumber, autosave) {
    renderSection(sectionNumber);
    if (autosave && state.gamebook) {
      writeAutoSave(state.gamebook.adventure_id, currentSavePayload());
    }
    showScreen("play");
  }

  async function openBundledAdventure(entry) {
    state.adventureMeta = entry;
    state.loadedFromFile = false;
    const book = await loadBundledGamebook(entry.id);
    validateGamebook(book);
    state.gamebook = book;
    showOpening();
  }

  async function openGamebookFromFile(file) {
    const text = await file.text();
    const data = JSON.parse(text);
    validateGamebook(data);
    state.gamebook = data;
    state.adventureMeta = {
      id: data.adventure_id,
      title: data.title,
    };
    state.loadedFromFile = true;
    showOpening();
  }

  document.getElementById("file-picker").addEventListener("change", async (event) => {
    const file = event.target.files && event.target.files[0];
    if (!file) {
      return;
    }
    try {
      await openGamebookFromFile(file);
    } catch (err) {
      alert(err.message || "Could not load gamebook file.");
    } finally {
      event.target.value = "";
    }
  });

  document.getElementById("btn-start").addEventListener("click", () => {
    clearSaves(state.gamebook.adventure_id);
    goToSection(state.gamebook.start_section, true);
  });

  document.getElementById("btn-continue").addEventListener("click", () => {
    const auto = readAutoSave(state.gamebook.adventure_id);
    if (auto) {
      goToSection(auto.section, false);
    }
  });

  document.getElementById("btn-back-library").addEventListener("click", () => {
    showScreen("library");
  });

  document.getElementById("btn-restart").addEventListener("click", () => {
    if (confirm("Restart this adventure? Save slots will be cleared.")) {
      clearSaves(state.gamebook.adventure_id);
      goToSection(state.gamebook.start_section, true);
    }
  });

  document.getElementById("btn-save").addEventListener("click", () => {
    writeAutoSave(state.gamebook.adventure_id, currentSavePayload());
    alert("Progress saved. Use Continue on the opening screen next time.");
  });

  document.getElementById("btn-quit").addEventListener("click", () => {
    showScreen("library");
  });

  window.IDNEPlayer = {
    init() {
      renderLibrary();
      showScreen("library");
    },
    openBundledAdventure,
    openGamebookFromFile,
    goToSection,
    getState: () => ({ ...state }),
  };
})();
