const METHOD_DESCRIPTIONS = {
  hybrid: "Blends user taste patterns with movie features for balanced picks.",
  collaborative: "Finds movies liked by users with similar rating history.",
  content: "Recommends movies similar to ones you select based on genre and director.",
};

const state = {
  method: "hybrid",
  movies: [],
  users: [],
};

const els = {
  methodDesc: document.getElementById("method-desc"),
  userSection: document.getElementById("user-section"),
  likedSection: document.getElementById("liked-section"),
  userSelect: document.getElementById("user-select"),
  userRatings: document.getElementById("user-ratings"),
  movieChecklist: document.getElementById("movie-checklist"),
  topN: document.getElementById("top-n"),
  topNValue: document.getElementById("top-n-value"),
  recommendBtn: document.getElementById("recommend-btn"),
  results: document.getElementById("results"),
  resultsMeta: document.getElementById("results-meta"),
  catalog: document.getElementById("catalog"),
  toast: document.getElementById("toast"),
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.remove("hidden");
  setTimeout(() => els.toast.classList.add("hidden"), 3000);
}

function setMethod(method) {
  state.method = method;
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.method === method);
  });
  els.methodDesc.textContent = METHOD_DESCRIPTIONS[method];
  els.userSection.classList.toggle("hidden", method === "content");
  els.likedSection.classList.toggle("hidden", method !== "content");
}

function renderUserRatings(ratings) {
  els.userRatings.innerHTML = ratings
    .map((r) => `<span class="rating-chip">${r.title} <strong>${r.rating}★</strong></span>`)
    .join("");
}

function renderMovieChecklist() {
  els.movieChecklist.innerHTML = state.movies
    .map(
      (movie) => `
      <label class="check-item">
        <input type="checkbox" value="${movie.id}" />
        <span>${movie.title} (${movie.year})</span>
      </label>`
    )
    .join("");
}

function renderCatalog() {
  els.catalog.innerHTML = state.movies
    .map(
      (movie) => `
      <article class="catalog-card" data-id="${movie.id}">
        <h3>${movie.title}</h3>
        <p>${movie.year} · ${movie.genres.join(", ")}</p>
        <p>Dir. ${movie.director}</p>
      </article>`
    )
    .join("");

  els.catalog.querySelectorAll(".catalog-card").forEach((card) => {
    card.addEventListener("click", () => loadSimilarMovies(Number(card.dataset.id)));
  });
}

function renderRecommendations(items, meta) {
  els.resultsMeta.textContent = meta;

  if (!items.length) {
    els.results.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <p>No recommendations found. Try a different user or selection.</p>
      </div>`;
    return;
  }

  els.results.innerHTML = items
    .map(
      (item, index) => `
      <article class="movie-card">
        <div class="rank">${index + 1}</div>
        <div>
          <h3>${item.movie.title}</h3>
          <p class="movie-meta">${item.movie.year} · ${item.movie.genres.join(", ")} · ${item.movie.director}</p>
        </div>
        <div class="score-badge">
          <div class="score-value">${item.score}</div>
          <div class="score-label">${item.score_label}</div>
        </div>
        <p class="reason">${item.reason}</p>
      </article>`
    )
    .join("");
}

async function loadUsers() {
  state.users = await api("/api/users");
  els.userSelect.innerHTML = state.users
    .map((user) => `<option value="${user.user_id}">${user.user_id} (${user.rating_count} ratings)</option>`)
    .join("");

  if (state.users.length) {
    await loadUserRatings(state.users[0].user_id);
  }
}

async function loadUserRatings(userId) {
  const ratings = await api(`/api/users/${userId}/ratings`);
  renderUserRatings(ratings);
}

async function loadMovies() {
  state.movies = await api("/api/movies");
  renderMovieChecklist();
  renderCatalog();
}

function getLikedMovieIds() {
  return [...els.movieChecklist.querySelectorAll("input:checked")].map((input) =>
    Number(input.value)
  );
}

async function fetchRecommendations() {
  const topN = Number(els.topN.value);
  const body = { method: state.method, top_n: topN };

  if (state.method === "content") {
    body.liked_movie_ids = getLikedMovieIds();
    if (!body.liked_movie_ids.length) {
      showToast("Select at least one movie you like.");
      return;
    }
  } else {
    body.user_id = els.userSelect.value;
  }

  els.recommendBtn.disabled = true;
  els.recommendBtn.textContent = "Loading...";

  try {
    const items = await api("/api/recommendations", {
      method: "POST",
      body: JSON.stringify(body),
    });
    const meta = `${state.method} · top ${topN} results`;
    renderRecommendations(items, meta);
  } catch (error) {
    showToast(error.message);
  } finally {
    els.recommendBtn.disabled = false;
    els.recommendBtn.textContent = "Get Recommendations";
  }
}

async function loadSimilarMovies(movieId) {
  const movie = state.movies.find((m) => m.id === movieId);
  if (!movie) return;

  try {
    const items = await api(`/api/movies/${movieId}/similar?top_n=5`);
    renderRecommendations(items, `Similar to "${movie.title}"`);
    document.querySelector(".results-panel").scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    showToast(error.message);
  }
}

function bindEvents() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => setMethod(tab.dataset.method));
  });

  els.userSelect.addEventListener("change", (e) => loadUserRatings(e.target.value));

  els.topN.addEventListener("input", (e) => {
    els.topNValue.textContent = e.target.value;
  });

  els.recommendBtn.addEventListener("click", fetchRecommendations);
}

async function init() {
  bindEvents();
  setMethod("hybrid");

  try {
    await Promise.all([loadMovies(), loadUsers()]);
    await fetchRecommendations();
  } catch (error) {
    showToast("Could not connect to API. Start the server with: py -m uvicorn api.app:app --reload");
  }
}

init();
